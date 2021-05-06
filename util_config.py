import json

#generate new unique book id.
def gen_new_lender_id():
    lender_config_file_name  = "config/lender_config.json"
    new_lender_id = 0
    #get new id from file.
    with open(lender_config_file_name, "r") as data_file:
        data = json.load(data_file)
        new_lender_id = data["current_id"] + 1
        data["current_id"] = new_lender_id

    #write new id to file.
    with open(lender_config_file_name, "w") as data_file:
        json.dump(data, data_file)
        # ___.dump(dictionary, file name)
    return new_lender_id

#generate new unique lender id.
def gen_new_book_id():
    book_config_file_name = "config/book_config.json"
    new_book_id = 0
    #get new id from file.
    with open(book_config_file_name, "r") as data_file:
        data = json.load(data_file)
        new_book_id = data["current_id"] + 1
        data["current_id"] = new_book_id
    #write new id to file.
    with open(book_config_file_name, "w") as data_file:
        json.dump(data, data_file)
    return new_book_id


