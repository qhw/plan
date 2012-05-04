#!/usr/bin/python

from sqlalchemy import *

db = create_engine('mysql+mysqldb://root:192052@localhost:3306/orm')
db.echo = True
metadata = MetaData(db)


users_table = Table('user', metadata,
		Column('user_id', Integer,primary_key=True),
		Column('user_name', String(40)),
		Column('password', String(10))
		)

metadata.engine.echo = True
users_table.create()

i = users_table.insert()

print i

i.execute(user_name='Mary', password='secure')

i.execute({'user_name':'Tom'},{'user_name':'Fred'},{'user_name':'Harry'})


