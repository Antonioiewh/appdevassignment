from flask import Flask, render_template, url_for,request,redirect,session,jsonify
import os,sys,stat
from werkzeug.utils import secure_filename
import Customer , Listing,Reviews,Report,operatoractions,Feedback #classes
from Forms import CustomerSignupForm, CustomerLoginForm, ListingForm,ReviewForm,CustomerUpdateForm,ReportForm,SearchBar,OperatorLoginForm,OperatorLoginVerifyForm,SearchUserField,OperatorSuspendUser,OperatorTerminateUser,OperatorRestoreUser #our forms
from Forms import OperatorDisableListing,OperatorRestoreListing,SearchListingField,SearchReportField,SearchOperatorActionField,FeedbackForm
import Email,Search,Notifications
import shelve, Customer
from pathlib import Path
from Messages import User
import string
import random
from datetime import datetime
import Filters
app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def check_allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_upload_file_type(file,type,id): #file obj here, listing/userid here too, type too
    file_to_upload = file
    if type == "listing" and check_allowed_file(file.filename):
        file.filename = f"listing{id}.jpg"
        check_dupe_file(file_to_upload,"listingpics")
   
    elif type == "customer" and check_allowed_file(file.filename):
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

    else:
        file_uploaded = file
        folder = type
        upload_file(folder,file_uploaded)

def upload_file(folder,file):
    filename = secure_filename(file.filename)
    file.save(os.path.join(f"static/{folder}", filename))
    #for some reason it keeps returning ERRNO13 aka no permission but err it works so idk

    

def send_welcomenotifcation(id): #id of person to add notifactions to
    db1 = shelve.open('customer.db','c')
    db6 = shelve.open('notifications.db','c')
    customers_dict = {}
    notifications_dict = {}
    try:
        if "Customers" in db1:
            customers_dict = db1["Customers"] #sync local with db1
        else:
            db1['Customers'] = customers_dict #sync db1 with local (basically null)
    except:
        print("Error in opening customer.db")
    try:
        if "Notifications" in db6:
            notifications_dict = db6["Notifications"] #sync local with db1
        else:
            db6['Notifications'] = customers_dict #sync db1 with local (basically null)
    except:
        print("Error in opening notifications.db")
    
    try:
        db6 = shelve.open('notifications.db','c')    
        Notifications.Notifications.count_ID = db6["NotificationsCount"] #sync count between local and db1
    except:
        print("Error in retrieving data from DB6 Notifications count or count is at 0")
    
    #create notifcation obj
    notification = Notifications.Notifications(id,"Welcome to Freesell!")
    notifications_dict[notification.get_ID()] = notification
    db6["Notifications"] = notifications_dict
    db6["NotificationsCount"] = Notifications.Notifications.count_ID
    db6.close()
    #add it to customer notifcations
    customer = customers_dict.get(id)
    customer.add_notifications(notification.get_ID()) #adds notifs
    db1["Customers"] = customers_dict

    #send the notifcation to their email

    Email.send_signup_notification_gmail(customer.get_email(),customer.get_username())

#current_sessionID IS FOR THE PROFILE!!
#Current session ID
#MAKE SURE AN USER WITH ID "X" EXISTS!      
session_ID = 0

