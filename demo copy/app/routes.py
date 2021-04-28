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


# posts = [
#     {
#         'author': 'Corey Schafer',
#         'title': 'Blog Post 1',
#         'content': 'First post content',
#         'date_posted': 'April 20, 2018'
#     },
#     {
#         'author': 'Jane Doe',
#         'title': 'Blog Post 2',
#         'content': 'Second post content',
#         'date_posted': 'April 21, 2018'
#     }
# ]


@app.route("/")
@app.route("/home")
def home():
    posts = []
    if forms.LOGGED_USER != 'empty':
        conn = db.connect()
        results = conn.execute('SELECT RestaurantName, Review, ReviewNumber FROM UserRestaurantReviews WHERE UserName = "{}";'.format(forms.LOGGED_USER)).fetchall()
        conn.close()
        for result in results:
            item = {
                "UserName": forms.LOGGED_USER,
                "RestaurantName": result[0],
                "Review": result[1],
                "ReviewNumber": result[2]
            }
            posts.append(item)
    return render_template('home.html', posts=posts, logged_user=forms.LOGGED_USER)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        conn = db.connect()
        conn.execute('Insert Into users (username, email, password) VALUES ("{}", "{}", "{}");'.format(
            form.username.data, form.email.data, hashed_password))
        conn.close()
        flash(f'Your acount has been created. You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form, logged_user=forms.LOGGED_USER)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        conn = db.connect()
        query_results = conn.execute("Select username from users;").fetchall()
        conn.close()
        for each in query_results:
            if form.username.data == each[0]:
                # no user object here
                conn = db.connect()
                password_query = conn.execute(
                    ("Select password from users where username LIKE '{}'").format(form.username.data)).fetchall()
                conn.close()
                for password in password_query:
                    if bcrypt.check_password_hash(password[0], form.password.data):
                        user = form.username.data
                        forms.LOGGED_USER = user
                        print(forms.LOGGED_USER)
                        flash(
                            ('Login Successful. Welcome {}').format(form.username.data), 'success')
                        return redirect(url_for('home'))
        flash('Login Unsuccessful. Please check username and password.', 'danger')
    return render_template('login.html', title='Login', form=form, logged_user=forms.LOGGED_USER)


@app.route("/logout")
def logout():
    forms.LOGGED_USER = 'empty'
    return redirect(url_for('home'))


@app.route("/create_reviews/new", methods=['GET', 'POST'])
def create_reviews():
    form = forms.ReviewsForm()
    if form.validate_on_submit():
        conn = db.connect()
        conn.execute('Insert Into UserRestaurantReviews (UserName, RestaurantName, MealCost, ConvenienceRating, FoodRating, Review) VALUES ("{}", "{}", "{}", "{}", "{}", "{}");'.format(
            forms.LOGGED_USER, form.title.data, form.meal_cost.data, form.convenience_rating.data, form.food_rating.data, form.content.data))
        conn.close()
        flash('Your post has been created! Thank you for your review!', 'success')
        return redirect(url_for('home'))
    return render_template('create_review.html', title='New Review', 
                                            form=form, legend='New Review')


@app.route("/create_reviews/<int:ReviewNumber>")
def access_reviews(ReviewNumber):
    conn = db.connect()
    post = []
    result = conn.execute(
        "SELECT * FROM UserRestaurantReviews WHERE ReviewNumber = '{}' AND UserName = '{}';".format(ReviewNumber, forms.LOGGED_USER)).fetchall()
    item = {
        "UserName": forms.LOGGED_USER,
        "RestaurantName": result[0][1],
        "MealCost": result[0][2],
        "ConvenienceRating": result[0][3],
        "FoodRating":result[0][4],
        "Review": result[0][5],
        "ReviewNumber": ReviewNumber   
    }
    post.append(item) 
    conn.close()
    return render_template('post.html', post=post)

          

@app.route("/create_reviews/<int:ReviewNumber>/update", methods=['GET', 'POST'])
def update_review(ReviewNumber):
    conn = db.connect()
    post = []
    result = conn.execute(
        "SELECT * FROM UserRestaurantReviews WHERE ReviewNumber = '{}';".format(ReviewNumber)).fetchall()
    item = {
        "UserName": forms.LOGGED_USER,
        "RestaurantName": result[0][1],
        "MealCost": result[0][2],
        "ConvenienceRating": result[0][3],
        "FoodRating":result[0][4],
        "Review": result[0][5]
        
    }
    post.append(item) 
    form = forms.ReviewsForm()
    if form.validate_on_submit():
        post[0]["RestaurantName"] = form.title.data
        post[0]["Review"] = form.content.data
        post[0]["UserName"] = forms.LOGGED_USER
        post[0]["MealCost"] = form.meal_cost.data
        post[0]["ConvenienceRating"] = form.convenience_rating.data
        post[0]["FoodRating"] = form.food_rating.data
        commit = conn.execute("Update UserRestaurantReviews SET Review = '{}', MealCost = '{}', ConvenienceRating = '{}', FoodRating = '{}', RestaurantName = '{}' WHERE ReviewNumber = '{}';".format(form.content.data, form.meal_cost.data, form.convenience_rating.data, form.food_rating.data, form.title.data, ReviewNumber))

        flash('Your review has been updated!', 'success')
        return redirect(url_for('access_reviews', ReviewNumber=ReviewNumber))
    elif request.method == 'GET':
        form.title.data = post[0]["RestaurantName"]
        form.content.data = post[0]["Review"]
        forms.LOGGED_USER = post[0]["UserName"]
        form.convenience_rating.data = post[0]["ConvenienceRating"]
        form.meal_cost.data = post[0]["MealCost"]
        form.food_rating.data = post[0]["FoodRating"]
    conn.close()
    return render_template('create_review.html', title='Update Review', 
                                form=form, legend='Update Review')



@app.route("/create_reviews/<int:ReviewNumber>/delete", methods=['POST'])
def delete_review(ReviewNumber):
    conn = db.connect()
    conn.execute("DELETE FROM UserRestaurantReviews WHERE ReviewNumber = '{}';".format(ReviewNumber))
    conn.close()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

# User will press search button in navigation bar. There they will search a restaurant by name and all the reviews and ratings will
# be listed 

@app.route("/search", methods=['GET', 'POST'])
def search_review():
    form = forms.SearchForm()
    posts = []
    if form.validate_on_submit():
        conn = db.connect()
        results = conn.execute("SELECT * FROM UserRestaurantReviews WHERE RestaurantName = '{}';".format(form.restaurant_name.data)).fetchall()
        count = conn.execute("SELECT COUNT(RestaurantName) FROM UserRestaurantReviews WHERE RestaurantName = '{}' GROUP BY RestaurantName;".format(form.restaurant_name.data)).fetchall()
        if len(results) == 0:
            flash('The restaurant you searched does not exist', 'danger')
            return redirect(url_for('search_review'))
        conn.close()
        for result in results:
            item = {
                "UserName": forms.LOGGED_USER,
                "RestaurantName": result[1],
                "MealCost": result[2],
                "ConvenienceRating": result[3],
                "FoodRating":result[4],
                "Review": result[5]
            }
            posts.append(item)
    return render_template('search.html', posts=posts, form=form)