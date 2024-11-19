import pytest


@pytest.mark.django_db
class TestProduct:

    def test_product_verbose_name_fields(self, product_factory):
        product = product_factory.create()
        assert product._meta.get_field("name").verbose_name == "название товара"
        assert product._meta.get_field("description").verbose_name == "описание товара"
        assert product._meta.get_field("price").verbose_name == "цена товара"
        assert (
            product._meta.get_field("count_reviews").verbose_name
            == "количество отзывов"
        )
        assert (
            product._meta.get_field("limited_edition").verbose_name
            == "ограниченный тираж"
        )
        assert (
            product._meta.get_field("count_goods").verbose_name == "количество товара"
        )
        assert (
            product._meta.get_field("free_delivery").verbose_name
            == "бесплатная доставка"
        )
        assert (
            product._meta.get_field("number_of_purchases").verbose_name
            == "количество покупок товара"
        )
        assert (
            product._meta.get_field("active_product").verbose_name
            == "активность товара"
        )
        assert (
            product._meta.get_field("date_product").verbose_name
            == "дата поступления товара"
        )

    def test_product_length_fields(self, product_factory):
        product = product_factory.create()
        assert product._meta.get_field("name").max_length == 1000
        assert product._meta.get_field("description").max_length == 10000

    def test_product_blank_fields(self, product_factory):
        product = product_factory.create()
        assert product._meta.get_field("tags").blank is True
        assert product._meta.get_field("category").blank is True
        assert product._meta.get_field("price").blank is True

    def test_product_meta_verbose_table(self, product_factory):
        product = product_factory.create()
        assert product._meta.verbose_name == "товар"
        assert product._meta.verbose_name_plural == "товары"

    def test_product_meta_ordering(self, product_factory):
        product = product_factory.create()
        assert product._meta.ordering == ["name", "number_of_purchases"]

    def test_product_for_date_time_field(self, product_factory):
        product = product_factory.create()
        assert product._meta.get_field("date_product").auto_now_add is True


@pytest.mark.django_db
class TestTag:

    def test_tag_verbose_name_fields(self, tag_factory):
        tag = tag_factory.create()
        assert tag._meta.get_field("name").verbose_name == "название тега"

    def test_tag_length_fields(self, tag_factory):
        tag = tag_factory.create()
        assert tag._meta.get_field("name").max_length == 1000

    def test_tag_meta_verbose_table(self, tag_factory):
        tag = tag_factory.create()
        assert tag._meta.verbose_name == "тег"
        assert tag._meta.verbose_name_plural == "теги"


@pytest.mark.django_db
class TestCategory:

    def test_category_verbose_name_fields(self, category_factory):
        category = category_factory.create()
        assert category._meta.get_field("name").verbose_name == "название категории"
        assert (
            category._meta.get_field("parent").verbose_name == "родительская категория"
        )
        assert (
            category._meta.get_field("active_category").verbose_name
            == "автивность категории"
        )
        assert category._meta.get_field("file_icon").verbose_name == "файл иконки"

    def test_category_length_fields(self, category_factory):
        category = category_factory.create()
        assert category._meta.get_field("name").max_length == 1000

    def test_category_blank_fields(self, category_factory):
        category = category_factory.create()
        assert category._meta.get_field("parent").blank is True
        assert category._meta.get_field("active_category").blank is True
        assert category._meta.get_field("file_icon").blank is True

    def test_category_upload_to_field(self, category_factory):
        category = category_factory.create()
        assert category._meta.get_field("file_icon").upload_to == "files_icon/"

    def test_category_meta_verbose_table(self, category_factory):
        category = category_factory.create()
        assert category._meta.verbose_name == "категория"
        assert category._meta.verbose_name_plural == "категории"

    def test_category_meta_ordering(self, category_factory):
        category = category_factory.create()
        assert category._meta.ordering == ["name"]


@pytest.mark.django_db
class TestComment:

    def test_comment_verbose_name_fields(self, comment_factory):
        comment = comment_factory.create()
        assert comment._meta.get_field("name_user").verbose_name == "имя пользователя"
        assert (
            comment._meta.get_field("text_comment").verbose_name == "текст комментария"
        )
        assert comment._meta.get_field("product").verbose_name == "продукт"
        assert comment._meta.get_field("user").verbose_name == "пользователь"
        assert (
            comment._meta.get_field("date_comment").verbose_name == "дата комментария"
        )

    def test_comment_length_fields(self, comment_factory):
        comment = comment_factory.create()
        assert comment._meta.get_field("name_user").max_length == 100
        assert comment._meta.get_field("text_comment").max_length == 10000

    def test_comment_blank_fields(self, comment_factory):
        comment = comment_factory.create()
        assert comment._meta.get_field("name_user").blank is True
        assert comment._meta.get_field("product").blank is True
        assert comment._meta.get_field("user").blank is True
        assert comment._meta.get_field("date_comment").blank is True

    def test_comment_meta_verbose_table(self, comment_factory):
        comment = comment_factory.create()
        assert comment._meta.verbose_name == "комментарий"
        assert comment._meta.verbose_name_plural == "комментарии"

    def test_comment_for_date_time_field(self, comment_factory):
        comment = comment_factory.create()
        assert comment._meta.get_field("date_comment").auto_now_add is True
