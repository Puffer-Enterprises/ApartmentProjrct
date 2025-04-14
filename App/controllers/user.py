from App.models import User
from App.database import db
from App.models import Landlord
from App.models import Tenant
from App.models import Apartment
from App.models import Review

def create_user(username, password):
    newuser = User(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None

def create_landlord(user_id,first_name,last_name):
    landlord = Landlord(user_id=user_id,first_name=first_name,last_name=last_name)
    db.session.add(landlord)
    db.session.commit()
    return landlord

def create_apartment(landlord_id,address,rent,bedrooms,bathrooms):
    apartment = Apartment(landlord_id=landlord_id,address=address,rent=rent,bedrooms=bedrooms,bathrooms=bathrooms)
    db.session.add(apartment)
    db.session.commit()
    return apartment
    
def create_tenant(user_id, first_name, last_name, apartment_id):
    tenant = Tenant(user_id=user_id, first_name=first_name, last_name=last_name, apartment_id=apartment_id)
    db.session.add(tenant)
    db.session.commit()
    return tenant

def get_all_landlords_json():
    landlords = Landlord.query.all()
    if not landlords:
        return []
    landlords = [landlord.get_json() for landlord in landlords]
    return landlords

def create_review(tenant_id,apartment_id,rating,comment):
    review = Review(tenant_id=tenant_id,apartment_id=apartment_id,rating=rating,comment=comment)
    db.session.add(review)
    db.session.commit()
    return review

def get_all_apartments_json():
    apartments = Apartment.query.all()
    if not apartments:
        return []
    apartments = [apartment.get_json() for apartment in apartments]
    return apartments

def get_all_tenants_json():
    tenants = Tenant.query.all()
    if not tenants:
        return []
    tenants = [tenant.get_json() for tenant in tenants]
    return tenants

def get_all_reviews_json():
    reviews = Review.query.all()
    if not reviews:
        return []
    reviews = [review.get_json() for review in reviews]
    return reviews