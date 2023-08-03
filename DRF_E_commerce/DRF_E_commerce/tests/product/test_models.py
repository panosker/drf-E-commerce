"""
Components of building the test (AAA)
    Arrange (gather all the resources-units that we need)
    Act (perform an action)
    Assert  (Testing to make sure that the outcome of the Action is exactly what expected)
"""
import pytest

# so the tests can have acces to the database
pytestmark = pytest.mark.django_db


class TestCategoryModel:
    def test_str_method(self, category_factory):
        # Arrange
        data_generated = category_factory(names="test_category")
        # Assert ( going to return true or false for the generated_data)
        assert data_generated.__str__() == "test_category"


class TestBrandModel:
    def test_str_method(self, brand_factory):
        data = brand_factory(names="test_brand")
        assert data.__str__() == "test_brand"


class TestProductModel:
    def test_str_method(self, product_factory):
        obj = product_factory(names="test_product")
        assert obj.__str__() == "test_product"


# if all passed check pytest --cov
