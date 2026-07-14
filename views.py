from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
import pymysql
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import datetime

global username, current_user, types, style, brand
username = ""
current_user = ""
types = "-"
style = "-"
brand = "-"
cart = []
bargain_price = {}

def TrackOrder(request):
    if request.method == 'GET':
        global current_user
        output = ''
        output+='<table border=1 align=center width=100%><tr><th>Purchaser Name</th><th>Product ID</th><th>Order Date</th><th>Purchaser Details</th>'
        output+='<th>Product Details</th><th>Amount</th><th>Card No</th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'AIBargainingAgent',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM customer_order")
            rows = cur.fetchall()
            output+='<tr>'
            for row in rows:
                if row[0] == current_user:
                    output+='<td><font size="" color="black">'+row[0]+'</td><td><font size="" color="black">'+row[1]+'</td><td><font size="" color="black">'+str(row[2])+'</td><td><font size="" color="black">'+row[3]+'</td><td><font size="" color="black">'+row[4]+'</td>'
                    output+='<td><font size="" color="black">'+str(row[5])+'</td><td><font size="" color="black">'+str(row[6])+'</td></tr>'
        output +='</table><br><br/>'               
        context= {'data':output}
        return render(request, 'ProductList.html', context)

def FeedbackAction(request):
    if request.method == 'POST':
        global current_user

        feedback = request.POST.get('t1', False)
        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        db_connection = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='root',database='AIBargainingAgent',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO feedback(username,feedback,feedback_date) VALUES('"+current_user+"','"+feedback+"','"+str(current_time)+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        if db_cursor.rowcount == 1:
            context = {'data':'Your feedback sent to admin for review'}
            return render(request,'Feedback.html',context)
        else:
            context = {'data':'Error in accepting feedback'}
            return render(request,'Feedback.html',context)

        
def Feedback(request):
    if request.method == 'GET':
       return render(request, 'Feedback.html', {})

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Login(request):
    if request.method == 'GET':
       return render(request, 'Login.html', {})

def AdminLogin(request):
    if request.method == 'GET':
       return render(request, 'AdminLogin.html', {})    

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})   

def AddProduct(request):
    if request.method == 'GET':
       return render(request, 'AddProduct.html', {})
    
def ViewFeedback(request):
    if request.method == 'GET':
        output = ''
        output += '<table border=1 align=center width=100%>'
        output += '<tr>'
        output += '<th>Username</th>'
        output += '<th>Feedback</th>'
        output += '<th>Feedback Date</th>'
        output += '</tr>'
        con = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='root',database='AIBargainingAgent',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * from feedback")
            rows = cur.fetchall()
            for row in rows:
                output += '<tr>'
                output += '<td>'+str(row[0])+'</td>'
                output += '<td>'+str(row[1])+'</td>'
                output += '<td>'+str(row[2])+'</td>'
                output += '</tr>'
        output += '</table>'
        context = {'data': output}
        return render(request, 'ViewFeedback.html', context)

def ViewOrders(request):
    if request.method == 'GET':
        output = ''
        output+='<table border=1 align=center width=100%><tr><th>Purchaser Name</th><th>Product ID</th><th>Order Date</th><th>Purchaser Details</th>'
        output+='<th>Product Details</th><th>Amount</th><th>Card No</th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'AIBargainingAgent',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM customer_order")
            rows = cur.fetchall()
            output+='<tr>'
            for row in rows:
                output+='<td><font size="" color="black">'+row[0]+'</td><td><font size="" color="black">'+row[1]+'</td><td><font size="" color="black">'+str(row[2])+'</td><td><font size="" color="black">'+row[3]+'</td><td><font size="" color="black">'+row[4]+'</td>'
                output+='<td><font size="" color="black">'+str(row[5])+'</td><td><font size="" color="black">'+str(row[6])+'</td></tr>'
        output +='</table><br><br/>'               
        context= {'data':output}
        return render(request, 'ViewOrders.html', context)          
        