@app.route('/', methods = ['GET', 'POST']) #shld be the same as href for buttons,links,navbar, etc...
def Customerhome():
    db1 = shelve.open('customer.db','c')
    customers_dict = {} #local one
    global session_ID
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
    #search func
    if request.method == 'POST' and search_field.validate():
        return redirect(url_for('searchresults', keyword = search_field.searchfield.data)) #get the word from the search field
    #get notifs
    if session_ID != 0:
        customer = customers_dict.get(session_ID)
        customer_notifications = customer.get_unread_notifications()
    elif session_ID == 0:
        customer_notifications = 0  

    return render_template('Customerhome.html', current_sessionID = session_ID,searchform =search_field,customer_notifications = customer_notifications)
    
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
        print("Error in retrieving data from DB4 Report count or count is at 0")


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
        customer = customers_dict.get(id)

        #create report obj and store it
        print(report_form.category.data,report_form.report_text.data)
        report = Report.Report(session_ID,id,customer.get_username(),report_form.category.data,report_form.report_text.data)
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
    try:
        if request.method == 'POST' and search_field.validate():
            return redirect(url_for('searchresults', keyword = search_field.searchfield.data))
    except:
        pass
    #get notifs
    if session_ID != 0:
        customer = customers_dict.get(session_ID)
        customer_notifications = customer.get_unread_notifications()
    elif session_ID == 0:
        customer_notifications = 0  

    #get img
    return render_template('Customerprofile.html',customer_imgid = user_id, customer=customer,
                            current_sessionID = session_ID,listings_list = listing_list,form=report_form,searchform =search_field,customer_notifications = customer_notifications)

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
    try:
        if request.method == 'POST' and search_field.validate():
            return redirect(url_for('searchresults', keyword = search_field.searchfield.data))
    except:
        pass
    
    #get notifs
    if session_ID != 0:
        customer = customers_dict.get(session_ID)
        customer_notifications = customer.get_unread_notifications()
    elif session_ID == 0:
        customer_notifications = 0  



    return render_template("CustomerUpdateProfile.html",current_sessionID = session_ID,form=customer_update_form,searchform =search_field,customer_notifications = customer_notifications)

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
        print("Error in retrieving data from DB4 Report count or count is at 0")


    
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
        customer = customers_dict.get(id)

        #create report obj and store it
        print(report_form.category.data,report_form.report_text.data)
        report = Report.Report(session_ID,id,customer.get_username(),report_form.category.data,report_form.report_text.data)
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
    try:
        if request.method == 'POST' and search_field.validate():
            return redirect(url_for('searchresults', keyword = search_field.searchfield.data))
    except:
        pass
    #get notifs
    if session_ID != 0:
        customer = customers_dict.get(session_ID)
        customer_notifications = customer.get_unread_notifications()
    elif session_ID == 0:
        customer_notifications = 0  

    return render_template('Customerprofile_reviews.html',customer = customer ,number_of_reviews = len(customer_reviews_list), list_reviews = customer_reviews_list, current_sessionID = session_ID,form=report_form,searchform =search_field,customer_notifications=customer_notifications)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    global session_ID
    create_customer_form = CustomerSignupForm(request.form)
    search_field = SearchBar(request.form)
    db1 = shelve.open('customer.db','c')  
    customers_dict = {} #local one
    if request.method == 'POST' and create_customer_form.validate():
        


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
        #notifs
        send_welcomenotifcation(customer.get_id())
        
        return redirect(url_for('Customerhome'))
    #search func
    try:
        if request.method == 'POST' and search_field.validate():
            return redirect(url_for('searchresults', keyword = search_field.searchfield.data))
    except:
        pass
    
    #get notifs
    if session_ID != 0:
        customer = customers_dict.get(session_ID)
        customer_notifcations = customer.get_unread_notifications()
    elif session_ID == 0:
        customer_notifcations = 0  

    return render_template("CustomerSignup.html",form=create_customer_form,current_sessionID = session_ID,searchform =search_field,customer_notifications = customer_notifcations)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    global session_ID
    login_customer_form = CustomerLoginForm(request.form)
    search_field = SearchBar(request.form)
    db1 = shelve.open('customer.db','c')
    customers_dict = {} #local one
    if request.method == 'POST' and login_customer_form.validate():
        

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
    try:
        if request.method == 'POST' and search_field.validate():
            return redirect(url_for('searchresults', keyword = search_field.searchfield.data))
    except:
        pass
    #get notifs
    if session_ID != 0:
        customer = customers_dict.get(session_ID)
        customer_notifcations = customer.get_unread_notifications()
    elif session_ID == 0:
        customer_notifcations = 0  

    return render_template("CustomerLogin.html",form=login_customer_form,current_sessionID = session_ID,searchform =search_field,customer_notifications=customer_notifcations)

@app.route('/loginoptions',methods = ['GET', 'POST'])
def loginoptions():
    global session_ID
    db1 = shelve.open('customer.db','c')
    customers_dict = {} #local one
    session_ID = 0
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
    #search func
    try:
        if request.method == 'POST' and search_field.validate():
            return redirect(url_for('searchresults', keyword = search_field.searchfield.data))
    except:
        pass
    #get notifs
    if session_ID != 0:
        customer = customers_dict.get(session_ID)
        customer_notifcations = customer.get_unread_notifications()
    elif session_ID == 0:
        customer_notifcations = 0  

    return render_template('Login.html',current_sessionID = session_ID,searchform =search_field,customer_notifications=customer_notifcations)

@app.route('/createlisting', methods = ['GET', 'POST'])
def createlisting():
    global session_ID
    db2 = shelve.open('listing.db','c')
    db1 = shelve.open('customer.db','c')
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

        paymentmethod = ""
        paymentinfo =[]
        print(create_listing_form.meetup.data,create_listing_form.delivery.data)
        #payment method etc
        if create_listing_form.meetup.data == True:
            paymentmethod += "meetup"
            paymentinfo.append(create_listing_form.meetupinfo.data)

        else:
            pass
        if create_listing_form.delivery.data == True:
            paymentmethod += "delivery"
            paymentinfo.append(create_listing_form.deliveryinfo.data)
        else:
            pass
        
        print(paymentmethod,paymentinfo)
        listing = Listing.Listing(session_ID,create_listing_form.title.data,create_listing_form.description.data,create_listing_form.condition.data,create_listing_form.category.data,paymentmethod,paymentinfo)
                
        #print(f"Listing count:{Listing.Listing.count_ID}\nListing ID: {listing.get_ID()} \nListing creator ID:{listing.get_creatorID()}\nListing title: {listing.get_title()}\nListing Desc: {listing.get_description()}\nListing condition: {listing.get_condition()}\nListing category: {listing.get_category()}\nListing payment method: {listing.get_deal_method()}")
        #stores into db2
        listings_dict[listing.get_ID()] = listing
        db2['Listings'] = listings_dict
        db2['ListingsCount'] = Listing.Listing.count_ID #syncs with db2

        
        #upload img
        file = request.files['file']
        check_upload_file_type(file,"listing",listing.get_ID())

        for key in customers_dict:
            if key == session_ID:
                customer = customers_dict[key]
                customer.add_listings(Listing.Listing.count_ID)
                db1['Customers'] = customers_dict #syncs with db1
                break #stop the for loop if this fulfills
        return redirect(url_for('Customerprofile', id=session_ID))# returns to YOUR profile
    #search func
    try:
        if request.method == 'POST' and search_field.validate():
            return redirect(url_for('searchresults', keyword = search_field.searchfield.data))
    except:
        pass
    #get notifs
    if session_ID != 0:
        customer = customers_dict.get(session_ID)
        customer_notifcations = customer.get_unread_notifications()
    elif session_ID == 0:
        customer_notifcations = 0 
    return render_template('CustomerCreateListing.html', form = create_listing_form, current_sessionID = session_ID,searchform =search_field,customer_notifications=customer_notifcations)

