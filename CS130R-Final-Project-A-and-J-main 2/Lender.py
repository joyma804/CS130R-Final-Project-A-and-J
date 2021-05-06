import csv
import json
import util_config
import util_csv_file
from datetime import datetime

# Joy wrote the functions for this Lender class :)
class Lender(object):
    #interal variable
    _lender_file_name = "Lender.CSV"

    #constructure
    def __init__(self, lender_id=None,name=None,book_id=None,date_borrowed=None,penalty=None):
        self.lender_id = lender_id
        self.name = name
        self.book_id = book_id
        self.date_borrowed = date_borrowed
        self.penalty = penalty
        # print(f'{self.lender_id} - {self.name} - {self.book_id} - {self.date_borrowed} - {self.penalty}')

    def add_lender(self, name):
        lender = []
        #get new lender id.
        self.lender_id = util_config.gen_new_lender_id()
        lender.append(self.lender_id)
        lender.append(name)
        lender.append('')
        lender.append('')
        lender.append('')

        #load all lenders to lender_list
        lender_list = util_csv_file.get_list_by_file(self._lender_file_name)
        #add the new lender to lender_list
        lender_list.append(lender)
        #write lender_list back to lender file.
        util_csv_file.write_list_to_lender_file(lender_list, self._lender_file_name)

    #remove a lender by id or name
    def remove_lender_by_id(self, lender_id=None):
        print(f'remove lender by id: {lender_id}')
        #load all lenders to lender_list
        lender_list = util_csv_file.get_list_by_file(self._lender_file_name)

        ### print(f'before: {lender_list}')
        #get the index of lender to be removed.
        index = -1
        for lender in lender_list:
            index += 1
            #check if the lender exist in lender_list
            if lender[0] == lender_id :
                break
        #remove the lender by index.
        if(index >=0 and index < len(lender_list)):        
            lender_list.pop(index)
        else:
            print(f'The lender({lender_id})does not exist')
        ### print(f'after: {lender_list}')

        #write lender_list back to lender file.
        util_csv_file.write_list_to_lender_file(lender_list, self._lender_file_name)


    def get_lender_by_id(self, lender_id=None):
        the_lender = None
        #load all lenders to lender_list
        lender_list = util_csv_file.get_list_by_file(self._lender_file_name)
        for lender in lender_list:
            if lender[0] == str(lender_id):
                the_lender = lender
                break
        return the_lender

    def get_lender_by_name(self, name=None):
        the_lender = None
        #load all lenders to lender_list
        lender_list = util_csv_file.get_list_by_file(self._lender_file_name)
        for lender in lender_list:
            if lender[1].lower() == name.lower():
                ## lender[1] is asking for the second column = "name" !! 
                the_lender = lender
                break
        return the_lender[0]

    def get_book_id_by_id(self, lender_id=None):
        the_lender = None
        #load all lenders to lender_list
        lender_list = util_csv_file.get_list_by_file(self._lender_file_name)
        for lender in lender_list:
            if lender[0] == lender_id:
                the_lender = lender
                break
        return the_lender[2]

    ## Extra Function ## 
    def remove_lender_by_name(self, name=None):
        lender = self.get_lender_by_name(name)
        if lender!=None:
            lender_id = lender[0]
        self.remove_lender_by_id(lender_id)


    def pay_penalty(self, lender_id, payment_amount):
        balance = self.get_penalty_by_lender_id(lender_id)
        balance = balance - payment_amount
        #save back to data file.
        self.update_lender_by_id(lender_id=lender_id, penalty=balance)
        print('Thank you for your payment!')
    
    def charge_penalty(self, lender_id, charge_amount):
        balance = self.get_penalty_by_lender_id(lender_id)
        balance = balance + charge_amount
        #save back to data file.
        self.update_lender_by_id(lender_id=lender_id, penalty=balance)
        print(f'Sorry, it is expired. You are changed {charge_amount}')


    def borrow_book(self, lender_id, book_id, date_borrowed):
        result = -1
        # get the_lender:
        the_lender = self.get_lender_by_id(lender_id)
        # get the_lender's balance and check if penalty > 10:
        if the_lender[4]=='':
            current_penalty = 0 
        else: 
            current_penalty = float(the_lender[4])
        if current_penalty>10:
            print("Your penalty is more than $10 so you cannot borrow a book until you pay your charges!")
            result = 1 
        else:
            self.update_lender_by_id(lender_id=lender_id, book_id=book_id, date_borrowed=date_borrowed)
            result = 0
        return result 


    def return_book(self, lender_id, book_id):
        result = -1 
        the_lender = self.get_lender_by_id(lender_id=lender_id)
        if the_lender==None:
            result = 1 
            print(f"Sorry your lender_id:{lender_id} does not exist!")
        else:
            # calculate new penalty! 
            # get the_lender borrow date:
            if the_lender[3]=='':
                print("Sorry you have no books to return!")
            else:  
                borrowed_date = datetime.strptime(the_lender[3], "%m/%d/%Y")
                # get the_lender current date:
                current_date = datetime.now() 
                date_difference = (current_date - borrowed_date).days
                # print(date_difference) 
                if date_difference > 7:
                    new_charge = (date_difference-7)*1
                    print("Your book was overdue!")
                else: 
                    new_charge = 0
                if the_lender[4]=='':
                    lender_balance = 0 
                else: 
                    lender_balance = float(the_lender[4])
                lender_balance = lender_balance + new_charge
                print(f"Your current penalty owed is: ${lender_balance}")
                payment_amount = float(input("Input Payment Amount: "))
                new_lender_balance = lender_balance - payment_amount
                lender_book_id = the_lender[2]
                if lender_book_id==book_id:
                    self.update_lender_by_id(lender_id=lender_id, book_id='', date_borrowed='', penalty=new_lender_balance)
                    result = 0
                else:
                    result = 2
                    print(f"Sorry, your input book_id:{book_id} does not match your book_id:{lender_book_id} on record!")
            return result 




    #This basic function is used by other.
    #    Sample to update penalty: lender2.update_lender_by_id(lender_id='10046', penalty=3.00)
    #    Sample to update book_id and date_borrowed: lender2.update_lender_by_id(lender_id='10046', book_id='3000000',date_borrowed='4/12/2021')
    def update_lender_by_id(self, lender_id=None,name=None,book_id=None,date_borrowed=None,penalty=None):

        #load all lenders to lender_list
        lender_list = util_csv_file.get_list_by_file(self._lender_file_name)
        for lender in lender_list:
            if lender[0] == str(lender_id):
                if name != None:
                    lender[1] = name
                if book_id != None:
                    lender[2] = book_id
                if date_borrowed != None:
                    lender[3] = date_borrowed
                if penalty != None:
                    lender[4] = penalty

        #write lender_list back to lender file.
        util_csv_file.write_list_to_lender_file(lender_list, self._lender_file_name)
        

    def get_penalty_by_lender_id(self, lender_id):
        #get the lender by lender_id.
        the_lender = self.get_lender_by_id(lender_id)
        #get the lender's penalty balance.
        balance = 0.00
        if the_lender[4] != '':
            balance = float(the_lender[4])
        return balance
    
    # Annie wrote this function
    def check_or_pay(self, input_):
        choice = False
        lender_id = input("Input your lender id: ")
        while choice == False:
            if input_ == '1':
                balance = self.get_penalty_by_lender_id(lender_id)
                print(f"You currently owe: ${balance}")
                answer = "dummy"
                while not(answer == 'Y' or answer == 'N'): 
                    answer = input("Would you like to pay now? (Y/N) :").upper()
                    try_again = answer
                    if try_again == "Y":
                        self.check_or_pay('2')
                        return None 
                    elif not(try_again == "N"):
                        print("Invalid Input. Please input Y or N.")
                    else:
                        return ":)"
            elif input_ == '2':
                the_lender = self.get_lender_by_id(lender_id=lender_id)
                if the_lender[4]=='':
                    print("You do not have any penalty owed currently :)")
                    return ":)"
                else:
                    lender_balance = float(the_lender[4])
                    payment_amount = float(input("How much would you like to pay:\n$"))
                    self.pay_penalty(lender_id=lender_id, payment_amount=payment_amount)
                    return ":)"
            else:
                print("Something went wrong :( Try Again")
                print("---------------------------------------")
                print("1 - Check Penalty Owed\n2 - Pay Penalty\n")
                input_ = input("Choose your option: ")

    
    # Joy and Annie wrote this function together
    def user_choice_1(self, input_):
        choice = False
        while choice == False:
            if input_ == '1':
                # #  ADD LENDER  ##
                lender_name = input('Please input lender name: ') 
                self.add_lender(name=lender_name)
                print("\nThe lender has been successfully added :)")
                choice = True
            elif input_ == '2':
                # #  REMOVE LENDER  ##
                lender_id = input('Please input lender id:')
                self.remove_lender_by_id(lender_id)
                print("\nThe lender has been successfully removed :)")
                choice = True
            else:
                print("Something went wrong :( Try Again")
                print("---------------------------------------")
                print("1 - Add New Lender\n2 - Remove Lender\n")
                input_ = input("Choose your option: ")

