from flask import Flask, render_template, url_for,request,redirect
import os,sys,stat
from werkzeug.utils import secure_filename
import Customer , Listing,Reviews,Report #classes
from Forms import CustomerSignupForm, CustomerLoginForm, ListingForm,ReviewForm,CustomerUpdateForm,ReportForm,SearchBar #our forms
import shelve, Customer
from pathlib import Path

def search_keyword(obj,keyword,outputlist): #enter keyword,obj and outputlist
    if keyword in obj.get_title():
        outputlist.append(obj)
    else:
        pass
    return outputlist