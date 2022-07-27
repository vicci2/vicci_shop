from flask import Flask, flash, redirect, render_template, request, url_for
# SQL Achemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import  func, extract, DateTime 
# flask login
from flask_login import UserMixin,login_user,logout_user,login_required,current_user,LoginManager
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime, date, time
from email.policy import default
# from configs.base_config import Config ,Development, Testing, Production


# import psycopg2
# passing the app to flask:
app =Flask(__name__)
app.secret_key="123secretkye"#THE SECRET KEY

#Establish Connection
try:
    # defining the UPI to establis a connection:     
    # app.config['SQLALCHEMY_DATABASE_URI']= "postgresql://postgres:vicciSQL@localhost:5432/alchemy"
    app.config['SQLALCHEMY_DATABASE_URI']='postgresql://rschqcsgcjxcuk:89063701bcfb6750313f9247b4ed9330b055aa4114d975baa82b474c65b9b57c@ec2-99-81-137-11.eu-west-1.compute.amazonaws.com:5432/dedp2umiglp1rr'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    print ("Successfullly connected to the  Vicci database")
except:
    print ("Unable to connect to the  Vicci database")

# db(app) we use this to give the app a database:

db = SQLAlchemy(app)

# Creating required tables
class Suppliers(db.Model):
    __tablename__='suppliers'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False)
    name=db.Column(db.String(80), nullable=False)
    email=db.Column(db.String(80), nullable=False)
    tel_1=db.Column(db.String(80) ,nullable=False)
    tel_2=db.Column(db.String(80) ,nullable=True)
    product=db.Column(db.String(80) ,nullable=False)

class Stock(db.Model):
    __tablename__='stock'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False)
    product_name=db.Column(db.String(80), nullable=False)
    quantity=db.Column(db.Numeric(15), nullable=False)
    b_p=db.Column(db.Numeric(15) ,nullable=False)
    date= db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    # date= db.Column(db.DateTime(timezone=True), nullable = False, default = func.now())

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True, nullable=False)
    name = db.Column(db.String(80), unique=True)
    bp = db.Column(db.Numeric(15), unique=False)
    sp = db.Column(db.Numeric(15), unique=False)
    quantity = db.Column(db.Numeric(15),nullable=False )
    serial_no = db.Column(db.Integer, unique=True)
    product=db.relationship('Sales',backref=db.backref('product',lazy=True))

class Sales(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True, nullable=False)
    product_id = db.Column (db.Integer, db.ForeignKey('product.id'), autoincrement = True)
    quantity = db.Column(db.Numeric(15), unique=False)
    created_at = db.Column(db.DateTime,nullable=False ,default=datetime.utcnow) 

class Newsletter(db.Model):
    __tablename__= 'newsletter'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True , nullable=False)
    fname=db.Column(db.String(150) , unique= False)
    lname = db.Column(db.String(80), unique=False)   
    email = db.Column(db.String(80), unique=True)
    tel=db.Column(db.String(80) ,nullable=True)
    status =db.Column(db.String(20),nullable=False,unique=False)
    date=db.Column(db.DateTime(timezone=True), nullable=False ,default = func.now() ) 

class Users(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True, nullable=False)
    designation = db.Column(db.String(80), unique=False)
    e_id = db.Column(db.Integer, unique=True)
    fname = db.Column(db.String(80), unique=False)
    lname = db.Column(db.String(80), unique=False)
    uname = db.Column(db.String(80), unique=True)    
    email = db.Column(db.String(80), unique=True)
    tel=db.Column(db.String(80) ,nullable=False)
    upasscode = db.Column(db.String(250), nullable=False)
    whatsapp=db.Column(db.String(80) ,nullable=True)
    tgram=db.Column(db.String(80) ,nullable=True,unique=True)
    igram=db.Column(db.String(80) ,nullable=True,unique=True)

#Using LoginManager
login_manager = LoginManager()
login_manager.login_view ="ims"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))
       
# Cucustom date cleaner jinja filter:
@app.template_filter("clean_date")
def clean_date(dt):
    return dt.strftime("%d %b %Y ")

