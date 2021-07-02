#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict
import re
import unicodedata

from food.settings import NO_DATA, STOPWORDS

class SearchParser:
    """
        Parser class
        To manage user question parsing
    """
    def __init__(self):
        """ Constructor """
        self.cleaned_string = ''
        self.cleaned_string_words_list = []

    def refuse_empty_string(self, raw_string):
        """
            We check that the user input value is not empty or made up of spaces
            :param: raw_string is a string
            :return: a string "no_data" indicating that the response is empty
            or consists of spaces
            :rtype: string
        """
        trim_raw_string = raw_string.strip()
        if re.match(r"^(?![\s\S])", trim_raw_string):
            return NO_DATA

    def remove_accented_characters(self, raw_string):
        """
            String cleaning to facilitate comparisons, step 1
            :param: raw_string is a string
            :return: a string without accented characters and in lower case
            :rtype: string
            Example : "Pâte à tartiner" --> "pate a tartiner"
        """
        trimmed_string = raw_string.strip()
        # We replace the accented characters and use lower case
        no_accent_data = ''.join(
            (c for c in unicodedata.normalize('NFD', trimmed_string)
             if unicodedata.category(c) != 'Mn')
            )

        return no_accent_data.lower()

    def remove_special_characters(self, raw_string):
        """
            String cleaning to facilitate comparisons, step 2
            :param: raw_string is a string
            :return: a string without special characters
            :rtype: string
            Example : "l'horloge de# no$tre-dame tourne ?" --> "l'horloge de notre-dame tourne"
        """
        # We delete the letters with quote (l', d', etc.)
        no_quote_letter_data = re.sub(r"(\s[a-z])'", " ", raw_string)
        # We delete the special characters except the hyphen
        return re.sub(r'[^\-\'\,\w\s]','',no_quote_letter_data)
    
    def get_cleaned_data_list(self, raw_string):
        """
            Cutting the string into words
            :param: raw_string is a string
            :return: a list containing all the words of the given string
            :rtype: list
        """
        # We transform the string into a list of words
        cleaned_data_temp_list = []
        cleaned_data_list = []
        cleaned_data_temp_list = raw_string.split(' ')
        # We delete the duplicates
        cleaned_data_list = list(OrderedDict.fromkeys(cleaned_data_temp_list))
        # We delete the empty items
        value_to_delete = ''
        cleaned_data_list = [i for i in cleaned_data_list if i != value_to_delete]

        return cleaned_data_list
    
    def get_clean_stopwords_list(self):
        """
            Remove accents in predefined stopwords list
            :return: a clean stopwords list without accents
            :rtype: list
        """
        clean_stopwords_list = []
        for word in STOPWORDS:
            clean_word = self.remove_accented_characters(word)
            clean_stopwords_list.append(clean_word.strip())

        # We delete the duplicates
        clean_stopwords_list = list(set(clean_stopwords_list))

        return clean_stopwords_list

    def remove_stopwords(self, raw_list, clean_stopwords_list):
        """
            Removal of unnecessary words from a pre-defined list
            :param: cleaned_data_list is a list of cleaned words (strings)
            :return: a list containing only the important words
            :rtype: list
        """
        # We determine the list of words to delete in the original list
        words_to_remove = list(set(raw_list) & set(clean_stopwords_list))

        # We remove unnecessary words from the original list
        for word in words_to_remove:
            raw_list.remove(word)

        self.cleaned_string_words_list = raw_list

        return self.cleaned_string_words_list

    def get_cleaned_string(self, raw_string):
        """
            Reconstruction of a string from the list of important words
            :param: raw_string is a raw string to parse
            :return: a parsed/cleaned string without accents, special
            charatcters or unnecessary words
            :rtype: string
        """
        if self.refuse_empty_string(raw_string) == NO_DATA:
            print("La question de l'utilisateur est vide ou constituée d'espaces.")
            return NO_DATA

        # We remove any accents and special characters (punctuation and others)
        no_accent_data = self.remove_accented_characters(raw_string)
        no_special_characters_data = self.remove_special_characters(no_accent_data)
        # We get the original cleaned word list
        cleaned_data_list = self.get_cleaned_data_list(no_special_characters_data)
        # A tuple is retrieved from the list of filtered words
        clean_stopwords_list = self.get_clean_stopwords_list()

        return list(tuple(self.remove_stopwords(cleaned_data_list, clean_stopwords_list)))