# Annie wrote the functions for this Books class :)   
class Books():

    def __init__(self, id_, title, author, copies, times_borrowed):
        self.id = id_
        self.title = title
        self.author = author
        self.copies = copies
        self.times_borrowed = times_borrowed

    def read_books(self):
        # reads books.csv and pulls out each book's attributes in dictionary form, each added to a big list

        fd = open('books.csv', 'r')
        reader = csv.DictReader(fd)

        book_list = []
        for row in reader:
            book_list.append(row)
    
        fd.close()
        return book_list # full list of dictionaries of books in the library system
    
    def books_available(self, book_list, user):
        # prints all books available to borrow if user is customer or prints all books in the books.csv file if user is manager

        if user == 'customer': # customers would be the ones borrowing / returning books
            print("\nBooks Available:")
            for book in range(len(book_list)):
                if not(book_list[book]['copies'] == '0'): # if no copies in library, it won't print
                    print(f"ID: {book_list[book]['id_']} -- {book_list[book]['title']} by {book_list[book]['author']}")
            print("\n")
        else: # managers would have access to the full database regardless of whether a book is borrowed or not
            for book in range(len(book_list)):
                print(f"ID: {book_list[book]['id_']} -- {book_list[book]['title']} by {book_list[book]['author']}")
            print("\n")
    
    #------------------------ ADDING BOOK ------------------------#
    def get_id(self):
        # gets the book id for the new book, pulling id number from book_id file and then adding one so that id is never used again

        fd = open('book_id.csv', 'r')
        reader = csv.DictReader(fd)

        reader2 = list(reader)
        id_ = int(reader2[0]['current_id'])
        fd.close()
        
        fwd = open('book_id.csv', 'w')
        csv_writer = csv.writer(fwd)
        csv_writer.writerow(['current_id'])
        csv_writer.writerow([f"{id_ + 1}"])
        fwd.close()

        return id_ # ID number to be used for the new book
    
    def add_book(self):
        # creates a dictionary of the new book's attributes and adds that to the larger list of dictionaries of books

        book_list = self.read_books()
        book_dict = {}
        book_dict['id_'] = self.get_id()
        book_dict['title'] = input("What is the title: ")
        book_dict['author'] = input("Who is the author: ")
        book_dict['copies'] = input("How many copies: ")
        book_dict['times_borrowed'] = 0 # initial value never been borrowed
        book_list.append(book_dict)

        self.write_book_to_file(book_list) # writes list of books updated with new addition

    #------------------------ REMOVING BOOK ------------------------#
    def remove_book(self, book_list):
        # finds and removes a book from the books.csv file

        self.books_available(book_list, 'manager')
        book_ = input("What is the ID of the book you wish to remove?\n")
        for book in range(len(book_list)):
            if (book_list[book]['id_'] == book_):
                book_list.remove(book_list[book])
                return book_list # updated full list of books excluding the one just deleted
                break
            elif book == len(book_list)-1: # if the code reaches the end of book_list and the book hasn't matched
                print("ID not found")
                try_again = "dummy" # place-holder
                while not(try_again == 'Y' or try_again == 'N'): 
                    try_again = input("Would you like to try again? (Y/N): ").upper()
                    if try_again == "Y":
                        self.user_choice_2(3)
                        return ":)" # returns this value to stop the books available from printing multiple times with the recursion 
                    elif not(try_again == "N"):
                        print("Invalid Input. Please input Y or N.")

    #------------------------ MODIFYING COPIES ------------------------#
    def modify_book_count(self, book_list):
        self.books_available(book_list, 'manager')
        book_ = input("What is the ID of the book you wish to change the book count of?\n")
        for book in range(len(book_list)):
            if (book_list[book]['id_'] == book_):
                self.access_book_info_by_id(book_, book_list)
                copies = input("What will be the new total copies?: ")
                book_list[book]['copies'] = copies
                return book_list, book_
            elif book == len(book_list)-1: # if the code reaches the end of book_list and the book hasn't matched
                print("ID not found")
                try_again = "dummy" # place-holder
                while not(try_again == 'Y' or try_again == 'N'): 
                    try_again = input("Would you like to try again? (Y/N): ").upper()
                    if try_again == "Y":
                        self.user_choice_2(4)
                        return ":)", None # returns this value to stop the books available from printing multiple times with the recursion 
                    elif not(try_again == "N"):
                        print("Invalid Input. Please input Y or N.")
                    else:
                        return None, None

    def access_book_info_by_id(self, book_id, book_list):
        for book in range(len(book_list)):
            if (book_list[book]['id_'] == book_id):
                print("\nBook info: ")
                print(f"ID: {book_list[book]['id_']} -- {book_list[book]['title']} by {book_list[book]['author']} -- copies: {book_list[book]['copies']} -- times borrowed: {book_list[book]['times_borrowed']}")

    #------------------------ BORROWING BOOK ------------------------#
    def borrow_book_by_id(self, book_list, book_id):
        # finds the proper book (the one that matches the inputted book_id) and updates the times borrowed and the copies in the library

        again = 'yes' # variable allowing this code to run until you find a book_id that matches what you want
        while again == 'yes':
            for book in range(len(book_list)):
                if book_list[book]['id_'] == book_id:
                    book_list[book]['times_borrowed'] = int(book_list[book]['times_borrowed']) + 1 # one more person has borrowed this book now
                    book_list[book]['copies'] = int(book_list[book]['copies']) - 1 # one less copy is now available in the library at the moment
                    self.write_book_to_file(book_list) 
                    again = 'no' # no need to run this code again as the book was found
                    break
                elif book == len(book_list) - 1: # if the code reaches the end of book_list and the book_id hasn't matched
                    print("Book ID not found.\n") 
                    try_again = "dummy" # place-holder
                    while not(try_again == 'Y' or try_again == 'N'):
                        try_again = input("Would you like to try again? (Y/N): ").upper()
                        if try_again == "N":
                            print("\nSorry we couldn't help. We hope to see you again!")
                            again = 'no'
                            return ":("
                        elif not(try_again == 'Y'):
                            print("Invalid Input. Please input Y or N.")
                        else:
                            book_id = input("Type the ID NUMBER of the book which you would like to check out: ")

    #------------------------ RETURNING BOOK ------------------------#
    def return_book_by_id(self, book_list, book_id):
        # updates the number of copies in the library once a book is returned

        for book in range(len(book_list)):
            if book_list[book]['id_'] == book_id:
                book_list[book]['copies'] = int(book_list[book]['copies']) + 1 # book back in library
                self.write_book_to_file(book_list)
                break

    #------------------------ SAVE INFO TO FILE ------------------------# 
    def write_book_to_file(self, book_list):
        # writes the full list of books in the library system to the books.csv file

        fd = open('books.csv', 'w')
        fieldnames = []
        for key in book_list[0].keys():
            fieldnames.append(key)
        csv_writer = csv.DictWriter(fd, fieldnames=list(fieldnames))
        csv_writer.writeheader()
        csv_writer.writerows(book_list)
    
        fd.close()

    #------------------------ BOOK SERVICES CHOICE ------------------------#    
    def user_choice_2(self, input_):
        # allows the user to choose what aspect of Book Services they would like to access

        choice = False # variable to see if the user types in a proper choice
        book_list = self.read_books()

        while (choice == False):
            ## Read the book titles in the database ##
            if (input_ == 1):
                self.books_available(book_list, 'manager') # shows all books
                choice = True

            ## Add a book to the database ##
            elif (input_ == 2):
                print("\nAdding New Book:")
                self.add_book()
                print("Your book has been successfully added :)")
                book_list = self.read_books()
                self.books_available(book_list, 'manager') # prints new book list to prove addition
                choice = True

            ## Remove a book from the database ##
            elif (input_ == 3):
                print("Removing Book:")
                if not(len(book_list) == 0): # has to be at least one book in the system to remove 
                    book_list = self.remove_book(book_list)
                    if (not(book_list == None) and not(book_list == ":)")): # remove_book will return None if the user says they don't want to try again and will return :) if the user took more than one try to get the ID
                        self.write_book_to_file(book_list)
                        print("\nYour book has been successfully removed :)\n")
                        book_list = self.read_books()
                        self.books_available(book_list, 'manager') # prints new book list to prove removal
                    elif book_list == None:
                        print("\nSorry we couldn't help. Come again!\n")
                else:
                    print("There aren't any books in the system yet! Try again after some have been added.")
                choice = True
            
            ## Modify the number of copies of a particular book ##
            elif (input_ == 4):
                print("Modifying Book Count:")
                if not(len(book_list) == 0): # has to be at least one book in the system to modify 
                    book_list, book_id = self.modify_book_count(book_list)
                    if (not(book_list == None) and not(book_list == ":)") and not(book_id == None)): # modify_book_count will return None if the user says they don't want to try again and will return :) if the user took more than one try to get the ID
                        self.write_book_to_file(book_list)
                        print("\nThe book count has been successfully modified!")
                        book_list = self.read_books()
                        self.access_book_info_by_id(book_id, book_list)
                    elif ((book_list == None) and (book_id == None)):
                        print("\nSorry we couldn't help. Come again!\n")
                else:
                    print("There aren't any books in the system yet! Try again after some have been added.")
                choice = True
            
            ## If the user inputs something not recoginzed ##
            else:
                print("Something went wrong :( Try Again")
                print("---------------------------------------")
                print("Choose your option:")
                print("1 - Read the book titles available\n2 - Add a book to the database\n3 - Remove a book from the database\n4 - Modify a particular book's count\n")
                input_ = int(input())

