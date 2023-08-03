import factory

from DRF_E_commerce.product.models import Brand, Category, Product


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    # every time we want more than one batch it will change the number
    names = factory.sequence(lambda n: "Category_%d" % n)


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    # because unique=true in models the names can t be  "test_brand"
    names = factory.sequence(lambda n: "Brand_%d" % n)


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    names = "test_product"
    description = "test_description"
    is_digital = True
    # because there is a relationship in models we need to initiate a new brand and category
    brand = factory.SubFactory(BrandFactory)
    category = factory.SubFactory(CategoryFactory)
