from app.extensions import ma
from app.models import CareerSession

class CareerSessionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CareerSession
        load_instance = True
        include_fk = True

session_schema = CareerSessionSchema()
sessions_schema = CareerSessionSchema(many=True)
