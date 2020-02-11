from django.test import TestCase
from .factories import ProductFactory
from ewardrobe_app.queries.products import ProductsQuery


class ProductQueryTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        ProductFactory.create_batch(40)

    def test_products_query_next_page(self):
        page_object, links = ProductsQuery(
            page_number=1, paginate_by=10
        ).get_products_and_links()
        assert len(page_object.object_list) == 10
        assert links.get("next")
        assert not links.get("previous")

    def test_products_query_previous_and_next_page(self):
        page_object, links = ProductsQuery(
            page_number=2, paginate_by=10
        ).get_products_and_links()
        assert len(page_object.object_list) == 10
        assert links.get("next")
        assert links.get("previous")

    def test_products_query_q_page(self):
        page_object, links = ProductsQuery(
            page_number=1, paginate_by=10, q="fake"
        ).get_products_and_links()
        assert len(page_object.object_list) == 0
        assert not links.get("next")
        assert not links.get("previous")

    def test_products_query_q_next_page(self):
        page_object, links = ProductsQuery(
            page_number=1, paginate_by=20, q="test"
        ).get_products_and_links()
        assert len(page_object.object_list) == 20
        assert page_object.paginator.count == 40
        assert links.get("next")
        assert not links.get("previous")

    def test_products_query_q_previous_and_next_page(self):
        page_object, links = ProductsQuery(
            page_number=2, paginate_by=20, q="test"
        ).get_products_and_links()
        assert len(page_object.object_list) == 20
        assert page_object.paginator.count == 40
        assert not links.get("next")
        assert links.get("previous")
