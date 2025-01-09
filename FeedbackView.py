
from flask import Flask, render_template, request, redirect, session, url_for
from Forms import FeedbackForm  # Import your form class
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')  # Render the home page


# Route for handling feedback submission
@app.route('/feedback', methods=['GET', 'POST'])
def submit_feedback():
    form = FeedbackForm()  # Instantiate the FeedbackForm
    if request.method == 'POST':
        if form.validate_on_submit():
            subject = form.subject.data
            feedback = form.feedback.data

            # You can process the feedback here, e.g., save it to a file or database
            # Example: Save feedback to a file
            with open('feedbacks.txt', 'a') as f:
                f.write(f"Subject: {subject}\nFeedback: {feedback}\n\n")

            return redirect(url_for('thank_you'))  # Redirect to thank-you page after submission
        else:
            # If form is not valid, re-render the form with error messages
            return render_template('feedback.html', form=form)
    return render_template('feedback.html', form=form)


# Route to display a thank you page after successful feedback submission
@app.route('/thank-you')
def thank_you():
    return render_template('feedback.html',)


if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode