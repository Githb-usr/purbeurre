#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views.generic import TemplateView, ListView

from food.database_service import DatabaseService
from food.forms import SmallSearchForm, LargeSearchForm
from food.models import Product, Category, Store
from food.search_parser import SearchParser
from food.settings import NUTRIENT_LEVELS
from users.models import Substitute

def small_search_form(request):
    """
       We display the small search form in all navbar of all pages.
       (through the context_processors in config/settings.py)
       :return: a dictionary
    """
    small_search_form = SmallSearchForm()

    return { "small_search_form": small_search_form }

def show_index(request):
    """
        We display the homepage of the application
        :return: a template
    """
    large_search_form = LargeSearchForm()

    return render(request, 'index.html', { 'large_search_form': large_search_form })

def show_search_result(request):
    """
        We display the products that match the user's search for a product to replace.
        :return: a template with product(s) data do display
    """
    searchParser = SearchParser()
    # We get the product name entered by the user
    query = request.GET.get('query')
    # We parse the string sent by the user (we obtain a list of words)
    cleaned_query = searchParser.get_cleaned_string(query)
    
    # If there is at least 1 word
    if cleaned_query != 'no_data' and len(cleaned_query) > 0:
        # if query = barcode only
        product_search_by_barcode = Product.objects.filter(barcode=cleaned_query[0])
        # We look for matches with all the words
        for i in range(len(cleaned_query)):
            product_search_by_name = Product.objects.filter(designation__unaccent__icontains=cleaned_query[i]).order_by('-nutriscore')
        # getting the desired page number from url
        page_number = request.GET.get('page', 1)
        paginator = Paginator(product_search_by_name, 6)
        # Management of the shortened display of the pagination
        page_range = paginator.get_elided_page_range(number=page_number, on_each_side=1, on_ends=1)
        
        try:
            page_obj = paginator.get_page(page_number)  # returns the desired page object
        except PageNotAnInteger:
            # if page_number is not an integer then assign the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if page is empty then return last page
            page_obj = paginator.page(paginator.num_pages)
    
        # If there are any matches, we send them to the template
        if len(product_search_by_name) > 0:
            return render(request, 'food/product_list.html', {
                'search_result': page_obj,
                'page_range': page_range,
                'query': query
                })
        # If the user has entered a barcode
        elif product_search_by_barcode:
            return render(request, 'food/product_list.html', {
                'search_result': product_search_by_barcode,
                'page_range': page_range,
                'query': query
                })

    return render(request, 'food/product_list.html', {
        'search_result': 'NO_DATA',
        'query': query
        })
        
def show_product_detail(request, barcode):
    """
        We display the detailed sheet of a product.
        :param barcode: the barcode of the product to display
        :return: a template with the product data to display
    """
    product_detail = get_object_or_404(Product, barcode=barcode)
    nutriment_level_data = determine_nutriment_level_data(product_detail)

    return render(request, 'food/product_detail.html', {
        'product_detail': product_detail,
        'nutriment_data': nutriment_level_data
        })

def show_substitute_choice_list(request, barcode):
    """
        We display products that are healthier than the product selected by the user.
        :param barcode: the barcode of the product to replace by a substitute
        :return: a template with substitute(s) data do display
    """
    initial_product = get_object_or_404(Product, barcode=barcode)
    initial_product_categories = initial_product.categories.all()
    substitute_search = Product.objects.filter(categories__in=initial_product_categories)\
                        .filter(nutriscore__lt=initial_product.nutriscore)\
                        .order_by('nutriscore').distinct()

    existing_substitutes = [];
    favourite_substitutes_with_initial_product = Substitute.objects.filter(
        initial_product=initial_product.id
        )

    if favourite_substitutes_with_initial_product:
        for fav in favourite_substitutes_with_initial_product:
            existing_substitutes.append(fav.substituted_product_id)
    
    if substitute_search:
        paginator = Paginator(substitute_search, 6)
        page_number = request.GET.get('page', 1)
        # Management of the shortened display of the pagination
        page_range = paginator.get_elided_page_range(number=page_number, on_each_side=1, on_ends=1)
        
        try:
            page_obj = paginator.get_page(page_number)  # returns the desired page object
        except PageNotAnInteger:
            # if page_number is not an integer then assign the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if page is empty then return last page
            page_obj = paginator.page(paginator.num_pages)
        
        return render(request, 'food/substitute_list.html', {
            'initial_product': initial_product,
            'search_result': page_obj,
            'page_range': page_range,
            'existing_substitutes': existing_substitutes,
            })

    return render(request, 'food/substitute_list.html', {
        'initial_product': initial_product,
        'search_result': 'NO_DATA'
        })

def determine_level_data(level):
    """
        We convert the 2-letter code into French words and colour.
        :param level: the original string of level data in Open Food Facts database
        :return: a dictionary with french string of level and the corresponding colour
        :rtype: dict()
    """
    level_data = {}
    if level == 'LO':
        level_data['color'] = 'green-dot'
        level_data['quantity'] = 'faible quantité'
    elif level =='MO':
        level_data['color'] = 'orange-dot'
        level_data['quantity'] = 'quantité modérée'
    elif level =='HI':
        level_data['color'] = 'red-dot'
        level_data['quantity'] = 'quantité élevée'

    return level_data

def determine_nutriment_level_data(product):
    """
        We associate product nutrients with their level information.
        This information will be used on the template proposing the detailed product sheet.
        :param product: one product object
        :return: a dictionary with all nutriments data of the product.
        :rtype: dict()
    """
    nutriment_level_data = {}
    if product.fat_level:
        nutriment_level_data['fat'] = determine_level_data(product.fat_level)
    
    if product.fat_level:
        nutriment_level_data['saturated_fat'] = determine_level_data(product.saturated_fat_level)
    
    if product.fat_level:
        nutriment_level_data['sugars'] = determine_level_data(product.sugars_level)
    
    if product.fat_level:
        nutriment_level_data['salt'] = determine_level_data(product.salt_level)

    return nutriment_level_data
