class Feedback:
    count_ID = 0
    def __init__(self,rating,remark):
        Feedback.count_ID+=1
        self.__ID = Feedback.count_ID
        self.__rating = rating
        self.__remark = remark
    
    def get_ID(self):
        return self.__ID
    def get_rating(self):
        return self.__rating    
    
    def get_remark(self):
        return self.__remark
    

    #DONT USE THESE FUNCS idk
    def set_rating(self,rating):
        self.__rating = rating
    
    def set_remark(self,remark):
        self.__remark = remark