@app.route('/updateListing/<int:id>/', methods=['GET', 'POST'])
def updateListing(id):
    global session_ID
    update_listing_form = ListingForm(request.form)
    db2 = shelve.open('listing.db','c') #RMBR THIS
    search_field = SearchBar(request.form)
    db1 = shelve.open('customer.db','c')
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
        
    try:
        if "Listings" in db2:
            listings_dict = db2["Listings"] #sync local with db2
        else:
            db2['Listings'] = listings_dict #sync db2 with local (basically null)
    except:
            print("Error in opening listings.db")
    paymentmethod = ""
    paymentinfo =[]
    print(update_listing_form.meetup.data,update_listing_form.delivery.data)
    #payment method etc
    if update_listing_form.meetup.data == True:
        paymentmethod += "meetup"
        paymentinfo.append(update_listing_form.meetupinfo.data)

    else:
        pass
    if update_listing_form.data == True:
        paymentmethod += "delivery"
        paymentinfo.append(update_listing_form.deliveryinfo.data)
    else:
        pass
        
    print(paymentmethod,paymentinfo)
    
    if request.method == 'POST' and update_listing_form.validate():
        

        listing = listings_dict.get(id)
        #upload img
        file = request.files['file']
        check_upload_file_type(file,"listing",listing.get_ID())
        listing.set_title(update_listing_form.title.data)
        listing.set_category(update_listing_form.category.data)
        listing.set_description(update_listing_form.description.data)
        listing.set_condition(update_listing_form.condition.data)
        listing.set_deal_method(paymentmethod)
        if paymentmethod == 'meetup':
            listing.set_deal_meetupinfo(paymentinfo[0])
        if paymentmethod =='delivery':
            listing.set_deal_deliveryinfo(paymentinfo[0])
        if paymentmethod == 'meetupdelivery':
            listing.set_deal_meetupinfo(paymentinfo[0])
            listing.set_deal_deliveryinfo(paymentinfo[1])

        
        db2['Listings'] = listings_dict #sync local to db2
        db2.close() 
        return redirect(url_for('Customerprofile', id = id)) #go back to profile page after submit
    try:
        if request.method == 'POST' and search_field.validate():
            return redirect(url_for('searchresults', keyword = search_field.searchfield.data))
    except:
        pass
    #get notifs
    if session_ID != 0:
        customer = customers_dict.get(session_ID)
        customer_notifcations = customer.get_unread_notifications()
    elif session_ID == 0:
        customer_notifcations = 0 
    return render_template('CustomerUpdateListing.html', form = update_listing_form,current_sessionID = session_ID,searchform =search_field,customer_notifications=customer_notifcations) #to render the form 

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
        user_liked_post = 'True'
    
    #search func
    try:
        if request.method == 'POST' and search_field.validate():
            return redirect(url_for('searchresults', keyword = search_field.searchfield.data))
    except:
        pass
    #get notifs
    if session_ID != 0:
        customer = customers_dict.get(session_ID)
        customer_notifcations = customer.get_unread_notifications()
    elif session_ID == 0:
        customer_notifcations = 0 
    return render_template('CustomerViewListing.html', listing = listing,seller = seller, current_sessionID = session_ID, user_liked_post = user_liked_post,searchform =search_field,customer_notifications=customer_notifcations)

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
    notifications_dict = {}
    db3 = shelve.open('reviews.db', 'c')
    db1 = shelve.open('customer.db','c')
    db6 = shelve.open('notifications.db','c')
    search_field = SearchBar(request.form)

    try:
        if "Notifications" in db6:
            notifications_dict = db6["Notifications"] #sync local with db1
        else:
            db6['Notifications'] = customers_dict #sync db1 with local (basically null)
    except:
        print("Error in opening notifications.db")
    try:
        db6 = shelve.open('notifications.db','c')    
        Notifications.Notifications.count_ID = db6["NotificationsCount"] #sync count between local and db1
    except:
        print("Error in retrieving data from DB6 Notifications count or count is at 0")
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

        #notif
        #create notif obj
        notification = Notifications.Notifications(customer.get_id(),f"{current_customer_username} has left you a review!")
        notifications_dict[notification.get_ID()] = notification
        db6['Notifications'] = notifications_dict
        db6['NotificationsCount'] = Notifications.Notifications.count_ID

        #add notif to customer
        customer.add_notifications(notification.get_ID())
        db1['Customers'] = customers_dict

        #Email user
        Email.send_review_notifcation_gmail(customer.get_email(),customer.get_username(),current_customer_username,review.get_comment())
        return redirect(url_for('Customerprofile', id = id))
    try:
        if request.method == 'POST' and search_field.validate():
            return redirect(url_for('searchresults', keyword = search_field.searchfield.data))
    except:
        pass
    #get notifs
    if session_ID != 0:
        customer = customers_dict.get(session_ID)
        customer_notifications = customer.get_unread_notifications()
    elif session_ID == 0:
        customer_notifications = 0 

    return render_template('CustomerReview.html',form=review_form, current_sessionID = session_ID,searchform =search_field,customer_notifications=customer_notifications)

