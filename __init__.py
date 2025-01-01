from flask import Flask, render_template, url_for,request,redirect
import os
import Customer , Listing, ListingImage,Reviews #classes
from Forms import CustomerSignupForm, CustomerLoginForm, ListingForm, uploadListingimg,ReviewForm #our forms
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
@app.route('/profile/<int:id>')
def Customerprofile(id):
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


    #code for profile pic img 
    pfpimg = os.path.join('..\static','profilepics')
    user_id = os.path.join(pfpimg,'hermos.jpg') 
    
    customer = customers_dict.get(id)
    customer_listings = customer.get_listings() #get ID list of current user listings
    print(f"\n*start of message *\nCurrent user has the following listings:{customer_listings}\n*end of message*")
    listing_list = []
    for key in listings_dict:
        print(key)
        if key in customer_listings:
            listing = listings_dict.get(key)
            listing_list.append(listing)
            break
    #test code for listing img
    listingimg = os.path.join('static','listingpic')
    return render_template('Customerprofile.html',customer_imgid = user_id, customer=customer,
                            current_sessionID = session_ID,listings_list = listing_list)

@app.route('/profilereviews/<int:id>')
def Customerprofile_reviews(id):
    global session_ID
    db1 = shelve.open('customer.db','c')
    customers_dict = {}
    reviews_dict ={}
    db3 = shelve.open('reviews.db', 'c')


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


    pfpimg = os.path.join('..\static', 'profilepics')
    user_id = os.path.join(pfpimg,'hermos.jpg') 
    
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
    
    #reviewer pfp
    reviewer_id = os.path.join(pfpimg,'hermos.jpg') 
    print(f"Reviews are {customer_reviews_list}")
    return render_template('Customerprofile_reviews.html',customer_imgid = user_id, customer = customer ,number_of_reviews = len(customer_reviews_list), list_reviews = customer_reviews_list, reviewer_imgid = reviewer_id, current_sessionID = session_ID)

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
        return redirect(url_for('Customerprofile', id=session_ID))# returns to YOUR profile
    return render_template('CustomerCreateListing.html', form = create_listing_form, form2 = create_listing_img_form, current_sessionID = session_ID)

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

    #determine if user already liked this post
    customer = customers_dict.get(session_ID) #current user
    customer_liked_posts = customer.get_liked_listings()
    user_liked_post = 'False'
    if listing.get_ID() in customer_liked_posts:
        print("User has already liked this post")
        user_liked_post = 'True'

    return render_template('CustomerViewListing.html', listing = listing,seller = seller, current_sessionID = session_ID, user_liked_post = user_liked_post)

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
    return redirect(url_for('Customerprofile', id=session_ID))

@app.route('/createReview/<int:id>', methods = ['GET', 'POST'])
def createReview(id):
    global session_ID
    review_form = ReviewForm(request.form)
    customers_dict = {}
    reviews_dict ={}
    db3 = shelve.open('reviews.db', 'c')
    db1 = shelve.open('customer.db','c')
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
    
    return render_template('CustomerReview.html',form=review_form, current_sessionID = session_ID)

@app.route('/createLikedListing/<int:id>')
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

@app.route('/createUnlikedListing/<int:id>')
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


@app.route('/viewLikedListings/<int:id>')
def viewLikedListings(id): #retrieve current session_ID
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

    customer = customers_dict.get(id) #current user
    customer_liked_listings = customer.get_liked_listings()
    listings_to_display = []
    for key in listings_dict:
        if key in customer_liked_listings:
            listing = listings_dict.get(key)
            listings_to_display.append(listing)
            
    return render_template('CustomerViewLikedListings.html', listings_to_display = listings_to_display, current_sessionID = session_ID)
if __name__ == "__main__":
    app.run()