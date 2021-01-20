import os
import sqlite3
from flask import Flask, redirect, request, render_template, flash, g, url_for
from db import Database
import requests


DATABASE_FILE = 'db.db'
DEBUG = True
SECRET_KEY = 'xzf39d7348yfui'
HOST = 'http://127.0.0.1'
PORT = '4997'


app = Flask(__name__)
app.config.from_object(__name__	)


def connect_db():
	conn = sqlite3.connect(app.config['DATABASE_FILE'])
	conn.row_factory = sqlite3.Row
	return conn

def get_db():
	if not hasattr(g, 'link_db'):
		g.link_db = connect_db()
	return g.link_db

def validation_link(link: str) -> bool:
	if link.startswith('https://'):
		return True

@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'link_db'):
		g.link_db.close()

@app.route('/',methods=['POST','GET'])
def index():
	if request.method == 'POST':
		if validation_link(request.form['link']):
			requests.post(f'{HOST}:{PORT}{url_for("create_link")}',params={'link': request.form['link'], 'redirect_link': request.form['rlink']})
			flash('Ссылка успешно добавлена!')
		else:
			flash('Ошибка добавления')

	return render_template('index.html',title='Главная')

@app.route('/<path:link>')
def get_link(link):
	try:
		db = get_db()
		dbase = Database(db)
		return redirect(dbase.get_link(link)['true_url'])
	except TypeError:
		return 'Такой ссылки нет!'

@app.route('/create_link',methods=['POST','GET'])
def create_link():
	db = get_db()
	dbase = Database(db)
	print(request.args.get('link'),request.args.get('redirect_link'))
	dbase.add_link(request.args.get('link'),request.args.get('redirect_link'))
	return redirect(url_for('index'))

if __name__ == '__main__': 
    app.run(port=PORT,debug=DEBUG)