@app.route('/createLikedListing/<int:id>', methods = ['GET', 'POST'])
def createLikedListing(id): #ID of listing
    global session_ID
    db1 = shelve.open('customer.db','c')
    db2 = shelve.open('listing.db','c')
    db6 = shelve.open('notifications.db','c') #RMBR THIS
    customers_dict = {} #local one
    listings_dict = {}
    notifications_dict = {}
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
    
    try:
        if "Notifications" in db6:
            notifications_dict = db6["Notifications"] #sync local with db1
        else:
            db6['Notifications'] = customers_dict #sync db1 with local (basically null)
    except:
        print("Error in opening notifications.db")
    try:
        db6 = shelve.open('notifications.db','c')    
        Notifications.Notifications.count_ID = db6["NotificationsCount"] #sync count between local and db1
    except:
        print("Error in retrieving data from DB6 Notifications count or count is at 0")
    
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
    
    #notif
    notification = Notifications.Notifications(listing.get_creatorID(),f"{customer.get_username()} liked your post:{listing.get_title()}")
    notifications_dict[notification.get_ID()] = notification
    db6['Notifications'] = notifications_dict
    db6['NotificationsCount'] = Notifications.Notifications.count_ID
    for key in notifications_dict:
        print(notifications_dict.get(key))

    #add notif to customer
    seller = customers_dict.get(listing.get_creatorID())
    seller.add_notifications(notification.get_ID())
    db1['Customers'] = customers_dict

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
    #search function
    try:
        if request.method == 'POST' and search_field.validate():
            return redirect(url_for('searchresults', keyword = search_field.searchfield.data))
    except:
        pass
    
    #get notifs
    if session_ID != 0:
        customer = customers_dict.get(session_ID)
        customer_notifications = customer.get_unread_notifications()
    elif session_ID == 0:
        customer_notifications == 0
    return render_template('CustomerViewLikedListings.html', listings_to_display = listings_to_display, current_sessionID = session_ID,searchform =search_field,customer_notifications=customer_notifications)

@app.route('/messages', methods=['GET', 'POST'])
def messages():

    global session_ID
    customers_dict = {}
    db1 = shelve.open('customer.db','c')
    #PS JUST COPY AND PASTE IF YOU'RE ACCESSING IT
    try:
        if "Customers" in db1:
            customers_dict = db1["Customers"] #sync local with db1
        else:
            db1['Customers'] = customers_dict #sync db1 with local (basically null)
    except:
        print("Error in opening customer.db")
    # add in for official project
    if session_ID == 0:
        return redirect(url_for('Customerhome'))
    db = shelve.open('messages.db', 'c')  # Open shelve database
    users_db = shelve.open('customer.db')
    user = User(session_ID)
    recent_chats = user.get_recent_chats() 
    search_field = SearchBar(request.form)

    #get notifs
    if session_ID != 0:
        customer = customers_dict.get(session_ID)
        customer_notifications = customer.get_unread_notifications()
    elif session_ID == 0:
        customer_notifications = 0 
    #search func
    try:
        if request.method == 'POST' and search_field.validate():
            return redirect(url_for('searchresults', keyword = search_field.searchfield.data))
    except:
        pass
    try:
        if request.method == 'POST':
            receiver_id = request.form.get('receiver_id', type=str)# searchbar refers to this code when used, causes crash
            content = request.form.get('content', '').strip()  # Strip leading/trailing spaces
            customers_dict = users_db.get('Customers', {})
            if not receiver_id.isdigit() or int(receiver_id) == 0 or int(receiver_id) not in customers_dict:
                return render_template(
                    'CustomerMessages.html',
                    error_message=f'User ID {receiver_id} is invalid or does not exist.',
                    show_error_modal=True,
                    current_sessionID=int(session_ID),
                    recent_chats=recent_chats,
                    selected_chat=None,
                    customer_notifications=customer_notifications,
                    searchform=search_field
                )
            if int(receiver_id) == session_ID:
                return render_template(
                    'CustomerMessages.html',
                    error_message="You can't message yourself",
                    show_error_modal=True,
                    current_sessionID=int(session_ID),
                    recent_chats=recent_chats,
                    selected_chat=None,
                    customer_notifications=customer_notifications,
                    searchform=search_field  #<- always put
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
                    "message_id": message.message_id,
                    "status": message.status
                }
                for message in db.get("Messages", [])
                if (message.sender_id == session_ID and message.receiver_id == receiver_id) or
                   (message.receiver_id == session_ID and message.sender_id == receiver_id)
            ]

            selected_chat = {
                'receiver_id': receiver_id,
                'messages': message
            }
        
        
        

        return render_template(
            'CustomerMessages.html',
            received_messages=received_messages,
            sent_messages=sent_messages,
            current_sessionID=session_ID,
            recent_chats=recent_chats,
            selected_chat=selected_chat,
            searchform =search_field,
            customer_notifcations=customer_notifications,
            show_error_modal=False,
        )
    finally:
        db.close()
    # dropdown menu: option to delete chat/hyperlink to user's profile/block profile,
    # option to send pictures in chat, make enter key send message, message delivered/read/notifications(red number icon),
    # message previews, make date appear like whatsapp, message deletion timer (max 15min to delete msg)

