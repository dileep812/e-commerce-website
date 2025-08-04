from market import app,db
from flask import render_template,redirect,url_for,flash,request
from market.models import Item,User
from market.forms import RegisterForm,LoginForm,PurchaseItemForm,SellItemForm
from flask_login import login_user,logout_user,login_required,current_user
@app.route('/')
@app.route("/home")
def home_page():
   return render_template('home.html')
@app.route('/market',methods=["GET","POST"])
@login_required
def market_page():
   purchase_form=PurchaseItemForm()
   sell_item=SellItemForm()
   if request.method=="POST":
      #purchased itms logic
      purchased_item=request.form.get('purchased_item')
      p_item=Item.query.filter_by(name=purchased_item).first()
      if p_item :
         if(current_user.budget>=p_item.price):
            p_item.owner=current_user.id
            current_user.budget-=p_item.price
            db.session.commit()
            flash(f"congratulations! you purchased {p_item.name} for {p_item.price}",category='success')
         else :
            flash(f"unfortunately you dont have enough money to purchase {p_item.name}",category='danger')
      #sold items logic 
      sold_item=request.form.get('sold_item')
      s_item=Item.query.filter_by(name=sold_item).first()
      if s_item:
         if s_item.owner==current_user.id:
            s_item.owner=None
            current_user.budget+=s_item.price
            db.session.commit()
            flash(f'successfully sold the item {s_item.name} back to market for the price {s_item.price}',category='success')
         else :
            flash(f'something went wrong {s_item.name}',category='danger')
      return redirect(url_for('market_page'))
   if request.method=="GET":
      items = Item.query.filter_by(owner=None).all()
      owned_items=Item.query.filter_by(owner=current_user.id).all()
      return render_template("market.html",items=items,purchase_form=purchase_form,owned_items=owned_items,selling_form=sell_item) 

@app.route('/register',methods=["POST","GET"])
def register_page():
   form=RegisterForm()
  
   if form.validate_on_submit():
      user_to_create=User(username=form.username.data,
                          email_address=form.email_address.data,
                          password=form.password1.data)
      db.session.add(user_to_create)
      db.session.commit()
      login_user(user_to_create)
      flash(f"Account created successfully for {user_to_create.username}!", category='success')
      return redirect(url_for("market_page"))
   if form.errors!={}:
      for i in form.errors.values():
         flash(f'the error is {i}')
   return render_template('register.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login_page():
   form=LoginForm()
   if form.validate_on_submit():
      attempted_user=User.query.filter_by(username=form.username.data).first()
      if attempted_user and attempted_user.check_password(form.password.data):
         login_user(attempted_user)
         flash(f'you are logged in successfully {attempted_user.username}',category='success')
         return redirect(url_for('market_page'))
      else:
         flash(f'username or password are not matched!plase try again',category='danger')
   return render_template('login.html',form=form)

@app.route('/logout')
def logout_page():
   logout_user()
   flash(f'you have been logged out',category="info")
   return redirect(url_for('home_page'))