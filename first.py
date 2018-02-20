from bottle import template,default_app,get, post, request, route,run # or route
import sqlite3
import tasks
import tuling

#DATABASE = '/home/hiffin/mysite/todo.db'
DATABASE = 'todo.db'

@get('/login') # or @route('/login')
def login():
    return '''
        <form action="/login" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Login" type="submit" />
        </form>
    '''
def check_login(username, password):
    if(username == password):
        return True
    else:
        return False
@post('/login') # or @route('/login', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_login(username, password):
        return "<p>Your login information was correct.</p>"
    else:
        return "<p>Login failed.</p>"
@route('/<what>')
def index(what="hello"):
    r = tuling.tuling(what)
    return r


@route('/')    
@route('/todo')
def todo_list():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT id, task FROM todo WHERE status LIKE '1'")
    
    result = c.fetchall()
    print(result)
    output = template('make_table', rows=result)
    return output
@route('/todoM')
def todo_list_mongo():
    result = list(tasks.current_tasks.find())
    print (result)
    output = template('make_table', rows=result)

@get('/new')
def new_item():

        return template('new_task.tpl')

@post('/new')
def post_new():
    new = request.forms.get('task')
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    c.execute("INSERT INTO todo (task,status) VALUES (?,?)", (new, 1))
    new_id = c.lastrowid

    conn.commit()
    c.close()

    return '<p>The new task was inserted into the database, the ID is %s</p>' % new_id

#application = default_app()
run(host='0.0.0.0', port=80)