@app.route('/')#landing page
def ims():
    return render_template("viccistockims.html")

@app.route('/home')
@login_required
def home():
    inventory=db.session.query(db.func.sum(Product.quantity)).all()
    stock=db.session.query(db.func.sum(Stock.quantity)).all()
    sales=db.session.query(db.func.count(Sales.id)).all()
    print(inventory,stock,sales)
    return render_template("viccistockhome.html", data1=inventory,data2=stock,data=sales)

@app.route('/dashboard')
@login_required
def dash():
    # cur.execute("SELECT  extract(year from sl.created_at) || '-' || extract(month from sl.created_at) || '-' |
    # | extract(day from sl.created_at)as date, sum((pr.sp-pr.bp)* sl.quantity) as totalprofit FROM public.sales as sl 
    # join products as pr on pr.id=sl.product_id  group by sl.created_at order by sl.created_at ASC")    
    label=[]
    data=[]   
    for i in data:
        label.append(i[0])
        data.append(int(i[1]))
    print("abxb",data,"uybce",label)
    return render_template("viccistockdash.html",label=label,data=data,user=current_user)

@app.route('/inventory', methods=["GET","POST"])
@login_required
def invent():
    invtory=Product.query.all()    
    print(invtory)    
    return render_template("viccistockinvetry.html",invtory=invtory)

@app.route('/add_item',methods=["POST"])
def adder():
    if request.method == "POST": 
        nam=request.form["name"]
        # desg=request.form["desg"]
        # upass=request.form["pass"]
        qtt=int(request.form["qtt"])
        result=Product.query.filter_by(name=nam ).first()
        if result:
            # usr=Users.query.filter(db.or_,desg=="Admin" , desg =="Manager" ).one()
            # usr=Users.query.filter_by(uname=desg).one()
            # if usr and usr.designation=="Admin" or usr.designation=="Manager":
                # if   check_password_hash(usr.upasscode ,upass):
                    data=Stock.query.filter_by(product_name=nam).one()
                    if data.quantity > qtt and qtt > 0:
                        result.quantity=result.quantity + qtt 
                        data.quantity= data.quantity - qtt
                        db.session.merge(result)
                        db.session.merge(data)
                        db.session.commit()
                        flash(f"{qtt} {nam} have been added to the inventory",'info') 
                        return redirect(url_for('invent')) 
                    else:
                        flash("Can't avail this much of the product","warning")
                        return redirect(url_for('invent'))
                # else:
                #     flash("Wrong password","danger")
                #     return redirect(url_for('invent'))
            # else:
            #   flash("Invalid user details","danger")
            #   return redirect(url_for("invent"))
        else:
            flash(f"{nam} is not available","danger")
            return redirect(url_for('invent'))

@app.route('/Make_Sale',methods=["POST"])
def saler():
    id= request.form["pid"]  
    quantity= request.form["quantity"]
    created_at="NOW()"
    data=Sales(product_id=id,quantity=quantity,created_at=created_at)
    prd=Product.query.filter_by(id=id).one()
    prd.quantity=prd.quantity-int(quantity)
    db.session.merge(prd)
    db.session.add(data)
    db.session.commit()
    flash('Purchace Successful','info') 
    return redirect(url_for('invent')) 

@app.route('/edit',methods=["POST"])
def editor():
    if request.method == "POST":
        id=request.form["id"] 
        sp=int(request.form["sp"])               
#   query='UPDATE public.products SET name=%s, bp=%s, sp=%s, serial_no=%s WHERE id=%s;'
        data=Product.query.filter_by(id=id).one()
        data.sp=sp
        db.session.merge(data)
        db.session.commit()
        flash(f"{data.name} are now being sold @ {sp} each", 'info') 
        return redirect(url_for('invent'))

@app.route('/edit2',methods=["POST"])
def editor2():
    if request.method == "POST":
        id=request.form["id"]
        qtt=int(request.form["qtt"])
        data=Stock.query.filter_by(id=id).one()
        data.quantity=data.quantity + qtt
        db.session.merge(data)
        db.session.commit()
        flash(f"{ qtt} more {data.product_name } are now available", 'info') 
        return redirect(url_for('stock'))