@app.route('/delete_chat', methods=['POST'])
def delete_chat():
    db = shelve.open('recentChat.db', 'c')
    user = User(session_ID)
    recent_chats = user.get_recent_chats()
    data = request.get_json()  # Get the JSON data
    receiver_id = data.get('receiver_id')
    # Process the receiver_id as needed
    print(recent_chats)
    print(f"Received receiver_id: {receiver_id}")
    updated_chats = []
    for chat in recent_chats:
        if not chat['receiver_id'] == int(receiver_id):
            updated_chats.append(chat)
    print(updated_chats)
    db[str(session_ID)] = updated_chats
    return jsonify({'message': f'Receiver ID {receiver_id} processed successfully.'})

@app.route('/delete_message', methods=['POST'])
def delete_message():

    data = request.get_json()  # Get the JSON data from the request
    message_id = data.get('message_id')  # Get the message ID

    db = shelve.open('messages.db', 'c')
    messages2 = db.get('Messages', [])
    message_to_delete = None

    for message in messages2:
        if message.message_id == message_id:
            message_to_delete = message
            break

    if not message_to_delete:
        return jsonify({'success': False, 'error': 'Message not found'}), 404

    # Delete the message from the database
    # messages2.remove(message_to_delete)
    message_to_delete.status = "deleted"
    message_to_delete.content = None #privacy concerns
    db['Messages'] = messages2

    db.close()


    # to do: ask teacher if it counts as "deletion" of database to do the above, must there be real time messages(current code only shows message upon refresh),
    # cannot enter own ID for new chat, option to edit/reply to messages
    # dropdown menu: option to delete chat/hyperlink to user's profile/block profile,
    # option to send pictures in chat, message delivered/read/notifications(red number icon),
    # message previews, make date appear like whatsapp

@app.route('/searchresults/<keyword>', methods=['GET', 'POST'])
def searchresults(keyword):
    global session_ID
    db1 = shelve.open('customer.db','c')
    db2 = shelve.open('listing.db','c') #RMBR THIS
    customers_dict = {}
    listings_dict = {}
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
    try:
        if request.method == 'POST' and search_field.validate():
            return redirect(url_for('searchresults', keyword = search_field.searchfield.data))
    except:
        pass
    #get notifs
    if session_ID != 0:
        customer = customers_dict.get(session_ID)
        customer_notifications = len(customer.get_notifications())
    elif session_ID == 0:
        customer_notifications = 0 
    return render_template("Customersearchresults.html",current_sessionID = session_ID,searchform =search_field,listings_list = show_listings,customer_notifications=customer_notifications)
    

@app.route('/category1', methods=['GET', 'POST'])
def category1():
    global session_ID
    customers_dict = {}
    db1 = shelve.open('customer.db','c')
    search_field = SearchBar(request.form)
    #
    try:
        if request.method == 'POST' and search_field.validate():
            return redirect(url_for('searchresults', keyword = search_field.searchfield.data))
    except:
        pass
    #get notifs
    if session_ID != 0:
        customer = customers_dict.get(session_ID)
        customer_notifications = customer.get_unread_notifications()
    elif session_ID == 0:
        customer_notifications = 0 
    
@app.route('/feedback', methods = ['GET', 'POST'])
def feedback():
    global session_ID
    customers_dict = {}
    db1 = shelve.open('customer.db','c')
    feedbacks_dict = {}
    db7 = shelve.open('feedback.db','c')
    search_field = SearchBar(request.form)
    feedback_form = FeedbackForm(request.form)
    #PS JUST COPY AND PASTE IF YOU'RE ACCESSING IT
    try:
        if "Customers" in db1:
            customers_dict = db1["Customers"] #sync local with db1
        else:
            db1['Customers'] = customers_dict #sync db1 with local (basically null)
    except:
        print("Error in opening customer.db")
    try:
        if "Feedback" in db7:
            feedbacks_dict = db7["Feedback"] #sync local with db1
        else:
            db7['Feedback'] = feedbacks_dict #sync db1 with local (basically null)
    except:
        print("Error in opening feedback.db")
        
    #sync IDs
    try:
        db7 = shelve.open('feedback.db','c')    
        Feedback.Feedback.count_ID = db7["FeedbackCount"] #sync count between local and db1
    except:
        print("Error in retrieving data from DB7 Feedback count or count is at 0")

    #search func
    try:
        if request.method == 'POST' and search_field.validate():
            return redirect(url_for('searchresults', keyword = search_field.searchfield.data))
    except:
        pass
    #get notifs
    if session_ID != 0:
        customer = customers_dict.get(session_ID)
        customer_notifications = customer.get_unread_notifications()
    elif session_ID == 0:
        customer_notifications = 0 

    if request.method == 'POST' and feedback_form.validate():
        feedback = Feedback.Feedback(feedback_form.rating.data,feedback_form.feedback.data)
        feedbacks_dict[feedback.get_ID()] = feedback #store obj in dict
        db7['Feedback'] = feedbacks_dict
        db7['FeedbackCount'] = Feedback.Feedback.count_ID
        db7.close()
        return redirect(url_for('Customerhome'))
    
    return render_template('CustomerFeedback.html',searchform =search_field,
            customer_notifications=customer_notifications,current_sessionID=int(session_ID),form=feedback_form)

