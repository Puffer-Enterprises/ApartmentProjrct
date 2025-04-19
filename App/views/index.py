from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify,url_for
from App.controllers import create_user, initialize
from App.models import Tenant,User,Landlord,Apartment,Review
from flask_jwt_extended import jwt_required, current_user,get_jwt_identity,verify_jwt_in_request
from App.database import db

index_views = Blueprint('index_views', __name__, template_folder='../templates')




@index_views.route('/', methods=['GET'])
def index_page():
    apartments = Apartment.query.all()
    return render_template('index.html', show_search=True
, apartments=apartments)

@index_views.route('/check')
@jwt_required()
def check():
    apartments = Apartment.query.all()
    user = current_user
    tenants = Tenant.query.all()
    landlords = Landlord.query.all()
    tenant_boolean = False
    landlord_boolean = False
    for t in tenants:
        if t.user_id == user.id:
            tenant_boolean = True

    for l in landlords:
        if l.user_id == user.id:
            landlord_boolean = True
    
    tenant = Tenant.query.filter_by(user_id=user.id).first()
    user_apartment2 = Apartment.query.filter_by(id=tenant.apartment_id).first() if tenant else None
    landlord_apartments = Apartment.query.filter_by(landlord_id=user.id).all()
    return render_template('index.html', apartments=apartments, landlord_boolean=landlord_boolean, tenant_boolean=tenant_boolean, user_apartment2=user_apartment2, landlord_apartments=landlord_apartments, tenants=tenants, landlords=landlords, show_search=True
)

@index_views.route('/apartments/<apartment_id>') 
@jwt_required()
def apartment_details(apartment_id):
    selected_apartment = Apartment.query.get(apartment_id)
    reviews = Review.query.filter_by(apartment_id=apartment_id).all()
    reviews2 = Review.query.all()
    tenant = Tenant.query.filter_by(user_id=current_user.id).first()
    user_apartment = Apartment.query.filter_by(id=tenant.apartment_id).first() if tenant else None
    tenants = Tenant.query.all()
    landlords = Landlord.query.all()
    landlord_apartment = Apartment.query.filter_by(landlord_id=current_user.id).first()
    return render_template('index.html', reviews=reviews, show_search=False
, selected_apartment=selected_apartment, reviews2=reviews2,user_apartment=user_apartment,tenant=tenant,tenants=tenants,landlords=landlords,landlord_apartment=landlord_apartment)


@index_views.route('/apartments/<apartment_id>/<tenant_id>/review', methods=['POST'])
def add_review(apartment_id, tenant_id):
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    review = Review(rating=rating, comment=comment, apartment_id=apartment_id, tenant_id=tenant_id)
    db.session.add(review)
    db.session.commit()
    return redirect(url_for('index_views.apartment_details', apartment_id=apartment_id))


@index_views.route('/apartments/add', methods=['POST'])
@jwt_required()
def add_apartment():
    user = current_user
    landlord = Landlord.query.filter_by(user_id=user.id).first()
    if not landlord:
        flash('Only landlords can add apartments.')
        return

    street = request.form.get('street')
    town = request.form.get('town')
    rent = request.form.get('rent')
    bedrooms = request.form.get('bedrooms')
    bathrooms = request.form.get('bathrooms')
    image = request.form.get('image')

    new_apartment = Apartment(
        landlord_id=landlord.id,
        street=street,
        town=town,
        rent=rent,
        bedrooms=bedrooms,
        bathrooms=bathrooms,
        image=image
    )

    db.session.add(new_apartment)
    db.session.commit()

    return redirect(url_for('index_views.check'))

@index_views.route('/apartments/search', methods=['GET'])
def search_apartments():
    town = request.args.get('town')
    min_bedrooms = request.args.get('min_bedrooms')
    min_bathrooms = request.args.get('min_bathrooms')
    max_rent = request.args.get('max_rent')

    query = Apartment.query

    if town:
        query = query.filter(Apartment.town.ilike(f"%{town}%"))
    if min_bedrooms:
        query = query.filter(Apartment.bedrooms >= int(min_bedrooms))
    if min_bathrooms:
        query = query.filter(Apartment.bathrooms >= int(min_bathrooms))
    if max_rent:
        query = query.filter(Apartment.rent <= float(max_rent))

    apartments = query.all()

    return render_template('search.html', apartments=apartments)


@index_views.route('/apartments/<apartment_id>/delete', methods=['POST'])
@jwt_required()
def delete_apartment(apartment_id):
    apartment = Apartment.query.get(apartment_id)
    if not apartment:
        return redirect(url_for('index_views.apartment_details', apartment_id=apartment_id))
    
    db.session.delete(apartment)
    db.session.commit()
    return redirect(url_for('index_views.check'))


@index_views.route('/deleteReview/<review_id>')
@jwt_required()
def delete_review(review_id):
    review = Review.query.get(review_id)
    if not review:
        return redirect(url_for('index_views.apartment_details', apartment_id=review.apartment_id))
    
    db.session.delete(review)
    db.session.commit()
    return redirect(url_for('index_views.apartment_details', apartment_id=review.apartment_id))

@index_views.route('/init', methods=['GET'])
def init():
    initialize()
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})
