import shelve

class Operatorstats:
    count_ID = 0
    def __init__(self):
        Operatorstats.count_ID+=1
        self.__ID = Operatorstats.count_ID
        #users related
        self.__users_count = 0
        self.__users_active_count = 0
        self.__users_suspended_count = 0
        self.__users_terminated_count = 0
        #listings related
        self.__listings_count = 0
        self.__listings_available_count = 0
        self.__listings_disabled_count = 0
        self.__listings_reserved_count = 0
        self.__listings_sold_count = 0
        #feedback related
        self.__feedback_count = 0
        self.__feedback_replied_count = 0
        self.__feedback_unreplied_count = 0
        #transactions
        self.__transactions_count = 0
        self.__transactions_Pending_count = 0
        self.__transactions_In_Transit_count = 0
        self.__transactions_Delivered_count = 0
        self.__transactions_Cancelled_count = 0
        #reports
        self.__report_count = 0
        #opactions
        self.__opactions_count = 0

    #ID
    def get_ID(self):
        return self.__ID
    #user related
    def get_users_count(self):
        return self.__users_count 
    def get_users_active_count(self):
        return self.__users_active_count
    def get_users_suspended_count(self):
        return self.__users_suspended_count
    def get_users_terminated_count(self):
        return self.__users_terminated_count 
    

    #listings related
    def get_listings_count(self):
        return self.__listings_count
    def get_listings_available_count(self):
        return self.__listings_available_count
    def get_listings_disabled_count(self):
        return self.__listings_disabled_count
    def get_listings_reserved_count(self):
        return self.__listings_reserved_count
    def get_listings_sold_count(self):
        return self.__listings_sold_count

    #feedback related
    def get_feedback_count(self):
        return self.__feedback_count
    def get_feedback_replied_count(self):
        return self.__feedback_replied_count
    def get_feedback_unreplied_count(self):
        return self.__feedback_unreplied_count
    
    #transactions related (delivery status here too)
    def get_transactions_count(self):
        return self.__transactions_count
    def get_transactions_Pending_count(self):
        return self.__transactions_Pending_count
    def get_transactions_In_Transit_count(self):
        return self.__transactions_In_Transit_count
    def get_transactions_Delivered_count(self):
        return self.__transactions_Delivered_count
    def get_transactions_Cancelled_count(self):
        return self.__transactions_Cancelled_count 
    
    #reports related
    def get_reports_count(self):
        return self.__report_count
    
    #opactions
    def get_opactions_count(self):
        return self.__opactions_count
    #user related
    #amount add/minus is hardcoded
    def increase_user_count(self):
        self.__users_count +=1
    #decrease should never be used
    def decrease_user_count(self):
        self.__users_count -= 1
    
    def increase_user_active_count(self):
        self.__users_active_count +=1
    def decrease_user_active_count(self):
        self.__users_active_count -=1

    def increase_user_suspended_count(self):
        self.__users_suspended_count +=1
    def decrease_user_suspended_count(self):
        self.__users_suspended_count -=1

    def increase_user_terminated_count(self):
        self.__users_terminated_count +=1
    def decrease_user_terminated_count(self):
        self.__users_terminated_count -=1

    #listing related
    def increase_listing_count(self):
        self.__listings_count +=1
    def decrease_listing_count(self):
        self.__listings_count -=1

    def increase_listing_available_count(self):
        self.__listings_available_count +=1
    def decrease_listing_available_count(self):
        self.__listings_available_count -=1 

    def increase_listing_disabled_count(self):
        self.__listings_disabled_count +=1
    def decrease_listing_disabled_count(self):
        self.__listings_disabled_count -=1

    def increase_listing_reserved_count(self):
        self.__listings_reserved_count +=1
    def decrease_listing_reserved_count(self):
        self.__listings_reserved_count -=1

    def increase_listing_sold_count(self):
        self.__listings_sold_count +=1
    def decrease_listing_sold_count(self):
        self.__listings_sold_count -=1

    #feedback related
    def increase_feedback_count(self):
        self.__feedback_count +=1
    def decrease_feedback_count(self):
        self.__feedback_count -=1
    
    def increase_feedback_replied_count(self):
        self.__feedback_replied_count +=1
    def decrease_feedback_replied_count(self):
        self.__feedback_replied_count -=1

    def increase_feedback_unreplied_count(self):
        self.__feedback_unreplied_count +=1
    def decrease_feedback_unreplied_count(self):
        self.__feedback_unreplied_count -=1
    
    
    #transactions

    def increase_transactions_count(self):
        self.__transactions_count +=1
    def decrease_transactions_count(self):
        self.__transactions_count -=1
    
    def increase_transactions_Pending_count(self):
        self.__transactions_Pending_count +=1
    def decrease_transactions_Pending_count(self):
        self.__transactions_Pending_count -=1
    
    def increase_transactions_In_Transit_count(self):
        self.__transactions_In_Transit_count +=1
    def decrease_transactions_In_Transit_count(self):
        self.__transactions_In_Transit_count -=1
    
    def increase_transactions_Delivered_count(self):
        self.__transactions_Delivered_count +=1
    def decrease_transactions_Delivered_count(self):
        self.__transactions_Delivered_count -=1

    def increase_transactions_Cancelled_count(self):
        self.__transactions_Cancelled_count +=1
    def decrease_transactions_Cancelled_count(self):
        self.__transactions_Cancelled_count -=1

    
    #reports
    def increase_reports_count(self):
        self.__report_count +=1
    def decrease_reports_count(self):
        self.__report_count -=1

    #opactions
    def increase_opactions_count(self):
        self.__opactions_count +=1
    def decrease_opactions_count(self):
        self.__opactions_count -=1

