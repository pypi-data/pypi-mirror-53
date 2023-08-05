import pandas as pd
from deap import file_reader as fr

def test_get_extension():
    result = fr.get_extension('some.csv')
    assert result == 'csv'

def test_get_extension_fail():
    result = fr.get_extension('some')
    assert result == None

def test_file_extensions_blob():
    result = fr.file_extentions()
    assert result.get('blob')

def test_file_extensions_matrix():
    result = fr.file_extentions()
    assert result.get('matrix')

def test_file_extensions_fail():
    result = fr.file_extentions()
    assert result.get('some') == None

def test_ext_handler():
    result = fr.ext_handler('json')
    assert result == pd.read_json
