from flask import Flask, render_template, request, session, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import json

with open('config.json','r') as c:
    params = json.load(c)["params"]


local_server = True
app = Flask(__name__)
app.secret_key = 'super-secret-key'



if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']


else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['proud_uri']

db = SQLAlchemy(app)


class orders(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    service = db.Column(db.String(500), nullable=False)
    supplier_names= db.Column(db.String(500), nullable=False)
    product_names = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    customer_id = db.Column(db.String(120), nullable=False)

class customers(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    phone_no = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(120), nullable=False)

class supplier(db.Model):
    supplier_id = db.Column(db.Integer,  primary_key=True)
    supplier_name = db.Column(db.String, nullable=False)
    

class product(db.Model):
    product_id = db.Column(db.Integer,  primary_key=True)
    product_name = db.Column(db.String, nullable=False)
    


class Logs(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String, nullable=True)
    action = db.Column(db.String(30), nullable=False)
    date = db.Column(db.String(100), nullable=False)



@app.route("/")
def hello():

    return render_template('index.html', params=params)

@app.route("/index")
def home():

    return render_template('dashboard.html', params=params)


@app.route("/search",methods=['GET','POST'])
def search():

    if request.method == 'POST':

        name = request.form.get('search')
        post = supplier.query.filter_by(supplier_name=name).first()
        pro = product.query.filter_by(product_name=name).first()

        if (post or pro):
            flash("Item Is Available.", "primary")

        else:
            flash("Item is not Available.", "danger")


    return render_template('search.html', params=params)

@app.route("/details", methods=['GET','POST'])
def details():

    if ('user' in session and session['user'] == params['user']):
        posts = Logs.query.all()
        return render_template('details.html', params=params, posts=posts)


@app.route("/aboutus")
def aboutus():
    return render_template('aboutus.html', params=params)



@app.route("/insert", methods = ['GET','POST'])
def insert():


    if (request.method == 'POST'):
        '''ADD ENTRY TO THE DATABASE'''
        customer_id=request.form.get('customer_id')

        customer_name = request.form.get('customer_name')
        age = request.form.get('age')
        phone_no = request.form.get('phone_no')
        address = request.form.get('address')
        push = customers(customer_id=customer_id,customer_name=customer_name, age=age, phone_no=phone_no, address=address)
        db.session.add(push)
        db.session.commit()

        flash("Thanks for submitting your details","danger")


    return render_template('insert.html',params=params)


@app.route("/supply", methods = ['GET','POST'])
def supply():


    if (request.method == 'POST'):
        '''ADD ENTRY TO THE DATABASE'''

        supplier_name = request.form.get('supplier_name')

        push=supplier(supplier_name = supplier_name,)
        db.session.add(push)
        db.session.commit()
        flash("Thanks for adding new items", "primary")
    return render_template('search.html', params=params)

@app.route("/products", methods = ['GET','POST'])


def products():


    if (request.method == 'POST'):
        '''ADD ENTRY TO THE DATABASE'''

        product_name = request.form.get('product_name')
        push=product(product_name=product_name,)
        db.session.add(push)
        db.session.commit()
        flash("Thanks for adding new items", "primary")
    return render_template('search.html', params=params)


@app.route("/list",methods=['GET','POST'])
def list():

    if ('user' in session and session['user'] == params['user']):

        posts = orders.query.all()
        return render_template('post.html', params=params, posts=posts)



@app.route("/items",methods=['GET','POST'])
def items():

    if ('user' in session and session['user'] == params['user']):

        posts = supplier.query.all()
        return render_template('items.html', params=params,posts=posts)


@app.route("/items2", methods=['GET','POST'])
def items2():

    if ('user' in session and session['user'] == params['user']):


        posts = product.query.all()
        return render_template('items2.html',params=params,posts=posts)


@app.route("/sp",methods=['GET','POST'])
def sp():

    if ('user' in session and session['user'] == params['user']):

        posts=orders.query.all()
        return render_template('store.html', params=params,posts=posts)


@app.route("/logout")
def logout():

    session.pop('user')
    flash("You are logout", "primary")

    return redirect('/login')


@app.route("/login",methods=['GET','POST'])
def login():

    if ('user' in session and session['user'] == params['user']):
        posts = customers.query.all()
        return render_template('dashboard.html',params=params,posts=posts)

    if request.method=='POST':

        username=request.form.get('uname')
        userpass=request.form.get('password')
        if(username==params['user'] and userpass==params['password']):

            session['user']=username
            posts=customers.query.all()
            flash("You are Logged in", "primary")

            return render_template('index.html',params=params,posts=posts)
        else:
            flash("wrong password", "danger")

    return render_template('login.html', params=params)


@app.route("/edit/<string:customer_id>",methods=['GET','POST'])

def edit(customer_id):
    if('user' in session and session['user']==params['user']):
        if request.method =='POST':
            customer_name=request.form.get('customer_name')
            age=request.form.get('age')
            phone_no=request.form.get('phone_no')
            address=request.form.get('address')


            if customer_id==0:
                posts=customers(customer_name=customer_name,age=age,phone_no=phone_no,address=address)

                db.session.add(posts)
                db.session.commit()
            else:
                post=customers.query.filter_by(customer_id=customer_id).first()
                post.customer_name=customer_name
                post.age=age
                post.phone_no=phone_no
                post.address=address
                db.session.commit()
                flash("data updated ", "success")

                return redirect('/edit/'+customer_id)
        post = customers.query.filter_by(customer_id=customer_id).first()
        return render_template('edit.html',params=params,post=post)




@app.route("/delete/<string:customer_id>", methods=['GET', 'POST'])
def delete(customer_id):
    if ('user' in session and session['user']==params['user']):
        post=customers.query.filter_by(customer_id=customer_id).first()
        db.session.delete(post)
        db.session.commit()
        flash("Deleted Successfully", "warning")

    return redirect('/login')

@app.route("/deletemp/<string:order_id>", methods=['GET', 'POST'])
def deletemp(order_id):
    if ('user' in session and session['user']==params['user']):
        post=orders.query.filter_by(order_id=order_id).first()
        db.session.delete(post)
        db.session.commit()
        flash("Deleted Successfully", "primary")

    return redirect('/list')


@app.route("/supplier_name", methods = ['GET','POST'])
def supplier_name():
    if(request.method=='POST'):
        '''ADD ENTRY TO THE DATABASE'''
        customer_id=request.form.get('customer_id')
        service=request.form.get('service')
        supplier_names=request.form.get('supplier_names')
        product_names=request.form.get('product_names')
        email=request.form.get('email')
        amount=request.form.get('amount')

        entry=orders(customer_id=customer_id,service=service,supplier_names=supplier_names,product_names=product_names,email=email,amount=amount)
        db.session.add(entry)
        db.session.commit()
        flash("Data Added Successfully","primary")


    return render_template('supplier_name.html',params=params)



app.run(debug=True)