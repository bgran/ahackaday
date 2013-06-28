#!/usr/bin/python
#
# This is a ProxyCommand wrapper for OpenSSH, to limit the usage of
# bandwidth. Just add:
#   ProxyCommand $HOME/bin/bw3.py %h %p 15
# Where $HOME/bin is a directory in your $PATH. That 15 is how many bytes
# per second you transit data. Tihs is totally vapourware code, or whatever.
#
# Oh, licenses? Well this file is in the public domain.
#

import sys, os, string, time
from socket import *
import select
import tty
import termios

def main():
        remote_host = sys.argv[1]
        remote_port = string.atoi(sys.argv[2])
        bitspersecond = string.atoi(sys.argv[3])

        sock = socket(AF_INET, SOCK_STREAM)
        con_tup = (remote_host, remote_port)
        sock.setblocking(True)
        sock.connect(con_tup)

        child = os.fork()

        if child < 0:
                sys.exit(1)
        elif child == 0:
                # Child context
		predict = 0
		t1 = time.time()
                while 1:

			bytes = os.read(sys.stdin.fileno(), 65535)
			len_bytes = len(bytes)
			if (not len_bytes):
                                sys.exit(1)
			t2 = time.time()
			delta = t2 - t1
			bandwidth = len_bytes / delta
			if bandwidth > bitspersecond:
				time.sleep(1)
			num_bytes_written = os.write(sock.fileno(), bytes)
        else:
                # parent context
		predict = 0
                while 1:
                        data = ""

			bytes = os.read(sock.fileno(), 65535)
                        if (not len(bytes)):
                                sys.exit(0)
			os.write(sys.stdout.fileno(), bytes)

	return 0
if __name__ == "__main__":
	sys.exit(main())
