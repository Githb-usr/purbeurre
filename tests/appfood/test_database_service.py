#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import SimpleTestCase, TestCase
import os
from unittest import mock
from unittest.mock import patch

from config.settings import BASE_DIR
from food.database_service import DatabaseService
from food.models import Product, Category, Store
import tests.config as test_result

class BaseTest(TestCase):
    def setUp(self):
        self.database_service = DatabaseService()
        self.database_service.products_dict_list = test_result.PRODUCT_DICT_LIST
        self.database_service.clean_product_fields = test_result.SEPARATED_DATA

        return super().setUp()

class DatabaseServiceTestCase(BaseTest):

    def test_populate_database_with_products(self):
        self.database_service.populate_database_with_products()
        one_product = Product.objects.get(barcode='3017620422003')
        self.assertEqual(one_product.barcode, '3017620422003')

    def test_get_field_value(self):
        field_value = self.database_service.get_field_value(test_result.PRODUCT_DICT_LIST[1], 'sugars')
        self.assertEqual(field_value, 56.3)

    def test_get_field_value_without_field(self):
        field_value = self.database_service.get_field_value(test_result.PRODUCT_DICT_LIST[0], 'sugars')
        self.assertEqual(field_value, 0)

    def test_get_field_value_with_key_error(self):
        field_value = self.database_service.get_field_value(test_result.OFF_API_RAW_DATA[3], 'sugars')
        self.assertEqual(field_value, None)

    def test_get_image_url(self):
        image_url = self.database_service.get_image_url(test_result.PRODUCT_DICT_LIST[1], 'image_url')
        self.assertEqual(image_url, 'https://images.openfoodfacts.org/images/products/301/762/042/2003/front_fr.270.400.jpg')

    def test_get_image_url_without_field(self):
        image_url = self.database_service.get_image_url(test_result.PRODUCT_DICT_LIST[1], 'toto')
        self.assertEqual(image_url, os.path.join(BASE_DIR, 'static/dist/assets/img/default_product_img.png'))

    def test_get_image_url_with_key_error(self):
        image_url = self.database_service.get_image_url(test_result.OFF_API_RAW_DATA[3], 'image_url')
        self.assertEqual(image_url, os.path.join(BASE_DIR, 'static/dist/assets/img/default_product_img.png'))

    def test_transcribe_nutrient_level_low(self):
        level_letters = self.database_service.transcribe_nutrient_level(test_result.PRODUCT_DICT_LIST[1], 'salt')
        self.assertEqual(level_letters, 'LO')

    def test_transcribe_nutrient_level_moderate(self):
        level_letters = self.database_service.transcribe_nutrient_level(test_result.PRODUCT_DICT_LIST[2], 'fat')
        self.assertEqual(level_letters, 'MO')

    def test_transcribe_nutrient_level_high(self):
        level_letters = self.database_service.transcribe_nutrient_level(test_result.PRODUCT_DICT_LIST[1], 'sugars')
        self.assertEqual(level_letters, 'HI')

    def test_transcribe_nutrient_level_with_key_error(self):
        level_letters = self.database_service.transcribe_nutrient_level(test_result.PRODUCT_DICT_LIST[1], 'toto')
        self.assertEqual(level_letters, None)

    def test_populate_database_with_categories(self):
        self.database_service.populate_database_with_categories()
        one_category = Category.objects.get(designation='Pâtes à tartiner aux noisettes')
        self.assertEqual(one_category.designation, 'Pâtes à tartiner aux noisettes')

    def test_populate_database_with_stores(self):
        self.database_service.populate_database_with_stores()
        one_store = Store.objects.get(designation='Magasins U')
        self.assertEqual(one_store.designation, 'Magasins U')
