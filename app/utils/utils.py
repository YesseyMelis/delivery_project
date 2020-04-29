import string
import random
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class Pagination(object):
    @classmethod
    def number_of_pages(cls, num_of_instances, instances_per_page=12):
        num_of_pages = (
            (num_of_instances // instances_per_page)
            if num_of_instances % instances_per_page == 0
            else (num_of_instances // instances_per_page) + 1
        )
        return num_of_pages


class CustomDefaultPagination(PageNumberPagination, Pagination):
    page_size = 12

    def get_paginated_response(self, data, *args, **kwargs):
        num_of_instances = self.page.paginator.count
        return Response(
            {
                'data': {
                    'next': self.get_next_link(),
                    'previous': self.get_previous_link(),
                    'page': self.number_of_pages(
                        self.page.paginator.count, self.page_size
                    ),
                    'per_page': self.page_size,
                    'current_page': self.page.number,
                    'total': num_of_instances,
                    'data': data,
                }
            }
        )


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
