import marshmallow
from marshmallow import Schema, fields
from marshmallow.decorators import post_load


class NameSchema(Schema):
    first = fields.String(required=True)
    last = fields.String(required=True)
    class Meta:
        unknown = marshmallow.EXCLUDE


class LocationSchema(Schema):
    state = fields.String(required=True)
    class Meta:
        unknown = marshmallow.EXCLUDE

class DoBSchema(Schema):
    age = fields.Int(required=True)
    class Meta:
        unknown = marshmallow.EXCLUDE


class UserSchema(Schema):
    """
    need gender, first name, last name, state, and age

    """

    gender = fields.String(required=True)
    name = fields.Nested(NameSchema)
    location = fields.Nested(LocationSchema)
    dob = fields.Nested(DoBSchema)


    class Meta:
        unknown = marshmallow.EXCLUDE

    @post_load
    def flatten_properties(self, data, **kwargs):
        return {
            'gender': data['gender'],
            'first_name':  data['name']['first'],
            'last_name': data['name']['last'],
            'state': data['location']['state'],
            'age': data['dob']['age'],
        }


class UserListSchema(Schema):
    results = fields.List(fields.Nested(UserSchema))
    info = fields.Mapping()

