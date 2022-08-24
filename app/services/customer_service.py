import uuid
import datetime

from app import db
# from app.models import Customer, CustomerSchema

# customer_schema = CustomerSchema()
# customers_schema = CustomerSchema(many=True)

# def save_new_customer(data):
#     customer = Customer.query.filter_by(ext_key=data['ext_key']).first() # check for existing customer
#     if not customer:
#         new_customer = Customer(
#             ext_key=data['ext_key'], 
#             party_type=data['party_type'], 
#             name_first=data['name_first'],
#             name_last = data['name_last'],
#             province = data['province'],
#             city = data['city'],
#             village = data['village'],
#             address = data['address'],
#             gender = data['gender']
#             )
#         save_changes(new_customer)
#         response_object = {
#             'status': 'success',
#             'message': 'Successfully registered.',
#             'customer': data['ext_key']
#         }
#         return response_object, 201
#     else:
#         # update user details
#         # print(customer.id) existing customer
#         print(data['ext_key'])
#         existing_customer = Customer.query.get(data['ext_key'])
        
#         db.session.commit()
        
#         response_object = {
#             'customer': data['ext_key'],
#             'status': 'User Already Exist',
#             'message': 'User Details updated',
#         }
#         return response_object, 409

# def save_new_transactions(data):
#     pass


# def get_all_customers():
#     all_customers = Customer.query.all()
#     result = customers_schema.dump(all_customers)
#     return result

# def get_a_customer(id):
#     return Customer.query.filter_by(id=id).first()

# def save_changes(data):
    # db.session.add(data)
    # db.session.commit()