@app.route('/edit3',methods=["POST"])
def editor3():
    if request.method == "POST":
        id=request.form["id"]
        data=Users.query.filter_by(id=id).one()
        dtls=Users.query.filter(db.or_(Users.igram==request.form["igram"],Users.tgram == request.form["tgram"])).first()
        if data :            
            if dtls:
                if data.designation == "Admin":
                    flash("The Instagram or telegram links already exist try again","danger") 
                    return redirect(url_for('admin'))
                if data.designation == "Manager":
                    flash("The Instagram or telegram links already exist try again","danger") 
                    return redirect(url_for('manager'))
                else:
                    flash("The Instagram or telegram links already exist try again","danger") 
                    return redirect(url_for('user'))
            else:
                data.uname=request.form["uname"]
                data.email=request.form["email"]
                data.whatsapp=request.form["wapp"]
                data.tgram=request.form["tgram"]
                data.igram=request.form["igram"]
                db.session.merge(data)
                db.session.commit()
                if data.designation == "Admin":
                    flash(f"{data.uname}'s details Successfully Edited", 'info') 
                    return redirect(url_for('admin'))
                if data.designation == "Manager":
                    flash(f"{data.uname}'s details Successfully Edited", 'info') 
                    return redirect(url_for('manager'))
                else:
                    flash(f"{data.uname}'s details Successfully Edited", 'info') 
                    return redirect(url_for('user'))
        else:
            flash("Invalid entery", 'danger') 
            return redirect(request.url)

@app.route('/edit4',methods=["POST"])
def edit4():
    if request.method=='POST':
        id=request.form["id"]
        data=Users.query.filter_by(id=id).one()
        dtls=Users.query.filter(db.or_(Users.igram==request.form["igram"],Users.tgram == request.form["tgram"])).first()
        if data :            
            if dtls:
                flash("The Instagram or telegram links already exist try again","danger") 
                return redirect(url_for('users'))
            else:
                data.uname=request.form["uname"]
                data.email=request.form["email"]
                data.whatsapp=request.form["wapp"]
                data.tgram=request.form["tgram"]
                data.igram=request.form["igram"]
                db.session.merge(data)
                db.session.commit()
                if data.designation == "Admin":
                    flash(f"{data.uname}'s details Successfully Edited", 'info') 
                    return redirect(url_for("users"))
                if data.designation == "Manager":
                    flash(f"{data.uname}'s details Successfully Edited", 'info') 
                    return redirect(url_for("users"))
                else:
                    flash(f"{data.uname}'s details Successfully Edited", 'info') 
                    return redirect(url_for("users"))

        flash(f" User {data.uname} details changed","info")
        return redirect(url_for("users"))

@app.route('/stock')
@login_required
def stock(): 
    stock=Stock.query.all()
    print(stock)
    return render_template("viccistockstock.html",stock=stock)

@app.route('/add_stock',methods=["POST"])
def stockup():
    if request.method == "POST": 
        product_name= request.form["product_name"]
        quantity=request.form["quantity"]
        bp= request.form["bp"]         
        created_at="NOW()"
        if product_name == "" or quantity == "" or bp == "":
            prodct=Stock.query.filter_by(product_name=product_name).first()
            if prodct:
                flash("You can't add an existing product","danger")
                return redirect(url_for('stock'))
            else:
                data=Stock(product_name = product_name,quantity = quantity, b_p=bp,date=created_at)
                db.session.add(data)
                db.session.commit()
                flash(f" {product_name} is now in stock",'info') 
                return redirect(url_for('stock'))
        else:
            flash('Required conditions not met!', 'danger') 
            return render_template("viccistock.html")
       
