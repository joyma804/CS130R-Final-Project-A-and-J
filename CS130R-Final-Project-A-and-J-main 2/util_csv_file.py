import csv

def get_list_by_file(data_file_name):
    data_list = []
    with open(data_file_name, 'r') as csv_file:
         csv_reader = csv.reader(csv_file, delimiter=',')
         data_list = list(csv_reader)
         #remove empty lenders if exist.
         data_list = remove_empty_item_from_list(data_list)
         #remove the first row for column title.
         if len(data_list) > 0:
            data_list.pop(0)
    return data_list
# at this point, it's still a large list of entire data --> not split into list of lists yet !! 


def write_list_to_lender_file(data_list, data_file_name):
    #check if column title line exists
    if len(data_list) <= 1 or data_list[0][0] != 'lender_id':
        data_list = add_lender_column_title_to_list(data_list)
    write_list_to_file(data_list, data_file_name)

def write_list_to_book_file(data_list, data_file_name):
    #check if column title line exists
    if len(data_list) == 1 or data_list[0][0] != 'book_id':
        data_list = add_book_column_title_to_list(data_list)
    write_list_to_file(data_list, data_file_name)

#shared functions
def write_list_to_file(data_list, data_file_name):
    with open(data_file_name,'w+', newline ='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(data_list)

def add_lender_column_title_to_list(lender_list):
    column_title = ['lender_id','name','book_id','date_borrowed','penalty']
    #add column title
    lender_list.insert(0,column_title)
    return lender_list

def add_book_column_title_to_list(book_list):
    column_title = ['book_id','title','author','copies','times_borrowed']
    book_list.insert(0,column_title)
    return book_list

def remove_empty_item_from_list(data_list):
    result_list = []
    for item in data_list:
        if item != []:
            result_list.append(item)
    return result_list
