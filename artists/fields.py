from rest_framework import relations


class CharRelatedField(relations.RelatedField):
    """A 'get or create' slug field."""

    default_error_messages = {
        'invalid': 'Invalid value.',
    }

    def __init__(self, slug_field, **kwargs):
        self.slug_field = slug_field
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get_or_create(**{self.slug_field: data})[0]
        except (TypeError, ValueError):
            self.fail('invalid')

    def to_representation(self, obj):
        return getattr(obj, self.slug_field)
