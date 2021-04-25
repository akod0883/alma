""" Specifies routing for the application"""
from flask import render_template, request, jsonify, url_for, flash, redirect, Flask
from app import app, bcrypt, db
from app import database as db_helper
from app import forms as forms


@app.route("/delete/<int:task_id>", methods=['POST'])
def delete(task_id):
    """ recieved post requests for entry delete """

    try:
        db_helper.remove_task_by_id(task_id)
        result = {'success': True, 'response': 'Removed task'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/edit/<int:task_id>", methods=['POST'])
def update(task_id):
    """ recieved post requests for entry updates """

    data = request.get_json()

    try:
        if "status" in data:
            db_helper.update_status_entry(task_id, data["status"])
            result = {'success': True, 'response': 'Status Updated'}
        elif "description" in data:
            db_helper.update_task_entry(task_id, data["description"])
            result = {'success': True, 'response': 'Task Updated'}
        else:
            result = {'success': True, 'response': 'Nothing Updated'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/create", methods=['POST'])
def create():
    """ recieves post requests to add new task """
    data = request.get_json()
    db_helper.insert_new_task(data['description'])
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)


@app.route("/newRestaurants")
def newRestaurants():
    """ returns rendered homepage """
    items = db_helper.fetch_todo()
    advanced_query = db_helper.advanced_query()
    return render_template("index.html", items=items, query=advanced_query[0])


@app.route("/testing")  # temp for now
def homepage():
    return render_template("homepage.html")


@app.route("/about")
def about():
    return render_template("about.html")


# THIS IS NEW


posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        conn = db.connect()
        conn.execute('Insert Into users (username, email, password) VALUES ("{}", "{}", "{}");'.format(
            form.username.data, form.email.data, hashed_password))
        flash(f'Your acount has been created. You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        conn = db.connect()
        query_results = conn.execute("Select username from users;").fetchall()
        conn.close()
        exists = False
        for each in query_results:
            if form.username.data == each[0]:
                # no user object here
                conn = db.connect()
                user_password = conn.execute(
                    ("Select password from users where username LIKE '{}'").format(form.username.data))
        flash('Login Unsuccessful. Please check username and password.', 'danger')
    return render_template('login.html', title='Login', form=form)
