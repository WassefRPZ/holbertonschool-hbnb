from app import db, bcrypt
from app.models.base_model import BaseModel
from sqlalchemy.ext.hybrid import hybrid_property

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    places = db.relationship('Place', backref='owner', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = bool(is_admin)

    @hybrid_property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if value is None:
            raise ValueError("Invalid first name")
        v = value.strip()
        if not v or len(v) > 50:
            raise ValueError("Invalid first name")
        self._first_name = v
    @hybrid_property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if value is None:
            raise ValueError("Invalid last name")
        v = value.strip()
        if not v or len(v) > 50:
            raise ValueError("Invalid last name")
        self._last_name = v

    @hybrid_property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if value is None:
            raise ValueError("Invalid email")
        v = value.strip().lower()
        if (not v) or (' ' in v) or ('@' not in v) or ('.' not in v):
            raise ValueError("Invalid email")
        self._email = v
    @hybrid_property
    def password(self):
        """
        Get the user's password.
        """
        return self._password
    
    @password.setter
    def password(self, value):
        """
        Set the user's password.
        """
        if not value or len(value) < 8:
            raise ValueError('Password must be at least 8 characters.')
        if len(value) > 255:
            raise ValueError('Password must be less than 255 characters.')
        self.hash_password(value)

    def hash_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        return {
            "id_user": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
        }
