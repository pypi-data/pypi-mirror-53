import asyncio, asyncssh, sys,os
from functools import partial
import time



async def run_client(host, port, password=None, keyfile=os.path.expanduser("~/.ssh/id_rsa"), remote_port=8888, local_port=8888):
    async with asyncssh.connect(host, port=port, password=password, client_keys=keyfile) as conn:
        print("conn ")
        server = await conn.forward_remote_port('0.0.0.0', 33456, 'localhost', local_port)
        cmd = "ssh -CfL 0.0.0.0:{remote_port}:localhost:{rand_port} localhost -N".format(remote_port=remote_port, rand_port=33456)
        res = await conn.run(cmd)
        if res.exit_status == 0:
            colorL("success put remote's %d --> local: %d" % (remote_port, local_port))
        await server.wait_closed()


try:
    asyncio.get_event_loop().run_until_complete(run_client(sys.argv[1], int(sys.argv[2])))
except (OSError, asyncssh.Error) as exc:
    sys.exit('SSH connection failed: ' + str(exc))
