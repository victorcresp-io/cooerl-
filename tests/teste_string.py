import pytest


def test_string():
    string = 'Fundação Santa Cabrini'

    string_formatada = 'fundacao santa cabrini'

    string = string.replace('ç', 'c')
    string = string.replace('ã', 'a')
    string = string.lower()

    assert string == string_formatada