def operatorstats_users(category,operation):
    dbmain = shelve.open('main.db', 'c')
    operatorstats_dict = {}
    try:
        if "Operatorstats" in dbmain:
            operatorstats_dict = dbmain["Operatorstats"]  # sync local with db1
        else:
            dbmain['Operatorstats'] = operatorstats_dict # sync db1 with local (basically null)
    except:
        print("Error in opening main.db")
    print("reached")
    print(operatorstats_dict)
    obj = operatorstats_dict.get(1)
    if category == "total":
        if operation == "plus":
            obj.increase_user_count()
            print(f" + | Current amount of total users is {obj.get_users_count()}")
            dbmain['Operatorstats'] = operatorstats_dict
            return 
        elif operation == "minus":
            obj.decrease_user_count()
            print(f" - | Current amount of total users is {obj.get_users_count()}")
            dbmain['Operatorstats'] = operatorstats_dict
            return
    elif category == "active":
        if operation == "plus":
            obj.increase_user_active_count()
            print(f" + | Current amount of active users is {obj.get_users_active_count()}")
            dbmain['Operatorstats'] = operatorstats_dict
            return
        elif operation == "minus":
            obj.decrease_user_active_count()
            print(f" - | Current amount of active users is {obj.get_users_active_count()}")
            dbmain['Operatorstats'] = operatorstats_dict
            return
    
    elif category == "suspended":
        if operation == "plus":
            obj.increase_user_suspended_count()
            print(f" + | Current amount of suspended users is {obj.get_users_suspended_count()}")
            dbmain['Operatorstats'] = operatorstats_dict
            return
        elif operation == "minus":
            obj.decrease_user_suspended_count()
            print(f" - | Current amount of suspended users is {obj.get_users_suspended_count()}")
            dbmain['Operatorstats'] = operatorstats_dict
            return
    elif category == "terminated":
        if operation == "plus":
            obj.increase_user_terminated_count()
            print(f" + | Current amount of terminated users is {obj.get_users_terminated_count()}")
            dbmain['Operatorstats'] = operatorstats_dict
            return
        elif operation == "minus":
            obj.decrease_user_terminated_count()
            print(f" - | Current amount of terminated users is {obj.get_users_terminated_count()}")
            dbmain['Operatorstats'] = operatorstats_dict
            return
    

