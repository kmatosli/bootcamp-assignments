from app.extensions import ma
from app.models import Resource

class ResourceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Resource
        load_instance = True

resource_schema = ResourceSchema()
resources_schema = ResourceSchema(many=True)
