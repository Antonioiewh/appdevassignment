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


def sortbycategory(category,listing,outputlist):#enter category,object,output list
    if listing.get_category == category: #check if it matches
        print(listing.get_category())
        outputlist.append(listing.get_ID())
    return outputlist

def dupechecker(inputlist,outputlist):#output list should be empty as in dupe checking shld be the final step

    for i in inputlist: #may have dupes
        if i not in outputlist: #check if it already exists
            outputlist.append(i) #if it does not, add
        else:
            pass #else skip it
    
def sortbycondition(condition,listing,outputlist): #enter condition, listingobj,output list
    if listing.get_condition == condition:
        print(listing.get_condition())
        outputlist.append(listing.get_ID())
    return outputlist

def finaliser(outputlist,finallist): #converts all the IDs into objects, Note: you can just write this as a function by itself in the init itself since idk if it will work lmao
    db2 = shelve.open('listing.db','c')
    listings_dict = {}
    try:
        if "Listings" in db2:
            listings_dict = db2["Listings"] #sync local with db2
        else:
            db2['Listings'] = listings_dict #sync db2 with local (basically null)
    except:
            print("Error in opening listings.db") 
    
    for i in outputlist:
        listing = listings_dict.get(i)
        finallist.append(listing) #add object to final list
    return finallist #send to html page


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


