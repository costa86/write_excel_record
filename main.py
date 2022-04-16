import csv
from datetime import datetime
from tabulate import tabulate


FILE_NAME = "sample.csv"
DATE_FORMAT = "%Y/%m/%d"
CATEGORIES = ["food", "bus", "restaurant"]
NA = "NA"
HEADER = ["Date", "Amount", "Category", "Note"]


def get_correct_date(raw: str) -> str:
    if len(raw) != 8:
        return NA
    year = int(raw[:4])
    month = int(raw[4:6])
    day = int(raw[6:])
    return datetime(year, month, day).strftime(DATE_FORMAT)


def read(file_name: str = FILE_NAME) -> list:
    with open(file_name) as f:
        r = csv.reader(f)
        return list(r)


def get_category(categories: list) -> str:
    categories_dict = {i:c.upper() for i,c in enumerate(categories)}

    print(f"Categories: \n{categories_dict} ")
    error_msg = "Invalid category"

    while 1:
        try:
            value = input("Category ID (default 0) : ")
            if not value:
                return categories_dict[0]
            value = int(value)
            if value in categories_dict:
                return categories_dict[value]
            print(error_msg)
        except Exception:
            print(error_msg)


def write(row: list, file_name: str = FILE_NAME):
    with open(file_name, "a+") as f:
        w = csv.writer(f)
        if not read():
            w.writerow(HEADER)
        w.writerow(row)


def get_note() -> str:
    return input(f"Note (default {NA}): ") or NA


def get_price() -> str:
    while 1:
        try:
            value = input(f"Price (default 0): ") or "0"
            if float(value) >= 0:
                return value
        except Exception:
            print("Invalid price")


def get_date() -> str:
    error_msg = "Invalid date"
    today = datetime.now().strftime(DATE_FORMAT)
    while 1:
        try:
            value = input(
                f"Date (format YYYYMMDD). Default is today ({today}): ")
            if not value:
                return today
            valid = get_correct_date(value)
            if valid != NA:
                return valid
        except Exception:
            print(error_msg)


def add_expense():
    expense = [
        get_date(),
        get_price(),
        get_category(CATEGORIES),
        get_note()
    ]
    write(expense)


def show_expenses():
    content = read()[1:]
    records = tabulate(content, headers=HEADER,
                       tablefmt="fancy_grid", showindex="always")
    print(records)

    total_amount = sum([float(i[1]) for i in content])
    quantity = len(content)
    summary = tabulate([[total_amount, quantity]], headers=[
                       "TOTAL AMOUNT", "QUANTITY"], tablefmt="fancy_grid")
    print(summary)


choices = {
    0: [add_expense, "New expense"],
    1: [show_expenses, "Show expenses"]
}


def main():
    for i in choices:
        info = choices[i][1]
        print(f"{i} - {info}")

    while 1:
        try:
            option = input("Option (default 0): ")
            if not option:
                choices[0][0]()
                break
            option = int(option)
            choices[option][0]()
            break
        except Exception:
            print("Invalid choice")


main()
