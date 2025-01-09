class Operatoractions:
    count_ID = 0
    def __init__(self,affecteduserID,category,reason,text):
        Operatoractions.count_ID +=1
        self.__ID = Operatoractions.count_ID
        self.__affecteduserID = affecteduserID
        self.__category = category
        self.__text = text
        self.__reason = reason

    def get_ID(self):
        return self.__ID
    
    def get_affecteduserID(self):
        return self.__affecteduserID
    
    def get_category(self):
        return self.__category

    def get_text(self):
        return self.__text

    def get_reason(self):
        return self.__reason
    
    def set_ID(self,id):
        self.__ID = id
    
    def set_affecteduserID(self,id):
        self.__affecteduserID = id
    
    def set_category(self,category):
        self.__category = category
    
    def set__text(self,text):
        self.__text = text
    
    def set_reason(self,reason):
        self.__reason = reason
    