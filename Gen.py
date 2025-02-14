import shelve
import Customer, Feedback,Listing,Operatorstats,Report,Reviews,Delivery
import random
import string
from datetime import timedelta, datetime
global_customer_GenID_list = []
#PS:
# - genuser before genlisting
# - all functions are meant to be ran only ONCE
# - error prevention has not been implemented for the functions
# - for some reason i cant retreive Customer_GenID on my listing function, i have tried multiple times but it does not work
# - hence to get this thing running ill be using the global list instead as a quick patch
# generate date func
def generate_random_dates(start_date, end_date, k):
    random_dates = []
    date_range = end_date - start_date
    for i in range(k):
        random_days = random.randint(0, date_range.days)
        random_date = start_date + timedelta(days=random_days)
        random_dates.append(random_date)
    return random_dates



#Generate users
#Options
#
#0 - only user 
#1 - review
#2 - report
#3 - feedback
# reportcount = no. of reports
# reviewcount = no. of reviews
# all var with "gen" is specifically for this and logging purposes
# opstats doesnt work as it does not exist  (yet)
def genuser(options,count,reportcount,reviewcount,feedbackcount):
    dbmain = shelve.open('main.db','c')
    customers_dict = {}
    #ONLY IN GEN USER:
    customers_username_list = []
    customers_email_list = []
    customers_Genpassword_list = []
    customers_GenID_list = []
    customer_Genusername_list = []
    customers_Genemail_list = []
    gen_count = 0
    #Get dbs
    try:
        if "Customers" in dbmain:
            customers_dict = dbmain["Customers"] 
        else:
            dbmain['Customers'] = customers_dict 
    except:
        print("Error in opening main.db")

    try:
        if "Customer_usernames" in dbmain:
            customers_username_list = dbmain["Customer_usernames"]
        else:
            dbmain['Customer_usernames'] = customers_username_list
    except:
        print("Error in opening main.db")


    try:
        if "Customer_emails" in dbmain:
            customers_email_list = dbmain["Customer_emails"]
        else:
            dbmain['Customer_emails'] = customers_email_list
    except:
        print("Error in opening main.db")
    #sync IDs
    try:
        dbmain = shelve.open('main.db','c')    
        Customer.Customer.count_id = dbmain["CustomerCount"]
    except:
        print("Error in retrieving data from DB main Customer count or count is at 0")
    
    
    i = 0
    gen_count = 0
    #gen option 0 
    #skip checking if username already exists as in theory there should be no duplicates
    if options >= 0:
        while i != (count):
            #email
            randomemailnumber = random.randrange(10000,99999)
            randomemailalphabet = chr(random.randint(ord('A'), ord('Z')))
            assigned_email = f"{randomemailnumber}{randomemailalphabet}@gmymail.nyp.edu.sg" #PS THIS EMAIL DOES NOT EXIST
            #username
            usernamepool = ['Timothy','John','Timmy','jake','binli','batman']
            assigned_username = f'{random.choice(usernamepool)}{randomemailnumber}'
            
            #password
            assigned_password = f"{randomemailnumber}{randomemailalphabet}"
            generated_customer = Customer.Customer(assigned_username,assigned_email,assigned_password)
            customers_dict[generated_customer.get_id()] = generated_customer
            dbmain['Customers'] = customers_dict
            dbmain['CustomerCount'] = Customer.Customer.count_id
            #update opstats
            try:
                Operatorstats.operatorstats_users("total","plus")
                Operatorstats.operatorstats_users("active","plus")
            except:
                print("Error! Operator stats did not update")
            #save em
            customers_Genemail_list.append(str(generated_customer.get_email()))
            customers_Genpassword_list.append(str(generated_customer.get_password()))
            customers_GenID_list.append(int(generated_customer.get_id()))
            customer_Genusername_list.append(generated_customer.get_username())
            dbmain['Customer_usernames'] = customers_username_list
            dbmain['Customer_emails'] = customers_email_list
            print(customers_GenID_list)
            dbmain['Customer_GenID'] = customers_GenID_list
            #increment
            gen_count +=1
            i +=1
            
        #Print out generated users
        #retrieve from DB
        #
        print(f"GEN user count is {gen_count}")
        print(f"ID|USERNAME|EMAIL|PASSWORD")
        i = 1
        c = 0
        customers_dict = {}
        try:
            if "Customers" in dbmain:
                customers_dict = dbmain["Customers"] 
            else:
                dbmain['Customers'] = customers_dict 
        except:
            print("Error in opening main.db")
        #prints out all
        while i != (int(gen_count+1)):
            selected_username = customer_Genusername_list[c]
            #find the obj via name
            for key in customers_dict:
                customer = customers_dict.get(key)
                if customer.get_username() == selected_username:
                    id = customer.get_id()

            selected_customer = customers_dict.get(id)
            
            print(f"{selected_customer.get_id()}|{customer_Genusername_list[c]}|{customers_Genemail_list[c]}|{customers_Genpassword_list[c]}")
            #increment i 
            c+=1
            i+=1
    
    #trigger review func
    if options >=1:
        #Variables
        i = 0 
        gen_review_count = 0
        #RE init this variable just to be safe
        customers_GenID_list = []
        customers_dict = {}
        reviews_dict ={}
        review_GencreatorID_list = []
        reviews_Gencreatorusername_list = []
        reviews_Genrating_list = []
        reviews_Gencomment_list = []
        reviews_Genreceiverusername_list = []
        #retrieve ID list
        try:
            if "Customer_GenID" in dbmain:
                customers_GenID_list = dbmain["Customer_GenID"]
            else:
                dbmain['Customer_GenID'] = customers_GenID_list
        except:
            print("!!Error in opening main.db")
        #Retrive customer obj
        try:
            if "Customers" in dbmain:
                customers_dict = dbmain["Customers"] 
            else:
                dbmain['Customers'] = customers_dict 
        except:
            print("Error in opening main.db")
        #sync IDs
        #retreive review obj
        try:
            if "Reviews" in dbmain:
                reviews_dict = dbmain["Reviews"]
            else:
                dbmain['Reviews'] = reviews_dict
        except:
            print("Error in opening main.db")
        try:
            dbmain = shelve.open('main.db','c')    
            Reviews.Reviews.count_ID = dbmain["ReviewsCount"] #sync count between local and db1
        except:
            print("Error in retrieving data from DB main Review count or count is at 0")

        #PS if there's an error here, i blame DB retriveal
        while i != reviewcount+1:
            
            #local vars
            useridlist = customers_GenID_list.copy()
            #select creatorID
            generated_creatorID = int(random.choice(useridlist))
            generated_creator = customers_dict.get(generated_creatorID)
            generated_creatorUsername = generated_creator.get_username()
            #remove ID from list to prevent user reviewing themselves
            useridlist.remove(generated_creatorID)
            #get rating
            generated_rating = random.randrange(1,5)
            #get comment 
            
            generated_comment = "review is here"
            #create review obj + save to db
            review = Reviews.Reviews(generated_creatorID,generated_creatorUsername,generated_rating,generated_comment)
            reviews_dict[review.get_ID()] = review
            dbmain['Reviews'] = reviews_dict
            dbmain['ReviewsCount'] = Reviews.Reviews.count_ID
            #get reivew ID temp code
            review_GencreatorID_list.append(int(review.get_creator_ID()))
            reviews_Gencreatorusername_list.append(str(review.get_creator_username()))
            reviews_Genrating_list.append(int(review.get_rating()))
            reviews_Gencomment_list.append(str(review.get_comment()))
            #assign review obj to someone 
            
            #select someone
            generated_receiverID = int(random.choice(useridlist))
            generated_receiver = customers_dict.get(generated_receiverID)
            generated_receiver.add_reviews(review.get_ID())
            generated_receiver.set_rating(float(review.get_rating()))
            reviews_Genreceiverusername_list.append(generated_receiver.get_username())
            dbmain['Customers'] = customers_dict
            print(f"Line end  {customers_GenID_list}")
            #increment variables
            i +=1
            gen_review_count +=1

        #Print out generated reviews
        #retrieve from DB
        print(f"GEN review count is {gen_review_count} ")
        print(f"REVIEWID|REVIEWCREATORID|REVIEWCREATORUSERNAME|RATING|COMMENT")
        i = 1
        c = 0
        reviews_dict={}
        #retreive review obj
        try:
            if "Reviews" in dbmain:
                reviews_dict = dbmain["Reviews"]
            else:
                dbmain['Reviews'] = reviews_dict
        except:
            print("Error in opening main.db")
        while i != (int(gen_review_count)):
            selected_review = reviews_dict.get(int(i))
            print(f"{selected_review.get_ID()}|{review_GencreatorID_list[c]}|{reviews_Gencreatorusername_list[c]}|{reviews_Genrating_list[c]}|{reviews_Gencomment_list[c]}")
            #increment i 
            i +=1
            c+=1
    
    #trigger report func
    if options >= 2:
        dbmain = shelve.open('main.db','c')
        #variables
        i = 0
        gen_report_count = 0 
        #RE init this variable just to be safe
        customers_GenID_list = []
        reports_GencreatorID_list = []
        reports_GenoffenderID_list = []
        reports_Genoffenderusername_list = []
        reports_Gencategory_list = []
        reports_Gencomment_list = []
        customers_dict = {}
        reports_dict ={}
        #retrieve ID list
        try:
            if "Customer_GenID" in dbmain:
                customers_GenID_list = dbmain["Customer_GenID"]
            else:
                dbmain['Customer_GenID'] = customers_GenID_list
        except:
            print("!!Error in opening main.db")
        #Retrive customer obj
        try:
            if "Customers" in dbmain:
                customers_dict = dbmain["Customers"] 
            else:
                dbmain['Customers'] = customers_dict 
        except:
            print("Error in opening main.db")
        try:
            if "Reports" in dbmain:
                reports_dict = dbmain["Reports"] #sync local with db2
            else:
                dbmain['Reports'] = reports_dict #sync db2 with local (basically null)
        except:
                print("Error in opening main.db")
        #sync report IDs
        try:
            dbmain = shelve.open('main.db','c')    
            Report.Report.count_ID = dbmain["ReportsCount"] #sync count between local and db1
        except:
            print("Error in retrieving data from DB main Report count or count is at 0")
        try:

            while i != reportcount+1:
                #localvars
                useridlist = customers_GenID_list.copy()
                #select creatorID
                generated_creatorID = int(random.choice(useridlist))
                #remove ID from list to prevent user reviewing themselves
                useridlist.remove(generated_creatorID)
                #select category
                categorylist = ['Phishing','Scamming','Suspicious account','Offering prohibited items',]
                generated_category = str(random.choice(categorylist))
                #generate comment
                generated_comment = 'report here'

                #offender
                generated_offenderID = int(random.choice(useridlist))
                generated_offender = customers_dict.get(generated_offenderID)
                print(generated_offenderID)
                generated_offender_username = generated_offender.get_username()

                #create report obj
                generated_report = Report.Report(generated_creatorID,generated_offenderID,generated_offender_username,generated_category,generated_comment)
                reports_dict[generated_report.get_ID()] = generated_report #store obj in dict
                dbmain['Reports'] = reports_dict
                dbmain['ReportsCount'] = Report.Report.count_ID
                generated_offender.add_reports(generated_report.get_ID())
                dbmain['Customers'] = customers_dict
                #add to local var
                reports_GencreatorID_list.append(int(generated_creatorID))
                reports_GenoffenderID_list.append(int(generated_offenderID))
                reports_Genoffenderusername_list.append(str(generated_offender_username))
                reports_Gencategory_list.append(str(generated_category))
                reports_Gencomment_list.append(str(generated_comment))
                
                #increment variables
                i +=1
                gen_report_count +=1
        except:
            print("Unknown error occured when generating report")

        print(f"GEN report count is {gen_report_count} ")
        print("ID|CREATORID|OFFENDERID|OFFENDERUSERNAME|CATEGORY|COMMENT")
        i = 1
        c = 0
        reports_dict = {}
        try:
            if "Reports" in dbmain:
                reports_dict = dbmain["Reports"] #sync local with db2
            else:
                dbmain['Reports'] = reports_dict #sync db2 with local (basically null)
        except:
                print("Error in opening main.db")
        #retrieve report obj
        while i != (int(gen_report_count+1)):
            selected_report = reports_dict.get(int(i))
            print(f"{selected_report.get_ID()}|{reports_GencreatorID_list[c]}|{reports_GenoffenderID_list[c]}|{reports_Genoffenderusername_list[c]}|{reports_Gencategory_list[c]}|{reports_Gencomment_list[c]}")
            #increment i 
            i +=1
            c+=1
    print(f"Option 2 {customers_GenID_list}")
    #trigger feedback func
    if options >= 3:
        
        dbmain  = shelve.open('main.db','c')
        #variables
        i = 0
          
        feedbacks_dict = {}
        customers_dict = {}
        feedbacks_rating_list = []
        feedbacks_feedback_list = []
        feedbacks_creatorusername_list = []
        #RE init this variable just to be safe
        #Retrive customer obj
        try:
            if "Customers" in dbmain:
                customers_dict = dbmain["Customers"] 
            else:
                dbmain['Customers'] = customers_dict

        except:
            print("Error in opening main.db")
        try:
            if "Feedback" in dbmain:
                feedbacks_dict = dbmain["Feedback"] #sync local with db1
            else:
                dbmain['Feedback'] = feedbacks_dict #sync db1 with local (basically null)
        except:
            print("Error in opening main.db")
        #sync IDs
        try:
            dbmain = shelve.open('main.db','c')    
            Feedback.Feedback.count_ID = dbmain["FeedbackCount"] #sync count between local and db1
        except:
            print("Error in retrieving data from DB main Feedback count or count is at 0")
        gen_feedback_count = 0 
        try:
            while i != (feedbackcount+1):
                #local var
                useridlist = customers_GenID_list.copy()
                #select creatorID
                generated_creatorID = int(random.choice(useridlist))
                #select rating
                generated_rating = random.randrange(1,5)
                #get remark
                remark = 'remark here'

                #create feedback obj
                generated_feedback = Feedback.Feedback(generated_rating,remark)
                feedbacks_dict[generated_feedback.get_ID()] = generated_feedback #store obj in dict
                dbmain['Feedback'] = feedbacks_dict
                dbmain['FeedbackCount'] = Feedback.Feedback.count_ID
                #assign to creator
                generated_creator = customers_dict.get(generated_creatorID)
                generated_creator.add_feedback(generated_feedback.get_ID())
                dbmain['Customers'] = customers_dict
                    
                gen_feedback_count +=1
                    
                #local var
                feedbacks_rating_list.append(int(generated_rating))
                feedbacks_feedback_list.append(str(generated_feedback))
                feedbacks_creatorusername_list.append(str(generated_creator))

                #increment
                    
                i+=1
        except:
            print("Error occured when generating feedback")
        
        #display feedback
        print("ID|RATING|FEEDBACK")
        i = 1
        feedbacks_dict = {}
        try:
            if "Feedback" in dbmain:
                feedbacks_dict = dbmain["Feedback"] #sync local with db1
            else:
                dbmain['Feedback'] = feedbacks_dict #sync db1 with local (basically null)
        except:
            print("Error in opening main.db")
        #sync IDs
        try:
            dbmain = shelve.open('main.db','c')    
            Feedback.Feedback.count_ID = dbmain["FeedbackCount"] #sync count between local and db1
        except:
            print("Error in retrieving data from DB main Feedback count or count is at 0")
        while i != (int(Feedback.Feedback.count_ID+1)):
            selected_feedback = feedbacks_dict.get(int(i))
            print(f"{selected_feedback.get_ID()}|{selected_feedback.get_rating()}|{selected_feedback.get_remark()}")
            #increment i 
            i +=1
    global global_customer_GenID_list
    global_customer_GenID_list = customers_GenID_list.copy()
    print(f"User gen list {customers_GenID_list}")
    print("User Generation ended.")


