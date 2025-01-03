class Report:
    count_ID = 0
    def __init__(self,creator_ID,offender_ID,category,comment):
        Report.count_ID +=1
        self.__ID = Report.count_ID
        self.__creator_ID = creator_ID
        self.__offender_ID = offender_ID
        self.__category = category
        self.__comment = comment

    def get_ID(self):
        return self.__ID
    
    def get_creator_ID(self):
        return self.__creator_ID
    
    def get_offender_ID(self):
        return self.__offender_ID
    def get_category(self):
        return self.__category
    
    def get_comment(self):
        return self.__comment
    
    def set_ID(self,id):
        self.__ID = id

    def set_creator_ID(self,id):
        self.__creator_ID = id
    
    def set_offender_ID(self,id):
        self.__creator_ID = id

    def set_category(self,category):
        self.__category = category

    def set_comment(self,comment):
        self.__comment = comment