def operatorstats_listings(category,operation):
    dbmain = shelve.open('main.db', 'c')
    operatorstats_dict = {}
    try:
        if "Operatorstats" in dbmain:
            operatorstats_dict = dbmain["Operatorstats"]  # sync local with db1
        else:
            dbmain['Operatorstats'] = operatorstats_dict # sync db1 with local (basically null)
    except:
        print("Error in opening main.db")
    obj = operatorstats_dict.get(1)
    
    if category == "total":
        if operation == "plus":
            obj.increase_listing_count()
            print(f" + | Current amount of total listings is {obj.get_listings_count()}")
            dbmain['Operatorstats'] = operatorstats_dict
            return
        elif operation == "minus":
            obj.decrease_listing_count()
            print(f" - | Current amount of total listings is {obj.get_listings_count()}")
            dbmain['Operatorstats'] = operatorstats_dict
            return

    elif category == "available":
        if operation == "plus":
            obj.increase_listing_available_count()
            print(f" + | Current amount of available listings is {obj.get_listings_available_count()}")
            dbmain['Operatorstats'] = operatorstats_dict
            return
        elif operation == "minus":
            obj.decrease_listing_available_count()
            print(f" - | Current amount of available listings is {obj.get_listings_available_count()}")
            dbmain['Operatorstats'] = operatorstats_dict
            return
    
    elif category == "disabled":
        if operation == "plus":
            obj.increase_listing_disabled_count()
            print(f" + | Current amount of disabled listings is {obj.get_listings_disabled_count()}")
            dbmain['Operatorstats'] = operatorstats_dict
            return
        elif operation == "minus":
            obj.decrease_listing_disabled_count()
            print(f" - | Current amount of disabled listings is {obj.get_listings_disabled_count()}")
            dbmain['Operatorstats'] = operatorstats_dict
            return

    elif category == "reserved":
        if operation == "plus":
            obj.increase_listing_reserved_count()
            print(f" + | Current amount of reserved listings is {obj.get_listings_reserved_count()}")
            dbmain['Operatorstats'] = operatorstats_dict
            return
        elif operation == "minus":
            obj.decrease_listing_reserved_count()
            print(f" - | Current amount of reserved listings is {obj.get_listings_reserved_count()}")
            dbmain['Operatorstats'] = operatorstats_dict
            return
    elif category == "sold":
        if operation == "plus":
            obj.increase_listing_sold_count()
            print(f" + | Current amount of sold listings is {obj.get_listings_sold_count()}")
            dbmain['Operatorstats'] = operatorstats_dict
            return
        elif operation == "minus":
            obj.decrease_listing_sold_count()
            print(f" - | Current amount of sold listings is {obj.get_listings_sold_count()}")
            dbmain['Operatorstats'] = operatorstats_dict
            return


def operatorstats_feedbacks(category,operation):
    dbmain = shelve.open('main.db', 'c')
    operatorstats_dict = {}
    try:
        if "Operatorstats" in dbmain:
            operatorstats_dict = dbmain["Operatorstats"]  # sync local with db1
        else:
            dbmain['Operatorstats'] = operatorstats_dict # sync db1 with local (basically null)
    except:
        print("Error in opening main.db")
    obj = operatorstats_dict.get(1)
    if category == "total":
        if operation == "plus":
            obj.increase_feedback_count()
            print(f" + | Current amount of total feedback is {obj.get_feedback_count()}")
            dbmain['Operatorstats'] = operatorstats_dict
            return
        elif operation == "minus":
            obj.decrease_feedback_count()
            print(f" - | Current amount of total feedback is {obj.get_feedback_count()}")
            dbmain['Operatorstats'] = operatorstats_dict
            return
    elif category == "replied":
        if operation == "plus":
            obj.increase_feedback_replied_count()
            print(f" + | Current amount of replied feedback is {obj.get_feedback_replied_count()}")
            dbmain['Operatorstats'] = operatorstats_dict
            return
        elif operation == "minus":
            obj.decrease_feedback_replied_count()
            print(f" - | Current amount of replied feedback is {obj.get_feedback_replied_count()}")
            dbmain['Operatorstats'] = operatorstats_dict
            return
    elif category == "unreplied":
        if operation == "plus":
            obj.increase_feedback_unreplied_count()
            print(f" + | Current amount of unreplied feedback is {obj.get_feedback_unreplied_count()}")
            dbmain['Operatorstats'] = operatorstats_dict
            return
        elif operation == "minus":
            obj.decrease_feedback_unreplied_count()
            print(f" - | Current amount of unreplied feedback is {obj.get_feedback_unreplied_count()}")
            dbmain['Operatorstats'] = operatorstats_dict
            return
    
    