@app.route('/notifications/<int:id>')
def viewnotifications(id): #id is current_sessionID
    global session_ID
    db1 = shelve.open('customer.db','c')
    db6 = shelve.open('notifications.db','c')
    notifications_dict = {}
    customers_dict = {}
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
    try:
        if "Notifications" in db6:
            notifications_dict = db6["Notifications"] #sync local with db1
        else:
            db6['Notifications'] = customers_dict #sync db1 with local (basically null)
    except:
        print("Error in opening notifications.db")
    
    try:
        db6 = shelve.open('notifications.db','c')    
        Notifications.Notifications.count_ID = db6["NotificationsCount"] #sync count between local and db1
    except:
        print("Error in retrieving data from DB6 Notifications count or count is at 0")

    #get own notifs
    customer = customers_dict.get(id)
    notifs_list = customer.get_notifications()
    notifs_to_display = []
    for key in notifications_dict:
        notification = notifications_dict.get(key)
        notifs_to_display.append(notification)
    #search func
    try:
        if request.method == 'POST' and search_field.validate():
            return redirect(url_for('searchresults', keyword = search_field.searchfield.data))
    except:
        pass

    #get notifs
    if session_ID != 0:
        customer = customers_dict.get(session_ID)
        customer_notifications = len(customer.get_notifications())
    elif session_ID == 0:
        customer_notifications = 0 
    
    
    return render_template("CustomerViewNotifications.html",current_sessionID = session_ID,searchform =search_field,customer_notifications=customer_notifications,notifications_list = notifs_to_display)

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
    terminate_user = OperatorTerminateUser(request.form,typeofaction='terminate user')
    suspend_user = OperatorSuspendUser(request.form,typeofaction='suspend user')
    restore_user = OperatorRestoreUser(request.form,typeofaction='report user')
    disable_listing = OperatorDisableListing(request.form,typeofaction='disable listing')
    restore_listing = OperatorRestoreListing(request.form,typeofaction='restore listing')
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

    #disable listing
    if request.method == 'POST' and disable_listing.validate():
        if disable_listing.password.data == "sysadmin1":
            #create operator action object)
            operator_action = operatoractions.Operatoractions(id,disable_listing.typeofaction.data,disable_listing.category.data,disable_listing.disable_text.data)
            operatoractions_dict[operator_action.get_ID()] = operator_action #store into local
            
            #syncs db5 with local dict
            #syncs db5 count with local count (aka customer class)
            db5['operatoractions'] = operatoractions_dict
            db5['operatoractionsCount'] = operatoractions.Operatoractions.count_ID
            db5.close()

            #make changes to affected listing
            listing = listings_dict.get(int(disable_listing.id.data))
            listing.set_status("disabled")
            print(listing.get_status())
            db2['Listings'] = listings_dict
            return(redirect(url_for('operatorviewprofile', id=id)))

    #restore listing
    if request.method == 'POST' and restore_listing.validate():
        if restore_listing.password.data == "sysadmin1":
            #create operator action object
            operator_action = operatoractions.Operatoractions(id,restore_listing.typeofaction.data,"nil","nil")
            operatoractions_dict[operator_action.get_ID()] = operator_action #store into local
            
            #syncs db5 with local dict
            #syncs db5 count with local count (aka customer class)
            db5['operatoractions'] = operatoractions_dict
            db5['operatoractionsCount'] = operatoractions.Operatoractions.count_ID
            db5.close()

            #make changes to affected listing
            listing = listings_dict.get(int(restore_listing.id.data))
            listing.set_status("available")
            print(listing.get_status())
            db2['Listings'] = listings_dict
            return(redirect(url_for('operatorviewprofile', id=id)))   
    #suspend user func
    if request.method == 'POST' and suspend_user.validate():
        if suspend_user.password.data == "sysadmin1":
            #create operator action object
            operator_action = operatoractions.Operatoractions(id,suspend_user.typeofaction.data,suspend_user.category.data,suspend_user.suspend_text.data)
            operatoractions_dict[operator_action.get_ID()] = operator_action #store into local

            #syncs db5 with local dict
            #syncs db5 count with local count (aka customer class)
            db5['operatoractions'] = operatoractions_dict
            db5['operatoractionsCount'] = operatoractions.Operatoractions.count_ID
            db5.close()

            #make changes to affected user
            customer = customers_dict.get(id)
            customer.set_status("suspended")
            db1['Customers'] = customers_dict
            return(redirect(url_for('operatorviewprofile', id=id)))
    
    #terminate user func
    if request.method == 'POST' and terminate_user.validate():
        if terminate_user.password.data == "sysadmin1":
            #create operator action object
            operator_action = operatoractions.Operatoractions(id,terminate_user.typeofaction.data,terminate_user.category.data,terminate_user.terminate_text.data)
            operatoractions_dict[operator_action.get_ID()] = operator_action #store into local

            #syncs db5 with local dict
            #syncs db5 count with local count (aka customer class)
            db5['operatoractions'] = operatoractions_dict
            db5['operatoractionsCount'] = operatoractions.Operatoractions.count_ID
            db5.close()

            #make changes to affected user
            customer = customers_dict.get(id)
            customer.set_status("terminated")
            db1['Customers'] = customers_dict
            return(redirect(url_for('operatorviewprofile', id=id)))
        
    #restore user func
    if request.method == 'POST' and restore_user.validate():
        if restore_user.password.data == "sysadmin1":
            #create operator action object
            operator_action = operatoractions.Operatoractions(id,restore_user.typeofaction.data,"nil","nil")
            operatoractions_dict[operator_action.get_ID()] = operator_action #store into local

            #syncs db5 with local dict
            #syncs db5 count with local count (aka customer class)
            db5['operatoractions'] = operatoractions_dict
            db5['operatoractionsCount'] = operatoractions.Operatoractions.count_ID
            db5.close()

            #make changes to affected user
            customer = customers_dict.get(id)
            customer.set_status("active")
            db1['Customers'] = customers_dict
            return(redirect(url_for('operatorviewprofile', id=id)))
    
    return render_template('OperatorViewProfile.html', customer=customer,
                            listings_list = listing_list,terminate_user_form = terminate_user, suspend_user_form = suspend_user, restore_user_form = restore_user,disable_listing_form = disable_listing,restore_listing_form=restore_listing)