# Joy and Annie wrote this function together :)                  
def borrow_book(lender_id):

    choice = False
    book = Books(None, None, None, None, None)
    while (choice == False):
        if lender_id == None: # Will be none if the user asked to borrow a book, will not be none if the user was prompted to borrow a book after returning
            answer = input("Are you a new or returning lender? (N/R): ")
        else:
            answer = 'R' # if the user is coming from returning, they must be a returning lender
        
        # new lender process
        if answer.upper() == 'N':
            print("\nWe'll need to get you signed up before you can check out\n")
            lender_name = input('What is your name? ') 
            lender1 = Lender()
            lender1.add_lender(name=lender_name)
            print(f"\nAlright you are all signed up, {lender_name}.")
            print("What book would you like to borrow?")
            book_list = book.read_books()
            book.books_available(book_list, 'customer')
            book_id = input("Type the id number of the book which you would like to borrow: ")
            answer = book.borrow_book_by_id(book_list, book_id)
            lender_id = lender1.get_lender_by_name(lender_name)
            date_borrowed = input("Input Date Borrowed: ") 
            result = lender1.borrow_book(lender_id=lender_id, book_id=book_id, date_borrowed=date_borrowed)
            if result==0:
                print("Thank you for borrowing your book!")
            elif result==1:
                payment_amount = float(input("Input payment amount: "))
                lender1.pay_penalty(lender_id=lender_id, payment_amount=payment_amount)
            if answer == None:
                print("Your book is due 7 days after the borrow date!")
            choice = True
        
        # returning lender process
        elif answer.upper() == 'R':
            if lender_id == None: # only runs if the user asked to borrow a book, if the user is coming from returns, we already asked for their ID
                print("\nWelcome Back!\n")
                lender_id = input("Input your Lender ID: ")
            lender1 = Lender()
            penalty = lender1.get_penalty_by_lender_id(lender_id)
            if penalty > 10.0:
                print("Your penalty is more than $10 so you cannot borrow a book until you pay your charges!")
                payment_amount = float(input("Input payment amount: "))
                lender1.pay_penalty(lender_id=lender_id, payment_amount=payment_amount)
            else:
                print("What book would you like to check out?")
                book_list = book.read_books()
                book.books_available(book_list, 'customer')
                book_id = input("Type the id number of the book which you would like to check out: ")
                answer = book.borrow_book_by_id(book_list, book_id)
                date_borrowed = input("Input Date Borrowed: ") 
                result = lender1.borrow_book(lender_id=lender_id, book_id=book_id, date_borrowed=date_borrowed)
                if result==0:
                    print("Thank you for borrowing your book!")
                elif result==1:
                    payment_amount = float(input("Input payment amount: "))
                    lender1.pay_penalty(lender_id=lender_id, payment_amount=payment_amount)
                if answer == None:
                    print("Your book is due 7 days after the borrow date!")
            choice = True
        else:
            print("Invalid Input. Please input N or R.")

