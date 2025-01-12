class Listing:
    count_ID = 0
    def __init__(self,creatorID,creatorusername,title,description,condition,category,deal_method,deal_methodinfo): #dealmethod info as an
        Listing.count_ID+=1
        self.__ID = Listing.count_ID
        self.__creatorID = creatorID #same as current_sessionID
        self.__creatorusername = creatorusername
        self.__title = title
        self.__description = description
        self.__condition = condition
        self.__category = category
        self.__deal_method = deal_method
        self.__likes = 0
        self.__status = "available" #or "disabled"
        if deal_method == "meetup":
            self.__deal_meetupinfo = deal_methodinfo[0]
        if deal_method == "delivery":
            self.__deal_deliveryinfo = deal_methodinfo[1]
        if deal_method =="meetupdelivery":
            self.__deal_meetupinfo = deal_methodinfo[0]
            self.__deal_deliveryinfo = deal_methodinfo[1]
        #self.__deal_delivery = deal_delivery

    
    def get_creatorID(self):
        return self.__creatorID
    
    def get_ID(self):
        return self.__ID
    
    def get_title(self):
        return self.__title
    
    def get_description(self):
        return self.__description
    
    def get_condition(self):
        return self.__condition
    
    def get_category(self):
        return self.__category

    def get_deal_method(self):
        return self.__deal_method
    
    def get_likes(self):
        return self.__likes
    
    def get_status(self):
        return self.__status
    
    def get_deal_meetupinfo(self):
        return self.__deal_meetupinfo
    
    def get_deal_deliveryinfo(self):
        return self.__deal_deliveryinfo
    
    def get_creator_username(self):
        return self.__creatorusername

    def set_creatorID(self,creatorID):
        self.__creatorID = creatorID
    
    def set_ID(self,ID):
        self.__ID = ID
    
    def set_title(self,title):
        self.__title = title

    def set_description(self,description):
        self.__description = description
    
    def set_condition(self,condition):
        self.__condition = condition

    def set_category(self,category):
        self.__category = category

    def set_deal_method(self,deal_method):
        self.__deal_method = deal_method
    
    def add_likes(self):
        self.__likes +=1
    
    def minus_likes(self):
        self.__likes -= 1
    
    def set_status(self,status):
        self.__status = status

    def set_deal_meetupinfo(self,info):
        self.__deal_meetupinfo = info
    
    def set_deal_meetupdelivery(self,info):
        self.__deal_deliveryinfo = info

    

