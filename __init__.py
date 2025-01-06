from flask import Flask, render_template, url_for,request,redirect,session,jsonify
import os,sys,stat
from werkzeug.utils import secure_filename
import Customer , Listing,Reviews,Report,operatoractions #classes
from Forms import CustomerSignupForm, CustomerLoginForm, ListingForm,ReviewForm,CustomerUpdateForm,ReportForm,SearchBar,OperatorLoginForm,OperatorLoginVerifyForm,SearchUserField,OperatorSuspendUser,OperatorTerminateUser,OperatorRestoreUser #our forms
import Email,Search
import shelve, Customer
from pathlib import Path
from Messages import User
import string
import random
app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def check_allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_upload_file_type(file,type,id): #file obj here, listing/userid here too, type too
    file_to_upload = file
    if type == "listing" and check_allowed_file(file.filename):
        print("check listing pic")
        file.filename = f"listing{id}.jpg"
        check_dupe_file(file_to_upload,"listingpics")
   
    elif type == "customer" and check_allowed_file(file.filename):
        print("check profile pic")
        file.filename = f"customer{id}.jpg"
        check_dupe_file(file_to_upload,"profilepics")
    else:
        print("invalid type or ID")

def check_dupe_file(file,type):
    myfile = Path(f"static/{type}/{file.filename}")
    if myfile.is_file():
        os.remove(f"static/{type}/{file.filename}")
        file_uploaded = file
        folder = type
        upload_file(folder,file_uploaded)
        print("file uploaded")

    else:
        file_uploaded = file
        folder = type
        upload_file(folder,file_uploaded)
        print("file uploaded")

def upload_file(folder,file):
    filename = secure_filename(file.filename)
    file.save(os.path.join(f"static/{folder}", filename))
    #for some reason it keeps returning ERRNO13 aka no permission but err it works so idk

#current_sessionID IS FOR THE PROFILE!!
#Current session ID
#MAKE SURE AN USER WITH ID "X" EXISTS!      
session_ID = 0

@app.route('/', methods = ['GET', 'POST']) #shld be the same as href for buttons,links,navbar, etc...
def Customerhome():
    global session_ID
    search_field = SearchBar(request.form)

    #search func
    if request.method == 'POST' and search_field.validate():
        return redirect(url_for('searchresults', keyword = search_field.searchfield.data)) #get the word from the search field
    

    return render_template('Customerhome.html', current_sessionID = session_ID,searchform =search_field)
    
@app.route('/profile/<int:id>', methods = ['GET', 'POST'])
def Customerprofile(id):
    global session_ID
    db1 = shelve.open('customer.db','c')
    db2 = shelve.open('listing.db','c')
    db4 =shelve.open('reports.db','c')
    customers_dict = {} #local one
    listings_dict = {}
    reports_dict = {}
    report_form = ReportForm(request.form)
    search_field = SearchBar(request.form)

    #make sure local and db1 are the same state
    #PS JUST COPY AND PASTE IF YOU'RE ACCESSING IT
    try:
        if "Customers" in db1:
            customers_dict = db1["Customers"] #sync local with db1
        else:
            db1['Customers'] = customers_dict #sync db1 with local (basically null)
    except:
        print("Error in opening customer.db")
        
    #sync IDs
    try:
        db1 = shelve.open('customer.db','c')    
        Customer.Customer.count_id = db1["CustomerCount"] #sync count between local and db1
    except:
        print("Error in retrieving data from DB1 Customer count or count is at 0")

    #sync listing dbs
    #PS JUST COPY AND PASTE IF YOU'RE ACCESSING IT
    try:
        if "Listings" in db2:
            listings_dict = db2["Listings"] #sync local with db2
        else:
            db2['Listings'] = listings_dict #sync db2 with local (basically null)
    except:
            print("Error in opening listing.db")
    #sync listing IDs
    try:
        db2 = shelve.open('listing.db','c')    
        Listing.Listing.count_ID = db2["ListingsCount"] #sync count between local and db1
    except:
        print("Error in retrieving data from DB2 Listing count or count is at 0")

    #sync report dbs
    #PS JUST COPY AND PASTE IF YOU'RE ACCESSING IT
    try:
        if "Reports" in db4:
            reports_dict = db4["Reports"] #sync local with db2
        else:
            db4['Reports'] = reports_dict #sync db2 with local (basically null)
    except:
            print("Error in opening reports.db")
    #sync listing IDs
    try:
        db4 = shelve.open('reports.db','c')    
        Report.Report.count_ID = db4["ReportsCount"] #sync count between local and db1
    except:
        print("Error in retrieving data from DB2 Listing count or count is at 0")


    #code for profile pic img 
    pfpimg = os.path.join('..\static','profilepics')
    user_id = os.path.join(pfpimg,'hermos.jpg') 
    
    #get ID list of current user listings
    customer = customers_dict.get(id)
    customer_listings = customer.get_listings()
    print(f"\n*start of message *\nCurrent user has the following listings:{customer_listings}\n*end of message*")
    listing_list = []
    if customer.get_status() == "active":
        for key in listings_dict:
            print(key)
            if key in customer_listings:
                listing = listings_dict.get(key)
                listing_list.append(listing)
    #report function
    if request.method == 'POST' and report_form.validate():
        
        #create report obj and store it
        print(report_form.category.data,report_form.report_text.data)
        report = Report.Report(session_ID,id,report_form.category.data,report_form.report_text.data)
        reports_dict[report.get_ID()] = report #store obj in dict
        db4['Reports'] = reports_dict
        db4['ReportsCount'] = Report.Report.count_ID
        db4.close()

        #store report in offender's report_listings
        customer = customers_dict.get(id)
        customer.add_reports(report.get_ID())
        db1['Customers'] = customers_dict
        db1.close()
        redirect(url_for('Customerprofile', id=id))

    #search func
    if request.method == 'POST' and search_field.validate():
        return redirect(url_for('searchresults', keyword = search_field.searchfield.data))
    #get img
    return render_template('Customerprofile.html',customer_imgid = user_id, customer=customer,
                            current_sessionID = session_ID,listings_list = listing_list,form=report_form,searchform =search_field)

