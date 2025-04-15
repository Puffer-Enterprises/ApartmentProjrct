from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.controllers import create_user, initialize
from App.models import Tenant,User,Landlord
from flask_jwt_extended import jwt_required, current_user,get_jwt_identity,verify_jwt_in_request

index_views = Blueprint('index_views', __name__, template_folder='../templates')




@index_views.route('/', methods=['GET'])
def index_page():
    tenants = Tenant.query.all()
    verify_jwt_in_request(optional=True)
    user_id = get_jwt_identity()
    landlords = Landlord.query.all()
    tenant_bool = False
    landlord_bool = False
    for t in tenants:
        if t.user_id == user_id:
            tenant_bool = True

    for l in landlords:
        if l.user_id == user_id:
            landlord_bool = True

    return render_template('index.html',tenants=tenants,landlord_bool=landlord_bool,tenant_bool=tenant_bool)

@index_views.route('/init', methods=['GET'])
def init():
    initialize()
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})
