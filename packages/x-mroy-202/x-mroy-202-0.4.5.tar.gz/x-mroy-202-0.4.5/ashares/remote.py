from mroylib.config import Config
from multiprocessing import Process, Queue
import asyncio
import asyncssh
from asyncssh.sftp import LocalFile
import os, time
import re
import atexit
import logging
import random
import json
from collections import Counter
from functools import wraps, partial
from hashlib import md5
from concurrent.futures.thread import ThreadPoolExecutor
import concurrent
from .log import colorL, notify
from .db import RDb
from hashlib import md5
from tqdm import tqdm
from aiohttp_socks import SocksConnector, SocksVer

KEY_DEFAULT_FILE = os.path.expanduser("~/.ssh/id_rsa") if os.path.exists(os.path.expanduser("~/.ssh/id_rsa")) else ""

CONF = Config(file=os.path.expanduser("~/.config/fshare.ini"))
asyncssh.set_log_level(CONF['verbose'])
if not os.path.exists("/tmp/ss-random"):
    os.mkdir("/tmp/ss-random")

class RemoteSyncException(Exception):pass





class AsyncConnection:
    timeout_t = 12
    loop = asyncio.get_event_loop()
    args = []

    @classmethod
    def load_args(cls,file, step='\n', decode='utf-8'):
        with open(file, "r", encoding=decode) as fp:
            res = fp.read()
            for l in res.split(step):
                if l.strip():
                    cls.args.append(l)


    @classmethod
    async def add_task(cls, cores):
        results = await asyncio.gather(*cores, return_exceptions=True)
        return results

    @classmethod
    def run_tasks(cls, cores):
        try:
            loop = cls.loop
            return loop.run_until_complete(cls.add_task(cores))
        finally:
            pass


    def __init__(self, host, name="root", port=22, keyfile=KEY_DEFAULT_FILE, password=None, remotepath=None, loop=None, src_path=None, sync_path=None):
        self.host = host
        self.name = name
        self.port = port
        self.keyfile = keyfile
        self.password = password
        self.remotepath = remotepath
        self.src_path = src_path
        self.db = RDb(12)
        if loop:
            self.__class__.loop = loop
        else:
            if self.__class__.loop.is_closed():
                self.__class__.loop = asyncio.new_event_loop()
        if not sync_path:
            self.sync_path = CONF['sync-index']
        else:
            self.sync_path = sync_path
            colorL("load sync_path:", self.sync_path)
        self.msg_room = CONF['msg-room']
        if self.msg_room.endswith("/"):
            self.msg_room = self.msg_room[:-1]
        self.room_name = CONF['nico']
        if self.keyfile:
            self.connector =  partial(asyncssh.connect, self.host,port=self.port, username=self.name, password=self.password,client_keys=self.keyfile )
        else:
            self.connector =  partial(asyncssh.connect, self.host,port=self.port, username=self.name, password=self.password,client_keys=self.keyfile, known_hosts=None) 
        #if 'proxy' in CONF.keys and CONF['proxy']:
            #print("use proxy")
            #conn = SocksConnector.from_url(CONF['proxy'], verify_ssl=False, rdns=True)
            #self.connector = partial(self.connector, connector=conn)
        self.sftp_con = None

    def re_init(self):
        if self.keyfile:
            self.connector =  partial(asyncssh.connect, self.host,port=self.port, username=self.name, password=self.password,client_keys=self.keyfile )
        else:
            self.connector =  partial(asyncssh.connect, self.host,port=self.port, username=self.name, password=self.password,client_keys=self.keyfile, known_hosts=None) 
        colorL(self.host,self.port, self.name, self.password,self.keyfile)

    async def ssh(self, cmd):
        _timeout = self.__class__.timeout_t

        # if _timeout > 12:
            # colorL("timeout:", _timeout)
        try:
            st = time.time()
            async with (await asyncio.wait_for(self.connector(), timeout=_timeout)) as conn:
                resulte = conn.run(cmd)
                result = await asyncio.wait_for(resulte, timeout=_timeout)
                if result.exit_status == 0:
                    return self.host,result.stdout,time.time() - st ,0
                else:
                    return self.host,result.stderr, time.time() - st, result.exit_status
                    logging.error(result.stderr)
        except concurrent.futures._base.TimeoutError:
            colorL(self.host, 'is not connect !!')
            return self.host,'is not connect !!', time.time() - st, 127 
        except OSError as e:
            colorL(self.host, str(e))
            return self.host,'os error ', time.time() - st, 126
        except Exception as e:
            colorL(self.host, str(e))
            return self.host, str(e),time.time() - st, 999

    async def tcp_ping(self, *port):
        st = time.time()
        try:
            if not port:
                port = self.port
            else:
                port = int(port[0])
            reader,writer = await asyncio.wait_for(asyncio.open_connection(self.host, port), timeout=AsyncConnection.timeout_t)
            et = time.time() - st
            return self.host,"%s:%d ✓" % (self.host, port),et,0
        except Exception as e:
            return self.host,"%s:%d x [%s]" % (self.host, port,str(e)[:30]),9999,99


    async def sftp_put(self, *file, remotepath=None, callback=None):
        if len(file) == 0:
            if self.src_path:
                file = [self.src_path]
            else:
                return
        if remotepath:
            remote = remotepath
        else:
            remote = self.remotepath
        async with self.connector() as conn:
            async with conn.start_sftp_client() as sftp:
                for f in file:
                    if os.path.isdir(f):
                        await sftp.mput(f, remotepath=remote, recurse=True)
                    else:
                        if await sftp.exists(os.path.join(remote, os.path.basename(f))):
                            host,res,t,c = await self.ssh("md5sum %s" % os.path.join(remote, os.path.basename(f)))
                            if c == 0:
                                l_md5 = md5(open(f,'rb').read()).hexdigest()
                                if l_md5 not in res:
                                    colorL("uploading: ","-","-",f )
                                    await sftp.put(f, remotepath=remote)
                                    colorL("finish   : ","-","-",f)
                        else:
                            colorL("up : ", f )
                            await sftp.put(f, remotepath=remote)
                            colorL("ok : ", f)

                    if callback:
                        callback()

    async def sync_files_index(self):
        async with self.connector() as conn:
            res = await conn.run(" for i in $(ls  %s ); do unzip -l $i ; done " % os.path.join(self.remotepath, "*.zip"))
            conn_dict = set()
            colorL("got from remote: ", len(res.stdout), " ->", self.sync_path)
            c = 0
            for f in res.stdout.split("\n"):
                if "{" not in f or "}" not in f:continue
                conn_dict.add(f.strip()+"\n")
                c += 1
                colorL("parse : ", c,end='\r')
            with open(self.sync_path, "a+") as fp:
                fp.writelines(list(conn_dict))
            if res.exit_status != 0:
                raise RemoteSyncException(res.stderr)


    async def check_files_sync(self):
        async with asyncssh.connect(self.host, port=self.port, username=self.name, client_keys=self.keyfile) as conn:
            check_cmd = """
            for f in $(ls  %s);
            do
              if [ -f %s/$f ];then
                  md5sum %s/$f;
              fi;
            done
            """ % (self.msg_room, self.msg_room, self.msg_room)
            res = await conn.run(check_cmd)
            ready = self.db['ready']
            if res.exit_status == 0:
                Remotes  = dict([i.split() for i in res.stdout.strip().split("\n")])
                locals = locals_dy(self.sync_path) 
                l_s = set(locals.keys())
                r_s = set(Remotes.keys())
                for k in r_s - l_s:
                    f = Remotes[k]
                    if f.endswith(".talkmsg"):
                        colorL("new talk", f)
                        await self.new_msg(f)
                        await self.get(os.path.join(self.msg_room,f), os.path.join(self.sync_path, os.path.basename(f)))
                    else:
                        notify(f + " [new] " + k)
                        ready[k] = f
                        #await self.get(os.path.join(self.msg_room,f), os.path.join(self.sync_path, os.path.basename(f)))
                self.db['ready'] = ready
                return Remotes
            else:
                return {}

    async def new_msg(self, talk_file):
        from_user = os.path.basename(talk_file).split(".talkmsg")[0]
        host,res,t,code = await self.ssh("cat %s" % os.path.join(self.msg_room, talk_file))
        local_talk = self.db['talking', from_user]
        if not local_talk:
            local_talk = []
        un = []
        for i,n in enumerate(res.split("\n")):
            if n not in local_talk:
                un.append(n)
        nmsg = '\n\t'.join(un)
        if nmsg:
            notify(from_user + " :\n" + nmsg)
            self.db['talking'] = {from_user : res}

    async def get(self, remote, local):
        async with asyncssh.connect(self.host,port=self.port, username=self.name, client_keys=self.keyfile) as conn:
            async with conn.start_sftp_client() as sftp:
                await sftp.get(remote, local)
    
    @classmethod
    def _break_point(remote, name, server_num, finish_num=None):
        with open(name + ".point", "w") as fp:
            fp.write(" , ".join([str(i) for i in [server_num, remote]]) +" ," )
            if finish_num:
                fp.write(",".join([str(i) for i in finish_num]))

    @classmethod
    def _read_break_point(name):
        with open(name + ".point") as fp:
            server_num, remote, finish_num =  fp.readline().split(",", 2)
            finish_point = [int(i) for i in finish_num.split(",")]
            points = [True if i in finish_point else False for i in range(int(server_num))] 
            return remote, server_num, points
            
    @classmethod
    def download_multi_route(cls, url, servers, remote=None, predownload_timeout=60, only_download=False
        ,keep_after_finish=False):
        if not remote:
            end = url.split(".")[-1]
            remote = '/tmp/%s.%s' % (md5(url.encode()).hexdigest(), end)
        colorL("pre downlaod: " ,url, '--->', remote)
        hsize = {}
        pconns = {}
        csize = -1
        task = []
        
        for host,kwargs in servers:
            
            try:
                con = AsyncConnection(host, **kwargs)
                AsyncConnection.timeout_t = predownload_timeout
                size_r = con.download_pre(url, remote, timeout=predownload_timeout)
                task.append(size_r)
                pconns[host] = con
            
            except Exception as e:
                colorL(host, str(e))
        res = AsyncConnection.run_tasks(task)
        res_md5 = {}
        md5_list = []
        size_count = []
        for h,v, md5_str in res:
            # colorL(h,v,md5_str)
            if h not in pconns:continue
            if not v:
                del pconns[h]
            else:
                size_count.append(v)
                res_md5[h] = md5_str.strip()
                md5_list.append(md5_str.strip())
        c = Counter(md5_list)
        most_md5 = c.most_common()[0][0].strip()
        # colorL("md5 : ", most_md5, res_md5)
        resq = []
        used_servers = []
        if csize == -1:
            csize = Counter(size_count).most_common()[0][0]
        for h,m in res_md5.items():
            # print(h,m)
            if m == most_md5:
                resq.append(csize)
                used_servers.append(h)

        conns = [pconns[i] for i in  used_servers]
        
        count = len(resq)
        
        if csize * count != sum(resq):
            colorL("download error")
            return
        if only_download:
            return pconns 
        task = []
        block = csize // count
        n = csize % count
        server_gen = iter(conns)
        files = []
        if block > 104857:
            bshow = '%.3f M' % (block / 1024 ** 2)
            cshow = '%.3f M' % (csize / 1024 ** 2)
        elif block > 1024:
            bshow = '%.3f k' % (block / 1024 )
            cshow = '%.3f k' % (csize / 1024 )
        else:
            bshow = '%.3f b' % block
            cshow = '%.3f b' % csize
        # colorL(used_servers, count,)
        colorL("alive:", used_servers , bshow, cshow)
        load_server_num = len(used_servers)
        if os.path.exists(remote + ".point"):
            url_, all_server_num, all_points = cls._read_break_point(remote)
        else:
            all_points = [False for i in range(load_server_num)]
        try:
            for i,offset in enumerate(range(0, csize, block)):
                con = next(server_gen)
                if i == count -1 and n != 0:
                    block += block 
                if all_points[i]:
                    colorL("jump point:", i)
                    continue
                fp_t = con.download_point(remote, offset, block, index=i, keep_after_finish=keep_after_finish)
                task.append(fp_t)
        except StopIteration:
            pass
        files = AsyncConnection.run_tasks(task)
        task = []
        for f in files:
            # if error append , random one connection to download continue
            if not isinstance(f, str):
                offset, index = f
                colorL(offset, index, "die try again")
                con = random.choice(conns)
                t = con.download_point(remote, offset, block, index=index, keep_after_finish=keep_after_finish) 
                task.append(t)
                files.remove(f)
        # only one time to try
        if task:
            for f in tqdm(AsyncConnection.run_tasks(task), 'break download'):
                if isinstance(f, str):
                    files.append(f)

        if len(files) != load_server_num:
            cls._break_point(url, remote, load_server_num, [i.split(".")[-1] for i in  files])
            colorL("break point exists , file record save to ", remote + ".point")
            return 
        files = sorted(files, key=lambda x: int(x.split(".")[-1]))
        for f in tqdm(files, desc='check if exists'):
            if not os.path.exists(f):
                colorL("tmp file los : ", f)
                return
        with open(remote, 'wb') as fp:
            for f in tqdm(files):
                if not os.path.exists(f):
                    colorL("tmp file los : ", f)
                    return 
                with open(f, 'rb') as rfp:
                    fp.write(rfp.read())
        for f in files:
            os.remove(f)
        if os.path.exists(remote + ".points"):
            os.remove(remote + ".point")
    
    
    async def download_pre(self, url, remote, timeout=60):
        try:
            async with (await asyncio.wait_for(self.connector(), timeout=timeout)) as conn:
                result_p = conn.run('wget -c -t 10 -O "%s" "%s" ' % (remote, url))
                result = await asyncio.wait_for(result_p, timeout=timeout)
                result_md5 = await conn.run('md5sum "%s"' % remote)
                md5_str = re.findall('\w{32}',result_md5.stdout)[0]
                if result.exit_status == 0:
                    async with conn.start_sftp_client() as sftp:
                        res = await sftp.stat(remote)
                        colorL("pre down, size: %.1f k  " % (res.size / 1024), self.host, md5_str)
                        return self.host, res.size, md5_str
                else:
                    colorL("run download failed", self.host)
                    return self.host, None,''
        except Exception as e:
            colorL(self.host,'error', str(e))
            return self.host, None, None
    
    async def download_delete(self, remote, timeout=60):
        try:
            async with (await asyncio.wait_for(self.connector(), timeout=self.timeout_t)) as conn:
                result_p = conn.run('rm "%s" ' % (remote))
                result = await asyncio.wait_for(result_p, timeout=timeout)
                return self.host, True
        except Exception as e:
            colorL(self.host,'error', str(e))
            return self.host, None


    async def sftp_func(self, func, *args, **kwargs):
        try:
            async with (await asyncio.wait_for(self.connector(), timeout=5)) as conn:
                async with conn.start_sftp_client() as sftp:
                    self.sftp_con = sftp
                    if hasattr(sftp, func):
                        res = await getattr(sftp, func)(*args, **kwargs)
                        return res
        except Exception as e:
            colorL(self.host, str(e))

    async def download_point(self,remote, offset, size, keep_after_finish=False, index=None):
        try:
            async with (await asyncio.wait_for(self.connector(), timeout=self.timeout_t)) as conn:
                async with conn.start_sftp_client() as sftp:
                    if not index:
                        index = offset
                    _dstpath = "/tmp/%s.tmp.%d" % (md5(remote.encode()).hexdigest(), index)

                    # colorL("ready to take back: %d" % offset)
                    # async with conn.start_sftp_client() as sftp:
                    # max_requests = 128
                    block_size = 16384
                    block_count = size // block_size
                    last_size = size % block_size 
                    if size > block_size * 100:
                        block_size = size // 100
                        block_count = 100
                        last_size = size % block_size 
                    
                    async with sftp.open(remote, 'rb') as sftpf:
                        _dst = await LocalFile.open(_dstpath, 'wb')
                        
                        _boffset = 0
                        _c = 0
                        
                        for _ in tqdm(range(block_count), desc='%19s[%d]' % (self.host,index)):
                            _c += 1
                            buf = await sftpf.read(block_size , offset=offset + _boffset)
                            await _dst.write(buf, _boffset)
                            _boffset += block_size

                        if last_size:
                            buf = await sftpf.read(last_size, offset=offset + _boffset)
                            await _dst.write(buf, _boffset) 
                        await _dst.close()

                    # colorL("Point : %d [ok]" % index)
                    if not keep_after_finish:
                        await conn.run('rm %s' % (remote))
                    return _dstpath
                
        except Exception as e:
            colorL(self.host, str(e))
            return offset, index

    async def download_by_md5(self, md5):
        ready = self.db['ready']
        ready.pop('save_time')
        if md5 in ready:
            f = ready[md5]
            await self.get(os.path.join(self.msg_room, os.path.basename(f)), os.path.join(self.sync_path, os.path.basename(f)))
            colorL("down[%s]: "% md5, f)
            self.db.r.hdel('ready', md5)

    async def download_by_ready(self):
        ready = self.db['ready']
        ready.pop("save_time")
        for m in ready:
            await self.download_by_md5(m)



    async def talk(self, msg):
        name = self.room_name + ".talkmsg"
        talk_command = """
        echo  %s  >> %s
        """ % (msg, os.path.join(self.msg_room, name))
        notify(self.room_name + ": "+ msg)
        os.popen("echo %s >> %s " %(msg, os.path.join(self.sync_path, name)))
        await self.ssh(talk_command)

    async def reg(self):
        try:
            async with (await asyncio.wait_for(self.connector(), timeout=self.timeout_t)) as conn:
        
                with open(os.path.expanduser("~/.ssh/id_rsa.pub")) as fp:
                    pub = fp.read()
                    cmd = "mkdir -p ~/.ssh;  echo '%s' >> ~/.ssh/authorized_keys" % pub
                    res = await conn.run(cmd)
                    if res.exit_status == 0:
                        colorL("reg success")
        except concurrent.futures._base.TimeoutError:
            colorL(self.host, ' timeout ')
        except Exception as e:

            colorL(self.host, str(e))
    async def check_room(self):
        try:
            st = time.time()
            async with (await asyncio.wait_for(self.connector(), timeout=self.timeout_t)) as conn:
                res = await conn.run("if [ -d %s ] ;then echo 0 else mkdir -p %s ;echo 1;fi" % (self.remotepath, self.remotepath))
                if res.exit_status == 0:
                    return self.host, "ok", time.time() - st, res.exit_status
        except Exception as e:
            return self.host, res.stderr, time.time() -st , res.exit_status

    async def enuma_elish(self, method='aes-256-cfb'):
        try:
            st = time.time()
            async with (await asyncio.wait_for(self.connector(), timeout=self.timeout_t)) as conn:
                pwd = os.urandom(8).hex()
                ip = self.host
                with open("/tmp/ss-random/%s" % ip,"w") as fp:
                    f = {"server":self.host, "port_password":{str(p):pwd+ str(p) for p in range(43000,43011)}, "method": method}
                    json.dump(f, fp)
                async with conn.start_sftp_client() as sftp:
                    await sftp.put("/tmp/ss-random/%s" % ip, "/tmp/ss.json")
                cmd = """
PY=python
if [ $(which python 1>/dev/null 2>&1 ; echo $? ) -ne 0 ];then
  PY=python3;
fi
function test_cmd {
    which $1 2>&1 1>/dev/null  && echo $?;
}
if [[ $(test_cmd ea) -eq 0 ]]; then
    ea -d stop;
fi
if [[ $(test_cmd ssserver ) -eq 0 ]]; then
    ssserver -d stop;
fi
RUN="yum"
if [[ $(test_cmd apt-get ) -eq 0 ]]; then
    RUN="apt-get";
fi
if [[ $(test_cmd git) -ne 0 ]]; then
   ps aux | grep apt-get | awk '{print $2 }' | xargs kill -9;
   $RUN install -y git;
fi
$RUN install -y python;
if [ -d /tmp/abc ];then
    rm -rf /tmp/abc
fi
cd /tmp/ && git clone https://github.com/f0cklinux/enuma-elish.git abc && cd abc ;
$PY -m enuma_elish.server -d stop;  
$PY -m enuma_elish.server -c /tmp/ss.json -d start  ;
echo $?
"""
                res = await conn.run(cmd)
                if res.exit_status == 0:
                    colorL(self.host, " ok")
                    return self.host, json.dumps({'res':'Good'}), time.time() - st, 0
                else:
                    colorL(self.host, res.stderr)
                return self.host, res.stderr, time.time() -st , res.exit_status
        except concurrent.futures._base.TimeoutError:
            colorL(self.host, ' timeout ')
        except Exception as e:
            colorL(self.host, str(e))

    async def check_ss(self, enuma=False):
        try:
            st = time.time()
            async with (await asyncio.wait_for(self.connector(), timeout=self.timeout_t)) as conn:
                cmd = "ps aux | grep shadowsocks | grep '\-c' | egrep -v '(grep|egrep)' "
                if enuma:
                    cmd = "cat /tmp/ss.json"
                res = await conn.run(cmd)
                if res.exit_status == 0 and not enuma:
                    args = res.stdout.split()
                    config_file = args[args.index("-c") + 1]
                    cmd = "cat %s" % config_file
                    result = await conn.run(cmd)
                    if not os.path.exists("/tmp/ss-random"):
                        os.mkdir("/tmp/ss-random")
                    with open("/tmp/ss-random/%s" % self.host, 'w') as fp:
                        j_p = json.loads(result.stdout)
                        if 'port_password' in j_p:
                            jj = j_p['port_password']
                            port = random.choice(list(jj.keys()))
                            pwd = jj[port]
                            j_p['server_port'] = port
                            j_p['password'] = pwd
                        if not 'local_port' in j_p: 
                            j_p['local_port'] = 1080
                        j_p['server'] = self.host
                        json.dump(j_p, fp)
                    return self.host,result.stdout, time.time() - st, result.exit_status
                elif res.exit_status == 0 and enuma:
                    if not os.path.exists("/tmp/ss-random"):
                        os.mkdir("/tmp/ss-random")
                    with open("/tmp/ss-random/%s" % self.host, 'w') as fp:
                        j_p = json.loads(res.stdout)
                        if 'port_password' in j_p:
                            jj = j_p['port_password']
                            port = random.choice(list(jj.keys()))
                            pwd = jj[port]
                            j_p['server_port'] = port
                            j_p['password'] = pwd
                        if not 'local_port' in j_p: 
                            j_p['local_port'] = 1080
                        j_p['server'] = self.host
                        json.dump(j_p, fp)
                    return self.host,res.stdout, time.time() - st, res.exit_status


                return self.host,res.stderr, time.time() - st, res.exit_status


        except concurrent.futures._base.TimeoutError:
            colorL(self.host, ' timeout ')
            #return self.host,'Timeout', 999, -1
        except Exception as e:
            colorL(self.host, str(e))

    async def build_ss(self, installer='apt'):
        cmd_dict = {
            'apt':'apt update && apt install -y python3 python3-pip libsodium-dev',
            'yum':'yum update -y && yum install -y python36 python36-pip libsodium-devel && pip3.6 install pip --upgrade && iptables -A IN_public_allow  -p tcp --dport %d  -j ACCEPT',
        }
        mo = {
            "server":"0.0.0.0",
            "server_port":43001,
            "password":"hello1234",
            "method":"aes-256-cfb",
            "log-file":"/dev/null",
            "timeout":200,
        }
        try:
            async with (await asyncio.wait_for(self.connector(), timeout=self.timeout_t)) as conn:
                r = random.randint(0,9)
                #cmd = cmd_dict.get(installer) % r  
                cmd = " pip install git+https://github.com/shadowsocks/shadowsocks.git@master"
                
                mo['password'] += str(r)
                mo['server_port'] += r
                res = await conn.run(cmd)
                if res.exit_status == 0:
                    # colorL(res.stdout)
                    async with conn.start_sftp_client() as sftp:
                        with open("/tmp/shadowsocks.json","w") as fp:
                            json.dump(mo, fp)
                        await sftp.put("/tmp/shadowsocks.json", "/tmp/.shadowsocks.json")
                    colorL('build ok')
                cmd = "ssserver -c /tmp/.shadowsocks.json -d start "
                await conn.run(cmd)
                print('ssserver -s ' + self.host + ' -k ' + mo['password'] + " -m " + mo['method'] + " -p " + str(mo['server_port']) + " -l 1080" )
        except concurrent.futures._base.TimeoutError:
            colorL(self.host, ' timeout ')
        except Exception as e:
            colorL(self.host, str(e))
    
    async def dd(self, f):
        _timeout = self.__class__.timeout_t
        if not os.path.exists("/tmp/sftp_files"):
            os.mkdir("/tmp/sftp_files")
        try:
            st = time.time()
            async with (await asyncio.wait_for(self.connector(), timeout=_timeout)) as conn:
                async with conn.start_sftp_client() as sftp:
                    local = "/tmp/sftp_files/" + f.split("/")[-1] + self.host
                    await sftp.get(f, local)
                    colorL(local, '[Good]')
        except concurrent.futures._base.TimeoutError:
            colorL(self.host, 'is not connect !!')
            return self.host,'is not connect !!', time.time() - st, 127 
        except OSError as e:
            colorL(self.host, str(e))
            return self.host,'os error ', time.time() - st, 126
        except Exception as e:
            colorL(self.host, str(e))
            return self.host, str(e),time.time() - st, 999
 


    async def pings(self, f):
        _timeout = self.__class__.timeout_t
        cmds = '''#!/bin/bash
for h in $(cat /tmp/ping-to-hosts.txt | xargs);do
    res="$(dig +short $h | xargs)"
    printf '%s %s \n' $h $res | tee /tmp/pinged-hosts.txt
done

        '''

        # if _timeout > 12:
            # colorL("timeout:", _timeout)
        if not os.path.exists('/tmp/ping-run.sh'):
            
            with open('/tmp/ping-run.sh', 'w') as fp:
                with open(f) as ff:
                    for l in ff:
                        if l.startswith("http:"):
                            _,_,l = l.split("/", 2)
                        if l.endswith("/"):
                            l = l[:-1]
                        fp.write('dig +short +time=5 +tries=1 %s | awk \'{ print "%s",$0 }\' \n' % (l.strip(), l.strip()))
        try:
            st = time.time()
            async with (await asyncio.wait_for(self.connector(), timeout=_timeout)) as conn:
                async with conn.start_sftp_client() as sftp:
                    # await sftp.put(f, '/tmp/ping-to-hosts.txt')

                    put_r =  sftp.put('/tmp/ping-run.sh', '/tmp/ping-run.sh')
                    await asyncio.wait_for(put_r, timeout=_timeout)
                    colorL("ready -> ping in %s"%  self.host)

                resulte = conn.run('echo "" > /tmp/pinge-host.txt ;\n bash /tmp/ping-run.sh |tee /tmp/pinge-host.txt ')
                result = await asyncio.wait_for(resulte, timeout=_timeout)
                if result.exit_status == 0:
                    return self.host,result.stdout,time.time() - st ,0
                else:
                    return self.host,result.stderr, time.time() - st, result.exit_status
                    logging.error(result.stderr)
        except concurrent.futures._base.TimeoutError:
            colorL(self.host, 'is not connect !!')
            return self.host,'is not connect !!', time.time() - st, 127 
        except OSError as e:
            colorL(self.host, str(e))
            return self.host,'os error ', time.time() - st, 126
        except Exception as e:
            colorL(self.host, str(e))
            return self.host, str(e),time.time() - st, 999

    async def script_log(self, f):
        _timeout = self.__class__.timeout_t
        # if _timeout > 12:
            # colorL("timeout:", _timeout)
        if not os.path.exists(f):
            return 'no script to do'
        fname = os.path.basename(f)
        r_f = os.path.join('/tmp/sftp_run', fname)
        a_f = os.path.join('/tmp/sftp_run_args', fname + ".args")
        o_f = os.path.join('/tmp/sftp_out', fname + ".log")
        e_f = os.path.join('/tmp/sftp_out', fname + ".err.log")
        try:
            st = time.time()
            async with (await asyncio.wait_for(self.connector(), timeout=_timeout)) as conn:
                patch_res = conn.run("tail  %s " % o_f)
                result = await asyncio.wait_for(patch_res, timeout=_timeout)
                if result.exit_status == 0:
                    return self.host,result.stdout,time.time() - st ,0
                else:
                    return self.host,result.stderr, time.time() - st, result.exit_status
                    logging.error(result.stderr)
        except concurrent.futures._base.TimeoutError:
            colorL(self.host, 'is not connect !!')
            return self.host,'is not connect !!', time.time() - st, 127 
        except OSError as e:
            colorL(self.host, str(e))
            return self.host,'os error ', time.time() - st, 126
        except Exception as e:
            colorL(self.host, str(e))
            return self.host, str(e),time.time() - st, 999



    async def script(self, f, args_file=None):
        _timeout = self.__class__.timeout_t
        # if _timeout > 12:
            # colorL("timeout:", _timeout)
        if not os.path.exists(f):
            return 'no script to do'
        fname = os.path.basename(f)
        r_f = os.path.join('/tmp/sftp_run', fname)
        a_f = os.path.join('/tmp/sftp_run_args', fname + ".args")
        o_f = os.path.join('/tmp/sftp_out', fname + ".log")
        e_f = os.path.join('/tmp/sftp_out', fname + ".err.log")
        try:
            st = time.time()
            async with (await asyncio.wait_for(self.connector(), timeout=_timeout)) as conn:
                patch_res = conn.run("mkdir -p /tmp/sftp_out ; mkdir -p /tmp/sftp_run; mkdir -p /tmp/sftp_run_args")
                await asyncio.wait_for(patch_res, timeout=_timeout)
                async with conn.start_sftp_client() as sftp:
                    # await sftp.put(f, '/tmp/ping-to-hosts.txt')

                    patch_res =  sftp.put(f, r_f)
                    await asyncio.wait_for(patch_res, timeout=_timeout)
                    colorL("ready -> run in %s" % self.host)
                    if args_file and os.path.exists(args_file):
                        patch_res = sftp.put(args_file, a_f)
                        await asyncio.wait_for(patch_res, timeout=_timeout)
                        colorL("ready args-> in %s" % self.host)
                        r_f = "%s %s" % (r_f , a_f)

                patch_res = conn.run('nohup bash %s 1>%s 2>%s &' %(r_f, o_f, e_f))
                result = await asyncio.wait_for(patch_res, timeout=_timeout)
                if result.exit_status == 0:
                    patch_res = conn.run('tail %s' %(o_f))
                    result = await asyncio.wait_for(patch_res, timeout=_timeout)
                    return self.host,result.stdout,time.time() - st ,0
                else:
                    patch_res = conn.run('tail %s' %(e_f))
                    result = await asyncio.wait_for(patch_res, timeout=_timeout)
                    return self.host,result.stderr, time.time() - st, result.exit_status
                    logging.error(result.stderr)
        except concurrent.futures._base.TimeoutError:
            colorL(self.host, 'is not connect !!')
            return self.host,'is not connect !!', time.time() - st, 127 
        except OSError as e:
            colorL(self.host, str(e))
            return self.host,'os error ', time.time() - st, 126
        except Exception as e:
            colorL(self.host, str(e))
            return self.host, str(e),time.time() - st, 999





    async def forward(self, remote_port, local_port):
        async with asyncssh.connect(self.host,port=self.port, username=self.name, client_keys=self.keyfile, password=self.password) as conn:
            server = await conn.forward_remote_port('0.0.0.0', 33456, 'localhost', local_port)
            cmd = "ssh -CfL 0.0.0.0:{remote_port}:localhost:{rand_port} localhost -N".format(remote_port=remote_port, rand_port=33456)
            res = await conn.run(cmd)
            if res.exit_status == 0:
                colorL("success put remote's %d --> local: %d" % (remote_port, local_port))
            await server.wait_closed()

    async def close_forward(self):
        cmd = "ps aux | grep ssh | grep CfL | grep -v 'grep' |  awk '{print $2}' | xargs kill -9"
        async with asyncssh.connect(self.host,port=self.port, username=self.name, client_keys=self.keyfile, password=self.password) as conn:
            res = await conn.run(cmd)
            if res.exit_status == 0:
                colorL("close port forward" )
        

    async def share_file(self, file):
        if not os.path.exists(file):return
        remotes = await self.check_files_sync()
        remote = os.path.join(self.msg_room, os.path.basename(file))
        async with asyncssh.connect(self.host,port=self.port, username=self.name, client_keys=self.keyfile) as conn:
            async with conn.start_sftp_client() as sftp:
                f = file
                m = md5sum(f)
                if m not in remotes:
                    colorL("up",m ,f,)
                    os.popen('cp %s %s' %(file, os.path.join(self.sync_path, os.path.basename(f))))
                    await sftp.put(f, remotepath=remote)
                    colorL("fi",m)

def md5sum(file):
    with open(file, 'rb') as fp:
        return md5(fp.read()).hexdigest()

def locals_dy(root):
    locals = {}
    for file in os.listdir(root):
        f = os.path.join(root, file)
        if not os.path.isfile(f): continue
        m = md5sum(f)
        locals[m] = f
    return locals