def operatorstats_transactions(category,operation):
    dbmain = shelve.open('main.db', 'c')
    operatorstats_dict = {}
    try:
        if "Operatorstats" in dbmain:
            operatorstats_dict = dbmain["Operatorstats"]  # sync local with db1
        else:
            dbmain['Operatorstats'] = operatorstats_dict # sync db1 with local (basically null)
    except:
        print("Error in opening main.db")
    obj = operatorstats_dict.get(1)
    if category == "total":
        if operation == "plus":
            obj.increase_transactions_count()
            print(f" + | Current amount of total transactions is {obj.get_transactions_count()}")
            dbmain['Operatorstats'] = operatorstats_dict
            return
        elif operation == "minus":
            obj.decrease_transactions_count()
            print(f" - | Current amount of total transactions is {obj.get_transactions_count()}")
            dbmain['Operatorstats'] = operatorstats_dict
            return
    elif category == "Pending":
        if operation == "plus":
            obj.increase_transactions_Pending_count()
            print(f" + | Current amount of transactions Pending is {obj.get_transactions_Pending_count()}")
            dbmain['Operatorstats'] = operatorstats_dict
            return
        elif operation == "minus":
            obj.decrease_transactions_Pending_count()
            print(f" - | Current amount of transactions Pending is {obj.get_transactions_Pending_count()}")
            dbmain['Operatorstats'] = operatorstats_dict
            return
    elif category == "In Transit":
        if operation == "plus":
            obj.increase_transactions_In_Transit_count()
            print(f" + | Current amount of transactions In Transit is {obj.get_transactions_In_Transit_count()}")
            dbmain['Operatorstats'] = operatorstats_dict
            return
        elif operation == "minus":
            obj.decrease_transactions_In_Transit_count()
            print(f" - | Current amount of transactions In Transit is {obj.get_transactions_In_Transit_count()}")
            dbmain['Operatorstats'] = operatorstats_dict
            return
    elif category == "Delivered":
        if operation == "plus":
            obj.increase_transactions_Delivered_count()
            print(f" + | Current amount of transactions Delivered is {obj.get_transactions_Delivered_count()}")
            dbmain['Operatorstats'] = operatorstats_dict
            return
        elif operation == "minus":
            obj.decrease_transactions_Delivered_count()
            print(f" - | Current amount of transactions Delivered is {obj.get_transactions_Delivered_count()}")
            dbmain['Operatorstats'] = operatorstats_dict
            return
    elif category == "Cancelled":
        if operation == "plus":
            obj.increase_transactions_Cancelled_count()
            print(f" + | Current amount of transactions Cancelled is {obj.get_transactions_Cancelled_count()}")
            dbmain['Operatorstats'] = operatorstats_dict
            return
        elif operation == "minus":
            obj.decrease_transactions_Cancelled_count()
            print(f" - | Current amount of transactions Cancelled is {obj.get_transactions_Cancelled_count()}")
            dbmain['Operatorstats'] = operatorstats_dict
            return


def operatorstats_reports(category,operation):
    dbmain = shelve.open('main.db', 'c')
    operatorstats_dict = {}
    try:
        if "Operatorstats" in dbmain:
            operatorstats_dict = dbmain["Operatorstats"]  # sync local with db1
        else:
            dbmain['Operatorstats'] = operatorstats_dict # sync db1 with local (basically null)
    except:
        print("Error in opening main.db")
    obj = operatorstats_dict.get(1)
    if category == "total":
        if operation == "plus":
            obj.increase_reports_count()
            print(f" + | Current amount of total reports is {obj.get_reports_count()}")
            dbmain['Operatorstats'] = operatorstats_dict
            return
        elif operation == "minus":
            obj.decrease_reports_count()
            print(f" - | Current amount of total transactions is {obj.get_reports_count()}")
            dbmain['Operatorstats'] = operatorstats_dict
            return    

def operatorstats_opactions(category,operation):
    dbmain = shelve.open('main.db', 'c')
    operatorstats_dict = {}
    try:
        if "Operatorstats" in dbmain:
            operatorstats_dict = dbmain["Operatorstats"]  # sync local with db1
        else:
            dbmain['Operatorstats'] = operatorstats_dict # sync db1 with local (basically null)
    except:
        print("Error in opening main.db")
    obj = operatorstats_dict.get(1)
    if category == "total":
        if operation == "plus":
            obj.increase_opactions_count()
            print(f" + | Current amount of total opactions is {obj.get_opactions_count()}")
            dbmain['Operatorstats'] = operatorstats_dict
            return
        elif operation == "minus":
            obj.decrease_opactions_count()
            print(f" - | Current amount of total opactions is {obj.get_opactions_count()}")
            dbmain['Operatorstats'] = operatorstats_dict
            return    