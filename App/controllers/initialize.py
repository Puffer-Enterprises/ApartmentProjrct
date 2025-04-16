from .user import create_user,create_landlord, create_apartment, create_tenant, create_review

from App.database import db
import csv


def initialize():
    db.drop_all()
    db.create_all()
    user_data()
    landlord_data()
    tenant_data()
    apartment_data()
    review_data()
    
def user_data():
  with open('App/Users.csv') as file:
    reader = csv.DictReader(file)
    for row in reader:
        user = create_user(row['username'], row['password'])
        db.session.add(user)
    db.session.commit()
    print("User data load successful")
    
def landlord_data():
  with open('App/Landlords.csv') as file:
    reader = csv.DictReader(file)
    for row in reader:
        landlord = create_landlord(row['user_id'], row['first_name'], row['last_name'])
        db.session.add(landlord)
    db.session.commit()
    print("Landlord data load successful")
    
def tenant_data():
  with open('App/Tenants.csv') as file:
    reader = csv.DictReader(file)
    for row in reader:
        tenant = create_tenant(row['user_id'], row['first_name'], row['last_name'], row['apartment_id'])
        db.session.add(tenant)
    db.session.commit()
    print("Tenant data load successful")
    
def apartment_data():
  with open('App/Apartments.csv') as file:
    reader = csv.DictReader(file)
    for row in reader:
        apartment = create_apartment(row['landlord_id'], row['street'], row['town'], row['rent'], row['bedrooms'], row['bathrooms'], row['image'])
        db.session.add(apartment)
    db.session.commit()
    print("Apartment data load successful")

def review_data():
  with open('App/Reviews.csv') as file:
    reader = csv.DictReader(file)
    for row in reader:
        review = create_review(row['tenant_id'], row['apartment_id'], row['rating'], row['comment'])
        db.session.add(review)
    db.session.commit()
    print("Review data load successful")

