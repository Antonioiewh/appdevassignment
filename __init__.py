from flask import Flask, render_template, url_for,request,redirect
import os
import Customer , Listing, ListingImage #classes
from Forms import CustomerSignupForm, CustomerLoginForm, ListingForm, uploadListingimg #our forms
import shelve, Customer
app = Flask(__name__)
#current_sessionID IS FOR THE PROFILE!!
#Current session ID
#MAKE SURE AN USER WITH ID "X" EXISTS!
session_ID = 0
@app.route('/') #shld be the same as href for buttons,links,navbar, etc...
def Customerhome():
    global session_ID

    return render_template('Customerhome.html', current_sessionID = session_ID)
@app.route('/profile')
def Customerprofile():
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


    #retrive data
    for key in customers_dict:
        if key == session_ID: 
            customer = customers_dict[key]
            current_username = customer.get_username()
            current_rating = customer.get_rating()
            current_date_joined = customer.get_date_joined()

    #code for profile pic img 
    pfpimg = os.path.join('static','profilepics')
    user_id = os.path.join(pfpimg,'hermos.jpg') 
    

    #test code for profile
    try:
        user_name = current_username
    except:
        user_name = "default"
    
    try:
        user_rating = current_rating
    except:
        user_rating = "N/A"
    
    try:
        user_date_joined = current_date_joined
    except:
        user_date_joined = "N/A"
    

    #find current session ID customer obj
    for key in customers_dict:
        if key == session_ID:
            customer = customers_dict[key]
            break #stop the for loop if this fulfills
    
    customer_listings = customer.get_listings() #get ID list of current user listings
    print(f"\n*start of message *\nCurrent user has the following listings:{customer_listings}\n*end of message*")
    listing_list = []
    for key in listings_dict:
        print(key)
        if key in customer_listings:
            listing = listings_dict.get(key)
            listing_list.append(listing)
    

    #test code for listing img
    listingimg = os.path.join('static','listingpic')
    listing_id = os.path.join(listingimg, 'pie.jpg')
    return render_template('Customerprofile.html',customer_imgid = user_id, customer_username = user_name, customer_rating = user_rating, customer_date_joined = user_date_joined,
                            current_sessionID = session_ID,listings_list = listing_list)

@app.route('/profilereviews')
def Customerprofile_reviews():
    global session_ID
     #code for profile pic img + listing pic img
    pfpimg = os.path.join('static', 'profilepics')

    #text here shld be name of img file + extension aka filetype (jpg,jpeg,png,etc.)
    #for the actual code just look repalce it with targeted user ID and etc.
    user_id = os.path.join(pfpimg,'hermos.jpg') 
    
    #test code for profile
    user_name = "hermos"
    user_rating = "4.5"
    user_date_joined = "567"

    #testcode for reviews
    reviewername = "hermos2" 
    reviews=["BRo sold me a gun","Sold me a cat"] #get reviews obj from current user (stored as list)
    number_of_reviews = len(reviews) #get NUMBER of reviews
    #reviewer pfp
    reviewer_id = os.path.join(pfpimg,'hermos.jpg') 

    return render_template('Customerprofile_reviews.html',customer_imgid = user_id, customer_username = user_name, customer_rating = user_rating, customer_date_joined = user_date_joined,
                           number_of_reviews = number_of_reviews, list_reviews = reviews, reviewer_username = reviewername, reviewer_imgid = reviewer_id,current_sessionID = session_ID)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    global session_ID
    create_customer_form = CustomerSignupForm(request.form)
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


        #verifies new user is stored
        customers_dict = db1['Customers'] #sync local dict with db1
        customer = customers_dict[customer.get_id()]
        print(f"\n*start of message\nRegistered sucess.\nId: {customer.get_id()}Username:{customer.get_username()}, Email:{customer.get_email()},Password:{customer.get_password()}\n Current session is {Customer.Customer.count_id}\n*end of message*")
        session_ID = Customer.Customer.count_id
        db1.close() #sync the count as it updated when creating the object, if you want to hard reset the count, add a line in customer class to hard reset it to 0 so when syncing, db's one becomes 0

        #misc code
        #This goes through the WHOLE DB AND PRINTS ALL NAMES
        #PS: COPY PASTE THIS CODE if using customer related functions
        return redirect(url_for('Customerhome'))
        
    return render_template("CustomerSignup.html",form=create_customer_form,current_sessionID = session_ID)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    global session_ID
    login_customer_form = CustomerLoginForm(request.form)
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
    

    return render_template("CustomerLogin.html",form=login_customer_form,current_sessionID = session_ID)