# Joy and Annie wrote this function together :)
def return_book():
    book = Books(None, None, None, None, None)
    lender_id = input("What is your lender ID: ")
    # Lender stuff about payment and everything
    book_list = book.read_books()
    lender1 = Lender() 
    book_id = lender1.get_book_id_by_id(lender_id)
    if book_id == '':
        print("You have no books to return")
    else:
        result = lender1.return_book(lender_id=lender_id, book_id=book_id)
        if result==0:
            book.return_book_by_id(book_list, book_id)
            print("Thank you for returning your book!")
            print("\nWould you like to borrow another book?")
            check_out = input("Y/N: ")
            if check_out.upper() == 'Y':
                borrow_book(lender_id)
            else:
                print("Thanks for coming!\n")
        elif result==1:
            print(f"We're sorry your lender_id:{lender_id} does not exist!")

# Annie wrote this function :)
def original_user_choice(input_):
    choice = False
    while choice == False:
        if input_ == '1':
            print("\nWelcome to Lender Services!\n")
            print("1 - Add New Lender\n2 - Remove Lender\n")
            lender1 = Lender()
            lender1.user_choice_1(input("Choose your option: "))
            choice = True
        elif input_ == '2':
            print("\nWelcome to Book Services!\n")
            print("1 - Read the book titles in the database\n2 - Add a book to the database\n3 - Remove a book from the database\n4 - Modify a particular book's count\n")
            book = Books(None, None, None, None, None)
            book.user_choice_2(int(input("Choose your option: ")))
            choice = True
        elif input_ == '3':
            print("\nLet's Borrow a Book!\n")
            borrow_book(None)
            choice = True
        elif input_ == '4':
            print("\nWelcome Back! Let's get that book returned!\n")
            return_book()
            choice = True
        elif input_ == '5':
            print("\nWelcome to Payment Services!\n")
            print("1 - Check Penalty Owed\n2 - Pay Penalty\n")
            lender1 = Lender()
            answer = lender1.check_or_pay(input("Choose your option: "))
            if answer == ":)":
                print("\nThanks for coming!\n")
            choice = True
        else:
            print("\nInvalid Input. Try Again\n")
            print("What can we help you with today?")
            print("1 - Lender Services\n2 - Book Services\n3 - Borrow a Book\n4 - Return a Book\n")
            input_ = input("Choose your option: ")

if __name__ == "__main__":

    print("\nWelcome to the Library!\n")
    print("What can we help you with today?")
    print("1 - Lender Services\n2 - Book Services\n3 - Borrow a Book\n4 - Return a Book\n5 - Check / Pay Fees\n")
    option = input("Choose your option: ")
    original_user_choice(option)

