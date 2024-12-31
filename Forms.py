from wtforms import Form, BooleanField, StringField, validators, PasswordField, SelectField, RadioField, SelectMultipleField, FileField #import the fields u need

class CustomerSignupForm(Form): #Form for CustomerSignup.html
    username = StringField('Username',[validators.Length(min=4, max=25),validators.DataRequired()])
    email        = StringField('Email Address', [validators.Length(min=6, max=35),validators.DataRequired()]) #we will add validator to this later
    password        = StringField('Password', [validators.Length(min=6, max=35),validators.DataRequired()])
    
class CustomerLoginForm(Form): #Form for CustomerLogin.html
    username = StringField('Username',[validators.Length(min=4, max=25),validators.DataRequired()])
    password        = StringField('Password', [validators.Length(min=6, max=35),validators.DataRequired()])


class ListingForm(Form):
    category = SelectField('Category', choices=[('cat1','Category 1'),('cat2','Category 2'),('cat3','Category 3'),('cat4','Category 4'),('cat5','Category 5'),validators.DataRequired()])
    condition = RadioField('Condition',choices=[('barely_used', "Barely used"), ('frequently_used', 'Frequently used'), ('daily_used', 'Used daily'),validators.DataRequired()])
    title = StringField('Title',[validators.Length(min=4, max=25),validators.DataRequired()])
    description = StringField('Description',[validators.Length(min=4, max=300),validators.DataRequired()])
    payment_method = RadioField('Payment method',choices=[('meetup','Meet-up'),('delivery','Delivery'),validators.DataRequired()]) #idk how to do this but gl to anyone trying to either

class uploadListingimg(Form):
    listingimg = FileField('image')


class ReviewForm(Form):
    rating = RadioField('Rating', choices=[(1,1),(2,2), (3,3),(4,4),(5,5),validators.DataRequired()])
    review_text = StringField('Add a comment', [validators.Length(min=4,max=1234),validators.DataRequired()])

