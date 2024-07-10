import gspread
from google.oauth2.service_account import Credentials
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
# const for security file not to be tracked
CREDS = Credentials.from_service_account_file('creds.json')
# const for credentials scoped
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
# const to allow auth of gspread client within these scoped credentials
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
# const to open spread sheet
SHEET = GSPREAD_CLIENT.open('budget_planner')




tracker = SHEET.worksheet('tracker')
summary = SHEET.worksheet('summary')


all_values = tracker.get_all_values()


# since first row is a header, skip it
existing_months = tracker.col_values(1)[1:]  # columns are 1 based not 0



full_months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]



# Create a dictionary for month abbreviations
# this line was created with help of chat GPT)
# only first 3 letters needed, making it easy for the user
month_abbr = {month[:3].capitalize(): month for month in full_months}
#set new_month as global variable to acess throughout the code
new_month = ""
data = {}



def budget_decision():
    global new_month


    while True:
        print('Question:  "What would you like to do now? \n')
        print('1. Display Budget Summary \n')
        print('2. Edit Current Budget \n')
        print('3. EXIT \n')
        try:
            choice = int(input('Enter Your Choice (1, 2 or 3) Here: ').strip())
            print("\n")
            if choice == 1:
                budget_summary(new_month)
                break
            elif choice == 2:
                add_income(new_month)
                break
            elif choice == 3:
                print("Exiing the program")
                break
            else:
                print('Number Out Of Range.\n')
                print('Please Enter Number From The List Provided:\n')
        except ValueError:
            print('Invalid Data. Please Enter Number From The List.\n')

###############################################################################
 
def add_income(new_month):

    """
    Append income data to the existing month
    """
    while True:
        try:
            print(f"{new_month} INCOME: Type in name and amount (e.g.: salary, 2000): \n")
            category, income = input().split(',')
            tracker.append_row([new_month, category.strip(), income.strip(), ''])
            #create a key :value dict where key is not changing
            data.setdefault(new_month, {'Category': [], 'Income': [], 'Outgoings': []})
            data[new_month]['Category'].append(category.strip())
            data[new_month]['Income'].append(income.strip())
            print(f"Added {income} to {category} for {new_month}.\n")
        except ValueError:
            print('Invalid input format, Please use format: "name, amount". \n')
            continue

        print("Add More - press ENTER ")
        print("Go To Next Stage - Type 'N' \n")
        decision = input()
        if decision.lower() == "n":
            add_outgoings(new_month)
            break



def add_outgoings(new_month):

    """
    Append income data to the existing month
    """
    while True:
        try:
            print(f"{new_month} OUTGOINGS: Type in name and amount (e.g.: shop, 2000): ")
            category, outgoings = input().split(',')
            tracker.append_row([new_month, category.strip(), '', outgoings.strip()])
            data.setdefault(new_month, {'Category': [], 'Income': [], 'Outgoings': []})
            data[new_month]['Category'].append(category.strip())
            data[new_month]['Outgoings'].append(outgoings.strip())
            print(f"Added {outgoings} to {category} for {new_month}.\n")
        except ValueError:
            print('Invalid input format, Please use format: "name, amount". \n')
            continue

        print("1. Press ENTER to continue ")
        print("2. Type 'N' for Next Stage \n")
        decision = input()
        if decision.lower() == "n":
            budget_decision()
            break

def chose_category(new_month):
    """
    Let user chose whatever category (income or outcome).
    """
    while True:
        print(f'What Category You Are Interested In for {new_month} ? ')
        print('Please chose your category(type in number only: 1 or 2): \n')
        print('1. Income \n')
        print('2. Outgoings \n')
        print('3. EXIT \n')
        try:
            choice = int(input('Please Enter Your Choice Here: \n').strip())
            if choice == 1:
                add_income(new_month)
                break
            elif choice == 2:
                add_outgoings(new_month)
                break
            elif choice == 3:
                print("Exitng the program")
                break
            else:
                print('Number Out Of Range.\n')
                print('Please Enter Number From The List Provided:\n')
        except ValueError:
            print('Invalid Data. Please Enter Number From The List.\n')