@app.route('/avail', methods=["POST"])
def avail():
    if request.method=="POST":
        pid=request.form["id"]
        deduction=Stock.query.filter_by(id=pid).first()
        qtt=int(request.form["quantity"])
        name=request.form["name"]
        sp=int(request.form["sp"])
        bp=int(request.form["bp"])
        serial=request.form["serial"]
        if qtt <= deduction.quantity and qtt>0:
            prodct=Product.query.filter_by(name=name).first()
            if not prodct:
                deduction.quantity=deduction.quantity - qtt
                data=Product(name=name,bp=bp,sp=sp,quantity=qtt,serial_no=serial)
                db.session.add(data)
                db.session.add(deduction)
                db.session.commit()
                flash(f"{qtt} {name} have been Availed",'info')
                return redirect(url_for('invent'))
            else:
                flash('Cant avail an existing product','danger')
                return redirect(url_for('stock'))
        else:
            flash('Cant avail this much of the product','danger')
            return redirect(url_for('stock'))

@app.route('/sales')
@login_required
def sales():
    # sales= db.session.query(Product.name,db.func.sum(Product.sp-Product.bp)*Sales.quantity.label("Profit"),db.func.sum(Sales.quantity).label("Quantity")).join(Sales,Product.id==Sales.product_id).group_by(Product.name).all()    
    sale = db.session.query(Product.name,db.func.sum(Sales.quantity).label("Quantity"),db.func.sum((Product.sp-Product.bp)*Sales.quantity).label("Profit")).join(Sales, Product.id == Sales.product_id).group_by(Product.name).all()
    for result in sale:
        print(' Name:', result[0], 'Quantity:', result[1], 'Profit:', result[2])
    return render_template("viccistocksales.html",sale=sale)

@app.route('/sale/<string:id>')
def sale(id):
    # cur.execute("SELECT pr.name,sum((pr.sp-pr.bp)* sl.quantity) as ttlprofit,sum(sl.quantity)as totalprofit FROM public.sales as sl join product as pr on pr.id=sl.product_id where pr.id=%s group by pr.name ",[id])    
    sales=db.session.query(Product.name,db.func.sum((Product.sp-Product.bp)*Sales.quantity).label("Profit"),db.func.sum(Sales.quantity).label("Quantity")).join(Sales,Product.id==Sales.product_id).group_by(Product.name).all()    
    return render_template("viccistocksales.html",sale=sales)
    