@app.route('/updateprofile/<int:id>', methods = ['GET', 'POST'])
def updateCustomerprofile(id):
    global session_ID
    db1 = shelve.open('customer.db','c')
    customers_dict = {} #local one
    customer_update_form = CustomerUpdateForm(request.form)
    search_field = SearchBar(request.form)

    #make sure local and db1 are the same state
    #PS JUST COPY AND PASTE IF YOU'RE ACCESSING IT
    try:
        if "Customers" in db1:
            customers_dict = db1["Customers"] #sync local with db1
        else:
            db1['Customers'] = customers_dict #sync db1 with local (basically null)
    except:
        print("Error in opening customer.db")
        
    #sync IDs
    try:
        db1 = shelve.open('customer.db','c')    
        Customer.Customer.count_id = db1["CustomerCount"] #sync count between local and db1
    except:
        print("Error in retrieving data from DB1 Customer count or count is at 0")

    
    if request.method == 'POST' and customer_update_form.validate():
        print(customer_update_form.username.data, customer_update_form.email.data,customer_update_form.password.data)
        customer = customers_dict.get(id) #get current customer
        if customer_update_form.confirmpassword.data == customer.get_password():

            if customer_update_form.email.data != "":
                customer.set_email(customer_update_form.email.data)
                print("Email changed!")
            else:
                print(customer_update_form.email.data)

            if customer_update_form.username.data !="":
                customer.set_username(customer_update_form.username.data)
                print("Username changed!")
            else:
                print(customer_update_form.username.data)

            if customer_update_form.password.data !="":
                customer.set_password(customer_update_form.password.data)
                print("Password changed!")
            else:
                print(customer_update_form.password.data)

            db1['Customers'] = customers_dict
            db1.close()
            #upload img
            file = request.files['file']
            check_upload_file_type(file,"customer",customer.get_id())
            print("Profile info chnaged!")
            return redirect(url_for('Customerprofile', id = id))
        else:
            print("Error in changing profile info")
            return redirect(url_for('Customerprofile', id = id))
        
    #search func
    if request.method == 'POST' and search_field.validate():
        return redirect(url_for('searchresults', keyword = search_field.searchfield.data))
        

    return render_template("CustomerUpdateProfile.html",current_sessionID = session_ID,form=customer_update_form,searchform =search_field)

@app.route('/profilereviews/<int:id>', methods = ['GET', 'POST'])
def Customerprofile_reviews(id):
    global session_ID
    db1 = shelve.open('customer.db','c')
    customers_dict = {}
    reviews_dict ={}
    db3 = shelve.open('reviews.db', 'c')
    db4 =shelve.open('reports.db','c')
    reports_dict = {}
    report_form = ReportForm(request.form)
    search_field = SearchBar(request.form)

    #make sure local and db1 are the same state
    #PS JUST COPY AND PASTE IF YOU'RE ACCESSING IT
    try:
        if "Customers" in db1:
            customers_dict = db1["Customers"] #sync local with db1
        else:
            db1['Customers'] = customers_dict #sync db1 with local (basically null)
    except:
        print("Error in opening customer.db")
        
    #sync IDs
    try:
        db1 = shelve.open('customer.db','c')    
        Customer.Customer.count_id = db1["CustomerCount"] #sync count between local and db1
    except:
        print("Error in retrieving data from DB1 Customer count or count is at 0")

    #PS JUST COPY AND PASTE IF YOU'RE ACCESSING IT
    try:
        if "Reviews" in db3:
            reviews_dict = db3["Reviews"] #sync local with db1
        else:
            db3['Reviews'] = reviews_dict #sync db1 with local (basically null)
    except:
        print("Error in opening reviews.db")
        
    #sync IDs
    try:
        db3 = shelve.open('reviews.db','c')    
        Reviews.Reviews.count_ID = db3["ReviewsCount"] #sync count between local and db1
    except:
        print("Error in retrieving data from DB3 Review count or count is at 0")

    #sync report dbs
    #PS JUST COPY AND PASTE IF YOU'RE ACCESSING IT
    try:
        if "Reports" in db4:
            reports_dict = db4["Reports"] #sync local with db2
        else:
            db4['Reports'] = reports_dict #sync db2 with local (basically null)
    except:
            print("Error in opening reports.db")
    #sync listing IDs
    try:
        db4 = shelve.open('reports.db','c')    
        Report.Report.count_ID = db4["ReportsCount"] #sync count between local and db1
    except:
        print("Error in retrieving data from DB2 Listing count or count is at 0")


    
    customer = customers_dict.get(id)
    customer_reviews = customer.get_reviews()#return list of review IDs
    print(customer_reviews)
    customer_reviews_list = [] #THIS is the one sent to the html 
    
    for key in reviews_dict:
        print(key)
        if key in customer_reviews:
            print(key)
            review = reviews_dict.get(key)
            customer_reviews_list.append(review)
    #report function
    if request.method == 'POST' and report_form.validate():

        #create report obj and store it
        print(report_form.category.data,report_form.report_text.data)
        report = Report.Report(session_ID,id,report_form.category.data,report_form.report_text.data)
        reports_dict[report.get_ID()] = report #store obj in dict
        db4['Reports'] = reports_dict
        db4['ReportsCount'] = Report.Report.count_ID
        db4.close()

        #store report in offender's report_listings
        customer = customers_dict.get(id)
        customer.add_reports(report.get_ID())
        db1['Customers'] = customers_dict
        db1.close()
        redirect(url_for('Customerprofile', id=id))
    #search func
    if request.method == 'POST' and search_field.validate():
        return redirect(url_for('searchresults', keyword = search_field.searchfield.data))
    #reviewer pfp
 
    print(f"Reviews are {customer_reviews_list}")
    return render_template('Customerprofile_reviews.html',customer = customer ,number_of_reviews = len(customer_reviews_list), list_reviews = customer_reviews_list, current_sessionID = session_ID,form=report_form,searchform =search_field)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    global session_ID
    create_customer_form = CustomerSignupForm(request.form)
    search_field = SearchBar(request.form)
    if request.method == 'POST' and create_customer_form.validate():
        db1 = shelve.open('customer.db','c')  
        customers_dict = {} #local one


        #make sure local and db1 are the same state
        #PS JUST COPY AND PASTE IF YOU'RE ACCESSING IT
        try:
            if "Customers" in db1:
                customers_dict = db1["Customers"] #sync local with db1
            else:
                db1['Customers'] = customers_dict #sync db1 with local (basically null)
        except:
            print("Error in opening customer.db")

        
        #sync IDs
        try:
            db1 = shelve.open('customer.db','c')    
            Customer.Customer.count_id = db1["CustomerCount"] #sync count between local and db1
        except:
            print("Error in retrieving data from DB1 Customer count or count is at 0")

        
        
        #create user, stores data in local dict
        customer =  Customer.Customer(create_customer_form.username.data, create_customer_form.email.data,create_customer_form.password.data)
        customers_dict[customer.get_id()] = customer


        #syncs db1 with local dict
        #syncs db1 count with local count (aka customer class)
        db1['Customers'] = customers_dict
        db1['CustomerCount'] = Customer.Customer.count_id

        #upload img
        file = request.files['file']
        check_upload_file_type(file,"customer",customer.get_id())

        #verifies new user is stored
        customers_dict = db1['Customers'] #sync local dict with db1
        customer = customers_dict[customer.get_id()]

        print(f"\n*start of message\nRegistered sucess.\nId: {customer.get_id()}Username:{customer.get_username()}, Email:{customer.get_email()},Password:{customer.get_password()}\n Current session is {Customer.Customer.count_id}\n*end of message*")
        session_ID = Customer.Customer.count_id
        db1.close() #sync the count as it updated when creating the object, if you want to hard reset the count, add a line in customer class to hard reset it to 0 so when syncing, db's one becomes 0

        return redirect(url_for('Customerhome'))
    #search func
    if request.method == 'POST' and search_field.validate():
        return redirect(url_for('searchresults', keyword = search_field.searchfield.data))
        
    return render_template("CustomerSignup.html",form=create_customer_form,current_sessionID = session_ID,searchform =search_field)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    global session_ID
    login_customer_form = CustomerLoginForm(request.form)
    search_field = SearchBar(request.form)
    if request.method == 'POST' and login_customer_form.validate():
        db1 = shelve.open('customer.db','c')
        customers_dict = {} #local one

        #make sure local and db1 are the same state
        #PS JUST COPY AND PASTE IF YOU'RE ACCESSING IT
        try:
            if "Customers" in db1:
                customers_dict = db1["Customers"] #sync local with db1
            else:
                db1['Customers'] = customers_dict #sync db1 with local (basically null)
        except:
            print("Error in opening customer.db")
        
        #sync IDs
        try:
            db1 = shelve.open('customer.db','c')    
            Customer.Customer.count_id = db1["CustomerCount"] #sync count between local and db1
        except:
            print("Error in retrieving data from DB1 Customer count or count is at 0")

        
        #retrieve data from the form
        input_username = login_customer_form.username.data
        input_password = login_customer_form.password.data

        #check
        for key in customers_dict:
            customer = customers_dict[key] #ID
            if input_username == customer.get_username():
                print("Username checked.")
                if input_password == customer.get_password():
                    print("Passwords match.")
                    session_ID = key #current session = this ID
                else:
                    print("password verification failed")
            else:
                print("invalid username")
        
        print(f"\n*start of message*Login success, current session ID is {session_ID}\n*end of message*")
        return redirect(url_for('Customerhome'))
    #search func
    if request.method == 'POST' and search_field.validate():
        return redirect(url_for('searchresults', keyword = search_field.searchfield.data))
    

    return render_template("CustomerLogin.html",form=login_customer_form,current_sessionID = session_ID,searchform =search_field)

