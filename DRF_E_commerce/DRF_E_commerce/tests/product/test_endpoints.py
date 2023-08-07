import json

import pytest

# so the tests can have acces to the database
pytestmark = pytest.mark.django_db


class TestCategoryEndpoints:
    endpoint = "/api/category/"

    def test_category_get(self, category_factory, api_client):
        # arrange
        # going to create 4 new batches in our test database
        category_factory.create_batch(4)
        # act
        response = api_client().get(self.endpoint)
        # assert
        # test the status code , you can try an other code
        assert response.status_code == 200
        # json loads will parse out json into a python list
        # the number of the list should equal to 4
        assert len(json.loads(response.content)) == 4


class TestBrandEndpoints:
    endpoint = "/api/brand/"

    def test_brand_get(self, brand_factory, api_client):
        brand_factory.create_batch(10)
        response = api_client().get(self.endpoint)
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 10


class TestProductEndpoints:
    endpoint = "/api/product/"

    def test_product_get(self, product_factory, api_client):
        product_factory.create_batch(4)
        response = api_client().get(self.endpoint)
        assert response.status_code == 200
        # we can change
        assert len(json.loads(response.content)) == 4
