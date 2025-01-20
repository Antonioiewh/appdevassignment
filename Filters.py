from flask import Flask, render_template, url_for,request,redirect,session,jsonify
import os,sys,stat
from werkzeug.utils import secure_filename
import Customer , Listing,Reviews,Report,operatoractions,Feedback #classes
from Forms import CustomerSignupForm, CustomerLoginForm, ListingForm,ReviewForm,CustomerUpdateForm,ReportForm,SearchBar,OperatorLoginForm,OperatorLoginVerifyForm,SearchUserField,OperatorSuspendUser,OperatorTerminateUser,OperatorRestoreUser #our forms
from Forms import OperatorDisableListing,OperatorRestoreListing,SearchListingField,SearchReportField,SearchOperatorActionField,FeedbackForm
import Email,Search,Notifications
import shelve, Customer
from pathlib import Path
from Messages import User
import string
import random
from datetime import datetime

def category(listingobject,selectedcategory,outputlist,flag):
    if flag == "addonly": #Default flag for category 
        if listingobject.get_category() == selectedcategory:
            outputlist.append(listingobject.get_ID())
        return outputlist
    if flag == "addanddelete":
        if listingobject.get_category() == selectedcategory:
            outputlist.append(listingobject.get_ID()) 
        else:
            outputlist.remove(listingobject.get_ID())
        return outputlist
def condition(listingobject,selectedcondition,outputlist,flag):
    if flag == "addonly":
        if listingobject.get_condition() == selectedcondition:
            outputlist.append(listingobject.get_ID())
        return outputlist
    if flag == "addanddelete": #Default flag for condition
        if listingobject.get_condition() == selectedcondition:
            outputlist.append(listingobject.get_ID())
        else:
            outputlist.remove(listingobject.get_ID())


