import logging; logging.basicConfig(level=logging.INFO)

import asyncio,os,json,time
from datetime import datetime
from aiohttp import web

def index(request):
	return web.Response(body=b'<h1>Awesome<h1>')


async def init(loop):
	app=web.Application(loop=loop)
	app.router.add_route('get','/',index)
	srv=await loop.create_server(app.make_handler(),'127.0.0.1',9000)
	logging.info('server started at http://127.0.0.1:9000')
	return srv

async def create_pool(loop,**kw):
	logging.info('create database connection pool')
	global __pool
	__pool=await aiomysql.create_pool(
		host=kw.get('host','localhost'),
		prot=kw.get('port',3306),
		user=kw['user'],
		password=kw['password'],
		db=kw['db'],
		charset=kw.get('charset','utf8'),
		autocommit=kw.get('autocommit', True),
		maxsize=kw.get('maxsize', 10),
		minsize=kw.get('minsize', 1),
		loop=loop
		)


loop=asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()