def SearchItemData(request):
    if request.method == 'POST':
        global types, style, brand

        pname = request.POST.get('pname', '').strip()

        if pname != '':
            output = ''
            output += '<table border=1 align=center width=100%>'
            output += '<tr>'
            output += '<th>Product ID</th>'
            output += '<th>Product Name</th>'
            output += '<th>Product Type</th>'
            output += '<th>Product Style</th>'
            output += '<th>Product Brand</th>'
            output += '<th>Cost</th>'
            output += '<th>Description</th>'
            output += '<th>Image</th>'
            output += '<th>Bargain</th>'
            output += '<th>View Cart</th>'
            output += '</tr>'

            con = pymysql.connect(
                host='127.0.0.1',
                port=3306,
                user='root',
                password='root',
                database='AIBargainingAgent',
                charset='utf8'
            )

            with con:
                cur = con.cursor()
                cur.execute(
                    "select * from addproduct where productname like %s",
                    ('%' + pname + '%',)
                )
                rows = cur.fetchall()

                for row in rows:
                    output += '<tr>'
                    output += '<td>' + str(row[0]) + '</td>'
                    output += '<td>' + str(row[1]) + '</td>'
                    output += '<td>' + str(row[2]) + '</td>'
                    output += '<td>' + str(row[3]) + '</td>'
                    output += '<td>' + str(row[4]) + '</td>'
                    output += '<td>' + str(row[5]) + '</td>'
                    output += '<td>' + str(row[6]) + '</td>'
                    output += '<td><img src="/static/products/' + str(row[7]) + '" width="200" height="200"></td>'
                    output += '<td><a href="Bargain?pid=' + str(row[0]) + '">Click Here</a></td>'
                    output += '<td><a href="ViewCart?pid=' + str(row[0]) + '">Click Here</a></td>'
                    output += '</tr>'

            output += '</table>'
            context = {'data': output}
            return render(request, 'ProductList.html', context)

        else:
            output = getCatalogue()
            context = {'data': output}
            return render(request, 'ProductList.html', context)

    return render(request, 'ItemSearch.html', {})
def ItemSearch(request):
    if request.method == 'GET':
        return render(request, 'ItemSearch.html', {})
def About(request):
    if request.method == 'GET':
       return render(request, 'About.html', {})    

def getPurchaserDetails(name):
    address = ''
    contact = ''
    con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'AIBargainingAgent',charset='utf8')
    with con:
            cur = con.cursor()
            cur.execute("select address,contact FROM register where username='"+name+"'")
            rows = cur.fetchall()
            for row in rows:
                contact = row[1]
                address = row[0]
                break
    return contact,address        

def getProductDetails(pid):
    pname = ''
    cname = ''
    cost = ''
    con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'AIBargainingAgent',charset='utf8')
    with con:
            cur = con.cursor()
            cur.execute("select productname,cost FROM addproduct where productid='"+pid+"'")
            rows = cur.fetchall()
            for row in rows:
                pname = row[0]
                cost = str(row[1])
                break
    return pname,cost

def PaymentAction(request):
    if request.method == 'POST':
        global username, current_user, cart

        amount = request.POST.get('t1', False)
        card = request.POST.get('t2', False)
        cvv = request.POST.get('t3', False)
        # Prevent empty card details
        if card.strip() == "" or cvv.strip() == "":
            context = {'total': amount,'data': 'Please enter Card Number and CVV'}
            return render(request, 'Purchase.html', context)
        # Prevent checkout if cart is empty
        if len(cart) == 0:
            context = {'data': 'Cart is Empty. Please add items first'}
            return render(request, 'UserScreen.html', context)
        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        contact, address = getPurchaserDetails(current_user)
        purchaser = "Phone : " + contact + " Address : " + address
        pids = ""
        products = ""
        for i in range(len(cart)):
            pids += cart[i] + ", "
            pname, cost = getProductDetails(cart[i])
            products += pname + ", "
        if len(products) > 0:
            products = products.strip()
            products = products[:-1]
        if len(pids) > 0:
            pids = pids.strip()
            pids = pids[:-1]
        db_connection = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='root',database='AIBargainingAgent',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = """INSERT INTO customer_order(purchaser_name,product_id,purchase_date,purchaser_details,product_details,amount,card_no,cvv_no)
        VALUES('%s','%s','%s','%s','%s','%s','%s','%s')
        """ % (current_user,pids,current_time,purchaser,products,amount,card,cvv)
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        cart.clear()
        if db_cursor.rowcount == 1:
            context = {'data': 'Order Confirmed Successfully'}
            return render(request, 'UserScreen.html', context)
        else:
            context = {'data': 'Error in confirming order'}
            return render(request, 'UserScreen.html', context)

