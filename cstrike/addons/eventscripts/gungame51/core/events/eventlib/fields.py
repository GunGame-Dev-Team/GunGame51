# =============================================================================
# IMPORTS
# =============================================================================
# Eventlib Imports
from validators import *


# =============================================================================
# GLOBAL VARIABLES/CONSTANTS
# =============================================================================
__all__ = ['EventField', 'BooleanField', 'ByteField', 'ShortField',
           'LongField', 'FloatField', 'StringField']
DATAKEYS = {'bool': int, 'byte': int, 'short': int, 'long': int,
            'float': float, 'string': str}


# =============================================================================
# CLASSES
# =============================================================================
class EventField(object):
    """The parent class of all event fields."""
    # Used to maintain order
    creation_counter = 0

    def __init__(self, data_key=None, comment='', validators=[]):
        # Set the validators
        self.validators = validators or []

        # Validate the data key
        data_key = str(data_key).lower()
        if data_key in DATAKEYS:
            self.data_key = data_key
        else:
            raise ESEventError('Invalid data key: %s. Expected ' % data_key +
                               '%s.' % str(', ').join(DATAKEYS.keys()))
        # Set the comment
        self.comment = str(comment)

        # Increase the creation counter
        self.creation_counter = EventField.creation_counter
        EventField.creation_counter += 1

    def run_validators(self, value):
        """Calls each validator and raises a single ValidationError for any
        errors that occur.

        """
        errors = []
        for validator in self.validators:
            try:
                validator(value)
            except ValidationError, e:
                [errors.append(msg) for msg in e.messages]
        if errors:
            raise ValidationError(errors)


class IntegerField(EventField):
    """EventField that the ByteField, ShortField, LongField, and FloatField
    inherits which adds the min_value and max_value validators.

    """
    def __init__(self, max_value=None, min_value=None, *args, **kwargs):
        self.max_value, self.min_value = max_value, min_value
        super(IntegerField, self).__init__(*args, **kwargs)

        if max_value is not None:
            self.validators.append(MaxValueValidator(max_value))
        if min_value is not None:
            self.validators.append(MinValueValidator(min_value))

    def is_valid(self, value):
        """Returns if the value given is a valid type for this EventField."""
        return isinstance(value, int)

    def to_python(self, value):
        """Validates that int() can be called on the input. Returns the result
        of int().

        """
        try:
            value = int(str(value))
        except (ValueError, TypeError):
            raise ValidationError('An integer is required.')
        return value


class BooleanField(EventField):
    """Event Field that validates the boolean type. This field must always be a
    boolean value.

    """
    def __init__(self, *args, **kwargs):
        super(BooleanField, self).__init__(data_key='bool', *args, **kwargs)

    def is_valid(self, value):
        """Returns if the value given is a valid type for this EventField."""
        if isinstance(value, bool):
            return True
        elif value in (0, 1):
            return True
        else:
            return False

    def to_python(self, value):
        """Returns a Python boolean value as an integer."""
        value = bool(value)
        self.run_validators(value)
        # Coerce to int() type for the Source engine
        return int(value)


class ByteField(IntegerField):
    """Event Field that validates the byte type. This field must always be an
    integer value. Minimum value is -128. Maximum value is 127.

    """
    def __init__(self, *args, **kwargs):
        validators = [MaxValueValidator(127), MinValueValidator(-128)]
        super(ByteField, self).__init__(validators=validators, data_key='byte',
                                        *args, **kwargs)

    def to_python(self, value):
        """Validates that int() can be called on the input. Returns the result
        of int().

        """
        value = super(ByteField, self).to_python(value)
        self.run_validators(value)
        return value


class ShortField(IntegerField):
    """Event Field that validates the short type. This field must always be an
    integer value. Minimum value is -32768. Maximum value is 32767.

    """
    def __init__(self, *args, **kwargs):
        validators = [MaxValueValidator(32767), MinValueValidator(-32768)]
        super(ShortField, self).__init__(validators=validators,
                                         data_key='short', *args, **kwargs)

    def to_python(self, value):
        """Validates that int() can be called on the input. Returns the result
        of int().

        """
        value = super(ShortField, self).to_python(value)
        self.run_validators(value)
        return value


class LongField(IntegerField):
    """Event Field that validates the long type. This field must always be an
    integer value. Minimum value is -2147483648. Maximum value is 2147483647.

    """
    def __init__(self, *args, **kwargs):
        validators = [MaxValueValidator(2147483647),
                      MinValueValidator(-2147483648)]
        super(LongField, self).__init__(validators=validators, data_key='long',
                                        *args, **kwargs)

    def to_python(self, value):
        """Validates that int() can be called on the input. Returns the result
        of int().

        """
        value = super(LongField, self).to_python(value)
        self.run_validators(value)
        return value


class FloatField(IntegerField):
    """Event Field that validates the float type. This field must always be an
    float value.

    """
    def __init__(self, *args, **kwargs):
        super(FloatField, self).__init__(data_key='float', *args, **kwargs)

    def is_valid(self, value):
        """Returns if the value given is a valid type for this EventField."""
        return isinstance(value, float)

    def to_python(self, value):
        """Validates that float() can be called on the input. Returns the
        result of float().

        """
        try:
            value = float(value)
        except (ValueError, TypeError):
            raise ValidationError('A float is required.')
        self.run_validators(value)
        return value


class StringField(EventField):
    """Event Field that validates the string type. This field must always be an
    string value.

    """
    def __init__(self, max_length=None, min_length=None, *args, **kwargs):
        self.max_length, self.min_length = max_length, min_length
        super(StringField, self).__init__(data_key='string', *args, **kwargs)

        if max_length is not None:
            self.validators.append(MaxLengthValidator(max_length))
        if min_length is not None:
            self.validators.append(MinLengthValidator(min_length))

    def is_valid(self, value):
        """Returns if the value given is a valid type for this EventField."""
        return isinstance(value, str)

    def to_python(self, value):
        """Converts the input to a string."""
        value = str(value)
        self.run_validators(value)
        return value
