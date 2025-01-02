class ListingImage: #db2["images"]
    def __init__(self,listingid,filename):
        self.__listingid = listingid
        self.__filename = filename

    def get_listingid(self):
        return self.__listingid
    
    def get_filename(self):
        return self.__filename
    
    def set_listingid(self,listingid):
        self.__listingid = listingid

    def set_filename(self,filename):
        self.__filename = filename