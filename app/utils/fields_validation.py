from flask_restplus import fields


"""
Skipping None
https://stackoverflow.com/questions/26867357/return-empty-json-object-with-flask-restful-nested-field-object-for-sqlalchemy-a

Accept null values during validation
https://stackoverflow.com/questions/60314378/how-to-accept-none-for-string-type-field-when-using-flask-restplus
"""
class NullableString(fields.String):
    __schema_type__ = ['string', 'null']
    __schema_example__ = 'nullable string'


class NullableInteger(fields.Integer):
    __schema_type__ = ['integer', 'null']
    __schema_example__ = 0

class NullableFloat(fields.Float):
    __schema_type__ = ['number', 'null']
    __schema_example__ = 'nullable float'


"""
Nested with Empty Strings
https://stackoverflow.com/questions/26867357/return-empty-json-object-with-flask-restful-nested-field-object-for-sqlalchemy-a
"""
class NestedWithEmpty(fields.Nested):
    """
    Allows returning an empty dictionary if marshaled value is None
    """
    def __init__(self, nested, allow_empty=False, **kwargs):
        self.allow_empty = allow_empty
        super(NestedWithEmpty, self).__init__(nested, **kwargs)

    def output(self, key, obj):
        value = get_value(key if self.attribute is None else self.attribute, obj)
        if value is None:
            if self.allow_null:
                return None
            elif self.allow_empty:
                return {}

        return marshal(value, self.nested)
