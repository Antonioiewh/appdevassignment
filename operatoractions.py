class Operatoractions:
    count_ID = 0
    def __init__(self,affecteduserID,category,text):
        Operatoractions.count_ID +=1
        self.__ID = Operatoractions.count_ID
        self.__affecteduserID = affecteduserID
        self.__category = category
        self.__text = text

    def get_ID(self):
        return self.__ID
    
    def get_affecteduserID(self):
        return self.__affecteduserID
    
    def get_category(self):
        return self.__category

    def get_text(self):
        return self.__text

    def set_ID(self,id):
        self.__ID = id
    
    def set_affecteduserID(self,id):
        self.__affecteduserID = id
    
    def set_category(self,category):
        self.__category = category
    
    def set__text(self,text):
        self.__text = text
    