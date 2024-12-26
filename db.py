from flask import Flask, render_template, url_for,request,redirect
import os
import Customer 
from Forms import CustomerSignupForm, CustomerLoginForm
import shelve, Customer

#db1 = customer
#db2 = listings 

def sync_customer_with_db1():
    db1 = shelve.open('customer.db','c')
    customers_dict = {} #local one
    try:
        if "Customers" in db1:
            customers_dict = db1["Customers"] #sync local with db1
        else:
            db1['Customers'] = customers_dict #sync db1 with local (basically null)
    except:
        print("Error in opening customer.db")