@app.route('/loginoptions',methods = ['GET', 'POST'])
def loginoptions():
    global session_ID
    session_ID = 0
    search_field = SearchBar(request.form)
    #search func
    if request.method == 'POST' and search_field.validate():
        return redirect(url_for('searchresults', keyword = search_field.searchfield.data))
    return render_template('Login.html',current_sessionID = session_ID,searchform =search_field)

@app.route('/createlisting', methods = ['GET', 'POST'])
def createlisting():
    global session_ID
    db2 = shelve.open('listing.db','c')
    db1 = shelve.open('customer.db','c')
    listings_images_dict = {}
    listings_dict = {}
    customers_dict = {}
    create_listing_form = ListingForm(request.form)
    search_field = SearchBar(request.form)

    #UPLOAD FOLDER, should be local
    UPLOAD_FOLDER = 'static/listingpics/'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    #sync listing dbs
    #PS JUST COPY AND PASTE IF YOU'RE ACCESSING IT
    try:
        if "Listings" in db2:
            listings_dict = db2["Listings"] #sync local with db2
        else:
            db2['Listings'] = listings_dict #sync db2 with local (basically null)
    except:
            print("Error in opening listings.db")
    #sync listing IDs
    try:
        db2 = shelve.open('listing.db','c')    
        Listing.Listing.count_ID = db2["ListingsCount"] #sync count between local and db1
    except:
        print("Error in retrieving data from DB2 Listing count or count is at 0")

     #make sure local and db1 are the same state
    #PS JUST COPY AND PASTE IF YOU'RE ACCESSING IT
    try:
        if "Customers" in db1:
            customers_dict = db1["Customers"] #sync local with db1
        else:
            db1['Customers'] = customers_dict #sync db1 with local (basically null)
    except:
        print("Error in opening customer.db")
        
    #sync IDs
    try:
        db1 = shelve.open('customer.db','c')    
        Customer.Customer.count_id = db1["CustomerCount"] #sync count between local and db1
    except:
        print("Error in retrieving data from DB1 Customer count or count is at 0")

        


    

    #retrieve data from form
    if request.method == 'POST' and create_listing_form.validate():
        #print(create_listing_form.data)
        #print(create_listing_img_form.data)
        
        #create img object
        #create listing obj
        listing = Listing.Listing(session_ID,create_listing_form.title.data,create_listing_form.description.data,create_listing_form.condition.data,
                                  create_listing_form.category.data,create_listing_form.payment_method.data)
        #returns listings details
        print(f"Listing count:{Listing.Listing.count_ID}\nListing ID: {listing.get_ID()} \nListing creator ID:{listing.get_creatorID()}\nListing title: {listing.get_title()}\nListing Desc: {listing.get_description()}\nListing condition: {listing.get_condition()}\nListing category: {listing.get_category()}\nListing payment method: {listing.get_deal_method()}")
        #stores into db2
        listings_dict[listing.get_ID()] = listing
        db2['Listings'] = listings_dict
        db2['ListingsCount'] = Listing.Listing.count_ID #syncs with db2

        
        #upload img
        file = request.files['file']
        check_upload_file_type(file,"listing",listing.get_ID())

        #create listingimg obj
        #listing = ListingImage.ListingImage(listing.get_ID(),file.filename)
        #stores into db2_1
        #db2_1['ListingImages'] =listings_images_dict #syncs with db2_1

        for key in customers_dict:
            if key == session_ID:
                customer = customers_dict[key]
                #add it to the user's listings
                customer.add_listings(Listing.Listing.count_ID)
                print(customer.get_listings())
                db1['Customers'] = customers_dict #syncs with db1
                break #stop the for loop if this fulfills
        return redirect(url_for('Customerprofile', id=session_ID))# returns to YOUR profile
    #search func
    if request.method == 'POST' and search_field.validate():
        return redirect(url_for('searchresults', keyword = search_field.searchfield.data))
    return render_template('CustomerCreateListing.html', form = create_listing_form, current_sessionID = session_ID,searchform =search_field)

