#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib.request import urlopen, Request
from urllib.parse import quote
import gzip
import json


class Translator:
    @staticmethod
    def get_response_from_request(request):
        response = urlopen(request)
        return response.read()

    @staticmethod
    def get_translation_from_response(response):
        lists = json.loads(response)
        translation_sentences = []
        for list_ in lists[0]:
            translation_sentences.append(list_[0])
        translation = ''.join(translation_sentences)
        return translation

    @staticmethod
    def translate(input_text, target_lang, source_lang='auto'):
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={source_lang}&tl={target_lang}&dt=t&q={quote(input_text)}"
        response = Translator.get_response_from_request(Request(url=url))
        return Translator.get_translation_from_response(response)