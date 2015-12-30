import logging; logging.basicConfig(level=logging.INFO)
from models import User, Blog, Comment
import asyncio,os,json,time,orm
from datetime import datetime
from aiohttp import web

def index(request):
	return web.Response(body=b'<h1>Awesome<h1>')


@asyncio.coroutine
def init(loop):
	yield from orm.create_pool(loop, user='root', password='77778888', db='awesome')
	app=web.Application(loop=loop)
	app.router.add_route('get','/',index)
	srv=yield from loop.create_server(app.make_handler(),'127.0.0.1',9000)
	logging.info('server started at http://127.0.0.1:9000')
	return srv



loop=asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()