@app.route('/payroll', methods=["GET","POST"] )
@login_required
def payroll():
    if request.method=="POST":
        sallary=request.form["sallary"]
        bnft1=request.form["bnft1"]
        bnft2=request.form["bnft2"]        
        if sallary !="":
            if bnft1 !="":
                if bnft2 !="":
                    gross_sallary=int(int(sallary)+(int(bnft1)+int(bnft2))) 
                    #Calculating the NHIF    
                    if gross_sallary>300:
                        nhf=150 
                        ans=request.form["ans"]
                        #Calculating the NSSF
                        if ans!="Permanent" or ans!="permanent":
                            nsf=(gross_sallary-nhf)*0 
                            ti=gross_sallary-nhf 

                            if ti<24000:
                                tax=ti*0
                                net=ti
                                print(tax,nhf,nsf,net)
                                return render_template("index.html",callow=bnft2,hallo=bnft1,bsc=sallary,txblI=tax,nhif=nhf,nssf=nsf,n_sal=net,gs=gross_sallary)

                            elif ti>24000 and ti<32333:
                                tax=ti*0.25
                                net=ti*0.75
                                print(tax,nhf,nsf,net)
                                return render_template("index.html",callow=bnft2,hallo=bnft1,bsc=sallary,txblI=tax,nhif=nhf,nssf=nsf,n_sal=net,gs=gross_sallary)
                            
                            else:
                                ti>32333
                                tax=ti*0.3
                                net=ti*0.7  
                                print(tax,nhf,nsf,net)                       
                                return render_template("index.html",callow=bnft2,hallo=bnft1,bsc=sallary,txblI=tax,nhif=nhf,nssf=nsf,n_sal=net,gs=gross_sallary)
                        else:
                            #Calculating the NSSF
                            if gross_sallary<18000 :
                               nsff=(gross_sallary-nhf)*0.06
                               txi=gross_sallary-(nsf+nhf)
                               # Calculating The payee
                               if txi<24000:
                                    tax=txi*0
                                    net=txi
                                    return render_template("index.html",callow=bnft2,hallo=bnft1,bsc=sallary,n_sal=net,txblI=tax,nhif=nhf,nssf=nsff,gs=gross_sallary)
                               elif txi>24000 and ti<32333:
                                    tax=txi*0.25
                                    net=txi*0.75
                                    return render_template("index.html",callow=bnft2,hallo=bnft1,bsc=sallary,n_sal=net,txblI=tax,nhif=nhf,nssf=nsff,gs=gross_sallary)
                               else:
                                    txi>32333
                                    tax=txi*3
                                    net=txi*0.7
                                    return render_template("index.html",callow=bnft2,hallo=bnft1,bsc=sallary,n_sal=net,txblI=tax,nhif=nhf,nssf=nsff,gs=gross_sallary)  
                            else:
                                nsff=(gross_sallary-nhf)*0.1
                                txi=gross_sallary-(nsf+nhf)
                                # Calculating The payee
                                if txi<24000:
                                    tax=txi*0
                                    net=txi
                                    return render_template("index.html",callow=bnft2,hallo=bnft1,bsc=sallary,n_sal=net,txblI=tax,nhif=nhf,nssf=nsff,gs=gross_sallary)
                                elif txi>24000  and ti<32333:
                                    tax=txi*0.25
                                    net=txi*0.75
                                    return render_template("index.html",callow=bnft2,hallo=bnft1,bsc=sallary,n_sal=net,txblI=tax,nhif=nhf,nssf=nsff,gs=gross_sallary)
                                else:
                                    txi>32333
                                    tax=txi*0.3
                                    net=ti*0.7
                                    return render_template("index.html",callow=bnft2,hallo=bnft1,bsc=sallary,n_sal=net,txblI=tax,nhif=nhf,nssf=nsff,gs=gross_sallary)  
                else:
                    flash("Enter commuter benefits:")
            else:
                flash("Enter house benefits:")    
        else:
            flash("Enter The Basic Sallary:")
    return render_template("payroll.html")   

@app.route("/manager",methods=["GET","POST"]) 
@login_required  
def manager():
    return render_template("manager.html",manager=current_user)

@app.route("/admin",methods=["GET","POST"])  
@login_required 
def admin():  
    return render_template("admin.html",admin=current_user)

@app.route("/adduser",methods=["GET","POST"])  
# @login_required 
def adduser():
    if request.method=="POST":
        uid=request.form["id"]
        fname=request.form["fname"] 
        lname=request.form["lname"]        
        email=request.form["email"]
        status=request.form["status"]
        upasscode=request.form['pwd1']
        tel=request.form["tel"]
        designation=request.form["desg"]
        e_id=request.form["eid"]  
        usr=Users.query.filter_by(email=email).first()
        if not usr:
            if len(fname or lname) > 2:
                if len(email)>5:
                    if len(upasscode)>7:
                        if len(tel) == 10 or len(tel) ==12 or len(tel) ==13:
                            if(designation =="Admin" or designation =="Manager" or designation =="User"):
                                id=Users.query.filter_by(e_id = e_id).first()
                                data=Newsletter.query.filter_by(id=uid).one()
                                if not id:
                                    row=Users(fname=fname,lname=lname,email=email,upasscode=generate_password_hash( upasscode,method='sha256'),tel=tel,designation=designation,e_id=e_id,uname=designation+e_id,igram=fname+".igram.com",tgram=fname+".tgram.com")    
                                    data.status=status
                                    db.session.add(row)
                                    db.session.merge(data)
                                    db.session.commit()
                                    flash(f"User {lname} successfully added","success")
                                    return redirect(url_for("users"))
                                else:
                                    flash(f"Can't assign this employee id {e_id}","danger")
                                    return redirect(request.url)
                            else:                
                                flash("Invalid entery!","danger")
                                return redirect(request.url)
                        else:
                            flash("Invalid entery Check phone Number","danger")
                            return redirect(request.url)
                    else:
                        flash("Enter a strong password of at least 8 charecters","danger")
                        return redirect(request.url)                
                else:
                    flash("Email must have more than 6 charecters","danger")
                    return redirect(request.url)
            else:
                flash("Both First and last name must have more than 3 charecters","danger")
                return redirect(request.url)                
        else:           
            flash(f"User {fname} {lname} @{email} already exists","danger")
            return redirect(request.url)          
    users=Newsletter.query.all()   
    return render_template("adduser.html",users=users)

