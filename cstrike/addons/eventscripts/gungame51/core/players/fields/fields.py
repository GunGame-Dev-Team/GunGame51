# ../core/players/fields/fields.py

'''
$Rev$
$LastChangedBy$
$LastChangedDate$
'''

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame Imports
from exceptions import ValidationError
from validators import *


# =============================================================================
# >> CLASSES
# =============================================================================
class PlayerField(object):
    def __init__(self, validators=[]):
        self.validators = validators or []

    def run_validators(self, value):
        errors = []
        for validator in self.validators:
            try:
                validator(value)
            except ValidationError, e:
                [errors.append(msg) for msg in e.messages]
        if errors:
            raise ValidationError(errors)


class IntegerField(PlayerField):
    def __init__(self, min_value=None, max_value=None, *args, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        super(IntegerField, self).__init__(*args, **kwargs)

        # Validators
        if min_value is not None:
            self.validators.append(MinValueValidator(min_value))
        if max_value is not None:
            self.validators.append(MaxValueValidator(max_value))

    def to_python(self, value):
        try:
            value = int(value)
        except (ValueError, TypeError):
            raise ValidationError('An integer is required: value of "%s" ' % (
                                  value) + 'given of type "%s".' % (
                                  type(value).__name__))
        self.run_validators(value)
        return value


class StringField(PlayerField):
    def __init__(self, min_length=None, max_length=None, *args, **kwargs):
        self.min_length, self.max_length = min_length, max_length
        super(StringField, self).__init__(*args, **kwargs)

        # Validators
        if min_length is not None:
            self.validators.append(MinLengthValidator(min_length))
        if max_length is not None:
            self.validators.append(MaxLengthValidator(max_length))

    def to_python(self, value):
        value = str(value)
        self.run_validators(value)
        return value


class InstanceField(PlayerField):
    def __init__(self, instance=None, *args, **kwargs):
        self.instance = instance
        super(InstanceField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, self.instance):
            return value
        raise ValidationError('This field is required to be a ' +
                              '%s instance' % self.instance)
