from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify,url_for
from App.controllers import create_user, initialize
from App.models import Tenant,User,Landlord,Apartment,Review
from flask_jwt_extended import jwt_required, current_user,get_jwt_identity,verify_jwt_in_request
from App.database import db

index_views = Blueprint('index_views', __name__, template_folder='../templates')




@index_views.route('/', methods=['GET'])
def index_page():
    apartments = Apartment.query.all()
    return render_template('index.html', apartments=apartments)

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
    
    return render_template('index.html', apartments=apartments, landlord_boolean=landlord_boolean, tenant_boolean=tenant_boolean, user_apartment2=user_apartment2)

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
    return render_template('index.html', reviews=reviews,selected_apartment=selected_apartment, reviews2=reviews2,user_apartment=user_apartment,tenant=tenant,tenants=tenants,landlords=landlords)


@index_views.route('/apartments/<apartment_id>/<tenant_id>/review', methods=['POST'])
def add_review(apartment_id, tenant_id):
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    review = Review(rating=rating, comment=comment, apartment_id=apartment_id, tenant_id=tenant_id)
    db.session.add(review)
    db.session.commit()
    return redirect(url_for('index_views.apartment_details', apartment_id=apartment_id))

@index_views.route('/init', methods=['GET'])
def init():
    initialize()
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})
