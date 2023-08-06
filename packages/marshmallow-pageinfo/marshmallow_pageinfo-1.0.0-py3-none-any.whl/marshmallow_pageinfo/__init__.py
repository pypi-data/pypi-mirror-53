from marshmallow import Schema, fields, EXCLUDE

__all__ = ('PAGE_INFO_SCHEMA', 'PageInfoSchema',)


class PageInfoSchema(Schema):
    page = fields.Integer(missing=1)
    per_page = fields.Integer(data_key='perPage', missing=10)
    total = fields.Integer()
    pages = fields.Integer(data_key='totalPages')
    has_next = fields.Boolean(data_key='hasNext')
    has_prev = fields.Boolean(data_key='hasPrev')

    class Meta:
        unknown = EXCLUDE
        dump_only = ('total', 'pages', 'has_next', 'has_prev')


PAGE_INFO_SCHEMA = PageInfoSchema()
