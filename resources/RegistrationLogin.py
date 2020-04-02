from main import Resource,api,fields, create_access_token
from models.UserModel import UserModel,user_schema
from werkzeug.security import generate_password_hash

ns_registration = api.namespace('register', description="Register details")
ns_userLogin = api.namespace('login', description="Login details")

a_user_model = api.model('User',{
    'full_name':fields.String(),
    'email':fields.String(),
    'password':fields.String(),
})

login_model = api.model('LoginCredentials',{
    'email':fields.String(),
    'password':fields.String()
})


@ns_registration.route('')
class RegisterUser(Resource):
    @api.expect(a_user_model)
    def post(self):
        """Add a new user"""
        data = api.payload
        user = UserModel(full_name=data['full_name'], email=data['email'],
                            password=generate_password_hash(data['password']))
        record = user.create_record()
        return user_schema.dump(record), 201


@ns_userLogin.route('')
class Login(Resource):

    @api.expect(login_model)
    def post(self):
        """use this endpoint to authenticate users"""
        data = api.payload
        if u'email' not in data or u'password' not in data:
            return {"message":"server cannot or will not process the request due to an apparent client error"},400
        else:
            if UserModel.check_email_exists(data['email']):
                if UserModel.validate_password(data['email'],data['password']):
                    # after a successfully login
                    uid = UserModel.get_userId(data['email'])
                    token = create_access_token(identity=uid)
                    return {"access_token":token}, 200
                else:
                    return {"message":"incorrect login credentials"}, 401
            else:
                return {"message":"incorrect login credentials"}, 401

        
        