@app.route('/operatorviewprofilereviews/<int:id>',methods=['GET', 'POST'])
def operatorviewprofilereviews(id):
    db1 = shelve.open('customer.db','c')
    db5 = shelve.open('operatoractions.db','c')
    db3 = shelve.open('reviews.db', 'c')
    reviews_dict ={}
    customers_dict = {} #local one
    operatoractions_dict = {}
    terminate_user = OperatorTerminateUser(request.form,typeofaction='terminate user')
    suspend_user = OperatorSuspendUser(request.form,typeofaction='suspend user')
    restore_user = OperatorRestoreUser(request.form,typeofaction='report user')
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


    
    #suspend user func
    if request.method == 'POST' and suspend_user.validate():
        if suspend_user.password.data == "sysadmin1":
            #create operator action object
            operator_action = operatoractions.Operatoractions(id,suspend_user.typeofaction.data,suspend_user.category.data,suspend_user.suspend_text.data)
            operatoractions_dict[operator_action.get_ID()] = operator_action #store into local

            #syncs db5 with local dict
            #syncs db5 count with local count (aka customer class)
            db5['operatoractions'] = operatoractions_dict
            db5['operatoractionsCount'] = operatoractions.Operatoractions.count_ID
            db5.close()

            #make changes to affected user
            customer = customers_dict.get(id)
            customer.set_status("suspended")
            db1['Customers'] = customers_dict
            return(redirect(url_for('operatorviewprofile', id=id)))
        
    
    #terminate user func
    if request.method == 'POST' and terminate_user.validate():
        if terminate_user.password.data == "sysadmin1":
            #create operator action object
            operator_action = operatoractions.Operatoractions(id,terminate_user.typeofaction.data,terminate_user.category.data,terminate_user.terminate_text.data)
            operatoractions_dict[operator_action.get_ID()] = operator_action #store into local

            #syncs db5 with local dict
            #syncs db5 count with local count (aka customer class)
            db5['operatoractions'] = operatoractions_dict
            db5['operatoractionsCount'] = operatoractions.Operatoractions.count_ID
            db5.close()

            #make changes to affected user
            customer = customers_dict.get(id)
            customer.set_status("terminated")
            db1['Customers'] = customers_dict
            return(redirect(url_for('operatorviewprofile', id=id)))
    
        
    #restore user func
    if request.method == 'POST' and restore_user.validate():
        if restore_user.password.data == "sysadmin1":
            #create operator action object
            operator_action = operatoractions.Operatoractions(id,restore_user.typeofaction.data,"nil","nil")
            operatoractions_dict[operator_action.get_ID()] = operator_action #store into local

            #syncs db5 with local dict
            #syncs db5 count with local count (aka customer class)
            db5['operatoractions'] = operatoractions_dict
            db5['operatoractionsCount'] = operatoractions.Operatoractions.count_ID
            db5.close()

            #make changes to affected user
            customer = customers_dict.get(id)
            customer.set_status("active")
            db1['Customers'] = customers_dict
            return(redirect(url_for('operatorviewprofile', id=id)))
    

    return render_template("OperatorViewProfile_reviews.html",customer = customer ,number_of_reviews = len(customer_reviews_list),list_reviews = customer_reviews_list,terminate_user_form = terminate_user, suspend_user_form = suspend_user, restore_user_form = restore_user)

@app.route('/dashboard/listings',methods=['GET', 'POST'])
def dashboardlistings():
    listing_search_field = SearchListingField(request.form)
    db2 = shelve.open('listing.db','c')
    listings_dict = {}

    try:
        if "Listings" in db2:
            listings_dict = db2["Listings"] #sync local with db2
        else:
            db2['Listings'] = listings_dict #sync db2 with local (basically null)
    except:
            print("Error in opening listings.db")
    listings_list = []
    for key in listings_dict:
        listing = listings_dict.get(key)
        listings_list.append(listing)

    if request.method == 'POST' and listing_search_field.validate():
        return redirect(url_for('dashboardlistingssearch',keyword = listing_search_field.searchfield.data))
    
    return render_template('Operatordashboard_listings.html',form = listing_search_field,listings_list = listings_list)