@app.route('/createlisting', methods = ['GET', 'POST'])
def createlisting():
    global session_ID
    db2 = shelve.open('listing.db','c') #RMBR THIS
    db1 = shelve.open('customer.db','c')
    listings_dict = {}
    customers_dict = {}
    create_listing_form = ListingForm(request.form)
    create_listing_img_form = uploadListingimg(request.form)

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
    if request.method == 'POST' and create_listing_form.validate and create_listing_img_form.validate():
        #print(create_listing_form.data)
        #print(create_listing_img_form.data)
        
        #create listing obj
        listing = Listing.Listing(session_ID,create_listing_form.title.data,create_listing_form.description.data,create_listing_form.condition.data,
                                  create_listing_form.category.data,create_listing_form.payment_method.data)
        #returns listings details
        print(f"Listing count:{Listing.Listing.count_ID}\nListing ID: {listing.get_ID()} \nListing creator ID:{listing.get_creatorID()}\nListing title: {listing.get_title()}\nListing Desc: {listing.get_description()}\nListing condition: {listing.get_condition()}\nListing category: {listing.get_category()}\nListing payment method: {listing.get_deal_method()}")
        #stores into db2
        listings_dict[listing.get_ID()] = listing
        db2['Listings'] = listings_dict
        db2['ListingsCount'] = Listing.Listing.count_ID #syncs with db2


        for key in customers_dict:
            if key == session_ID:
                customer = customers_dict[key]
                #add it to the user's listings
                customer.add_listings(Listing.Listing.count_ID)
                print(customer.get_listings())
                db1['Customers'] = customers_dict #syncs with db1
                break #stop the for loop if this fulfills

    return render_template('CustomerCreateListing.html', form = create_listing_form, form2 = create_listing_img_form)

@app.route('/updateListing/<int:id>/', methods=['GET', 'POST'])
def updateListing(id):
    global session_ID
    update_listing_form = ListingForm(request.form)
    update_listing_img_form = uploadListingimg(request.form)
    db2 = shelve.open('listing.db','c') #RMBR THIS
    listings_dict = {}
    try:
        if "Listings" in db2:
            listings_dict = db2["Listings"] #sync local with db2
        else:
            db2['Listings'] = listings_dict #sync db2 with local (basically null)
    except:
            print("Error in opening listings.db")
    if request.method == 'POST' and update_listing_form.validate and update_listing_img_form.validate():
        listing = listings_dict.get(id)
        listing.set_title(update_listing_form.title.data)
        listing.set_category(update_listing_form.category.data)
        listing.set_description(update_listing_form.description.data)
        listing.set_condition(update_listing_form.condition.data)
        listing.set_deal_method(update_listing_form.payment_method.data)
        db2['Listings'] = listings_dict #sync local to db2
        db2.close() 
        return redirect(url_for('Customerprofile')) #go back to profile page after submit

    return render_template('CustomerUpdateListing.html', form = update_listing_form, form2 = update_listing_img_form,current_sessionID = session_ID) #to render the form 

@app.route('/viewListing/<int:id>/')
def viewListing(id):
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

    listing = listings_dict.get(id)
    for key in customers_dict:
        if key == listing.get_creatorID():
            seller = customers_dict.get(key)
            break
    return render_template('CustomerViewListing.html', listing = listing,seller = seller, current_sessionID = session_ID)

@app.route('/deleteListing/<int:id>/')
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
    return redirect(url_for('Customerprofile'))
if __name__ == "__main__":
    app.run()