def generate_month():
    """
    Confirm weather or not month exists in the tracking list.
    If not generate new one and append tothe lsit
    """
    global new_month

    #print('Please Type First 3 letters Of The Month You Wish To Add:\n')
    while True:
        try:
            user_input = input('Please Type First 3 letters Of The Month You Wish To Add:\n').strip().capitalize()
            new_month = month_abbr.get(user_input)
            if new_month:
                if new_month in existing_months:
                    print(f'{new_month} Already Exists')
                    print('Please Add New Month or :\n')

                    print('1. To EDIT This Month')
                    print('2. Go Back To Main Menu')
                    print('3. To ADD New Month \n')
                    
                    print('Please Enter Your Choice Here: ')
                    choice = (input('\n').strip())   
                    if choice == '1':
                        chose_category(new_month)
                        break
                    elif choice == '2':
                        main()
                        break
                    elif choice == '3':
                        continue
                else:
                    print(f"Creating new month: {new_month}")
                    # append month to the google sheet tracker
                    #tracker.append_row([new_month, '', '', ''])
                    #existing_months.append(new_month)
                    data[new_month] = {"Category": [], "Income": [], "Outgoings": []}
                    print(f"{new_month} has been added sucessfully\n")
                    ("\n")
                    chose_category(new_month)
                    break
            else:
                print(f"{user_input} Does not match the criteria, please try again. \n")
        except ValueError:
            print('Invalid Data.\n')



def budget_summary(new_month):
    """
    Filter through the data and display only one with coresponding month
    """


    # Pull data from tracker worksheet
    all_values = tracker.get_all_values()

    # List to collect all the data with chosen month
    month_rows = []
   
    total_income = 0
    total_outgoings = 0


    for row in all_values:
        if row[0] == new_month:
            month_rows.append(row)
            # Append filtered rows to the summary worksheets
            income = int(row[2]) if row[2] else 0
            outgoings = int(row[3]) if row[3] else 0
            total_income += income
            total_outgoings += outgoings


    # Calculate balance
    balance = total_income - total_outgoings


    # Append totals to the 'summary' worksheet
    summary.append_row([new_month, total_income, total_outgoings, balance])
    summary_data = {"Month": [new_month], "Total income": [total_income], "Total outgoings": [total_outgoings], "balance": [balance]}


    if not month_rows:
        print(f"no data available for {new_month}.")
    else:
        print(f'Summary for {new_month}: Total Income: {total_income}, Total Outgoings :{total_outgoings}, Balance: {balance}\n')
        print(f"Detailed Data for {new_month}:\n")
        for row in month_rows:
            print(row)
    return summary_data




def chose_month():
    """
    fetch month that user is interested in.
    """

    global new_month

    print("What month are you interested in ? ")
    while True:
        try:
            user_input = input().strip().capitalize()
            new_month = month_abbr.get(user_input)
            if new_month in existing_months:
                budget_summary(new_month)
            else: 
                if new_month in full_months and new_month not in existing_months:
                    print(f'{new_month} Have No Current Record')
                print("1. To Generate New Month - Type 'G' \n")
                print("2. Go Back To Main Menu - press 'B' \n")
                decision = input().strip()
                if decision.lower() == 'g':
                    generate_month()
                elif decision.lower() == 'b':
                    main()
                    break
        except ValueError:
            print('Invalid Data. Please Try Again\n')



def main():
    """
    Welcome Message to the user with options to chose from for the next step.
    """


    print('*** WELCOME TO BUDGET TRACKER ***\n')
    print('WOULD YOU LIKE TO GET CLEAR ON WHERE YOUR MONEY GOES ?\n')
    print("LET'S GET STARTED THEN!\n")


    # loop throught the choices2
    # Source : Python Exception Handling(CI)
    while True:
        print('Please choose from the following options: \n')
        print('1. Display Budget Summary\n')
        print('2. Generate Budget\n')
        print('3. Edit Budget\n')
        print('4. EXIT\n')
        try:
            choice = int(input('Choice: 1, 2, 3, 4. Please Enter Number: ').strip())
            print("\n")
            if choice == 1:
                chose_month()
                break
            elif choice == 2:
                generate_month()
                break
            elif choice == 3:
                chose_category(new_month)
                break
            elif choice == 4:
                print("Exitng the program \n")
                print("GOODBYE")
                break
            else:
                print('Number Out Of Range.\n')
                print('Please Enter Number From The List Provided:\n')
        except ValueError:
            print('Invalid Data. Please Enter Number From The List.\n')


generate_month()
# calling the main function
main()






