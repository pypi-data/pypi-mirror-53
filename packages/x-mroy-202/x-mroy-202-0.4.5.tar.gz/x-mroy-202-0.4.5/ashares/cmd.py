from argparse import ArgumentParser
from mroylib.config import Config
import os
import sys
import time
import random
from functools import partial
from .init import init_config
from tabulate import tabulate
from termcolor import colored

INIT_FLAG = False
if not os.path.exists(os.path.expanduser("~/.config/fshare.ini")):
    if not os.path.exists(os.path.expanduser("~/.config")):
        os.mkdir(os.path.expanduser("~/.config"))
    init_config()
    INIT_FLAG = True

from .remote import AsyncConnection
from .db import Sql as Sqldb
from .db import Cache, change_sqlite_file
from .db import RDb, HostDb
from .log import colorL
from .daemon import run, stop

CONF = Config(file=os.path.expanduser("~/.config/fshare.ini"))

def FShareDaemon(name,host, port, remote):
    while 1:
        time.sleep(3)
        a = AsyncConnection(host,name=name, port=int(port), remotepath=remote)
        r = a.check_files_sync()
        AsyncConnection.run_tasks([r])


def main():
    parser = ArgumentParser()
    parser.add_argument("operator", nargs="*", default=None, help="[push , pull]")
    parser.add_argument("-r", "--reg", default=None, help="reg server")
    parser.add_argument("--from-db", default=False, action='store_true', help="reg from db .")
    parser.add_argument("--db-file", default=None, help="use other db file .")
    parser.add_argument("-q", "--query", default=None, help="query talk in all msg")
    parser.add_argument("-L", "--query-host", default='', help="query host in\
                        local  db")
    parser.add_argument("-e", "--exe", default=None, help="run in remote . after -L  | -e ss/build-ss/script is special\
                        \n build-ss:\n\tto build shadowsocks in server\
                        \n ss: \n\tto check progress ss in server\
                        \n script \n\t -e scirpt -A some_bash.sh [args_file]\
                        \n\t\t\t if -sf will split args_file to match all host.\
                        \n log: -e log -A some_file  # will tail /tmp/sftp_out/{some_file}.log.err.log " )
    parser.add_argument("-s", "--send-msg", nargs="*", help="send msg")
    parser.add_argument("--sync", default=False,action='store_true', help="sync from room in centry server")
    parser.add_argument("-S", "--screenshot", default=False, action='store_true', help="screensshot ")
    parser.add_argument("-f", "--forward", nargs="*", help="port fording  listen in remote's port --> local's port exm: host rport:lport")
    parser.add_argument("--start", default=False, action='store_true', help="start a daemon server")
    parser.add_argument("--stop", default=False, action='store_true', help="stop a daemon server")
    parser.add_argument("--change-server", default=None, action='store_true', help="change centry server")
    parser.add_argument("--check-room", default=False, action='store_true', help="check room in centry server")
    parser.add_argument("-l", "--list-ready-files", default=False, action='store_true',help="after scan , new file can be list here")
    parser.add_argument("-T", "--timeout", type=int, default=12, help='set timeout')

    parser.add_argument("-D","--down-url", default='', type=str, help="download mode , this mode can \
        \n1. ssh many server and wget -c 'xx.xxx.xx' to download\
        \n2. split offset and sftp get from alive point\
        \n3. delete 'xx.xxx.xx' in server and concat all local files to one.")
    parser.add_argument("--download-only", default=False, action='store_true', help='only run --down-url  step .1 ')
    parser.add_argument("--keep-download", default=True, action='store_false', help='keep file after download to local  ')
    parser.add_argument("-dt","--download-timeout", default=60, type=int, help='set download\'s timeout, default 60')
    parser.add_argument("-c","--download-count", default=10, type=int, help='set route\'s count when download.')
    parser.add_argument("-sf","--split-file", default=False, action='store_true', help='split args file for hosts\' count and as args file for every host')
    parser.add_argument("--Not", default=10,nargs="*", type=str, help='grep -v ')
    parser.add_argument("-A", "--args", nargs="*", help="set args for exe ")

    args = parser.parse_args()
    if args.db_file and os.path.exists(args.db_file):
        Sql = Cache(args.db_file)
        change_sqlite_file(Sql)
    else:
        Sql = Sqldb
    CONF = Config(file=os.path.expanduser("~/.config/fshare.ini"))
    host = CONF['remote-host']
    port= CONF['remote-port']
    name = CONF.get('remote-user','root')
    remotepath = CONF['msg-room']
    a = AsyncConnection(host, port=int(port), name=name,remotepath=remotepath)
    task = []

    if args.timeout:
        AsyncConnection.timeout_t = args.timeout

    if args.sync:
        r = a.check_files_sync()
        AsyncConnection.run_tasks([r])
        sys.exit(0)


    if INIT_FLAG:
        passwd = input("password init %s  \n>" % (name + "@" +host + ":"+port) )
        a.password = passwd.strip()
        r = a.reg()
        AsyncConnection.run_tasks([r])
        colorL("init ok !!")
        sys.exit(0)
    
    if args.check_room:
        r = a.check_room()
        AsyncConnection.run_tasks([r])
        colorL("check room ok !!")
        sys.exit(0)

    if args.down_url:
        h = HostDb(Sql)
        q = args.query_host
        if not q:
            q = '.'
        res = [(i.host,{"password": i.passwd, 'keyfile':None}) for i in h.search(q)][:args.download_count]
        res2 = []
        if args.Not:
            
            for m in res:
                _if_not = False
                for s in args.Not:
                    if s in m[0]:
                        _if_not = True
                if not _if_not:
                    # colorL("[s]", m[0] )
                    res2.append(m)
        
        r = AsyncConnection.download_multi_route(
            args.down_url, 
            res2,
            predownload_timeout=args.download_timeout,
            keep_after_finish=args.keep_download,
            only_download=args.download_only)
        sys.exit(0)

    if args.query_host:
        h = HostDb(Sql)
        if args.exe:
            if args.exe == "ss":
                res = h.search_run(args.query_host, AsyncConnection, 'ssh', 'if [ ! "$( ps aux | grep shadowsock | grep -v grep |xargs )" ];then echo no ;else echo ok ;fi')
            elif 'build-ss' in args.exe :
                cmds = args.exe.split()
                ins = 'apt'
                if len(cmds) > 1:
                    if cmds[1] == 'centos':
                        ins = 'yum'
                res = h.search_run(args.query_host, AsyncConnection, 'build_ss', ins) 
            elif args.exe == 'log':
                res = h.search_run(args.query_host, AsyncConnection, 'script_log', args.args[0])
            elif args.exe == 'script':
                if len(args.args) > 1 and os.path.exists(args.args[1]):
                    if args.split_file:
                        res = h.search_run(args.query_host, AsyncConnection, 'script',args.args[0], args_file=args.args[1], split_file="args_file")
                    else:
                        res = h.search_run(args.query_host, AsyncConnection, 'script',args.args[0], args_file=args.args[1])

                else:
                    res = h.search_run(args.query_host, AsyncConnection, 'script', args.args[0])
            elif hasattr(AsyncConnection, args.exe):
                colorL("Use:", args.exe.strip())
                if not args.args:
                    args.args = []
                res = h.search_run(args.query_host, AsyncConnection, args.exe, *args.args)

            else:
                res = h.search_run(args.query_host, AsyncConnection, 'ssh', args.exe)
            rest = []
            for i in res:
                if not i :continue
                if isinstance(i, Exception):
                    raise i
                if i[-1] == 0:
                    # colorL("[Good]",i[0], i[1])
                    if i[1]:
                        if i[1].strip() == 'no':
                            rest.append([colored(i[0], 'yellow'), colored(i[1].strip(), 'yellow'), i[-2]])
                        else:
                            rest.append([colored(i[0], 'yellow'), colored(i[1].strip(), 'green') , i[-2]])
                    
                    else:
                        rest.append([colored(i[0], 'yellow'), '(Null)' , i[-2]])

                else:
                    rest.append([colored(i[0], 'red'), colored(i[1], 'red'), i[-2] ])

            print(tabulate(rest, headers=['Host', 'console', 'connect time']))
        else:
            h.search(args.query_host)
        sys.exit(0)

    

    if args.change_server:
        init_config()
        CONF = Config(file=os.path.expanduser("~/.config/fshare.ini"))
        host = CONF['remote-host']
        port= CONF['remote-port']
        name = CONF.get('remote-user','root')
        remotepath = CONF['msg-room']
        with open(os.path.expanduser("~/.ssh/known_hosts")) as fp:
            if host not in fp.read():
                ssh_res =os.popen("ssh-keyscan -t rsa,dsa %s  2>&1 >> ~/.ssh/known_hosts" % host).read()
                colorL("add host to known hosts")
        a = AsyncConnection(host, port=int(port), name=name,remotepath=remotepath)
        r = a.reg()
        r2 = a.ssh("mkdir -p  %s " % remotepath)
        AsyncConnection.run_tasks([r, r2])
        colorL("init ok !!")
        sys.exit(0)


    if args.send_msg:
        r = a.talk( " ".join(args.send_msg))
        AsyncConnection.run_tasks([r])
        sys.exit(0)

    if args.query:
        roof = CONF['sync-index']
        for l in os.popen("grep -Inr '%s' %s " % (args.query, roof)).read().split("\n"):
            try:
                filname, line, content = l.split(":", 2)
                name = os.path.basename(filname)
                colorL(name, line, content)
            except ValueError:
                continue
        sys.exit(0)

    if args.screenshot:
        if sys.platform.startswith("linux"):
            os.popen("mate-screenshot -i ").read()
        else:
            os.popen("imgur-screenshot.sh ").read()
        sys.exit(0)

    if args.forward and len(args.forward) ==2 :
        host,rl = args.forward
        rp,lp = rl.split(":")
        if '@' in host:
            user, host = host.split("@")
        else:
            user = 'root'
        if ':' in host:
            host, port = host.split(":")
        else:
            port = 22
        colorL(host,user, port, rp, lp)
        a = AsyncConnection(host, port=int(port),name=user, remotepath='/tmp')
        r = a.forward(int(rp), int(lp))
        try:
            AsyncConnection.run_tasks([r])
        except:
            a = AsyncConnection(host, port=int(port),name=user, remotepath='/tmp')
            r = a.close_forward()
            AsyncConnection.run_tasks([r])
        sys.exit(0)

    if args.reg:

        if ":" in args.reg:
            userhost , port = args.reg.split(":")
        else:
            userhost = args.reg
            port = "22"
        
        if "@" in userhost:
            user, host = userhost.split("@")
        else:
            user = "root"
            host = userhost
        pwd = None
        if args.from_db:
            h = list(Sql.run("passwd", Obj="Host", host=host))
            if h:
                pwd = h[0][0]

        with open(os.path.expanduser("~/.ssh/known_hosts")) as fp:
            if host not in fp.read():
                ssh_res =os.popen("ssh-keyscan -t rsa,dsa %s  2>&1 >> ~/.ssh/known_hosts" % host).read()
                colorL("add host to known hosts")
        a = AsyncConnection(host, port=int(port),name=user, remotepath='/tmp')

        pwd = None
        if args.from_db:
            pwds = list(Sql.run("passwd", Obj="Host", host=host))
            if pwds:
                pwd = pwds[0][0]
        if not pwd:
            pwd = input("ssh password :")
        a.password = pwd.strip()
        a.re_init()
        r = a.reg()
        AsyncConnection.run_tasks([r])
        sys.exit(0)

    if args.list_ready_files:
        db = RDb(12)
        ready = db['ready']
        ready.pop("save_time")
        for v in ready.items():
            colorL(*v)
        sys.exit(0)

    if args.operator:
        if args.operator[0] == 'push' :
            if len(args.operator) == 2:
                f = args.operator[1]
                if os.path.exists(f) and os.path.isfile(f):
                    task.append(a.share_file(f))
                else:
                    colorL("path is not correct !! ", f)

        elif args.operator[0] == 'pull':
            if len(args.operator) == 1:
                task.append(a.check_files_sync())
                task.append(a.download_by_ready())
            elif len(args.operator) == 2:
                task.append(a.download_by_md5(args.operator[1]))
    elif args.start:
        f = partial(FShareDaemon,name, host, port, remotepath)
        run(f,"Fshare")
    elif args.stop:
        f = partial(FShareDaemon,host, port, remotepath)
        stop(f, "Fshare")

    else:
        task.append(a.check_files_sync())

    AsyncConnection.run_tasks(task)

if __name__ == '__main__':
    main()
