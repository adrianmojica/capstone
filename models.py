from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt= Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User."""
    __tablename__ = "users"
    
    username = db.Column(db.String(20), nullable =False, unique=True, primary_key=True)
    password = db.Column(db.Text(), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    bday = db.Column(db.String(20), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    stage = db.Column(db.Integer(), nullable=False, default='1')
    emergency_contact_email = db.Column(db.String(50), nullable=False)
    forms = db.relationship('Form')

    @property
    def full_name(self):
        """full name property"""
        return f"{self.first_name} {self.last_name}"


    
    @classmethod
    def register(cls,username,password,email,bday,first_name,last_name):
        secure = bcrypt.generate_password_hash(password)
        hashed = secure.decode("utf8")
        user = cls(
            username=username,
            password=hashed,
            email = email,
            bday = bday,
            first_name = first_name,
            last_name = last_name
        )

        db.session.add(user)
        return user
    
    @classmethod 
    def authenticate(cls, username, password):
        user = User.query.filter_by(username = username).first()
        if user and bcrypt.check_password_hash(user.password,password):
            return user
        else:
            return False

class Therapist(db.Model):
    """therapist."""
    __tablename__ = "therapists"
    
    username = db.Column(db.String(20), nullable =False, unique=True, primary_key=True)
    password = db.Column(db.Text(), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    @property
    def full_name(self):
        """full name property"""
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def register_therapist(cls,username,password,email,first_name,last_name):
        secure = bcrypt.generate_password_hash(password)
        hashed = secure.decode("utf8")
        therapist = cls(
            username=username,
            password=hashed,
            email = email,
            first_name = first_name,
            last_name = last_name
        )

        db.session.add(therapist)
        return therapist
    
    @classmethod 
    def authenticate_therapist(cls, username, password):
        therapist = Therapist.query.filter_by(username = username).first()
        if therapist and bcrypt.check_password_hash(therapist.password,password):
            return therapist
        else:
            return False



class Form(db.Model):
    """forms."""

    __tablename__ = "forms"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(20),
        db.ForeignKey('users.username'),
        nullable=False,
    )
    date = db.Column(db.String(100), nullable=False)
    therapist = db.Column(db.String(100), nullable=False)
    nrs1 = db.Column(db.Integer(), nullable=False)
    nrs2 = db.Column(db.Integer(), nullable=False)
    nrs3 = db.Column(db.Integer(), nullable=False)
    nrs4 = db.Column(db.Integer(), nullable=False)
    nrs5 = db.Column(db.Integer(), nullable=False)
    a_event = db.Column(db.Text(), nullable=False)
    beliefs = db.Column(db.Text(), nullable=False)
    #distortions
    c_distortions=db.Column(db.Text(), nullable=False)
    # consequences
    c_consequences=db.Column(db.Text(), nullable=False)
    reactions = db.Column(db.Text(), nullable=False)
    user = db.relationship('User')
    #risk assessment
    is_at_risk = db.Column(db.Boolean(), nullable=False)

    



class Reports(db.Model):
    """ Reports """

    __tablename__ = "reports"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),
            db.ForeignKey('users.username'),
            nullable = False,
            )
    date = db.Column(db.Text(), nullable = True)
    