#Generate listings

#NEW OPTIONS
# 0 - create available listings
# 1 - create meetup listings with reserved status
# 2 - create delivery listings with sold status
# 3 - create disabled listings
# listingcount - number of listings
# meetupcount - number of meetup listings
# deliverycount - number of delivery listings
def genlisting(options,listingcount,meetupcount,deliverycount,disabledcount):
    dbmain = shelve.open('main.db','c')
    customers_dict = {}
    listings_dict = {}
    #Var
    global global_customer_GenID_list
    customers_GenID_list = global_customer_GenID_list
    listings_GenID_list = []
    #Gen var
    listings_GencreatorID_list = []
    listings_Gencreatorusername_list = []
    listings_Gentitle_list = []
    listings_Gendesc_list = []
    listings_Gencondition_list = []
    listings_Gencategory_list = []
    listings_GencreationDate_list= []
    listings_Genstatus_list = []
    #temp var
    listings_tempGenID_list = []
    #Get dbs
    try:
        if "Customers" in dbmain:
            customers_dict = dbmain["Customers"] 
        else:
            dbmain['Customers'] = customers_dict 
    except:
        print("Error in opening main.db")
    
    try:
        if "Listings" in dbmain:
            listings_dict = dbmain["Listings"]
        else:
            dbmain["Listings"] = listings_dict
    except:
        print("Error in opening Listings data.")
    #sync listing IDs
    try:
        dbmain = shelve.open('main.db','c')    
        Listing.Listing.count_ID = dbmain["ListingsCount"] #sync count between local and db1
    except:
        print("Error in retrieving data from DB main Listing count or count is at 0")
    try:
        if "Listings_GenID" in dbmain:
            listings_GenID_list = dbmain["Listings_GenID"]
        else:
            dbmain['Listings_GenID'] = listings_GenID_list
    except:
        print("Error in opening main.db")   
    
    i = 0
    gen_listings_count = 0
    
    print(F"from listing gen {customers_GenID_list}")
    #TODO ADD AVAIL STATUS
    if options >= 0:
        while i != (listingcount):
            useridlist = customers_GenID_list.copy()
            #get creator ID
            generated_creatorID = random.choice(useridlist)
            #get creator username
            generated_creatorusername = (customers_dict.get(generated_creatorID).get_username())

            #get title,desc,category
            categorylist = ['Category 1','Category 2','Category 3','Category 4','Category 5']
            generated_category = random.choice(categorylist)
            #code to assign suitable title + desc for own category
            if generated_category == 'Category 1':
                titlelist = ['Airpods','Nintendo Switch', 'USB C cable','iphone 14']
                desclist = ['looking to give away','stopped using it','do not really want it']
                generated_title = random.choice(titlelist)
                generated_desc = random.choice(desclist)
            elif generated_category == 'Category 2':
                titlelist = ['Book']
                desclist = ['looking to give away','stopped using it','do not really want it']
                generated_title = random.choice(titlelist)
                generated_desc = random.choice(desclist)
            elif generated_category == 'Category 3':
                titlelist = ['shirt','pants','dress','mini skirt']
                desclist = ['still in packaging', 'outgrown it']
                generated_title = random.choice(titlelist)
                generated_desc = random.choice(desclist)
            elif generated_category == 'Category 4':
                titlelist = ['monopoly','game of life']
                desclist = ['got bored of it', 'stopped playing it']
                generated_title = random.choice(titlelist)
                generated_desc = random.choice(desclist)
            elif generated_category == 'Category 5':
                titlelist = ['apple pie' , 'Pokemon cards' ]
                desclist = ['i dont want it']
                generated_title = random.choice(titlelist)
                generated_desc = random.choice(desclist)
            else:
                print('Error! invalid category was selected terminating process')
                break
            #condition 
            condition_list = ['Barely used','Frequently used','Worn out']
            generated_condition = random.choice(condition_list)
            #get creation date
            start_date = datetime(2024, 2, 1)
            end_date = datetime(2024, 2, 10)
            random_date = generate_random_dates(start_date,end_date,1)
            for index, date in enumerate(random_date):
                generated_creationdate = (f"{date.strftime('%d/%m/%y')}")
            
            #create listing obj
            generated_listing = Listing.Listing(generated_creatorID,generated_creatorusername,generated_title,generated_desc,generated_condition,generated_category,generated_creationdate)
            listings_dict[generated_listing.get_ID()] = generated_listing
            print(generated_listing.get_ID())
            #set status
            generated_listing.set_status('available')
            dbmain['Listings'] = listings_dict
            dbmain['ListingsCount'] = Listing.Listing.count_ID
            #store in temp var
            listings_tempGenID_list.append(generated_listing.get_ID())
            #store in local var
            listings_GenID_list.append(generated_listing.get_ID())
            dbmain['Listings_GenID'] = listings_GenID_list
            listings_GencreatorID_list.append(generated_listing.get_creatorID())
            listings_Gencreatorusername_list.append(generated_listing.get_creator_username())
            listings_Gentitle_list.append(generated_listing.get_title())
            listings_Gendesc_list.append(str(generated_listing.get_description()))
            listings_Gencondition_list.append(str(generated_listing.get_condition()))
            listings_Gencategory_list.append(str(generated_listing.get_category()))
            listings_GencreationDate_list.append(str(generated_listing.get_creation_date()))
            listings_Genstatus_list.append(str(generated_listing.get_status()))
            #increment var
            i +=1
            gen_listings_count +=1
        print("Listing generation ended.")
        #PRINT OUT GENERATED LISTINGS
        print(f"GEN listing count is {gen_listings_count}")
        print("ID|CREATORID|CREATORUSERNAME|TITLE|DESCRIPTION|CONDITION|CATEGORY|CREATIONDATE|STATUS")
        i = 1
        c = 0
        listings_dict = {}
        try:
            if "Listings" in dbmain:
                listings_dict = dbmain["Listings"]
            else:
                dbmain["Listings"] = listings_dict
        except:
            print("Error in opening Listings data.")
        
        while i !=(int(gen_listings_count+1)):
            

            print(f"{listings_tempGenID_list[c]}|{listings_GencreatorID_list[c]}|{listings_Gencreatorusername_list[c]}|{listings_Gentitle_list[c]}|{listings_Gendesc_list[c]}|{listings_Gencondition_list[c]}|{listings_Gencategory_list[c]}|{listings_GencreationDate_list[c]}|{listings_Genstatus_list[c]}")

            #increment
            i +=1
            c +=1

    #change to meetup
    if options >= 1:
        #Vars
        listings_GenID_list = []
        listings_dict = {}
        gen_listings_meetup_count = 0
        #TO display
        listings_Gentitle_list = []
        listings_Gendealmethod_list = []
        listings_Genstatus_list = []
        #temp var
        listings_tempGenID_list = []
        
        try:
            if "Listings_GenID" in dbmain:
                listings_GenID_list = dbmain["Listings_GenID"]
            else:
                dbmain['Listings_GenID'] = listings_GenID_list
        except:
            print("Error in opening main.db")
        #VERY IMPT TO ENSURE NO OVERRIDES:
        try:
            if "Listings_GenID_status" in dbmain:
                listings_GenID_status_list = dbmain["Listings_GenID"]
            else:
                dbmain['Listings_GenID_status'] = listings_GenID_status_list
        except:
            print("Error in opening main.db")
        try:
            if "Listings" in dbmain:
                listings_dict = dbmain["Listings"]
            else:
                dbmain["Listings"] = listings_dict
        except:
            print("Error in opening Listings data.")   
        i = 0
        #NOTE THIS LINE OF CODE ONLY SHLD BE HERE ONCE:
        listings_GenID_status_list = listings_GenID_list.copy()
        while i != (int(meetupcount)):
            #select a random listing ID
            selectedid = random.choice(listings_GenID_status_list)
            #rmbr remove it - needed for option 2 to prevent overrides
            listings_GenID_status_list.remove(selectedid)
            #get listing obj
            selectedlisting = listings_dict.get(selectedid)
            #change its status
            selectedlisting.set_status("reserved")
            #change deal method
            selectedlisting.set_deal_method('meetup')
            #save to temp var
            listings_tempGenID_list.append(selectedlisting.get_ID())
            listings_Gentitle_list.append(selectedlisting.get_title())
            listings_Gendealmethod_list.append(selectedlisting.get_deal_method())
            listings_Genstatus_list.append(selectedlisting.get_status())
            #save it to db
            dbmain['Listings'] = listings_dict
            dbmain['Listings_GenID_status'] = listings_GenID_status_list
            #increment var
            i +=1
            gen_listings_meetup_count +=1
        
        print(F"Finished generating meetup only listings")
        print(f"GEN listings meetup is {gen_listings_meetup_count}")
        print(f"AFFECTEDID|TITLE|STATUS|DEALMETHOD")
        i = 1
        c = 0
        listings_dict = {}
        try:
            if "Listings" in dbmain:
                listings_dict = dbmain["Listings"]
            else:
                dbmain["Listings"] = listings_dict
        except:
            print("Error in opening Listings data.")
        while i != int(gen_listings_meetup_count+1):
            
            selected_listing = listings_dict.get(int(listings_tempGenID_list[c]))
            print(f"{selected_listing.get_ID()}|{listings_Gentitle_list[c]}|{listings_Genstatus_list[c]}|{listings_Gendealmethod_list[c]}|")
            #increment
            i +=1
            c +=1

    #change to delivery
    if options >= 2:
        #Vars
        listings_GenID_list = []
        listings_dict = {}
        gen_listings_delivery_count = 0
        #TO display
        listings_Gentitle_list = []
        listings_Gendealmethod_list = []
        listings_Genstatus_list = []
        #temp var
        listings_tempGenID_list = []
        listings_GenID_status_list = []
        #for delivery obj later on
        delivery_listingsID_list = []
        delivery_listingstitle_list = []
        try:
            if "Listings_GenID" in dbmain:
                listings_GenID_list = dbmain["Listings_GenID"]
            else:
                dbmain['Listings_GenID'] = listings_GenID_list
        except:
            print("Error in opening main.db")
        #VERY IMPT TO ENSURE NO OVERRIDES:
        try:
            if "Listings_GenID_status" in dbmain:
                listings_GenID_status_list = dbmain["Listings_GenID_status"]
            else:
                dbmain['Listings_GenID_status'] = listings_GenID_status_list
        except:
            print("Error in opening main.db")
        #VERY IMPT 
        try:
            if "delivery_listingsID" in dbmain:
                delivery_listingsID_list = dbmain["delivery_listingsID"]
            else:
                dbmain['delivery_listingsID'] = delivery_listingsID_list
        except:
            print("Error in opening main.db")
        #VERY IMPT 
        try:
            if "delivery_listingstitle" in dbmain:
                delivery_listingstitle_list = dbmain["delivery_listingstitle"]
            else:
                dbmain['delivery_listingstitle'] = delivery_listingstitle_list
        except:
            print("Error in opening main.db")
        try:
            if "Listings" in dbmain:
                listings_dict = dbmain["Listings"]
            else:
                dbmain["Listings"] = listings_dict
        except:
            print("Error in opening Listings data.")   
        #sync listing IDs
        try:
            dbmain = shelve.open('main.db','c')    
            Listing.Listing.count_ID = dbmain["ListingsCount"] #sync count between local and db1
        except:
            print("Error in retrieving data from DB main Listing count or count is at 0")
        i = 0
        while i != (int(deliverycount)):
            #select a random listing ID
            selectedid = random.choice(listings_GenID_status_list)
            #rmbr remove it - needed for option 2 to prevent overrides
            listings_GenID_status_list.remove(selectedid)
            #get listing obj
            selectedlisting = listings_dict.get(selectedid)
            #change its status
            selectedlisting.set_status("sold")
            
            #change deal method
            selected_listing.set_deal_method('delivery')
            #save to temp var
            listings_tempGenID_list.append(selectedlisting.get_ID())
            listings_Gentitle_list.append(selectedlisting.get_title())
            listings_Gendealmethod_list.append(selected_listing.get_deal_method())
            listings_Genstatus_list.append(selected_listing.get_status())
            delivery_listingsID_list.append(selected_listing.get_ID())
            delivery_listingstitle_list.append(selected_listing.get_title())
            #save it to db
            dbmain['Listings'] = listings_dict
            dbmain['Listings_GenID_status'] = listings_GenID_status_list
            dbmain['delivery_listingsID'] = delivery_listingsID_list
            dbmain['delivery_listingstitle'] = delivery_listingstitle_list
            #increment var
            i +=1
            gen_listings_delivery_count +=1
        
        print(F"Finished generating delivery only listings")
        print(f"GEN listings reserved is {gen_listings_delivery_count}")
        print(f"AFFECTEDID|TITLE|STATUS|DEALMETHOD")
        i = 1
        c = 0
        listings_dict = {}
        try:
            if "Listings" in dbmain:
                listings_dict = dbmain["Listings"]
            else:
                dbmain["Listings"] = listings_dict
        except:
            print("Error in opening Listings data.")
        while i != int(gen_listings_delivery_count+1):
            
            selected_listing = listings_dict.get(int(listings_tempGenID_list[c]))
            print(f"{selected_listing.get_ID()}|{listings_Gentitle_list[c]}|{listings_Genstatus_list[c]}|{listings_Gendealmethod_list[c]}|")
            #increment
            i +=1
            c +=1
    
    #change to disabled
    if options >= 3:
        #Vars
        listings_GenID_list = []
        listings_dict = {}
        gen_listings_disabled_count = 0
        #TO display
        listings_Gentitle_list = []
        listings_Genstatus_list = []
        #temp var
        listings_tempGenID_list = []
        listings_GenID_status_list = []
        try:
            if "Listings_GenID" in dbmain:
                listings_GenID_list = dbmain["Listings_GenID"]
            else:
                dbmain['Listings_GenID'] = listings_GenID_list
        except:
            print("Error in opening main.db")
        #VERY IMPT TO ENSURE NO OVERRIDES:
        try:
            if "Listings_GenID_status" in dbmain:
                listings_GenID_status_list = dbmain["Listings_GenID_status"]
            else:
                dbmain['Listings_GenID_status'] = listings_GenID_status_list
        except:
            print("!!Error in opening main.db")
        try:
            if "Listings" in dbmain:
                listings_dict = dbmain["Listings"]
            else:
                dbmain["Listings"] = listings_dict
        except:
            print("Error in opening Listings data.")   
        #sync listing IDs
        try:
            dbmain = shelve.open('main.db','c')    
            Listing.Listing.count_ID = dbmain["ListingsCount"] #sync count between local and db1
        except:
            print("Error in retrieving data from DB main Listing count or count is at 0")

        i = 0
        while i != (int(disabledcount)):
            #select a random listing ID
            selectedid = random.choice(listings_GenID_status_list)
            #rmbr remove it - needed for option 2 to prevent overrides
            listings_GenID_status_list.remove(selectedid)
            #get listing obj
            selectedlisting = listings_dict.get(selectedid)
            #change its status
            selectedlisting.set_status("disabled")
            #save to temp var
            listings_tempGenID_list.append(selectedlisting.get_ID())
            listings_Gentitle_list.append(selectedlisting.get_title())
            listings_Genstatus_list.append(selectedlisting.get_status())
            #save it to db
            dbmain['Listings'] = listings_dict
            dbmain['Listings_GenID_status'] = listings_GenID_status_list
            #increment var
            i +=1
            gen_listings_disabled_count +=1

        print(F"Finished generating delivery only listings")
        print(f"GEN listings reserved is {gen_listings_disabled_count}")
        print(f"AFFECTEDID|TITLE|STATUS")
        i = 1
        c = 0
        listings_dict = {}
        try:
            if "Listings" in dbmain:
                listings_dict = dbmain["Listings"]
            else:
                dbmain["Listings"] = listings_dict
        except:
            print("Error in opening Listings data.")
        while i != int(gen_listings_delivery_count+1):
            
            selected_listing = listings_dict.get(int(listings_tempGenID_list[c]))
            print(f"{selected_listing.get_ID()}|{listings_Gentitle_list[c]}|{listings_Genstatus_list[c]}|")
            #increment
            i +=1
            c +=1
genuser(3,3,0,0,0)
genlisting(3,6,2,2,2)




