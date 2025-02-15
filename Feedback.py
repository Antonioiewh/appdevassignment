class Feedback:
    count_ID = 0
    def __init__(self,rating,remark,category,reply=None):
        Feedback.count_ID+=1
        self.__ID = Feedback.count_ID
        self.__rating = rating
        self.__remark = remark
        self.__reply = reply
        self.__category = category
    
    def get_ID(self):
        return self.__ID
    def get_rating(self):
        return self.__rating    

    def get_category(self):
        return self.__category

    def get_remark(self):
        return self.__remark
    
    def get_reply(self):
        return self.__reply

    #DONT USE THESE FUNCS idk
    def set_rating(self,rating):
        self.__rating = rating
    
    def set_remark(self,remark):
        self.__remark = remark

    def set_reply(self,reply):
        self.__reply = reply

    def set_category(self,category):
        self.__category = category