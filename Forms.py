
from wtforms import Form, BooleanField, StringField, validators, PasswordField, SelectField, RadioField, SelectMultipleField, FileField,HiddenField,TextAreaField,SubmitField #import the fields u need
class CustomerSignupForm(Form): #Form for CustomerSignup.html
    username = StringField('Username',[validators.Length(min=4, max=25),validators.DataRequired()])
    email        = StringField('Email Address', [validators.Length(min=6, max=35),validators.DataRequired()]) #we will add validator to this later
    password        = StringField('Password', [validators.Length(min=6, max=35),validators.DataRequired()])
    
class CustomerLoginForm(Form): #Form for CustomerLogin.html
    username = StringField('Username',[validators.Length(min=4, max=25),validators.DataRequired()])
    password        = StringField('Password', [validators.Length(min=6, max=35),validators.DataRequired()])

class CustomerUpdateForm(Form): #can change profile pic,email,username and password, prompt enter CURRENT password to confirm changes, leave blank for no change
    username = StringField('New username')
    email        = StringField('New email Address')
    password        = StringField('New Password')
    confirmpassword = StringField('Confirm Password', [validators.Length(min=6, max=35),validators.DataRequired()])

class ListingForm(Form):
    category = SelectField('Category',[validators.DataRequired()], choices=[('Category 1','Electronics'),('Category 2','Books'),('Category 3','Fashion'),('Category 4','Entertainment'),('Category 5','Misc')])
    condition = RadioField('Condition', [validators.DataRequired()], choices=[('Barely used', "Barely used"), ('Frequently used', 'Frequently used'), ('Worn out', 'Worn out')])
    title = StringField('Title',[validators.Length(min=4, max=25),validators.DataRequired()])
    description = StringField('Description',[validators.Length(min=4, max=300),validators.DataRequired()])

#class uploadListingimg(Form): 
    #listingimg = FileField('image')
class DeliveryForm(Form):
    delivery_id = StringField('Delivery ID', [validators.DataRequired()])
    submit = SubmitField('Check Status')
    address = StringField('Delivery Address', [validators.DataRequired()])
    deliveryinfo = StringField('Delivery Information', [validators.DataRequired()])

class ReviewForm(Form):
    rating = RadioField('Rating', [validators.DataRequired()],choices=[(1,1),(2,2), (3,3),(4,4),(5,5)])
    review_text = StringField('Add a comment', [validators.Length(min=4,max=1234),validators.DataRequired()])

class ReportForm(Form):
    affectedusername = StringField('Enter username of user you are reporting',[validators.Length(min=1,max=1234)])
    category = SelectField('Category',[validators.DataRequired()], choices=[('Phishing','Phishing'),('Scamming','Scamming'),('Suspicious account','Suspicious account'),('Offering prohibited items','Offering prohibited items')])
    report_text = StringField('Add a comment',[validators.Length(min=4,max=1234)])

class SearchBar(Form):
    searchfield = StringField('Search')

class OperatorLoginForm(Form):
    operator_username = StringField('Username',[validators.Length(min=4, max=25),validators.DataRequired()])
    password        = StringField('Password', [validators.Length(min=6, max=35),validators.DataRequired()])
    email        = StringField('Email Address', [validators.Length(min=6, max=35),validators.DataRequired()])

class OperatorLoginVerifyForm(Form):
    OTP = StringField('Username',[validators.Length(min=4, max=25),validators.DataRequired()])

#for user dashboard
class SearchUserField(Form):
    searchfield = StringField("Enter username to sort by",[validators.Length(min=1, max=35),validators.DataRequired()])
class SearchUserStatus(Form):
    category = SelectField('Category', [validators.DataRequired()],choices=[('active','Active'),('suspended','Suspended'),('terminated','Terminated')])

#operator actions
class OperatorSuspendUser(Form):
    affectedid = StringField('Enter ID of user',[validators.DataRequired(),validators.Length(min=1,max=1234)])
    category = SelectField('Category',[validators.DataRequired()], choices=[('Phishing','Phishing'),('Scamming','Scamming'),('Suspicious account','Suspicious account'),('Offering prohibited items','Offering prohibited items')])
    suspend_text = StringField('Add a comment',[validators.Length(min=4,max=1234)])
    password = StringField('Password', [validators.Length(min=6, max=35),validators.DataRequired()])
    typeofaction = HiddenField()

