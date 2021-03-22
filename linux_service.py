import signal
import sys
import os
import time
import threading


class Daemon:
    daemon_dir = '/opt/PyServices'
    timeout = 10000

    def __init__(self, app_name="InvoiceStatistics", stdin='/dev/null', stdout='/dev/null', stderr='/dev/null', pid_file='/dev/null'):
        from InvStat import InvStat
        self.md = InvStat(self.daemon_dir, app_name)
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pid_file = pid_file
        self.event_stop = threading.Event()
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

    def daemonize(self):
        # Perform first fork.
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)  # Exit first parent.
        except OSError as e:
            sys.stderr.write("fork #1 failed: (%d) %sn" % (e.errno, e.strerror))
            sys.exit(1)
        # Decouple from parent environment.
        os.chdir("/")
        os.umask(0)
        os.setsid()
        # Perform second fork.
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)  # Exit second parent.
        except OSError as e:
            sys.stderr.write("fork #2 failed: (%d) %sn" % (e.errno, e.strerror))
            sys.exit(1)
        # The process is now daemonized, redirect standard file descriptors.
        for f in sys.stdout, sys.stderr:
            f.flush()
        si = open(self.stdin, 'r')
        so = open(self.stdout, 'a+')
        se = open(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
        with open(self.pid_file, 'w+') as pid_file:
            pid_file.write('%s\n' % str(os.getpid()))

    def stop(self, signum, frame):
        self.event_stop.set()

    def run(self):

        try:
            ret = self.md.start()
            if ret == 0:
                while True:
                    self.md.work()

                    self.timeout = self.md.get_timeout()
                    if self.event_stop.isSet():
                        self.md.stop()
                        break
                    time.sleep(self.timeout / 1000.0)
        except Exception as e:
            sys.stderr.write(str(e))

    def start(self):
        self.daemonize()
        self.run()


if __name__ == "__main__":
    daemon = Daemon(app_name=sys.argv[1], stderr=sys.argv[3], pid_file=sys.argv[2])
    daemon.start()