@app.route('/updateListing/<int:id>/', methods=['GET', 'POST'])
def updateListing(id):
    global session_ID
    update_listing_form = ListingForm(request.form)
    db2 = shelve.open('listing.db','c') #RMBR THIS
    search_field = SearchBar(request.form)
    listings_dict = {}
    try:
        if "Listings" in db2:
            listings_dict = db2["Listings"] #sync local with db2
        else:
            db2['Listings'] = listings_dict #sync db2 with local (basically null)
    except:
            print("Error in opening listings.db")
    if request.method == 'POST' and update_listing_form.validate():
        

        listing = listings_dict.get(id)
        #upload img
        file = request.files['file']
        check_upload_file_type(file,"listing",listing.get_ID())
        listing.set_title(update_listing_form.title.data)
        listing.set_category(update_listing_form.category.data)
        listing.set_description(update_listing_form.description.data)
        listing.set_condition(update_listing_form.condition.data)
        listing.set_deal_method(update_listing_form.payment_method.data)
        db2['Listings'] = listings_dict #sync local to db2
        db2.close() 
        return redirect(url_for('Customerprofile', id = id)) #go back to profile page after submit
    #search func
    if request.method == 'POST' and search_field.validate():
        return redirect(url_for('searchresults', keyword = search_field.searchfield.data))

    return render_template('CustomerUpdateListing.html', form = update_listing_form,current_sessionID = session_ID,searchform =search_field) #to render the form 

@app.route('/viewListing/<int:id>/', methods = ['GET', 'POST'])
def viewListing(id):
    global session_ID
    db1 = shelve.open('customer.db','c')
    db2 = shelve.open('listing.db','c') #RMBR THIS
    listings_dict = {}
    customers_dict = {}
    search_field = SearchBar(request.form)
    try:
        if "Listings" in db2:
            listings_dict = db2["Listings"] #sync local with db2
        else:
            db2['Listings'] = listings_dict #sync db2 with local (basically null)
    except:
            print("Error in opening listings.db")
    
    #PS JUST COPY AND PASTE IF YOU'RE ACCESSING IT
    try:
        if "Customers" in db1:
            customers_dict = db1["Customers"] #sync local with db1
        else:
            db1['Customers'] = customers_dict #sync db1 with local (basically null)
    except:
        print("Error in opening customer.db")

    listing = listings_dict.get(id)
    for key in customers_dict:
        if key == listing.get_creatorID():
            seller = customers_dict.get(key)
            break

    #determine if user already liked this post
    customer = customers_dict.get(session_ID) #current user
    customer_liked_posts = customer.get_liked_listings()
    user_liked_post = 'False'
    if listing.get_ID() in customer_liked_posts:
        print("User has already liked this post")
        user_liked_post = 'True'
    #search func
    if request.method == 'POST' and search_field.validate():
        return redirect(url_for('searchresults', keyword = search_field.searchfield.data))
    return render_template('CustomerViewListing.html', listing = listing,seller = seller, current_sessionID = session_ID, user_liked_post = user_liked_post,searchform =search_field)

@app.route('/deleteListing/<int:id>/', methods = ['GET', 'POST'])
def deleteListing(id):
    global session_ID
    db1 = shelve.open('customer.db','c')
    db2 = shelve.open('listing.db','c') #RMBR THIS
    listings_dict = {}
    customers_dict = {}
    try:
        if "Listings" in db2:
            listings_dict = db2["Listings"] #sync local with db2
        else:
            db2['Listings'] = listings_dict #sync db2 with local (basically null)
    except:
            print("Error in opening listings.db")
    
    #PS JUST COPY AND PASTE IF YOU'RE ACCESSING IT
    try:
        if "Customers" in db1:
            customers_dict = db1["Customers"] #sync local with db1
        else:
            db1['Customers'] = customers_dict #sync db1 with local (basically null)
    except:
        print("Error in opening customer.db")
    
    listings_dict.pop(id)
    customer = customers_dict.get(session_ID)
    customer.remove_listings(id)
    print("listing has been removed")
    print(customer.get_listings())
    db1['Customers'] = customers_dict
    db2['Listings'] = listings_dict
    
    return redirect(url_for('Customerprofile', id=session_ID))

