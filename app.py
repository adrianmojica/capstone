"""Feedback Flask app."""
from flask import Flask, render_template, redirect, session, jsonify, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized
import json
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.rest import Client
from models import connect_db, db, User, Therapist, Form
from forms import RegisterForm, LoginForm, DeleteForm, AddEntryForm, RegisterTherapistForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:///mentalHealthNet"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secrets"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)


@app.route("/")
def home():
    """redirect to register"""
    return redirect("/login")

@app.route("/register", methods=['GET', 'POST'])
def register():
    """Registration flow show form and create user"""
    if "username" in session:
        return redirect(f"/users/{session['username']}")
    
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        bday = form.bday.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        stage = 1
        emergency_contact_email = form.emergency_contact_email.data


        user = User.register(username, password, email, bday, first_name, last_name, stage,  emergency_contact_email)

        db.session.commit()
        session['username'] = user.username

        return redirect(f"/users/{user.username}")

    else:
        return render_template("users/register.html", form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    """Login Flow."""
    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Invalid username/password."]
            return render_template("users/login.html", form=form)

    return render_template("users/login.html", form=form)


@app.route("/register/therapists", methods=['GET', 'POST'])
def register_therapist():
    """Registration flow show form and create Therapist User"""
    if "therapist" in session:
        return redirect(f"/therapists/{session['therapist']}")
    
    form = RegisterTherapistForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        therapist = Therapist.register_therapist(username, password, email, first_name, last_name)

        db.session.commit()
        session['therapist'] = therapist.username

        return redirect(f"/therapists/{therapist.username}")

    else:
        return render_template("therapists/register.html", form=form)


@app.route('/login/therapists', methods=['GET','POST'])
def login_therapists():
    """Login Flow for therapists."""
    if "therapist" in session:
        return redirect(f"/therapists/{session['therapist']}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        therapist = Therapist.authenticate_therapist(username, password)
        if therapist:
            session['therapist'] = therapist.username
            return redirect(f"/therapists/{therapist.username}")
        else:
            form.username.errors = ["Invalid username/password."]
            return render_template("therapists/login.html", form=form)

    return render_template("therapists/login.html", form=form)


@app.route("/logout")
def logout():
    """Logout."""

    session.pop("username")
    return redirect("/login")

@app.route("/logout/therapists")
def logout_therapists():
    """Logout."""

    session.pop("therapist")
    return redirect("/login")

####################################################
#       Route for retrieving data for graph         #
#####################################################

@app.route("/<username>/data")
def get_data(username):
    if "username" not in session or username != session["username"]:
        raise Unauthorized()
    dates = []
    nrs1 = []
    nrs2 = []
    nrs3 = []
    nrs4 = []
    nrs5 = []
    forms = (Form.query.filter(Form.username == username).all())
    print("**************")
    print(forms)
    for data in forms:
      dates.append(data.date)
      nrs1.append(data.nrs1)
      nrs2.append(data.nrs2)
      nrs3.append(data.nrs3)
      nrs4.append(data.nrs4)
      nrs5.append(data.nrs5)
    data_set = { "dates": dates, "nrs1": nrs1, "nrs2": nrs2, "nrs3": nrs3, "nrs4":nrs4, "nrs5":nrs5}
    return jsonify(data_set)




@app.route("/users/<username>")
def show_user(username):
    """user detail page"""
    
    if "username" not in session or username != session["username"]:
        raise Unauthorized()

    user = User.query.get(username)
    form = DeleteForm()

    return render_template('users/show.html', user = user, form = form)


################################################################
##############Emergency UseCase ################################
################################################################

@app.route("/emergency/<username>/<therapist>")
def emergency(username,therapist):
    """sends email to final emergency contact and therapist"""

    if "username" not in session or username != session["username"]:
        raise Unauthorized()
    
    user = User.query.get(username)
    therapist = Therapist.query.get(therapist)
    
    to_emails = [
        (user.emergency_contact_email, 'Emergency Contact'),
        (therapist.email, 'Therapist')
    ]
    
    print("*******EMERGENCY*******")
    message = Mail(
    from_email='adrian@houseofbeards.me',
    to_emails= to_emails,
    is_multiple=True,
    subject=f'Mental Health Net has an Emergency Case: {user.full_name} is having a crisis.',
    html_content=f'<strong>Hello,<br> We have been notified by  {user.full_name} that they are having a crisis.<br> Our Team Has been notified and are working on the case')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.body)

    
    #####################################################
    #             Twilio SMS notification               #
    #####################################################


    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="Join Earth's mightiest heroes. Like Kevin Bacon.",
        from_='+18722505272',        
        to='+17609043999' 
    ) 

    print(message.sid)
    flash("Emergency SMS and Email Have been sent, Hang in there!")        
    return  redirect(f"/users/{username}")


@app.route('/users/<username>/form/new', methods=["GET", "POST"])
def form(username):
    """user submit feedback route"""
    if "username" not in session or username != session['username']:
        raise Unauthorized()

    form = AddEntryForm()

    if form.validate_on_submit():
        date = form.date.data
        therapist = form.therapist.data 
        nrs1 = form.nrs1.data
        nrs2 = form.nrs2.data
        nrs3 = form.nrs3.data
        nrs4 = form.nrs4.data
        nrs5 = form.nrs5.data
        a_event = form.a_event.data
        beliefs = form.beliefs.data
        c_distortions = ', '.join([str(distortion) for distortion in form.c_distortions.data]) 
        c_consequences = ', '.join([str(consequence) for consequence in form.c_consequences.data]) 
        reactions = form.reactions.data
        is_at_risk = False

        if nrs1 <= 35 or nrs2<= 35 or nrs3<= 35 or nrs5<35:
            is_at_risk = True

        entry = Form(
            username = username,
            therapist = therapist.username,
            date= date,
            nrs1 = nrs1,
            nrs2 = nrs2,
            nrs3 = nrs3,
            nrs4 = nrs4,
            nrs5 = nrs5,
            a_event = a_event,
            beliefs = beliefs,
            c_distortions = c_distortions,
            c_consequences = c_consequences,
            reactions = reactions,
            is_at_risk = is_at_risk
        )

        db.session.add(entry)
        db.session.commit()

        return  redirect(f"/users/{username}")

    else:
        return render_template("form/newJournal.html", form=form)

@app.route('/users/<int:form_id>/form/detail', methods=["GET","POST"])
def update_feedback(form_id):

    form = Form.query.get(form_id)
    if "username" not in session or form.username != session['username']:
        raise Unauthorized()

    return render_template('/form/show.html', form= form, user=form.user)


@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Delete feedback."""

    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")

