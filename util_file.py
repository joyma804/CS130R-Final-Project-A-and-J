'''
common functions for file operations.
'''
import json
import util_config

#get lender file name.
def get_lender_file_name():
    lender_file_name = util_config.get_config_value("lender_file_name")
    return lender_file_name

#get book file name.
def get_book_file_name():
    book_file_name = util_config.get_config_value("book_file_name")
    return book_file_name

#get book list
def get_book_list():
    data_file_name = get_book_file_name()
    return get_list_by_file(data_file_name)

#get lender_list
def get_lender_list():
    data_file_name = get_lender_file_name()
    return get_list_by_file(data_file_name)

#add a lender
def add_lender(lender):
    data_file_name = get_lender_file_name()
    lender_list = get_lender_list();
    lender_list.append(lender)
    write_list_to_file(lender_list, data_file_name)

#shared functions
def get_list_by_file(data_file_name):
    data_list = []
    with open(data_file_name, "r") as data_file:
        data_list = json.load(data_file)
    return data_list

def write_list_to_file(data_list, data_file_name):
    with open(data_file_name, "w") as data_file:
        json.dump(data_list, data_file)

#initialize book file
def create_book_file(data_file_name):
    book_list = []

    book1 = {
      "book_id": "18880",
      "title": "The History of Ancient Roman",
      "author": "Mary Beard",
      "copies": 10,
      "times_borrow": 5
    }

    book2 = {
      "book_id": "18881",
      "title": "The Tale of Two Cities",
      "author": "Charles Dickens",
      "copies": 5,
      "times_borrow": 2
    }

    book_list.append(book1)
    book_list.append(book2)

    with open(data_file_name, "w") as write_file:
        write_file.write(json.dumps(book_list, indent=4))

#initialize lender file
def create_lender_file(data_file_name):
    lender_list = []

    lender1 = {
      "lender_id": "199990",
      "name": "Melissa Woods",
      "borrow_book_id": "",
      "borrow_date": "",
      "penalty": 0
    }

    lender2 = {
      "lender_id": "199991",
      "name": "James William",
      "borrow_book_id": "",
      "borrow_date": "",
      "penalty": 0
    }

    lender_list.append(lender1)
    lender_list.append(lender2)

    with open(data_file_name, "w") as write_file:
        write_file.write(json.dumps(lender_list, indent=4))


    