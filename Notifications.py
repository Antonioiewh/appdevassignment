from datetime import datetime
import Email
import Customer
from flask import Flask, render_template, url_for,request,redirect,session,jsonify
import os,sys,stat
from werkzeug.utils import secure_filename
import Customer , Listing,Reviews,Report,operatoractions #classes
from Forms import CustomerSignupForm, CustomerLoginForm, ListingForm,ReviewForm,CustomerUpdateForm,ReportForm,SearchBar,OperatorLoginForm,OperatorLoginVerifyForm,SearchUserField,OperatorSuspendUser,OperatorTerminateUser,OperatorRestoreUser #our forms
from Forms import OperatorDisableListing,OperatorRestoreListing,SearchListingField,SearchReportField
import Email,Search
import shelve, Customer
from pathlib import Path
from Messages import User
import string
import random
class Notifications:
    count_ID = 0
    def __init__(self,receiverID,content):
        Notifications.count_ID+=1
        self.__receiverID = receiverID
        self.__content = content
        self.__datetimestamp = (datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.__ID = Notifications.count_ID
    def get_receiverID(self):
        return self.__receiverID
    
    def get_content(self):
        return self.__content
    
    def get_datetimestamp(self):
        return self.__datetimestamp

    def get_ID(self):
        return self.__ID
    
    def set_receiverID(self,id):
        self.__receiverID = id

    def set_content(self,content):
        self.__content = content

    def set_datetimestamp(self,timestamp):
        self.__datetimestamp = timestamp

    def set_ID(self,id):
        self.__ID = id
    