@app.route('/createReview/<int:id>', methods = ['GET', 'POST'])
def createReview(id):
    global session_ID
    review_form = ReviewForm(request.form)
    customers_dict = {}
    reviews_dict ={}
    db3 = shelve.open('reviews.db', 'c')
    db1 = shelve.open('customer.db','c')
    search_field = SearchBar(request.form)
     #PS JUST COPY AND PASTE IF YOU'RE ACCESSING IT
    try:
        if "Customers" in db1:
            customers_dict = db1["Customers"] #sync local with db1
        else:
            db1['Customers'] = customers_dict #sync db1 with local (basically null)
    except:
        print("Error in opening customer.db")
        
    #sync IDs
    try:
        db1 = shelve.open('customer.db','c')    
        Customer.Customer.count_id = db1["CustomerCount"] #sync count between local and db1
    except:
        print("Error in retrieving data from DB1 Customer count or count is at 0")

     #PS JUST COPY AND PASTE IF YOU'RE ACCESSING IT
    try:
        if "Reviews" in db3:
            reviews_dict = db3["Reviews"] #sync local with db1
        else:
            db3['Reviews'] = reviews_dict #sync db1 with local (basically null)
    except:
        print("Error in opening reviews.db")
        
    #sync IDs
    try:
        db3 = shelve.open('reviews.db','c')    
        Reviews.Reviews.count_ID = db3["ReviewsCount"] #sync count between local and db1
    except:
        print("Error in retrieving data from DB3 Review count or count is at 0")

    if request.method == 'POST' and review_form.validate():
        #get current user username
        current_customer = customers_dict.get(session_ID)
        current_customer_username = current_customer.get_username()
        

        #update reviews
        review = Reviews.Reviews(session_ID,current_customer_username,(float(review_form.rating.data)), review_form.review_text.data)
        reviews_dict[review.get_ID()] = review
        db3['Reviews'] = reviews_dict
        db3['ReviewsCount'] = Reviews.Reviews.count_ID
        print(f"Review has been added to db3\nReview ID:{review.get_ID()}\nReview creator_ID:{review.get_creator_ID()}\nReview rating:{review.get_rating()}\nReview comment:{review.get_comment()}")

        #update customer's reviews
        customer = customers_dict.get(id)#get opbject
        customer.add_reviews(review.get_ID())
        customer.set_rating(float(review.get_rating()))
        print(f"Customer reviews are {customer.get_reviews()}\n Customer current rating is {customer.get_rating()}")
        db1['Customers'] = customers_dict
        db1.close()
        return redirect(url_for('Customerprofile', id = id)) #goes back to profile u left a review on.
    #search func
    if request.method == 'POST' and search_field.validate():
        return redirect(url_for('searchresults', keyword = search_field.searchfield.data))
    
    return render_template('CustomerReview.html',form=review_form, current_sessionID = session_ID,searchform =search_field)

@app.route('/createLikedListing/<int:id>', methods = ['GET', 'POST'])
def createLikedListing(id): #ID of listing
    global session_ID
    db1 = shelve.open('customer.db','c')
    db2 = shelve.open('listing.db','c') #RMBR THIS
    customers_dict = {} #local one
    listings_dict = {}
    #make sure local and db1 are the same state
    #PS JUST COPY AND PASTE IF YOU'RE ACCESSING IT
    try:
        if "Customers" in db1:
            customers_dict = db1["Customers"] #sync local with db1
        else:
            db1['Customers'] = customers_dict #sync db1 with local (basically null)
    except:
        print("Error in opening customer.db")
        
    #sync IDs
    try:
        db1 = shelve.open('customer.db','c')    
        Customer.Customer.count_id = db1["CustomerCount"] #sync count between local and db1
    except:
        print("Error in retrieving data from DB1 Customer count or count is at 0")

    #sync listing dbs
    #PS JUST COPY AND PASTE IF YOU'RE ACCESSING IT
    try:
        if "Listings" in db2:
            listings_dict = db2["Listings"] #sync local with db2
        else:
            db2['Listings'] = listings_dict #sync db2 with local (basically null)
    except:
            print("Error in opening listings.db")
    #sync listing IDs
    try:
        db2 = shelve.open('listing.db','c')    
        Listing.Listing.count_ID = db2["ListingsCount"] #sync count between local and db1
    except:
        print("Error in retrieving data from DB2 Listing count or count is at 0")
    
    customer = customers_dict.get(session_ID) #get current user obj
    listing = listings_dict.get(id) #id that was entered

    #increment liked count of listing
    listing.add_likes() #add 
    db2['Listings'] = listings_dict
    print(f'Listing ID:{listing.get_ID()}, likes count is {listing.get_likes()}')

    #add liked post ID 
    customer.add_liked_listings(listing.get_ID())
    db1['Customers'] =  customers_dict
    print(f"Customer ID:{customer.get_id()} liked posts are {customer.get_liked_listings()}")


    return redirect(url_for('viewListing', id = id))

@app.route('/createUnlikedListing/<int:id>', methods = ['GET', 'POST'])
def createUnlikedListing(id):
    global session_ID
    db1 = shelve.open('customer.db','c')
    db2 = shelve.open('listing.db','c') #RMBR THIS
    customers_dict = {} #local one
    listings_dict = {}

    #make sure local and db1 are the same state
    #PS JUST COPY AND PASTE IF YOU'RE ACCESSING IT
    try:
        if "Customers" in db1:
            customers_dict = db1["Customers"] #sync local with db1
        else:
            db1['Customers'] = customers_dict #sync db1 with local (basically null)
    except:
        print("Error in opening customer.db")
        
    #sync IDs
    try:
        db1 = shelve.open('customer.db','c')    
        Customer.Customer.count_id = db1["CustomerCount"] #sync count between local and db1
    except:
        print("Error in retrieving data from DB1 Customer count or count is at 0")

    #sync listing dbs
    #PS JUST COPY AND PASTE IF YOU'RE ACCESSING IT
    try:
        if "Listings" in db2:
            listings_dict = db2["Listings"] #sync local with db2
        else:
            db2['Listings'] = listings_dict #sync db2 with local (basically null)
    except:
            print("Error in opening listings.db")
    #sync listing IDs
    try:
        db2 = shelve.open('listing.db','c')    
        Listing.Listing.count_ID = db2["ListingsCount"] #sync count between local and db1
    except:
        print("Error in retrieving data from DB2 Listing count or count is at 0")
    
    customer = customers_dict.get(session_ID) #get current user obj
    listing = listings_dict.get(id) #id that was entered

    #increment liked count of listing
    listing.minus_likes() #minus
    db2['Listings'] = listings_dict
    print(f'Listing ID:{listing.get_ID()}, likes count is {listing.get_likes()}')


    customer.remove_liked_listings(id)
    db1['Customers'] = customers_dict
    print(f"Customer ID:{customer.get_id()} liked posts are {customer.get_liked_listings()}")

    return redirect(url_for('viewListing', id = id))

