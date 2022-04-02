# Write your code here
import random
import sqlite3
class Bank:

    def __init__(self):
        self.account_digit = 400000000000000
        self.balance = 0
        self.accounts = {}

    #Method to create database
    def create_database(self):
        self.conn = sqlite3.connect("card.s3db") # connection to database file.
        self.c = self.conn.cursor() #cursor object for executing query functionality
        self.c.execute('''
                CREATE TABLE IF NOT EXISTS card (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
                number TEXT NOT NULL UNIQUE,
                pin TEXT NOT NULL,
                balance INTEGER DEFAULT 0 NOT NULL
                );
                ''')
        self.conn.commit() # committing your query
        self.conn.close()

    # Algorithm to validate credit card number and returns it by using luhn algorithm
    def luhns_algorithm(self):

        checksum = 0  # 16th number of the card which is the remaining number need to be a number divisable by 10
        account_identifier = random.randint(000000000, 999999999) # 15 digit number of card
        tot_account = self.account_digit + account_identifier
        acc_no_list = [int(x) for x in str(tot_account)]
        # Using for loop to multiply digits in even index
        for i in range(0, len(acc_no_list) + 1, 2):
            acc_no_list[i] *= 2
            if acc_no_list[i] > 9: # if the number is greater than 9 subtract the number by 9
                acc_no_list[i] -= 9
        # Acquiring the appropriate number for checksum so that the sum of all the 16 digits is divisable by 10
        for i in range(0, 10):
            if (sum(acc_no_list) + i) % 10 == 0:
                checksum = i
                break
            else:
                continue
        return str(tot_account) + str(checksum)

    #Card validity checker
    def validity(self, acc):
        self.acc = acc
        acc_no_list = [int(x) for x in self.acc]
        checksum = acc_no_list.pop(-1)
        # Using for loop to multiply digits in even index
        for i in range(0, len(acc_no_list) + 1, 2):
            acc_no_list[i] *= 2
            if acc_no_list[i] > 9:  # if the number is greater than 9 subtract the number by 9
                acc_no_list[i] -= 9
        # Acquiring the appropriate number for checksum so that the sum of all the 16 digits is divisable by 10
        if (sum(acc_no_list) + checksum) % 10 == 0:
            return True
        else:
            return False

    #Method to generate pin for your account.
    def pinno(self):
        return str(random.randint(1000, 9999))

   # Method that is called at the start of the program
    def start(self):
        action = int(input("1. Create an account\n"
                           "2. Log into account\n"
                           "0. Exit"))
        if action == 1:
            self.create_account()
            self.start()
        elif action == 2:
            self.log_in()
        elif action == 0:
            exit()

    # Method to create a new account
    def create_account(self):
        self.create_database()
        card_no = self.luhns_algorithm()
        pin = self.pinno()
        print("Your card has been created")
        print("Your card number:")
        print(card_no)
        print("Your card PIN:")
        print(pin)

        #Updating your database with account and pin no
        conn = sqlite3.connect("card.s3db")
        c = conn.cursor()
        param = (card_no, pin)
        c.execute('INSERT INTO card (number, pin) VALUES (?, ?)', param)
        conn.commit()
        conn.close()

        #Saving to self.accounts instance attribute as well
        self.accounts[card_no] = pin # Saves the account no and password in a dictionary.
        self.start()

    #Method that is called after logging into an account.
    def logged_in(self):
        self.conn = sqlite3.connect("card.s3db")
        self.c = self.conn.cursor()

        #Different operations that you can do with this program
        action = int(input("1. Balance\n"
                           "2. Add income\n"
                           "3. Do transfer\n"
                           "4. Close account\n"
                           "5. Log out\n"
                           "0. Exit"))

        self.c.execute("""SELECT balance FROM card WHERE number = (?) """, (self.saved_card_no,))
        self.data = self.c.fetchall()
        if action == 1:
            print("\nBalance: ", self.data[0][0])
            print("\n")
            self.conn.commit()
            self.logged_in()

        elif action == 2:
            i = int(input("Enter income:"))
            self.c.execute('UPDATE card SET balance = (balance + ?) WHERE number = (?);',(i, self.saved_card_no),)
            self.conn.commit()
            print("Income was added!")
            self.logged_in()

        elif action == 3:
            self.c.execute("""SELECT number FROM card""")
            self.acc = self.c.fetchall()
            self.account = [self.acc[x][0] for x in range(len(self.acc))]
            self.conn.commit()
            print("Transfer")
            transfer_account = input("Enter card number:")

            if transfer_account in self.account:
                self.c.execute("""SELECT balance FROM card WHERE number = (?);""", (transfer_account,))
                account_balance = self.c.fetchall()

                self.conn.commit()
                transfer_amount = int(input("Enter how much money you want to transfer:"))

                if transfer_amount > self.data[0][0]:
                    print("Not enough money!")
                    self.logged_in()

                else:
                    self.c.execute('UPDATE card SET balance = (balance + ?) WHERE number = (?)',
                    (transfer_amount, transfer_account))
                    self.conn.commit()
                    self.c.execute('UPDATE card SET balance = (balance - ?) WHERE number = (?)',
                    (transfer_amount, self.saved_card_no))
                    self.conn.commit()

            elif not Bank.validity(self,transfer_account):
                print("Probably you made a mistake in the card number. Please try again!")
                self.logged_in()

            elif transfer_account not in self.account:
                print("Such a card does not exist.")
                self.logged_in()

        elif action == 4:
            self.c.execute('DELETE FROM card WHERE number =(?);', (self.saved_card_no,))
            self.conn.commit()
            del self.accounts[self.saved_card_no]

            self.logged_in()

        elif action == 5:
            print("You have successfully logged out!")
            self.start()

        elif action == 0:
            print("\nBye")
            exit()

    #Method that initializes loggin in to an account.
    def log_in(self):

        self.saved_card_no = str(input("Enter your card number:"))
        self.saved_pin = str(input("Enter your PIN:"))
        if self.saved_card_no in self.accounts and self.accounts[self.saved_card_no] == self.saved_pin:
            print("\nYou have successfully logged in!")
            self.logged_in()
        else:
            print("\nWrong card number or PIN!")
            self.start()

banking = Bank()
banking.create_database()
banking.start()

"""
   While updating the database pass the values inside a tuple.
  
"""





