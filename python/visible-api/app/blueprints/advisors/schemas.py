from app.extensions import ma
from app.models import Advisor

class AdvisorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Advisor
        load_instance = True
        exclude = ('password',)

class AdvisorLoginSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Advisor
        load_instance = False
        fields = ('email', 'password')

advisor_schema = AdvisorSchema()
advisors_schema = AdvisorSchema(many=True)
advisor_login_schema = AdvisorLoginSchema()