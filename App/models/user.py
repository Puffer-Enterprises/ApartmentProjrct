from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

class Landlord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(90),nullable=False)
    last_name = db.Column(db.String(90),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def get_json(self):
        return{
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name
        }


class Apartment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    landlord_id = db.Column(db.Integer, db.ForeignKey('landlord.id'), nullable=False)
    street = db.Column(db.String(100), nullable=False)
    town = db.Column(db.String(100), nullable=False)
    rent = db.Column(db.Float, nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False)
    bathrooms = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(255), nullable=True)
    
    def get_json(self):
        return{
            'id': self.id,
            'street': self.street,
            'town': self.town,
            'rent': self.rent
        }
    
class Tenant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id'), nullable=False)
    first_name = db.Column(db.String(90),nullable=False)
    last_name = db.Column(db.String(90),nullable=False)
    
    def get_json(self):
        return{
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name
        }

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'), nullable=False)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(255), nullable=True)
    
    def get_json(self):
        return{
            'id': self.id,
            'rating': self.rating,
            'comment': self.comment
        }
