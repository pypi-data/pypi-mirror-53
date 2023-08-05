import argparse
import fcntl
import logging
import multiprocessing
import os
import sys

if sys.version_info[0] >= 3:
    import queue
else:
    import Queue as queue
import shutil
import signal
import subprocess
import tempfile

MATCH = "26820623525859311892"

if sys.version_info[0] >= 3:
    run = subprocess.run
else:
    def run(args, x=None, check=False, **kwargs):
        if x is not None:
            if 'stdin' in kwargs:
                raise ValueError('stdin and input arguments may not both be used.')
            kwargs['stdin'] = subprocess.PIPE

        process = subprocess.Popen(args, **kwargs)
        try:
            stdout, stderr = process.communicate(x)
        except:
            process.kill()
            process.wait()
            raise
        retcode = process.poll()
        if check and retcode:
            raise subprocess.CalledProcessError(
                retcode, process.args, output=stdout, stderr=stderr)
        return retcode, stdout, stderr


def tunnel_main(host, local_socket, remote_socket, kill_queue, done_queue):
    tunnel_spec = '%s:%s' % (local_socket, remote_socket)
    args = ["ssh", "-o", "ExitOnForwardFailure yes", "-L", tunnel_spec, host]

    total_lines = 0
    lines_buffer = []

    proc = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.STDOUT,
    )

    def readline():
        if sys.version_info[0] >= 3:
            return proc.stdout.readline()
        else:
            try:
                return proc.stdout.readline()
            except IOError as e:
                if e.errno == 11:
                    return b''
                else:
                    raise

    try:
        proc.stdin.write(b'echo %s\n' % MATCH.encode())
        proc.stdin.flush()
        while True:
            line = readline()

            if line == b'':
                proc.wait(0)
                for x in lines_buffer:
                    logging.getLogger('error').error('SUB: %s', repr(x))
                done_queue.put('ERROR')
                return

            total_lines += 1

            if total_lines > 50:
                raise SystemError("")

            if line == MATCH.encode() + b'\n':
                done_queue.put('DONE')
                break
            else:
                lines_buffer.append(line)

        fcntl.fcntl(proc.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)

        while True:
            while True:
                line = readline()

                if line != b'':
                    logging.getLogger('main').error('OUT: %s', line)
                else:
                    break

            try:
                kill_queue.get(timeout=1)
                proc.kill()
                return
            except queue.Empty:
                pass
    finally:
        proc.kill()
        proc.wait()


def main():
    parser = argparse.ArgumentParser()
    create_parser(parser)
    args, unknown = parser.parse_known_args()
    args.docker_args = unknown

    tempdir = tempfile.mkdtemp()

    docker_socket = os.path.join(tempdir, 'docker.sock')

    kill_queue = multiprocessing.Queue()
    done_queue = multiprocessing.Queue()

    process_tunnel = multiprocessing.Process(target=tunnel_main, args=(
        args.host, docker_socket, args.remote_socket,
        kill_queue, done_queue
    ))
    process_tunnel.start()

    res = None

    try:
        res = done_queue.get(timeout=args.timeout)

        if res != 'DONE':
            raise queue.Empty('Incorrect result `%s`' % res)

        if len(args.docker_args) == 0:
            return

        env = dict(os.environ)
        env[args.env] = 'unix://' + docker_socket

        res = run(args.docker_args, stderr=sys.stderr, stdout=sys.stdout, stdin=sys.stdin, env=env)
    except KeyboardInterrupt:
        os.kill(process_tunnel.pid, signal.SIGTERM)
    except queue.Empty:
        logging.getLogger('main').error('failed to establish a tunnel: `%s`', res)
        os.kill(process_tunnel.pid, signal.SIGTERM)
    finally:
        kill_queue.put("DONE")
        try:
            process_tunnel.join(args.timeout)
        except multiprocessing.TimeoutError:
            os.kill(process_tunnel.pid, signal.SIGTERM)
        shutil.rmtree(tempdir)


def create_parser(parser):
    parser.add_argument(
        '--timeout',
        dest='timeout',
        default=5.,
        type=float,
        help='Timeout for establishing the remote tunnel (default: %(default)s)',
    )

    parser.add_argument(
        '--remote-socket',
        dest='remote_socket',
        default='/var/run/docker.sock',
        help='Where the remote socket is located (default: %(default)s)',
    )

    parser.add_argument(
        '--local-socket-env',
        dest='env',
        default='DOCKER_HOST',
        help='Environment variable to set the new socket to (default: %(default)s)',
    )

    parser.add_argument(
        dest='host',
        help='SSH host to tunnel through',
    )
