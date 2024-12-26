class Customer:
    count_id=0
    def __init__(self,username,email,password): #what to ask when they sign up!
        Customer.count_id+=1
        self.__id = Customer.count_id
        self.__username = username
        self.__email = email
        self.__password = password
        self.__listings = [] #store the listing ids in here
        self.__reviews = [] #store reviews they received
        self.__address = None 
        self.__credit_card = None
        self.__rating = 0
        self.__date_joined = "1/1/1"

    def get_id(self):
        return self.__id
    
    def get_username(self):
        return self.__username
    
    def get_email(self):
        return self.__email
    
    def get_password(self):
        return self.__password
    
    def get_listings(self):
        return self.__listings
    
    def get_reviews(self):
        return self.__reviews
    
    def get_address(self):
        return self.__address
    
    def get_credit_card(self):
        return self.__credit_card

    def get_date_joined(self):
        return self.__date_joined

    def get_rating(self):
        return self.__rating

    def set_id(self,id): #just here but god forbid u actually run this as why would u
        self.__id = id 
    
    def set_username(self,username):
        self.__username = username
    
    def set_email(self,email):
        self.__email = email
    
    def set_password(self,password):
        self.__password = password
    

    #VERY IMPT DO NOT USE SET_LISTINGS!!!!
    def set_listings(self,listings):
        self.__listings = listings
    
    def add_listings(self,listingid):
        self.__listings.append(listingid)
    
    #VERY IMPT DO NOT USE SET_REVIEWS!!!!
    def set_reviews(self,reviews):
        self.__reviews = reviews
    
    def add_reviews(self,review):
        self.__reviews.append(review)
    

    
    def set_address(self,address):
        self.__address = address
    
    def set_credit_card(self,credit_card):
        self.__credit_card = credit_card
    


    
    
