import os
from mroylib.config import Config
from qlib.data import Cache, dbobj
from redis import Redis
from termcolor import colored
import logging
import time
from functools import partial
from glob import glob



C = Config(file=os.path.expanduser("~/.config/fshare.ini"))

logging.basicConfig(level=C.get('verbose', 'ERROR'))

SQL_PATH = os.path.expanduser("~/.config/seed/cache.db")
Sql = Cache(SQL_PATH)

def change_sqlite_file(ff):
    global Sql
    Sql = ff

class Host(dbobj):pass

class HostDb:
    task = []
    split_file={}
    
    def __init__(self, sql=None):
        self.sql= sql
        if not self.sql:
            self.sql = Sql
        

    def log(self, obj):
        if hasattr(self, "_result"):
            self._result.append(obj)
        msg = ""
        cmd = "%s: %s " 
        D = obj.get_dict()
        for k in D:
            msg += cmd % (colored(k,'green'), colored(D[k], attrs=['underline']))
        print(msg)
    
    def patch_one(self, obj, asyn=None,fun=None, args=None, kargs=None):
        a = asyn(host=obj.host, password=obj.passwd, port=int(obj.port), name=obj.user, keyfile=None)
        f = getattr(a, fun)
        # print(obj.get_dict(),args, kargs)
        run_f = f(*args, **kargs)
        self.__class__.task.append(run_f)

    def patch_mul(self, obj, asyn=None,fun=None, args=None, kargs=None):
        a = asyn(host=obj.host, password=obj.passwd, port=int(obj.port), name=obj.user, keyfile=None)
        f = getattr(a, fun)
        # print(obj.get_dict(),args, kargs)
        for k in self.__class__.split_file:
            vals = self.__class__.split_file[k]
            if k in kargs:
                kargs[k] = vals.pop()
        run_f = f(*args, **kargs)
        self.__class__.task.append(run_f)

    @classmethod
    def split_args(cls,k, f, num):
        c = os.popen("wc -l %s" % f).read().split()[0]
        ec =  int(c) // (num -1)
        r = "split -l %d %s %s && ls %s.s.* "% (ec, f, f+".s.", f)
        print(c,num,r)
        os.popen(r).read()
        s = []
        for f in glob(f + ".s.*"):
            s.append(f)
        cls.split_file[k] =s


    def search_run(self, key,asyn,fun, *args, split_file=False, **kargs):
        if asyn and fun:
            if split_file and split_file in kargs:
                c = len([1 for i in self.sql.fuzzy_search(Host, key)])
                fs = HostDb.split_args(split_file, kargs[split_file], c)

                pt = partial(self.patch_mul, asyn=asyn ,fun=fun, args=args, kargs=kargs)
                [i for i in self.sql.fuzzy_search(Host, key, printer=pt)]
                res = asyn.run_tasks(self.task)
                self.__class__.split_file = {}
                return res
            else:
                pt = partial(self.patch_one, asyn=asyn ,fun=fun, args=args, kargs=kargs)
                [i for i in self.sql.fuzzy_search(Host, key, printer=pt)]
                res = asyn.run_tasks(self.task)
                return res

    def search(self, key):
        self._result = []
        [i for i in self.sql.fuzzy_search(Host, key, printer=self.log)]
        return self._result


class RDb:
    def __init__(self, db, decode=True,rolling=True):
        self.if_decode = decode
        self.rolling = rolling
        self.r = Redis(host=C['db-host'], db=db, decode_responses=decode)

    def __setitem__(self, p, mapping):
        if isinstance(p, tuple) and len(p) == 2:
            self.r.hset(p[0], p[1], mapping)
        else:
            save_time = time.time()
            mapping['save_time'] = save_time
            self.r.hmset(p, mapping)

    def __getitem__(self, k):
        if isinstance(k,tuple) and len(k) == 2:
            return self.r.hget(k[0], k[1])
        else:
            return self.r.hgetall(k)

    def keys(self, k=None, group_by=None, sorted_key=None):
        if k:
            return self.r.hkeys(k)
        if group_by:
            e = {}
            for k in self.keys():
                val = self[k, group_by]
                w = e.get(val, [])
                w.append(k)
                e[val] = w
        else:
            e = self.r.keys()


        if sorted_key:
            return sorted(e, key=sorted_key)
        else:
            return e

    def search(self, key, subkey=None):
        for k in self.keys():
            if key in k:
                if not subkey:
                    yield self[k]
                else:
                    yield self[k,subkey]
    def search_one(self, key, subkey=None):
        return next(self.search(key, subkey))

    @property
    def chains_name(self):
        _e = "|" if self.if_decode else b"|"
        names = set()
        for k in self.keys():
            names.add(k.split(_e,1)[0])
        return names

    def _chains(self, name):
        _e = "|" if self.if_decode else b"|"
        for k in self.keys():
            if k.startswith(name + _e):
                yield self[k]
    def chains(self, name, sort_by='save_time'):
        _e = sort_by if self.if_decode else sort_by.encode()
        res = self._chains(name)
        return sorted(res, key=lambda x: x[_e], reverse=True)

