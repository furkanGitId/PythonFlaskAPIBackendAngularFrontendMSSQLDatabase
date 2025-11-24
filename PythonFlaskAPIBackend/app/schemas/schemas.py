from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    """Schema for validating user data (CRUD operations)."""
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    email = fields.Email(required=True)

    class Meta:
        strict = True


class UserLoginSchema(Schema):
    """Schema for login credentials."""
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    password = fields.Str(required=True, validate=validate.Length(min=1))

    class Meta:
        strict = True
