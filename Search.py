from flask import Flask, render_template, url_for,request,redirect
import os,sys,stat
from werkzeug.utils import secure_filename
import Customer , Listing,Reviews,Report #classes
from Forms import CustomerSignupForm, CustomerLoginForm, ListingForm,ReviewForm,CustomerUpdateForm,ReportForm,SearchBar #our forms
import shelve, Customer
from pathlib import Path

print("Made db1 here lmao")
def search_keyword(obj,keyword,outputlist): #enter keyword,obj and outputlist
    if keyword in obj.get_title() and check_listing(obj):
        outputlist.append(obj)
    else:
        pass
    return outputlist

def check_listing(obj): #check if creator is suspended,terminated and if listing is disabled/deleted
    #check creator
    db1 = shelve.open('customer.db','c')
    customers_dict = {}
    try:
        if "Customers" in db1:
            customers_dict = db1["Customers"] #sync local with db1
        else:
            db1['Customers'] = customers_dict #sync db1 with local (basically null)
    except:
        print("Error in opening customer.db")
        
    customer = customers_dict.get(obj.get_creatorID())
    if customer.get_status() == "active":
        return True
    else:
        return False