"""
this file contains all the tasks used in bond app
"""
import csv
import datetime
import os
from io import StringIO

from django.core.validators import EMPTY_VALUES

from products.models import Product, ProductSize

FILE_NAME = "product-csv-{}.csv"

HEADER_FIELD = ROW_FIELD_LIST = [
    "Name",
    "Price",
    "Discount Price",
    "Fabric Type",
    "Color",
    "Size",
    "Description",
    "Is Active",
]

DATA_DICT = {
    "name": "Name",
    "price": "Price",
    "discount_price": "Discount Price",
    "product_fabric": "Fabric Type",
    "color": "Color",
    "size": "Size",
    "description": "Description",
    "is_active": "Is Active",
}


def filter_model_object(**kwargs: dict):
    """
    This function is used to filter data from model
    kwargs should be first name, last name, email, username, password and user type
    """
    model = kwargs.pop('model_name')  # get the model name
    filter_object = model.objects.filter(**kwargs)
    return filter_object


def row_append(create_row_list: list, status_bool: bool, status_value: int) -> int:
    """
    this function is used to append row status and update counter for success or failed record
    """
    if status_bool:
        create_row_list.append("success")
    else:
        create_row_list.append("failed")
    status_value += 1
    return status_value


def validate_field(fields: list, attrs: dict) -> dict:
    """
    This method validate attrs data
    return error dict if data field is empty or not valid
    """
    # initialize errors dict.
    errors = {}
    for field in fields:
        if attrs.get(field) in EMPTY_VALUES:
            errors.update({field: 'This field is required.'})
    return errors


def return_file_name():
    """
    this function return file name for creating new csv file
    """
    time = str(datetime.datetime.now())
    file_name = FILE_NAME.format(time)
    return file_name


def create_data_row(row) -> [list, dict]:
    row_dict = DATA_DICT.copy()

    for key in DATA_DICT:
        row_dict.update({key: row.get(DATA_DICT.get(key))})

    row_list = list(row_dict.values())
    return row_list, row_dict


def read_csv_data(write_line, csv_data):
    success_count = 0
    failed_count = 0
    for row in csv_data:
        # check all data of row exists
        data_row, row_dict = create_data_row(row)
        errors = validate_field(ROW_FIELD_LIST, row)
        if errors:
            # if any field not exists then
            failed_count = row_append(
                data_row, False, failed_count
            )
        else:
            try:
                is_active = True if row_dict.pop("is_active").lower() == "true" else False
                sizes = [ProductSize.objects.filter(symbol__iexact=i).first().id for i in
                         row_dict.pop("size").split(',')]

                # create record
                product_obj = Product.objects.update_or_create(**row_dict)
                product_obj.sizes.set(sizes)
                product_obj.is_active = is_active
                product_obj.save()
                success_count = row_append(
                    data_row, True, success_count
                )
            except:
                # if record did not create then
                failed_count = row_append(
                    data_row, False, failed_count
                )
        # add row to new file of success status of record
        write_line.writerow(data_row)
    return failed_count, success_count


def upload_csv_for_bonds(file: dict) -> dict:
    """
    this function used for uploading bonds data from csv file
    """
    # Read csv file InMemoryUploadedFile
    reader = csv.DictReader(StringIO(file))

    # Generate a list comprehension
    csv_data = [line for line in reader]
    file_path = os.path.abspath(".")

    if not os.path.isdir(file_path):
        os.mkdir(file_path)

    # create new file with bond create status
    with open(f"{file_path}/{return_file_name()}", "a") as created_file:
        # add row to new file create for record status
        write_line = csv.writer(created_file)
        write_line.writerow(HEADER_FIELD)

        failed_count, success_count = read_csv_data(write_line, csv_data)

    # log the total number of record failed and success
    record_status_dict = {
        "success_records": success_count,
        "failed_records": failed_count,
    }
    return record_status_dict
