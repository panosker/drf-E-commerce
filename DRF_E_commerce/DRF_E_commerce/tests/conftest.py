import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from .factories import BrandFactory, CategoryFactory, ProductFactory

register(CategoryFactory)
# to access the CategoryFactory --> category_factory after the format is done
register(BrandFactory)
register(ProductFactory)

# provides a way to include the resources that we created more than once


@pytest.fixture
def api_client():
    return APIClient