@app.route('/viewLikedListings/<int:id>', methods = ['GET', 'POST'])
def viewLikedListings(id): #retrieve current session_ID
    global session_ID
    db1 = shelve.open('customer.db','c')
    db2 = shelve.open('listing.db','c') #RMBR THIS
    listings_dict = {}
    customers_dict = {}
    search_field = SearchBar(request.form)
    try:
        if "Listings" in db2:
            listings_dict = db2["Listings"] #sync local with db2
        else:
            db2['Listings'] = listings_dict #sync db2 with local (basically null)
    except:
            print("Error in opening listings.db")
    
    #PS JUST COPY AND PASTE IF YOU'RE ACCESSING IT
    try:
        if "Customers" in db1:
            customers_dict = db1["Customers"] #sync local with db1
        else:
            db1['Customers'] = customers_dict #sync db1 with local (basically null)
    except:
        print("Error in opening customer.db")

    customer = customers_dict.get(id) #current user
    customer_liked_listings = customer.get_liked_listings()
    listings_to_display = []
    for key in listings_dict:
        if key in customer_liked_listings:
            listing = listings_dict.get(key)
            listings_to_display.append(listing)
    #search func
    if request.method == 'POST' and search_field.validate():
        return redirect(url_for('searchresults', keyword = search_field.searchfield.data))
    return render_template('CustomerViewLikedListings.html', listings_to_display = listings_to_display, current_sessionID = session_ID,searchform =search_field)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    global session_ID
    db = shelve.open('messages.db', 'c')  # Open shelve database
    users_db = shelve.open('customer.db')
    user = User(session_ID)
    recent_chats = user.get_recent_chats() 
    search_field = SearchBar(request.form)
    try:
        if request.method == 'POST':
            receiver_id = request.form.get('receiver_id', type=str)
            content = request.form.get('content', '').strip()  # Strip leading/trailing spaces
            customers_dict = users_db.get('Customers', {})
            if not receiver_id.isdigit() or int(receiver_id) == 0 or int(receiver_id) not in customers_dict:
                return render_template(
                    'CustomerMessages.html',
                    error_message=f'User ID {receiver_id} is invalid or does not exist.',
                    show_error_modal=True,
                    current_sessionID=int(session_ID),
                    recent_chats=recent_chats,
                    selected_chat=None
                )
            receiver_id = int(receiver_id)  # Convert to integer after validation
            # Handle Start New Chat (without content) logic
            if receiver_id and content == '':  # Only receiver_id is provided, no content
                return redirect(url_for('messages', receiver_id=receiver_id))  # Open the chat in the right column without changing recent chats order
            # Handle sending a message only if content is provided
            if content:
                user.send_message(receiver_id, content, db)  # This will update recent chats order
            return redirect(url_for('messages', receiver_id=receiver_id))  # Reload to show the new message
        # Display messages and recent chats

        received_messages = user.get_received_messages(db)
        sent_messages = user.get_sent_messages(db)

        selected_chat = None
        if 'receiver_id' in request.args:
            receiver_id = request.args.get('receiver_id', type=int)
            message = [
                {
                    "type": "sent" if message.sender_id == session_ID else "received",
                    "content": message.content,
                    "timestamp": message.timestamp.strftime("%Y-%m-%d %H:%M"),
                    "receiver_id": message.receiver_id,
                    "sender_id": message.sender_id,
                }
                for message in db.get("Messages", [])
                if (message.sender_id == session_ID and message.receiver_id == receiver_id) or
                   (message.receiver_id == session_ID and message.sender_id == receiver_id)
            ]

            selected_chat = {
                'receiver_id': receiver_id,
                'messages': message
            }

        #search func
        if request.method == 'POST' and search_field.validate():
            return redirect(url_for('searchresults', keyword = search_field.searchfield.data))
        

        return render_template(
            'CustomerMessages.html',
            received_messages=received_messages,
            sent_messages=sent_messages,
            current_sessionID=session_ID,
            recent_chats=recent_chats,
            selected_chat=selected_chat,searchform =search_field
        )
    finally:
        db.close()
    # to do: convert recent chat into button not just hyperlink, option to delete/edit/reply to messages
    # dropdown menu: option to delete chat/hyperlink to user's profile/block profile,
    # option to send pictures in chat, make enter key send message, message delivered/read/notifications(red number icon),
    # message previews, make date appear like whatsapp
    #

@app.route('/searchresults/<keyword>')
def searchresults(keyword):
    global session_ID
    
    db2 = shelve.open('listing.db','c') #RMBR THIS
    listings_dict = {}
    search_field = SearchBar(request.form)

    try:
        if "Listings" in db2:
            listings_dict = db2["Listings"] #sync local with db2
        else:
            db2['Listings'] = listings_dict #sync db2 with local (basically null)
    except:
            print("Error in opening listings.db") 

    show_listings = []
    for key in listings_dict:
        listing = listings_dict.get(key)
        
        Search.search_keyword(listing,keyword,show_listings)#check if it fulfills the condition
    
    #search func
    if request.method == 'POST' and search_field.validate():
        return redirect(url_for('searchresults', keyword = search_field.searchfield.data))
    
    return render_template("Customersearchresults.html",current_sessionID = session_ID,searchform =search_field,listings_list = show_listings)

@app.route('/loginoperator', methods=['GET', 'POST'])
def loginoperator():
    global session_ID
    search_field = SearchBar(request.form)
    operator_login_form = OperatorLoginForm(request.form)
    OTP = False #set it to false if you dont want to use the OTP feature
    if request.method == 'POST' and operator_login_form.validate():
        session['Email'] = operator_login_form.email.data #stores the data
        if operator_login_form.operator_username.data == "sysadmin1":
            if operator_login_form.password.data == "sysadmin1":
                if OTP == True:
                    OTP = ' '.join([str(random.randint(0,999999)).zfill(6)])
                    session['OTP'] = OTP
                    #print(f"Session OTP is {session['OTP']}")
                    Email.send_message_operator_OTP(operator_login_form.email.data,OTP)
                    return redirect(url_for('verifyoperator', email = operator_login_form.email.data))
                elif OTP == False:
                    return(redirect(url_for('dashboardusers')))
                
    return render_template('Operatorlogin.html',searchform =search_field, form=operator_login_form)

@app.route('/verifyoperator/<email>',methods=['GET', 'POST'])
def verifyoperator(email):
    search_field = SearchBar(request.form)
    operator_OTP = OperatorLoginVerifyForm(request.form)

    if request.method == 'POST' and operator_OTP.validate():#submit action

        print(operator_OTP.OTP.data)
        if session['OTP'] == operator_OTP.OTP.data:
            return(redirect(url_for('dashboardusers')))
        else:#IF first time fail then
            OTP = ' '.join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])
            session['OTP'] = OTP
            print(f"Session OTP is {session['OTP']}")
            Email.send_message_operator_OTP(email,OTP)
            return redirect(url_for('verifyoperator', email = email))
    
    
    return render_template('OperatorLoginVerify.html', searchform =search_field,form = operator_OTP)

