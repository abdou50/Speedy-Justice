from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from pymongo import MongoClient
from uuid import uuid4
from datetime import datetime

# init mongodb client

db = MongoClient('mongodb+srv://aymensystem7:qhdwCZJI9yVruWFf@cluster0.w2w6pon.mongodb.net/?retryWrites=true&w=majority', connect=False)
# init database
db = db['test-database']
# init collection
users = db['users']
atlas_pw = 'qhdwCZJI9yVruWFf'

app = Flask(__name__)
app.secret_key = 'secret123'

def get_form_to_dict(form):
    print(form)
    dic = {}
    if "_id" not in form:
        dic["_id"] = str(uuid4())
    for key, value in form.items():
        dic[key] = value
    dic["created_at"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    dic["updated_at"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    print(dic)
    return dic


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', user=current_user)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        dic = get_form_to_dict(request.form)
        print(dic.keys())
        error = None
        found = db.users.find_one({'email': dic.get('email')})
        if not dic["username"]:
            error = 'Username is required.'
        elif not dic["password"]:
            error = 'Password is required'
        elif  found != None:
            error = 'Email already in use'

        if error is None:
                db.users.insert_one(dic)
                print('user created')
                return redirect(url_for('login'))
        else:
            return redirect(url_for('signup'))

    return render_template('signup.html', user=current_user)
       

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None
        user = db.users.find_one({'email': email})

        if user is None:
            error = 'Incorrect email.'
        elif not user['password'] == password:
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['_id']
            return render_template('check.html')

        flash(error)

    return render_template('login.html', title='Login')

@app.route('/logout')
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for('home'))
@app.route
@app.route('/check')
def check():
    return redirect(url_for('check'))

@app.route('/law')
def law():
	return render_template('law.html')



@app.route('/av1')
def av1():
	return render_template('1-avocat.html')
@app.route('/av2')
def av2():
	return render_template('2-avocat.html')
@app.route('/av3')
def av3():
	return render_template('3-avocat.html')
@app.route('/pers')
def pers():
	return render_template('personal-card.html')
@app.route('/cri')
def cri():
	return render_template('criminal-card.html')
@app.route('/lab')
def lab():
	return render_template('labour-card.html')



if __name__ == '__main__':
    app.run(debug=True)