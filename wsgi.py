import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.models import Landlord
from App.models import Tenant
from App.models import Apartment
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize, create_landlord, create_apartment,create_tenant,create_review )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')
    
# Create a landlord
@user_cli.command("create_landlord", help="Creates a landlord")
@click.argument("user_id",default="1")
@click.argument("first_name", default="rob")
@click.argument("last_name", default="martin")
def create_landlord_command(user_id,first_name, last_name):
    create_landlord(user_id, first_name,last_name)
    print(f' landlord {first_name} {last_name} created!!!!')
    
# Create a tenant
@user_cli.command("create_tenant", help="Creates a tenant")
@click.argument("user_id",default="1")
@click.argument("first_name", default="rob")
@click.argument("last_name", default="martin")
@click.argument("apartment_id",default=1)
def create_tenant_command(user_id, first_name, last_name, apartment_id):
    create_tenant(user_id, first_name, last_name, apartment_id)
    print(f'Tenant {first_name} {last_name} created in apartment {apartment_id}!')
    
# Create an apartment
@user_cli.command("create_apartment", help="Creates an apartment")
@click.option("--landlord-id", default=1, prompt="Landlord ID", type=int)
@click.option("--street", default="street #1", prompt="Address Street")
@click.option("--town", default="Port-Of-Spain", prompt="Address Town")
@click.option("--rent", default=1000.00, prompt="Rent", type=float)
@click.option("--bathrooms", default=2, prompt="Number of bathrooms", type=int)
@click.option("--bedrooms", default=2, prompt="Number of bedrooms", type=int)
@click.option("--image", default="", prompt="Image")
def create_apartment_command(landlord_id,street,town, rent, bathrooms, bedrooms,image):
    create_apartment(landlord_id,street,town, rent, bathrooms, bedrooms, image)
    print(f'Apartment created with {bathrooms} bathrooms and {bedrooms} bedrooms!')


# Create a review
@user_cli.command("create_review", help="Creates a review")
@click.option("--tenant-id", default=1, prompt="tenant ID", type=int)
@click.option("--apartment-id", default=1, prompt="apartment ID", type=int)
@click.option("--comment", default="", prompt="comment")
@click.option("--rating", default=10, prompt="Rating", type=int)
def create_review_command(tenant_id, apartment_id, comment, rating):
    create_review(tenant_id, apartment_id, rating,comment)
    print(f'Review created for apartment {apartment_id} with rating {rating}!')


# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)
