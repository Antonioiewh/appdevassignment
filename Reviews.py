class Reviews:
    count_ID = 0
    def __init__(self,creator_ID,creatorUsername,rating,comment):
        Reviews.count_ID+=1
        self.__ID = Reviews.count_ID
        self.__creator__ID = creator_ID
        self.__creator_username = creatorUsername
        self.__rating = rating
        self.__comment = comment

    def get_ID(self):
        return self.__ID
    
    def get_creator_ID(self):
        return self.__creator__ID
    
    def get_creator_username(self):
        return self.__creator_username
    
    def get_rating(self):
        return self.__rating
    
    def get_comment(self):
        return self.__comment
    

    #NOT SUPPOSED TO USE THESE:
    def set_ID(self,id):
        self.__ID = id

    def set_creator_ID(self,id):
        self.__creator__ID = id

    def set_creator_username(self,username):
        self.__creator_username = username

    def set_rating(self,rating):
        self.__rating = rating

    def set_comment(self,comment):
        self.__comment = comment