@app.route("/user",methods=["GET","POST"])
@login_required   
def user():        
    return render_template("user.html", user=current_user)

@app.route("/users",methods=["GET","POST"])  
@login_required 
def users():
    users=Users.query.order_by(Users.designation).filter(Users.designation !="Admin").all()
    print(users)    
    return render_template("users.html",users=users)

@app.route("/purchase",methods=["GET","POST"])   
def purchase():
    mbp=Product.query.all()
    print(mbp)
    return render_template("purchase.html",invtory=mbp)

@app.route("/login",methods=["POST"])
def login():
    if request.method=="POST":      
        name=request.form["name"]
        password=request.form["password"]
        user=Users.query.filter_by(uname=name).first()  
        print(user)
        if  not user:
            flash('Wrong username try again!','warning')
            return redirect(url_for("ims"))
        else:
            # counter=0
            # while counter < 3:
                if check_password_hash(user.upasscode, password):
                # if user.upasscode == password:
                    if user.designation=="Admin":
                        flash(f"{user.uname} you successfully Logged in!",'info')
                        login_user(user,remember=True)
                        # return redirect(url_for("dash"))
                        return redirect(url_for("admin"))
                    elif user.designation=="Manager":
                        flash(f"{user.uname} you successfully Logged in!",'info')
                        login_user(user,remember=True)
                        return redirect(url_for("manager"))
                    else:
                        flash(f"{user.uname} you successfully Logged in!",'info')
                        login_user(user,remember=True)  
                        return redirect(url_for("user"))
                else:
                    flash('Wrong password. Try again!','danger') 
                    return redirect(url_for("ims"))

@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        fname=request.form["fname"]
        lname=request.form["lname"]
        status=request.form["status"]
        email=request.form["email"]
        tel=request.form["tel"]
        user=Newsletter.query.filter_by(email=email).first()
        if user :
            flash(f" Sorry {fname} you cant apply twice","warning")
            return redirect(request.url)
        elif email=="":
            flash(" Invalid entery check your email address","danger")
            return redirect(request.url)
        else:
            if len(lname)>2 and len(lname)>2 and lname!="" and fname!="":
                if len(tel)==10 or len(tel)==12 or len(tel)==13 and tel!="":
                    data=Newsletter(fname=fname, lname=lname,status=status,email=email,tel=tel)
                    db.session.add(data)
                    db.session.commit()
                    flash("You will get the login details after evaluation","info")
                    return redirect(url_for("ims"))
                else:
                    flash("Invalid entery. Check Your Phone number","warning")
                    return redirect(request.url)
            else:
                flash("Your First and last name must be of atleast 3 charecters","warning")
                return redirect(request.url)
    return render_template("signUp.html")

@app.route("/forgot",methods=["GET","POST"])
def forgot():
    if request.method=="POST":
        email=request.form["email"]
        usr=Users.query.filter_by(email=email).all()
        if email == "":
            flash("Please enter a valid email address","warning")
            return redirect(request.url)
        elif usr and len(email) > 2:             
            return redirect(url_for("newpass")) 
        else:
            flash("User doesn't exist check your email address and try again","warning")
            return redirect(request.url)
    return render_template("forgot.html")

@app.route("/newpass",methods=["GET","POST"])
def newpass():
    if request.method=="POST":
        pw1=request.form["pw1"]
        pw2=request.form["pw2"]
        if len(pw1)> 5:
            if pw1 == pw2:
                flash("Password reset successful","info")
                return redirect(url_for("ims"))
            else:
                flash("Passwords do not match","danger")
                return redirect(request.url)
        else:
            flash("Enter astonger password of at least 6 charecters","danger")
            return redirect(request.url)
    return render_template("new.html")

