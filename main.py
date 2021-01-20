import os
import sqlite3
from flask import Flask, redirect, request, render_template, flash, g, url_for
from db import Database


DATABASE_FILE = 'db.db'
DEBUG = True
SECRET_KEY = 'xzf39d7348yfui'


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

@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'link_db'):
		g.link_db.close()



@app.route('/',methods=['POST','GET'])
def index():
	if request.method == 'POST':
		if request.form['link'].startswith('https://') and len(request.form['rlink']) < 32:
			db = get_db()
			dbase = Database(db)
			flash('Ссылка успешно добавлена!')
			print(request.form['link'],request.form['rlink'])
			dbase.add_link(request.form['link'],request.form['rlink'])
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
    port = int(os.environ.get('PORT', 4997))
    app.run(port=port,debug=True)