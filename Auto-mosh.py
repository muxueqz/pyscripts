#!/usr/bin/env python2
#-*- coding: utf-8 -*-

import pexpect
import base64
import os
import sys

def ssh_con(host,
        port, user, passwd,
        sshoptions,
        cmd=""):
#    print sigwinch_passthrough('test','test')
    columns=115
    lines=38
    ssh_program = 'ssh -o "StrictHostKeyChecking=no"'
    kwargs = locals()
    spawn = (
        'mosh --ssh="{ssh_program} {sshoptions} -p {port} -l {user}" {host} {cmd}'
        ).format(**kwargs)
    print user, host, cmd
    child = pexpect.spawn(spawn)
    try:
        lines, columns = getwinsize()
    except:
        pass
    child.expect("assword:", timeout=120)
    child.sendline(passwd)
    print child.before   # Print the result of the ls command.
    child.setwinsize(lines,columns)
    print "resize windows(%s,%s)"%(columns,lines)
    child.interact()     # Give control of the child to the user.

def uspw_read(name):
    usr_home = os.path.expanduser('~')
    pass_file = open(usr_home+'/.pass')
    for uspw in pass_file.readlines():
        if not uspw.startswith('#'):
            uspw_list = uspw.split()
            if len(uspw_list) > 1 and name in uspw_list[0]:
                name = uspw_list[0][5:]
                host = uspw_list[1].split('@')[1]
                try:
                    port = uspw_list[3]
                except:
                    port = 22
                user = uspw_list[1].split('@')[0]
                opasswd = uspw_list[2]
                passwd = base64.decodestring(opasswd)
                return name,host,port,user,passwd
#            return list[0], list[1]

#host = '127.0.0.1'
#user = 'muxueqz'

def getwinsize():
    # Use the curses module if installed
    try:
        import curses
        stdscr = curses.initscr()
        curses.endwin()
        rows, cols = stdscr.getmaxyx()
        return rows, cols
    except ImportError:
        pass

    # Nope, so deal with ioctl directly.  What value for TIOCGWINSZ?
    try:
        import termios
        TIOCGWINSZ = termios.TIOCGWINSZ
    except ImportError:
        TIOCGWINSZ = 0x40087468  # This is Linux specific

    import struct, fcntl
    s = struct.pack("HHHH", 0, 0, 0, 0)
    try:
        x = fcntl.ioctl(sys.stdout.fileno(), TIOCGWINSZ, s)
    except IOError:
        return 80
    rows, cols = struct.unpack("HHHH", x)[:2]
    return rows, cols
#print name, host, user, passwd

def main():
    """main method"""
    import optparse
    parser = optparse.OptionParser()
    parser.add_option('-n', '--name', help='name')
    parser.add_option('-o', '--sshopt', help='ssh options', default='')
    opts, args= parser.parse_args()
    if len(sys.argv) >= 2:
        cmd = ' '.join(args)
    if len(sys.argv) >= 1:
        name, host, port, user, passwd = uspw_read(opts.name)
        ssh_con(host,
            port, user, passwd,
            opts.sshopt, cmd)


if __name__ == "__main__":
    main()
