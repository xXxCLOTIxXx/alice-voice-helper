from .. import settings

import re

from num2words import num2words


def clear_names(text: str) -> str:
    names = settings.settings.get("other", settings.default_settings.get("other")).get("names").lower().split(',')
    text = text.lower()

    pattern = r'\b(?:' + '|'.join([re.escape(name.strip()) for name in names]) + r')(?:[а-яА-ЯёЁ]*?)\b'
    text = re.sub(pattern, '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def text_to_words(text):
    def replace_numbers(match):
        number = int(match.group())
        return num2words(number, lang='ru')
    
    def replace_letters(match):
        letter_map = {
            'a': 'ай', 'b': 'би', 'c': 'си', 'd': 'ди', 'e': 'и', 'f': 'эф', 'g': 'джи',
            'h': 'эйч', 'i': 'ай', 'j': 'джей', 'k': 'кей', 'l': 'эль', 'm': 'эм', 'n': 'эн',
            'o': 'о', 'p': 'пи', 'q': 'кью', 'r': 'ар', 's': 'эс', 't': 'ти', 'u': 'ю',
            'v': 'ви', 'w': 'дабл-ю', 'x': 'икс', 'y': 'вай', 'z': 'зед', '+': 'плюс', '-': 'минус',
            '=': 'равно', '%': 'процент', '@': 'собачка', '№': 'номер', '#': 'решетка'
        }
        letter = match.group().lower()
        return letter_map.get(letter, letter)
    text = re.sub(r'\d+', replace_numbers, text)
    text = re.sub(r'[a-zA-Z]', replace_letters, text)

    return text