@app.route('/dashboard/users',methods=['GET', 'POST'])
def dashboardusers():
    user_search_field = SearchUserField(request.form)
    db1 = shelve.open('customer.db','c')
    customers_dict = {}
    try:
        if "Customers" in db1:
            customers_dict = db1["Customers"] #sync local with db1
        else:
            db1['Customers'] = customers_dict #sync db1 with local (basically null)
    except:
        print("Error in opening customer.db")
        
    #sync IDs
    try:
        db1 = shelve.open('customer.db','c')    
        Customer.Customer.count_id = db1["CustomerCount"] #sync count between local and db1
    except:
        print("Error in retrieving data from DB1 Customer count or count is at 0")


    customers_list = []
    for key in customers_dict:
        customer = customers_dict.get(key)
        customers_list.append(customer)
    
    if request.method == 'POST' and user_search_field.validate():
        return redirect(url_for('dashboarduserssearch',keyword = user_search_field.searchfield.data))
    
    return render_template('Operatordashboard_users.html',form = user_search_field,customers_list = customers_list)


@app.route('/dashboard/users/search=<keyword>',methods=['GET', 'POST'])
def dashboarduserssearch(keyword):
    user_search_field = SearchUserField(request.form)
    db1 = shelve.open('customer.db','c')
    try:
        if "Customers" in db1:
            customers_dict = db1["Customers"] #sync local with db1
        else:
            db1['Customers'] = customers_dict #sync db1 with local (basically null)
    except:
        print("Error in opening customer.db")
        
    #sync IDs
    try:
        db1 = shelve.open('customer.db','c')    
        Customer.Customer.count_id = db1["CustomerCount"] #sync count between local and db1
    except:
        print("Error in retrieving data from DB1 Customer count or count is at 0")

    customers_list = []
    for key in customers_dict:
        customer = customers_dict.get(key)
        if keyword in customer.get_username():
            customers_list.append(customer)
        else:
            pass
    
    if request.method == 'POST' and user_search_field.validate():
        return redirect(url_for('dashboarduserssearch',keyword = user_search_field.searchfield.data))
    
    
    return render_template('Operatordashboard_users_search.html',form = user_search_field,customers_list = customers_list)
@app.route('/operatorviewprofile/<int:id>',methods=['GET', 'POST'])
def operatorviewprofile(id): #id of profile they are viewing
    db1 = shelve.open('customer.db','c')
    db2 = shelve.open('listing.db','c')
    db5 = shelve.open('operatoractions.db','c')
    customers_dict = {} #local one
    listings_dict = {}
    operatoractions_dict = {}
    terminate_user = OperatorTerminateUser(request.form)
    suspend_user = OperatorSuspendUser(request.form)
    restore_user = OperatorRestoreUser(request.form)

    #make sure local and db1 are the same state
    #PS JUST COPY AND PASTE IF YOU'RE ACCESSING IT
    try:
        if "Customers" in db1:
            customers_dict = db1["Customers"] #sync local with db1
        else:
            db1['Customers'] = customers_dict #sync db1 with local (basically null)
    except:
        print("Error in opening customer.db")
        
    #sync IDs
    try:
        db1 = shelve.open('customer.db','c')    
        Customer.Customer.count_id = db1["CustomerCount"] #sync count between local and db1
    except:
        print("Error in retrieving data from DB1 Customer count or count is at 0")

    #sync listing dbs
    #PS JUST COPY AND PASTE IF YOU'RE ACCESSING IT
    try:
        if "Listings" in db2:
            listings_dict = db2["Listings"] #sync local with db2
        else:
            db2['Listings'] = listings_dict #sync db2 with local (basically null)
    except:
            print("Error in opening listing.db")
    #sync listing IDs
    try:
        db2 = shelve.open('listing.db','c')    
        Listing.Listing.count_ID = db2["ListingsCount"] #sync count between local and db1
    except:
        print("Error in retrieving data from DB2 Listing count or count is at 0")

    #sync db5
    try:
        if "operatoractions" in db5:
            operatoractions_dict = db5["operatoractions"] #sync local with db1
        else:
            db5['operatoractions'] = operatoractions_dict #sync db1 with local (basically null)
    except:
        print("Error in opening operatoractions.db")
        
    #sync IDs
    try:
        db5 = shelve.open('operatoractions.db','c')    
        operatoractions.Operatoractions.count_ID = db5["operatoractionsCount"] #sync count between local and db1
    except:
        print("Error in retrieving data from DB5 operatoractions count or count is at 0")
    
    #get ID list of current user listings
    customer = customers_dict.get(id)
    customer_listings = customer.get_listings()
    print(f"\n*start of message *\nCurrent user has the following listings:{customer_listings}\n*end of message*")
    listing_list = []

    if customer.get_status() == "active": #show listings only when not suspended/terminated
        for key in listings_dict:
            print(key)
            if key in customer_listings:
                listing = listings_dict.get(key)
                listing_list.append(listing)
    #suspend func
    if request.method == 'POST' and suspend_user.validate():
        if suspend_user.password.data == "sysadmin1":
            #create operator action object
            operator_action = operatoractions.Operatoractions(id,suspend_user.category.data,suspend_user.suspend_text.data)
            operatoractions_dict[operator_action.get_ID()] = operator_action #store into local

            #syncs db1 with local dict
            #syncs db1 count with local count (aka customer class)
            db5['operatoractions'] = operatoractions_dict
            db5['operatoractionsCount'] = operatoractions.Operatoractions.count_ID
            db5.close()

            #make changes to affected user
            customer = customers_dict.get(id)
            customer.set_status("suspended")
            db1['Customers'] = customers_dict
            return(redirect(url_for('operatorviewprofile', id=id)))
    

    #terminate func
    if request.method == 'POST' and terminate_user.validate():
        if terminate_user.password.data == "sysadmin1":
            #create operator action object
            operator_action = operatoractions.Operatoractions(id,terminate_user.category.data,terminate_user.terminate_text.data)
            operatoractions_dict[operator_action.get_ID()] = operator_action #store into local

            #syncs db1 with local dict
            #syncs db1 count with local count (aka customer class)
            db5['operatoractions'] = operatoractions_dict
            db5['operatoractionsCount'] = operatoractions.Operatoractions.count_ID
            db5.close()

            #make changes to affected user
            customer = customers_dict.get(id)
            customer.set_status("terminated")
            db1['Customers'] = customers_dict
            return(redirect(url_for('operatorviewprofile', id=id)))
        
    #restore func
    if request.method == 'POST' and restore_user.validate():
        if terminate_user.password.data == "sysadmin1":
            #create operator action object
            operator_action = operatoractions.Operatoractions(id,"restored user","nil")
            operatoractions_dict[operator_action.get_ID()] = operator_action #store into local

            #syncs db1 with local dict
            #syncs db1 count with local count (aka customer class)
            db5['operatoractions'] = operatoractions_dict
            db5['operatoractionsCount'] = operatoractions.Operatoractions.count_ID
            db5.close()

            #make changes to affected user
            customer = customers_dict.get(id)
            customer.set_status("active")
            db1['Customers'] = customers_dict
            return(redirect(url_for('operatorviewprofile', id=id)))
        

    return render_template('OperatorViewProfile.html', customer=customer,
                            listings_list = listing_list,terminate_user_form = terminate_user, suspend_user_form = suspend_user, restore_user_form = restore_user)

