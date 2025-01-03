class Report:
    count_ID = 0
    def __init__(self,creator_ID,offender_ID,category,comment):
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
    