def getCatalogue():
    global types, style, brand

    output = ''
    output += '<table border=1 align=center width=100%><tr>'
    output += '<th>Product ID</th>'
    output += '<th>Product Name</th>'
    output += '<th>Product Type</th>'
    output += '<th>Product Style</th>'
    output += '<th>Product Brand</th>'
    output += '<th>Cost</th>'
    output += '<th>Description</th>'
    output += '<th>Image</th>'
    output += '<th>Bargain</th>'
    output += '<th>View Cart</th>'
    output += '</tr>'
    con = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='root',database='AIBargainingAgent',charset='utf8')
    query = "select * from addproduct where "
    option = 0
    if types != '-':
        query += "product_type='"+types+"'"
        option = 1
    if style != '-':
        if option == 0:
            query += "product_style='"+style+"'"
            option = 1
        else:
            query += " and product_style='"+style+"'"
    if brand != '-':
        if option == 0:
            query += "product_brand='"+brand+"'"
            option = 1
        else:
            query += " and product_brand='"+brand+"'"
    if option == 0:
        query = "select * from addproduct"
    print(query)
    with con:
        cur = con.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            output += '<tr>'
            output += '<td><font color="black">'+str(row[0])+'</font></td>'
            output += '<td><font color="black">'+str(row[1])+'</font></td>'
            output += '<td><font color="black">'+str(row[2])+'</font></td>'
            output += '<td><font color="black">'+str(row[3])+'</font></td>'
            output += '<td><font color="black">'+str(row[4])+'</font></td>'
            output += '<td><font color="black">'+str(row[5])+'</font></td>'
            output += '<td><font color="black">'+str(row[6])+'</font></td>'
            output += '<td><img src="/static/products/'+str(row[7])+'" width="200" height="200"></td>'
            output += '<td><a href="Bargain?pid='+str(row[0])+'"><font color="black">Click Here</font></a></td>'
            output += '<td><a href="ViewCart?pid='+str(row[0])+'"><font color="black">Click Here</font></a></td>'
            output += '</tr>'
    output += '</table><br><br/><br/>'
    return output

def AddCart(request):
    if request.method == 'GET':
        global cart

        pid = request.GET['pid']
        if pid not in cart:
            cart.append(pid)
        output = getCatalogue()
        context = {'data': output}
        return render(request, 'ProductList.html', context)
        
def Checkout(request):
    if request.method == 'GET':
        global cart, bargain_price

        if len(cart) == 0:
            context = {'data':'<center><font size="4" color="red">Please add item to cart first</font></center>'}
            return render(request, 'ProductList.html', context)
        total = 0
        for pid in cart:
            if pid in bargain_price:
                total += float(bargain_price[pid])
            else:
                con = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='root',database='AIBargainingAgent',charset='utf8')
                with con:
                    cur = con.cursor()
                    cur.execute("select cost from addproduct where productid='"+pid+"'")
                    rows = cur.fetchall()
                    for row in rows:
                        total += float(row[0])
        context = {'total': total}
        return render(request, 'Purchase.html', context)
    
def ViewCart(request):
    if request.method == 'GET':
        global cart, bargain_price

        pid = request.GET.get('pid')
        if pid is not None and pid not in cart:
            cart.append(pid)
        output = '<table border=1 align=center width=100%>'
        output += '<tr><th>Product ID</th><th>Product Name</th><th>Cost</th><th>Removed Item</th></tr>'
        for i in range(len(cart)):
            pid = cart[i]
            con = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='root',database='AIBargainingAgent',charset='utf8')
            with con:
                cur = con.cursor()
                cur.execute("select productname,cost from addproduct where productid='"+pid+"'")
                rows = cur.fetchall()
                for row in rows:
                    cost = row[1]
                    if pid in bargain_price:
                        cost = str(bargain_price[pid])
                    output += '<tr>'
                    output += '<td>'+str(pid)+'</td>'
                    output += '<td>'+str(row[0])+'</td>'
                    output += '<td>'+str(cost)+'</td>'
                    output += '<td><a href="RemoveCart?pid='+str(pid)+'">Click Here</a></td>'
                    output += '</tr>'
        output += '</table>'
        if len(cart) > 0:
            output += '<br><br/><center><button class="btn btn-register" onclick="window.location.href=\'Checkout?pid=0\'">Checkout</button></center>'
        else:
            output += '<br><br/><center><font size="4" color="red">Please add item to cart first</font></center>'
        context = {'data': output}
        return render(request, 'ProductList.html', context)
            
def RemoveCart(request):
    if request.method == 'GET':
        global cart

        pid = request.GET['pid']
        if pid in cart:
            cart.remove(pid)
        return ViewCart(request)

def SearchItemData(request):
    if request.method == 'POST':
        global types, style, brand

        types = request.POST.get('t1', False)
        style = request.POST.get('t2', False)
        brand = request.POST.get('t3', False)
        output = getCatalogue()
        context = {'data': output}
        return render(request, 'ProductList.html', context)
    return render(request, 'ItemSearch.html', {})

