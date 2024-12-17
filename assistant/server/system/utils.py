from ..config import names

import re


def clear_names(text: str) -> str:
    text = text.lower()

    pattern = r'\b(?:' + '|'.join([re.escape(name) for name in names]) + r')(?:[а-яА-ЯёЁ]*?)\b'
    text = re.sub(pattern, '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def split_space(text, num: int = 3):
    result = []
    count = 0
    current_part = []

    for char in text:
        if char == ' ':
            count += 1
        current_part.append(char)

        if count == num:
            result.append(''.join(current_part).strip())
            current_part = []
            count = 0

    if current_part:
        result.append(''.join(current_part).strip())
    return result