@app.route('/dashboard/listings/search=<keyword>',methods=['GET', 'POST'])
def dashboardlistingssearch(keyword):
    listing_search_field = SearchListingField(request.form)
    db2 = shelve.open('listing.db','c')
    listings_dict = {}

    try:
        if "Listings" in db2:
            listings_dict = db2["Listings"] #sync local with db2
        else:
            db2['Listings'] = listings_dict #sync db2 with local (basically null)
    except:
            print("Error in opening listings.db")
    listings_list = []        
    for key in listings_dict:
        listing = listings_dict.get(key)
        if keyword in listing.get_title():
            listings_list.append(listing)
        else:
            pass

    if request.method == 'POST' and listing_search_field.validate():
        return redirect(url_for('dashboardlistingssearch',keyword = listing_search_field.searchfield.data))
    
    return render_template('Operatordashboard_listings_search.html',form = listing_search_field,listings_list = listings_list)

@app.route('/operatorviewlisting/<int:id>',)
def operatorviewlisting(id):
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
    
    listing = listings_dict.get(id)
    for key in customers_dict:
        if key == listing.get_creatorID():
            seller = customers_dict.get(key)
            break
    
    return render_template('OperatorViewListing.html', listing = listing,seller = seller, current_sessionID = session_ID)
    
@app.route('/dashboard/reports',methods=['GET', 'POST'])
def dashboardreports():
    db4 =shelve.open('reports.db','c')
    reports_dict = {}
    report_search_field = SearchReportField(request.form)
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
        print("Error in retrieving data from DB4 Report count or count is at 0")

    reports_list = []
    for key in reports_dict:
        report = reports_dict.get(key)
        reports_list.append(report)
    try:
        if request.method == 'POST' and report_search_field.validate():
            return redirect(url_for('dashboardreportssearch',keyword = report_search_field.searchfield.data))
    except:
        pass
    return render_template("Operatordashboard_reports.html",reports_list=reports_list,form =report_search_field)

@app.route('/dashboard/reports/search=<keyword>',methods=['GET', 'POST'])
def dashboardreportssearch(keyword):
    db4 =shelve.open('reports.db','c')
    reports_dict = {}
    report_search_field = SearchReportField(request.form)
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
        print("Error in retrieving data from DB4 Report count or count is at 0")

    reports_list = []
    for key in reports_dict:
        report = reports_dict.get(key)
        if keyword in report.get_offender_username():
            reports_list.append(report)
    
    try:
        if request.method == 'POST' and report_search_field.validate():
            return redirect(url_for('dashboardreportssearch',keyword = report_search_field.searchfield.data))
    except:
        pass
    return render_template('Operatordashboard_reports_search.html',reports_list=reports_list,form=report_search_field)

@app.route('/dashboard/operatoractions',methods=['GET', 'POST'])
def dashboardoperatoractions():
    db5 = shelve.open('operatoractions.db','c')
    operatoractions_dict = {}
    operatoraction_search_field = SearchOperatorActionField(request.form)
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
    operator_actions_list = []
    for key in operatoractions_dict:
        operatoraction = operatoractions_dict.get(key)
        operator_actions_list.append(operatoraction)
    try:
        if request.method == 'POST' and operatoraction_search_field.validate():
            return redirect(url_for('dashboardoperatoractionssearch',keyword = operatoraction_search_field.searchfield.data))
    except:
        pass
    return render_template('Operatordashboard_operatoraction.html',form = operatoraction_search_field,operator_actions_list=operator_actions_list)

@app.route('/dashboard/operatoractions/search=<keyword>',methods=['GET', 'POST'])
def dashboardoperatoractionssearch(keyword):
    db5 = shelve.open('operatoractions.db','c')
    operatoractions_dict = {}
    operatoraction_search_field = SearchOperatorActionField(request.form)
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

    operator_actions_list = []
    for key in operatoractions_dict:
        operatoraction = operatoractions_dict.get(key)
        if operatoraction.get_category() == keyword:
            operator_actions_list.append(operatoraction)
    try:
        if request.method == 'POST' and operatoraction_search_field.validate():
            return redirect(url_for('dashboardoperatoractionssearch',keyword = operatoraction_search_field.searchfield.data))
    except:
        pass
    
    return render_template('Operatordashboard_operatoraction_search.html',form = operatoraction_search_field,operator_actions_list=operator_actions_list)

@app.route('/dashboard/feedbacks')
def dashboardfeedbacks():
    feedbacks_dict = {}
    db7 = shelve.open('feedback.db','c')
    try:
        if "Feedback" in db7:
            feedbacks_dict = db7["Feedback"] #sync local with db1
        else:
            db7['Feedback'] = feedbacks_dict #sync db1 with local (basically null)
    except:
        print("Error in opening feedback.db")
    feedbacks_list=[]
    for key in feedbacks_dict:
        feedback = feedbacks_dict.get(key)
        feedbacks_list.append(feedback)
    
    return render_template("Operatordashboard_feedback.html",feedbacks_list=feedbacks_list)
if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()
