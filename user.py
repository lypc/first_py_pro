from orm import Model,StringField,IntegerField
import app

async def select(sql,args,size=None):
	log(sql,args)
	global __pool
	with(await __pool)as conn:
		cur=await conn.cursor(aiomysql.DictCursor)
		await cur.execute(sql.replace('?','%s'),args or ())
		if size:
			rs=await cur.fetchmany(size)
		else:
			rs=await cur.fetchall
		await cur.close()
		logging.info('rows return : %s' % len(rs))
		return rs

async def execute(sql,args):
	log(sql)
	with(await __pool)as conn:
		try:
			cur=await conn.cursor()
			await cur.execute(sql.replace('?','%s'),args or ())
			affected=cur.rowcount
			await cur.close()
		except BaseException as e:
			raise
		return affected

class User(Model):
	__table__='users'

	id=IntegerField(primary_key=True)
	name=StringField()

def test():
	user=User(id=123,name='Michael')
	yield from user.save()
	users=user.findAll()
