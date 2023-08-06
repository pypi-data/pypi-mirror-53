import os
from pprint import pprint
from typing import List, Dict

import numpy as np
import pytest
from goodtables.validate import validate
from tableschema import Schema

from tsfaker import tstype
from tsfaker.generator.table import TableGenerator
from tsfaker.io.io_arguments import replace_json_to_csv_ext
from tsfaker.io.utils import smart_open_write


def build_schema_from_types(types: List[str]) -> Schema:
    fields = [{'name': '{}_{}'.format(tstype_name, i), 'type': tstype_name}
              for i, tstype_name in enumerate(types)]
    return Schema({'fields': fields})


tstypes_to_np_dtype = [
    ([tstype.NUMBER], np.number),
    ([tstype.NUMBER, tstype.INTEGER], np.unicode_),
    ([tstype.INTEGER], np.unicode_),
    ([tstype.INTEGER, tstype.INTEGER], np.unicode_),
    ([tstype.DATETIME], np.unicode_),
    ([tstype.DATE], np.unicode_),
    ([tstype.NUMBER, tstype.DATE], np.unicode_),
    ([tstype.NUMBER, tstype.YEAR], np.unicode_),
    ([tstype.YEAR, tstype.DATE], np.unicode_),
    (tstype.implemented, np.unicode_),
]
test_input = [(types, nrows, np_type) for (types, np_type) in tstypes_to_np_dtype for nrows in (1, 7)]


@pytest.mark.parametrize('types,nrows,np_type', test_input)
def test_generate_from_types(types, nrows, np_type):
    # Given
    schema = build_schema_from_types(types)
    csv_path = os.path.join('tests', 'tmp', "{}_{}_{}.csv".format('_'.join(types), nrows, np_type))

    # When
    table_generator = TableGenerator(schema, nrows)
    array = table_generator.get_array()

    # Then
    assert np.issubdtype(array.dtype, np_type)
    assert (nrows, len(types)) == array.shape

    generate_validate(schema, csv_path)


@pytest.mark.parametrize('schema_filename', ['implemented_types.json', 'bounded.json', 'enum.json'])
def test_generate_from_schema(schema_filename):
    # Given
    schema_path = os.path.join('tests', 'schemas', schema_filename)
    csv_path = os.path.join('tests', 'tmp', replace_json_to_csv_ext(schema_filename))

    # When
    generate_validate(Schema(schema_path), csv_path)


def test_generate_from_schema_with_foreign_key():
    # Given
    child_schema_relative_path = os.path.join('parent_child', 'child1.json')
    child_schema_path = os.path.join('tests', 'schemas', child_schema_relative_path)
    child_csv_path = os.path.join('tests', 'tmp', replace_json_to_csv_ext(child_schema_relative_path))
    resource_name_to_path_or_schema = {'parent': os.path.join('tests', 'csv', 'parent.csv')}

    # When
    schema = Schema(child_schema_path)
    generate_validate(schema, child_csv_path, resource_name_to_path_or_schema)


def generate_validate(schema: Schema, csv_path: str, resource_name_to_path_or_schema: Dict[str, str]=None):
    table_generator = TableGenerator(schema, 10, resource_name_to_path_or_schema)
    table_string = table_generator.get_string(pretty=False)
    print('\n' + table_string)
    with smart_open_write(csv_path) as f:
        f.write(table_string)
    report = validate(csv_path, schema=schema, skip_checks=['duplicate-row'])
    pprint(report)
    assert report['error-count'] == 0
    os.remove(csv_path)