@app.route('/operatorviewprofilereviews/<int:id>',methods=['GET', 'POST'])
def operatorviewprofilereviews(id):
    db1 = shelve.open('customer.db','c')
    db5 = shelve.open('operatoractions.db','c')
    db3 = shelve.open('reviews.db', 'c')
    reviews_dict ={}
    customers_dict = {} #local one
    operatoractions_dict = {}
    terminate_user = OperatorTerminateUser(request.form)
    suspend_user = OperatorSuspendUser(request.form)
    restore_user = OperatorRestoreUser(request.form)
    #make sure local and db1 are the same state
    #PS JUST COPY AND PASTE IF YOU'RE ACCESSING IT
    try:
        if "Customers" in db1:
            customers_dict = db1["Customers"] #sync local with db1
        else:
            db1['Customers'] = customers_dict #sync db1 with local (basically null)
    except:
        print("Error in opening customer.db")
        
    #sync IDs
    try:
        db1 = shelve.open('customer.db','c')    
        Customer.Customer.count_id = db1["CustomerCount"] #sync count between local and db1
    except:
        print("Error in retrieving data from DB1 Customer count or count is at 0")

    #PS JUST COPY AND PASTE IF YOU'RE ACCESSING IT
    try:
        if "Reviews" in db3:
            reviews_dict = db3["Reviews"] #sync local with db1
        else:
            db3['Reviews'] = reviews_dict #sync db1 with local (basically null)
    except:
        print("Error in opening reviews.db")
        
    #sync IDs
    try:
        db3 = shelve.open('reviews.db','c')    
        Reviews.Reviews.count_ID = db3["ReviewsCount"] #sync count between local and db1
    except:
        print("Error in retrieving data from DB3 Review count or count is at 0")

    #sync db5
    try:
        if "operatoractions" in db5:
            operatoractions_dict = db5["operatoractions"] #sync local with db1
        else:
            db5['operatoractions'] = operatoractions_dict #sync db1 with local (basically null)
    except:
        print("Error in opening operatoractions.db")
        
    #sync IDs
    try:
        db5 = shelve.open('operatoractions.db','c')    
        operatoractions.Operatoractions.count_ID = db5["operatoractionsCount"] #sync count between local and db1
    except:
        print("Error in retrieving data from DB5 operatoractions count or count is at 0")

    customer = customers_dict.get(id)
    customer_reviews = customer.get_reviews()#return list of review IDs
    print(customer_reviews)
    customer_reviews_list = [] #THIS is the one sent to the html 
    
    for key in reviews_dict:
        print(key)
        if key in customer_reviews:
            print(key)
            review = reviews_dict.get(key)
            customer_reviews_list.append(review)


    #suspend func
    if request.method == 'POST' and suspend_user.validate():
        if suspend_user.password.data == "sysadmin1":
            #create operator action object
            operator_action = operatoractions.Operatoractions(id,suspend_user.category.data,suspend_user.suspend_text.data)
            operatoractions_dict[operator_action.get_ID()] = operator_action #store into local

            #syncs db1 with local dict
            #syncs db1 count with local count (aka customer class)
            db5['operatoractions'] = operatoractions_dict
            db5['operatoractionsCount'] = operatoractions.Operatoractions.count_ID
            db5.close()

            #make changes to affected user
            customer = customers_dict.get(id)
            customer.set_status("suspended")
            db1['Customers'] = customers_dict
            return(redirect(url_for('operatorviewprofile', id=id)))
        
    #terminate func
    if request.method == 'POST' and terminate_user.validate():
        if terminate_user.password.data == "sysadmin1":
            #create operator action object
            operator_action = operatoractions.Operatoractions(id,terminate_user.category.data,terminate_user.terminate_text.data)
            operatoractions_dict[operator_action.get_ID()] = operator_action #store into local

            #syncs db1 with local dict
            #syncs db1 count with local count (aka customer class)
            db5['operatoractions'] = operatoractions_dict
            db5['operatoractionsCount'] = operatoractions.Operatoractions.count_ID
            db5.close()

            #make changes to affected user
            customer = customers_dict.get(id)
            customer.set_status("terminated")
            db1['Customers'] = customers_dict
            return(redirect(url_for('operatorviewprofile', id=id)))
    
    #restore func
    if request.method == 'POST' and restore_user.validate():
        if terminate_user.password.data == "sysadmin1":
            #create operator action object
            operator_action = operatoractions.Operatoractions(id,"restored user","nil")
            operatoractions_dict[operator_action.get_ID()] = operator_action #store into local

            #syncs db1 with local dict
            #syncs db1 count with local count (aka customer class)
            db5['operatoractions'] = operatoractions_dict
            db5['operatoractionsCount'] = operatoractions.Operatoractions.count_ID
            db5.close()

            #make changes to affected user
            customer = customers_dict.get(id)
            customer.set_status("active")
            db1['Customers'] = customers_dict
            return(redirect(url_for('operatorviewprofile', id=id)))
    

    return render_template("OperatorViewProfile_reviews.html",customer = customer ,number_of_reviews = len(customer_reviews_list),list_reviews = customer_reviews_list,terminate_user_form = terminate_user, suspend_user_form = suspend_user, restore_user_form = restore_user)

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()
