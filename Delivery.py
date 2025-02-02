class Delivery:
    count_ID = 0
    def __init__(self,listing_id,item_title,status,expected_date,address):
        Delivery.count_ID+=1
        self.__ID = Delivery.count_ID
        self.__customer_id = listing_id
        self.__item_title = item_title
        self.__status = status
        self.__expected_date = expected_date
        self.__address = address

    def get_ID(self):
        return self.__ID


    def get_customer_id(self):
        return self.__customer_id
    def get_item_title(self):
        return self.__item_title
    def get_address(self):
        return self.__address
    def get_status(self):
        return self.__status

    def get_expected_date(self):
        return self.__expected_date

    def set_item_title(self,item_title):
        self.__item_title = item_title
    def set_address(self,address):
        self.__address = address
    def set_status(self,status):
        self.__status = status

    def set_expected_date(self,expected_date):
        self.__expected_date = expected_date

    def set_ID(self,ID):
        self.__ID = ID

    def set_customer_id(self,listing_id):
        self.__customer_id = listing_id

    def cancel_delivery(self):
        if self.__status != 'Cancelled':
            self.__status = 'Cancelled'