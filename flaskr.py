#!/usr/bin/python
from __future__ import with_statement
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound
import os
from flask import Flask, request, session, g, redirect, url_for, \
		abort, render_template, flash

from contextlib import closing

DEBUG = True
SECRET_KEY = 'development key'


engine = create_engine('mysql+mysqldb://root:192052@localhost:3306/plan')
Session = sessionmaker(bind=engine)
sess = Session()
Base = declarative_base()
class User(Base):
	__tablename__ = "user"

	id = Column(Integer, primary_key = True)
	username = Column(String(50))
	password = Column(String(50))
	createtime = Column(DateTime)

class Plan(Base):
	__tablename__ = "plan"
	id = Column(Integer, primary_key = True)
	userid = Column(Integer)
	content = Column(String(100))
	posttime = Column(DateTime)

class Follower(Base):
	__tablename__ = "follower"
	id = Column(Integer, primary_key = True)
	userid = Column(Integer)
	followers = Column(String(50))

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def show_plan():
	plans = sess.query(Plan).filter('userid=' + str(session['userid']))
	entries = [dict(plan=row.content, posttime=row.posttime) for row in plans] 
	return render_template('show_plans.html', entries=entries)

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		try:
			user = sess.query(User).filter("username='" + request.form['username'] +"'", 
					"password='" +request.form['password'] +"'").one()
			session['userid'] =  user.id
			flash("You were logged in")
			return redirect(url_for('show_plan'))
		except NoResultFound, e:
			error = "Invalid username or Invalid password"
	return render_template('login.html', error = error)

@app.route('/logout')
def logout():
	session.pop('userid', None)
	flash('You were logged out')
	return redirect(url_for('login'))


@app.route('/add_plan', methods=["GET", "POST"])
def add_plan():
	if request.method == 'POST':
		content = request.form['content']
		plan = Plan()
		plan.content = content
		plan.posttime = '2012-04-21 12:12:13'
		plan.userid = session['userid']
		sess.add(plan)
		sess.flush()
		return redirect(url_for('show_plan'))
	return redirect(url_for('show_plan'))



#test
@app.route('/show/<username>')
def show(username):
	s = sess.query(User,Plan).filter(Plan.userid == User.id)
	for a in s:
			print a.User.username, a.Plan
	return username

if __name__ == '__main__':
	app.run()
