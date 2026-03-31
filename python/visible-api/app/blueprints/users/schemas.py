from app.extensions import ma
from app.models import VisibleUser

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = VisibleUser
        load_instance = True
        exclude = ('password',)

class UserLoginSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = VisibleUser
        load_instance = False
        fields = ('email', 'password')

user_schema = UserSchema()
users_schema = UserSchema(many=True)
user_login_schema = UserLoginSchema()