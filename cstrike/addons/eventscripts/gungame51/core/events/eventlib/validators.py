# =============================================================================
# IMPORTS
# =============================================================================
# Eventlib Imports
from exceptions import ValidationError


# =============================================================================
# CLASSES
# =============================================================================
class MinValueValidator(object):
    """Validates that a value is greater than or equal to the set minimum."""
    def __init__(self, value):
        self.value = value

    def __call__(self, check_value):
        if check_value < self.value:
            raise ValidationError('The value given (%s) must ' % check_value +
                                  'be greater than or equal to ' +
                                  '%s.' % self.value)


class MaxValueValidator(object):
    """Validates that a value is less than or equal to the set minimum."""
    def __init__(self, value):
        self.value = value

    def __call__(self, check_value):
        if check_value > self.value:
            raise ValidationError('The value given (%s) must ' % check_value +
                                  'be less than or equal to %s.' % self.value)


class MinLengthValidator(object):
    """Validates that the length of a value is greater than or equal to the
    minimum.

    """
    def __init__(self, value):
        self.value = value

    def __call__(self, check_value):
        if len(check_value) < self.value:
            raise ValidationError('Ensure this value has at least ' +
                                  '%d characters (it has %d).' % (self.value,
                                  len(check_value)))


class MaxLengthValidator(object):
    """Validates that the length of a value is less than or equal to the
    minimum.

    """
    def __init__(self, value):
        self.value = value

    def __call__(self, check_value):
        if len(check_value) > self.value:
            raise ValidationError('Ensure this value has at most ' +
                                  '%d characters (it has %d).' % (self.value,
                                  len(check_value)))
