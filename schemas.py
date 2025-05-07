from marshmallow import Schema, fields, validate, ValidationError

class LibraryItemSchema(Schema):
    uid = fields.Int(required=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    writer = fields.Str(required=True, validate=validate.Length(min=1))
    published = fields.Int(required=True)
