from market import app
from flask import render_template,redirect,url_for,flash
from market.models import Item,User
from market.forms import RegisterForm,LoginForm,PurchaseItemForm,SellItemForm
from market import db
from market import login_manager
from flask_login import login_user,logout_user
@app.route('/')
@app.route('/home')
def home_page():
    return redirect(url_for('register'))
@app.route("/market",methods=["GET","POST"])
def market():
    
    items = Item.query.all()
    purchase = PurchaseItemForm()
    if purchase.validate_on_submit():
        print(purchase['submit'])
    return render_template("market.html",title="Market",items=items,purchase=purchase)

@app.route("/register",methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        print("VALIDATING")
        user_to_create = User(username=form.username.data,
                                email=form.email.data,
                                name=form.name.data,
                                password=form.confirm_password.data)
        db.session.add(user_to_create)
        db.session.commit()
        flash(f"Successfully Registered,You are logged in as {user_to_create.username}",category="success")
        return redirect(url_for('market'))
    if form.errors!={}:
        for error_msg in form.errors.values():
            flash(f'There was an error creating the user {error_msg}',category='danger')
    return render_template('register.html',form = form,title="Register")

@app.route("/login",methods=['GET','POST'])
def login():
    form =LoginForm()
    if form.validate_on_submit():
        attempted_user=User.query.filter_by(email=form.email.data)
        if attempted_user:
            attempted_user=attempted_user.first()
            if attempted_user.check_password_correction(attempted_password=form.password.data):
                login_user(attempted_user)
                flash(f'Your are logged in as  {attempted_user.username}',category="success")
                return redirect(url_for("market"))
            else:
                flash("Wrong Password",category='danger')

        else:
            flash("The user does not exist please create an account",category='danger')


    return render_template('login.html',form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out",category='info')
    return redirect("/")