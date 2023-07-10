import csv
import typing

from django.db.models import Model


def create_parent_model_test_data(
        *,
        model: typing.Type[Model],
        filename: str,
        column_name_for_mapping: str,
) -> typing.Union[dict[str, int], None]:

    name_pk_map: dict[str, int] = {}

    with open(filename, 'r', encoding='utf-8') as csv_file:
        for row in csv.DictReader(csv_file):
            pk = model.objects.create(**row).pk
            name_pk_map[row[column_name_for_mapping]] = pk

    return name_pk_map


def create_test_data(
        *,
        model: typing.Type[Model],
        filename: str,
        foreign_key_field_name: typing.Union[str, None],
        parent_data_map: typing.Union[dict[str, int], None],
) -> None:

    with open(filename, 'r', encoding='utf-8') as csv_file:
        for row in csv.DictReader(csv_file, delimiter=';'):
            if row[foreign_key_field_name]:
                parent_pk = parent_data_map[row[foreign_key_field_name]]
                row[f'{foreign_key_field_name}_id'] = parent_pk
            del row[foreign_key_field_name]

            model.objects.create(**row)
