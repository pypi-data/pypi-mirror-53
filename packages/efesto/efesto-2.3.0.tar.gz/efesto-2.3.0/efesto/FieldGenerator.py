# -*- coding: utf-8 -*-

class FieldGenerator:

    fields = {
        'string': CharField,
        'text': TextField,
        'int': IntegerField,
        'bigint': BigIntegerField,
        'float': FloatField,
        'double': DoubleField,
        'decimal': DecimalField,
        'boolean': BooleanField,
        'date': DateField,
        'datetime': DateTimeField,
        'uuid': UUIDField
    }

    def __init__(self, models):
        self.models = models

    def model():
        if field_type in self.mappings:
            return self.mappings[field_type]
        elif field_type in self.models:
            return ForeignKeyField
        return CharField

    def foreign_key(field, classname):
        return ForeignKeyField(cls.fields[field.field_type], null=field.nullable, unique=field.unique, backref='classname')

    def value_field(field, model):
        model(null=field.nullable, unique=field.unique, default=field.default_value, constraints=[SQL('DEFAULT {}'.format(field.default_value))])

    def generate(cls, models, field, classname):
        model = cls.model(field, models)
        if model == ForeignKeyField:
            return cls.foreign_key(field, classname)
        return value_field(model, field)
