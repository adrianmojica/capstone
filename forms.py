from wtforms import StringField, PasswordField, SelectField,IntegerField, TextAreaField, widgets, SelectMultipleField 
from wtforms.validators import InputRequired, Length, NumberRange, Email, Optional
from wtforms.fields.html5 import IntegerRangeField, DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_wtf import FlaskForm
from models import Therapist


class LoginForm(FlaskForm):
    """Login form."""
    username = StringField(
        "Username",
        validators=[InputRequired(),Length(min=1,max=20)],
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6,max=55)],
    )


class RegisterForm(FlaskForm):
    """Registration Form."""
    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1,max=20)]
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6,max=55)],
    )
    email = StringField(
        "Email",
        validators=[InputRequired(), Email(), Length(max=50)], 
    )

    bday = StringField(
        "Birthday",
        validators=[ InputRequired(), Length(max=30)],
    )
    first_name = StringField(
        "First Name",
        validators=[ InputRequired(), Length(max=30)],
    )
    last_name = StringField(
        "Last Name",
        validators=[ InputRequired(), Length(max=30)],
    )
    emergency_contact_email = StringField(
        "Emergency Contact Email",
        validators=[InputRequired(), Email(), Length(max=50)], 
    )

class RegisterTherapistForm (FlaskForm):
    """Registration Form."""
    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1,max=20)]
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6,max=55)],
    )
    email = StringField(
        "Email",
        validators=[InputRequired(), Email(), Length(max=50)], 
    )

    first_name = StringField(
        "First Name",
        validators=[ InputRequired(), Length(max=30)],
    )
    last_name = StringField(
        "Last Name",
        validators=[ InputRequired(), Length(max=30)],
    )

    

class DeleteForm(FlaskForm):
    """leave empty"""


class AddEntryForm(FlaskForm):
    """Add new session entry form"""
    date = DateField("Date",validators=[InputRequired()])
    therapist = QuerySelectField('Therapist',query_factory=lambda: Therapist.query.all(), allow_blank = False, get_label='full_name')
    nrs1 = IntegerRangeField("NRS1", validators=[InputRequired(), NumberRange(min=0, max=100)])
    nrs2 = IntegerRangeField("NRS2", validators=[InputRequired(), NumberRange(min=0, max=100)])
    nrs3 = IntegerRangeField("NRS3", validators=[InputRequired(), NumberRange(min=0, max=100)])
    nrs4 = IntegerRangeField("NRS4", validators=[InputRequired(), NumberRange(min=0, max=100)])
    nrs5 = IntegerRangeField("NRS5", validators=[InputRequired(), NumberRange(min=0, max=100)])
    a_event = TextAreaField("A: Adversity/ Activating Event: Now that you've checked in with yourself, what would you like to start with today?", validators=[InputRequired()])
    beliefs = TextAreaField("Beliefs (About this Adversity):", validators=[InputRequired()])
    c_distortions = SelectMultipleField('Cognitive Distortions', choices=[('All-or-Nothing Thinking / Polarized Thinking','All-or-Nothing Thinking / Polarized Thinking'),('Awfulizing, Catastrophizing','Awfulizing, Catastrophizing'),('Overgeneralization','Overgeneralization'),('Mental Filter','Mental Filter'),('Disqualifying the Positive','Disqualifying the Positive'),('Jumping to Conclusions – Mind Reading', 'Jumping to Conclusions – Mind Reading'),('Jumping to Conclusions – Fortune Telling', 'Jumping to Conclusions – Fortune Telling'),('Magnification (Catastrophizing) or Minimization','Magnification (Catastrophizing) or Minimization'),('Emotional Reasoning', 'Emotional Reasoning'),('Should Statements', 'Should Statements'),('Labeling and Mislabeling', 'Labeling and Mislabeling'),('Personalization', 'Personalization'),('Control Fallacies','Control Fallacies'),('Fallacy of Fairness', 'Fallacy of Fairness'),('Fallacy of Change', 'Fallacy of Change'),('Always Being Right', 'Always Being Right'),('If/Then, Non-sequitur', 'If/Then, Non-sequitur')], option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    c_consequences = SelectMultipleField('C: Consequences: Emotional- Unhealthy Negative Emotions Identified', choices=[('Anger','Anger'),('Anxiety','Anxiety'),('Depression','Depression'),('Guilt','Guilt'),('Shame','Shame'),('Resentment','Resentment'),('Jealousy','Jealousy'),('Panic','Panic')], option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    reactions = TextAreaField("C- Consequences: Behaviors & Reactions", validators=[InputRequired()])

