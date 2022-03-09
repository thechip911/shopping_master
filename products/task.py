"""
this file contains all the tasks used in bond app
"""
import csv
import datetime
import logging
import os
from io import StringIO


FILE_NAME = "product-csv-{}.csv"

DATA_DICT = {
    "name": "BOND NAME",
    "sector__name": "SECTOR NAME",
    "mid_price": "MID PRICE",
    "amount_outstanding": "AMOUNT OUTSTANDING",
    "coupon": "COUPON",
    "maturity": "MATURITY",
    "coupon_frequency": "COUPON FREQUENCY",
    "isin": "ISIN",
    "issuer_name": "ISSUER NAME",
    "description": "DESCRIPTION"
}

logger = logging.getLogger("celery")


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
        errors = api_utils.validate_field(ROW_FIELD_LIST, row)
        if errors:
            # if any field not exists then
            failed_count = api_utils.row_append(
                data_row, False, failed_count
            )
        else:
            model_dict = {"model_name": Sector, "name": row.get("SECTOR NAME")}
            sector = api_utils.filter_model_object(**model_dict).first()
            if sector:
                try:
                    row_dict["sector_id"] = sector.id
                    # create record
                    Bond.objects.update_or_create(**row_dict)
                    success_count = api_utils.row_append(
                        data_row, True, success_count
                    )
                except:
                    # if record did not create then
                    failed_count = api_utils.row_append(
                        data_row, False, failed_count
                    )
            else:
                # if record did not create then
                failed_count = api_utils.row_append(
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
    file_path = os.path.abspath(".") + "/" + "bonds" + "/bonds_data"

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
    logger.info(record_status_dict)
    return record_status_dict