class OperatorTerminateUser(Form):
    affectedid = StringField('Enter ID of user',[validators.DataRequired(),validators.Length(min=1,max=1234)])
    category = SelectField('Category',[validators.DataRequired()], choices=[('Phishing','Phishing'),('Scamming','Scamming'),('Suspicious account','Suspicious account'),('Offering prohibited items','Offering prohibited items')])
    terminate_text = StringField('Add a comment',[validators.Length(min=4,max=1234)])
    password        = StringField('Password', [validators.Length(min=6, max=35),validators.DataRequired()])
    typeofaction = HiddenField()

class OperatorRestoreUser(Form):
    affectedid = StringField('Enter ID of user',[validators.DataRequired(),validators.Length(min=1,max=1234)])
    password = StringField('Password', [validators.Length(min=6, max=35),validators.DataRequired()])
    typeofaction = HiddenField()

class OperatorDisableListing(Form):
    listingid = StringField('Enter ID of listing',[validators.DataRequired(),validators.Length(min=1,max=1234)])
    category = SelectField('Category',[validators.DataRequired()], choices=[('Phishing','Phishing'),('Scamming','Scamming'),('Suspicious account','Suspicious account'),('Offering prohibited items','Offering prohibited items')])
    disable_text = StringField('Add a comment',[validators.Length(min=4,max=1234)])
    password        = StringField('Password', [validators.Length(min=6, max=35),validators.DataRequired()])
    typeofaction = HiddenField()

class OperatorRestoreListing(Form):
    listingid = StringField('Enter ID of listing',[validators.DataRequired(),validators.Length(min=1,max=1234)])
    password = StringField('Password', [validators.Length(min=6, max=35),validators.DataRequired()])
    typeofaction = HiddenField()

#listing dashboard
class SearchListingField(Form):
    searchfield = StringField("Enter listing name")
class SearchListingIDField(Form):
    searchidfield = StringField("Enter ID of listing")
class SearchListingStatusField(Form):
    searchstatusfield = SelectField('Choose status', [validators.DataRequired()],choices=[('available','Available'),('disabled','Disabled'),('reserved','Reserved'),('sold','Sold')])

#feedback dashboard
class FilterFeedback(Form):
    searchstatusfield = SelectField('Choose status', [validators.DataRequired()],choices=[('unreplied','Unreplied'),('replied','Replied')])

#transactions dashboard
class FilterTransactions(Form):
    searchstatusfield = SelectField('Select status',[validators.DataRequired()],choices=[('Pending','Pending'),('In Transit','In Transit'),('Delivered','Delivered'),('Cancelled','Cancelled')])
    
class SearchReportField(Form):
    searchfield = StringField("Enter offender username")

class SearchOperatorActionField(Form):
    searchfield = SelectField('Category',[validators.DataRequired()], choices=[('suspend user','Suspend user'),('terminate user','Terminate user'),('restore user','restore user'),('restore listing','Restore listing'),('disable listing','Disable listing')])

class SearchTransactionField(Form):
    searchfield = StringField("Enter Listing title",[validators.DataRequired()])
class FeedbackForm(Form):
    rating = RadioField('Rate your experience', [validators.DataRequired()],choices=[(1,1),(2,2), (3,3),(4,4),(5,5)])
    feedback = TextAreaField('Have you encountered any issues so far? If so, please describe it', [validators.InputRequired(), validators.Length(max=500)])
    category = SelectField("Feedback Type", choices=[
        ('Bug', 'Report a Bug'),
        ('Suggestion', 'Feature Suggestion'),
        ('General', 'General Feedback')
    ])


class ReplyFeedback(Form):
    reply = TextAreaField('Anything you want to declare with the customer? If so, please describe it',[validators.InputRequired(), validators.Length(max=500)])
class FilterForm(Form):
    category1 = BooleanField('Electronics')
    category2 = BooleanField('Books', false_values=None)
    category3 = BooleanField('Fashion', false_values=None)
    category4 = BooleanField('Entertainment', false_values=None)
    category5 = BooleanField('Misc', false_values=None)
    condition_barelyused = BooleanField('Barely used', false_values=None)
    condition_frequentlyused = BooleanField('Frequently used', false_values=None)
    condition_wornout = BooleanField('Worn out', false_values=None)
    sortlatest = BooleanField('Sort latest',false_values=None)
    #sortoldest = BooleanField('Sort oldest',false_values=None)

class UpdateFeedback(Form):
    rating = RadioField('Rate your experience', [validators.DataRequired()],choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])
    feedback = TextAreaField('Have you encountered any issues so far? If so, please describe it',[validators.InputRequired(), validators.Length(max=500)])
    category = SelectField("Feedback Type", choices=[
        ('Bug', 'Report a Bug'),
        ('Suggestion', 'Feature Suggestion'),
        ('General', 'General Feedback')
    ])