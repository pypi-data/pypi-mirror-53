from mroylib.config import Config
import re
import os

BASE_TMP = """
[base]
sync-index = {shareroot}
verbose = ERROR
msg-room = /tmp/room
db-host = 127.0.0.1
nico = {nico}
remote-host = {host}
remote-port = {port}
remote-user = {user}
"""

def iS(s,default='', check=None):
    while 1:
        w = input(s)
        if check:
            if check(w):
                return w
        else:
            if not w.strip():
                return default
            else:
                return w.strip()

pan = os.path.expanduser

def init_config():
    nico = iS("nico name : ", check=lambda x:' ' not in x and len(x) > 1 )
    remote_server = iS("remote server  [exm: root@xxx.xxx.xxx:22] >",
                       default='x@xxxx:12345')
    uh, remote_port = remote_server.split(":")
    remote_user, remote_host = uh.split("@")

    share_root = iS('share dir [~/Desktop/ShareFiles] : ', default='~/Desktop/ShareFiles')
    if not os.path.exists(os.path.expanduser(share_root)):
        os.mkdir(os.path.expanduser(share_root))
    ba = BASE_TMP.format(host=remote_host, port=remote_port, nico=nico, shareroot=share_root, user=remote_user)
    with open(os.path.expanduser("~/.config/fshare.ini"), 'w') as fp:
        fp.write(ba)



