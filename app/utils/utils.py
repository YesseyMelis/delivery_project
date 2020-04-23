import string
import random


def generate_random_string(length=8):
    """
    :param length: length of string
    :return: random string of letters & digits
    """
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(length))


def get_or_none(model, **kwargs):
    """
    :param model: name of the Model
    :param kwargs: lookup_fields
    :return: instance or None
    """
    try:
        obj = model.objects.get(**kwargs)
    except model.DoesNotExist:
        obj = None
    return obj