@app.route("/view",methods=["POST"])
def view():
    if request.method=="POST":
        desg=request.form["desg"]
        code=request.form["passw"]
        uid=request.form["id"]
        # name=request.form["uname"]
        # dcnv=check_password_hash(Users.upasscode, code)
        data=Users.query.filter(Users.designation =="Admin").first()
        user=Users.query.filter_by(id=uid).one()
        if data:
            if desg=="Manager":
                flash(f" Welcome {data.uname}","success")
                login_user(user,remember=True)
                return redirect(url_for("manager"))
            elif desg=="User":
                flash(f" Welcome {data.uname}","success")
                login_user(user,remember=True)
                return redirect(url_for("user"))
        else:
            flash(" Wrong password!","danger")
            return redirect(url_for("users"))

@app.route("/delete",methods=["POST"])
def delete():
    if request.method=="POST":
        id=request.form["id"]
        code=request.form["passw"]
        data=Users.query.filter_by(designation="Admin").first()
        print("data",data.upasscode)
        if check_password_hash(data.upasscode, code):
            Users.query.filter_by(id=id).delete()
            db.session.commit()
            flash("User deleted","info")
            return redirect(url_for("users"))
        else:
            flash("Wrong password!","danger")
            return redirect(url_for("users"))

@app.route("/delete1",methods=["POST"])
def delete1():
    if request.method=="POST":
        id=request.form["id"]
        code=request.form["passw"]
        # name=request.form["uname"]
        data=Users.query.filter_by(designation="Admin").first()
        print("data",data.upasscode)
        user=Newsletter.query.filter_by(id=id)
        if user :
            if check_password_hash(data.upasscode, code):
                Newsletter.query.filter_by(id=id).delete()
                db.session.commit()
                flash("Candidate deleted","info")
                return redirect(url_for("adduser"))
            else:
                flash("Wrong password!","danger")
                return redirect(url_for("adduser"))
        else:
            flash("No such User","danger")
            return redirect(request.url)

@app.route("/confirm", methods=["POST"])
def confirm():
    if request.method=="POST":
        uid=request.form["id"]
        upass=request.form["password"]
        npass=request.form["password1"]
        npass1=request.form["password2"]
        data=Users.query.filter_by(id=uid).one()
        if data:
            if check_password_hash(data.upasscode, upass):
                if npass==npass1 and npass !="":
                    if  len(npass)>7:
                        data.upasscode=generate_password_hash( npass,method='sha256')
                        db.session.merge(data)
                        db.session.commit()
                        flash("Change updated","info")
                        return redirect(url_for("ims"))
                    else:
                        if data.designation =="Admin":
                            flash("Password should contain atleast 8 charecters","warning")
                            return redirect(url_for("admin"))
                        elif data.designation == "Manager":
                            flash("Password should contain atleast 8 charecters","warning")
                            return redirect(url_for("manager"))
                        else:
                            flash("Password should contain atleast 8 charecters","warning")
                            return redirect(url_for("user"))
                else:
                    if data.designation =="Admin":
                        flash("New passwords didn't match","danger")
                        return redirect(url_for("admin"))
                    elif data.designation == "Manager":
                        flash("New passwords didn't match","danger")
                        return redirect(url_for("manager"))
                    else:
                        flash("New passwords didn't match","danger")
                        return redirect(url_for("user"))
            else:
                if data.designation =="Admin":
                    flash("Wrong password","danger")
                    return redirect(url_for("admin"))
                elif data.designation == "Manager":
                    flash("Wrong password","danger")
                    return redirect(url_for("manager"))
                else:
                    flash("Wrong password","danger")
                    return redirect(url_for("user"))
        else:
            
            flash("Invalid","danger")
            return redirect(url_for("admin"))

@app.route("/logout",methods=["GET","POST"])
@login_required#decorator
def logout():
    logout_user()
    flash("You logged out","info")
    return redirect(url_for("ims"))

if __name__ == '__main__':
    app.run(debug=True)