def AddProductData(request):
    if request.method == 'POST':
        pname = request.POST.get('t1', False)
        ptype = request.POST.get('t2', False)
        style = request.POST.get('t3', False)
        brand = request.POST.get('t4', False)
        cost = request.POST.get('t5', False)
        description = request.POST.get('t6', False)
        myfile = request.FILES['t7']
        count = 0
        con = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='root',database='AIBargainingAgent',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select max(cast(productid as unsigned)) FROM addproduct")
            rows = cur.fetchall()
            for row in rows:
                count = row[0]
        if count is not None:
            count = int(count) + 1
        else:
            count = 1
        fs = FileSystemStorage(location='BargainingApp/static/products')
        filename = fs.save(myfile.name, myfile)
        db_connection = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='root',database='AIBargainingAgent',charset='utf8')
        db_cursor = db_connection.cursor()
        sql = """
        INSERT INTO addproduct(productid,productname,product_type,product_style,product_brand,cost,description,image)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
        """
        db_cursor.execute(sql, (str(count),pname,ptype,style,brand,cost,description,filename))
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            context = {'data':'Product Details Added'}
            return render(request, 'AddProduct.html', context)
        else:
            context = {'data':'Error in adding product details'}
            return render(request, 'AddProduct.html', context) 
    
def Signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        contact = request.POST.get('contact', False)
        email = request.POST.get('email', False)
        address = request.POST.get('address', False)
        status = "none"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'AIBargainingAgent',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username FROM register where username='"+username+"'")
            rows = cur.fetchall()
            for row in rows:
                status = "exists"
        if status == "none":
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'AIBargainingAgent',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO register(username,password,contact,email,address) VALUES('"+username+"','"+password+"','"+contact+"','"+email+"','"+address+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                context= {'data':'Signup Process Completed'}
                return render(request, 'Register.html', context)
            else:
                context= {'data':'Error in signup process'}
                return render(request, 'Register.html', context)
        else:
            context= {'data':'Username already exists'}
            return render(request, 'Register.html', context) 
        
def UserLogin(request):
    if request.method == 'POST':
        global username, current_user
        global types, style, brand

        username = request.POST.get('username', False)
        password = request.POST.get('password', False)

        utype = 'none'

        con = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='root',
            database='AIBargainingAgent',
            charset='utf8'
        )

        with con:
            cur = con.cursor()
            cur.execute("select * from register")
            rows = cur.fetchall()

            for row in rows:
                if row[0] == username and row[1] == password:
                    utype = "success"
                    current_user = username
                    break

        if utype == 'success':
            types = '-'
            style = '-'
            brand = '-'

            output = getCatalogue()
            context = {
                'data': output
            }
            return render(request, 'ProductList.html', context)

        else:
            context = {
                'data': 'Invalid login details'
            }
            return render(request, 'Login.html', context)
def UserScreen(request):
    global current_user
    return render(request, 'UserScreen.html',{'data': 'welcome ' + current_user})
        
def AdminLoginAction(request):
    if request.method == 'POST':
        global username

        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        if username == 'admin' and password == 'admin':
            context = {'data':'Welcome Admin'}
            return render(request,'AdminScreen.html',context)
        else:
            context = {'data':'Invalid login details'}
            return render(request,'AdminLogin.html',context)
    return render(request,'AdminScreen.html',
                 {'data':'Welcome Admin'})

def Bargain(request):
    if request.method == 'GET':
        pid = request.GET['pid']
        cost = ""
        con = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='root',database='AIBargainingAgent',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select cost from addproduct where productid='"+pid+"'")
            rows = cur.fetchall()
            for row in rows:
                cost = row[0]
        context = {'pid': pid,'cost': cost}
        return render(request,'Bargain.html',context)

def BargainAction(request):
    if request.method == 'POST':
        global bargain_price

        pid = request.POST.get('pid', False)
        cost = float(request.POST.get('cost', False))
        counter = float(request.POST.get('counter', False))
        accepted_price = cost * 0.90
        if counter > cost:
            output = '''
            <center>
            <font size="4" color="red">
            Counter Price Cannot Be Greater Than Original Price
            </font>
            </center>
            <br/><br/>
            '''
        elif counter >= accepted_price:
            bargain_price[pid] = counter
            output = '''
            <center>
            <font size="4" color="green">
            Price Accepted!
            </font>
            <br/><br/>
            <a href="AddCart?pid=''' + str(pid) + '''"
            style="
            background:#10b981;
            color:white;
            padding:10px 20px;
            border-radius:8px;
            text-decoration:none;
            font-weight:bold;">
            Add To Cart
            </a>
            </center>
            <br/><br/>
            '''
        else:
            output = '''
            <center>
            <font size="4" color="red">
            Sorry! Given Price Cannot Be Accepted.<br/>
            </font>
            </center>
            <br/><br/>
            '''
        output += getCatalogue()
        context = {'data': output}
        return render(request, 'ProductList.html', context)