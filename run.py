# Python Typing Text Effect
# Credits: 101computing.net/python-typing-text-effect/
import time
import sys
import os
import gspread
from google.oauth2.service_account import Credentials

# Constants for google sheets API
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]


# Security file not to be tracked
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
# Authorize of gspread client within these scoped credentials
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('budget_planner')


tracker = SHEET.worksheet('tracker')
summary = SHEET.worksheet('summary')

full_months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]
# Dictionary for month abbreviations
# only first 3 letters needed, making it easy for the user
month_abbr = {month[:3].capitalize(): month for month in full_months}


# since first row is a header, skip it
existing_months = tracker.col_values(1)[1:]  # columns are 1 based not 0
# set new_month as global variable to acess throughout the code
data = {}
new_month = ""


# Tutorial:https://www.101computing.net/python-typing-text-effect/
def typingPrint(text):
    """
    Create a typing like effect for print statements
    """
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)


def typingInput(text):
    """
    Create a typing like effect for inputs statements
    """
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    value = input()
    return value


def clear_screen():
    """
    Function to clear screen for terminal based program
    """
    os.system("clear")


def welcome_page():
    """
    Display welcome message to the user with prompt to confirm entry
    """
    clear_screen()
    #  prefixing the string with an r,to avoid invalid escape sequence
    print(r"""

  _   ______           _            _    ______ _
 | |  | ___ \         | |          | |   | ___ \ |
/ __) | |_/ /_   _  __| | __ _  ___| |_  | |_/ / | __ _ _ __  _ __   ___ _ __
\__ \ | ___ \ | | |/ _` |/ _` |/ _ \ __| |  __/| |/ _` | '_ \| '_ \ / _ \ '__|
(   / | |_/ / |_| | (_| | (_| |  __/ |_  | |   | | (_| | | | | | | |  __/ |
 |_|  \____/ \__,_|\__,_|\__, |\___|\__| \_|   |_|\__,_|_| |_|_| |_|\___|_|
                          __/ |
                         |___/
 """)
    print("\n")
    print('$$$ WELCOME TO THE BUDGET PLANNER $$$\n')
    print('WOULD YOU LIKE TO GET CLEAR ON WHERE YOUR MONEY GOES?')
    print("LET'S GET STARTED THEN!\n")
    print('\n')
    typingInput("Press ENTER to begin... ")


def catch_month():
    """
    Function to catch month that user wants to interact with for validation
    """
    global new_month
    while True:
        clear_screen()
        print('WHAT MONTH YOU ARE INTERESTED IN?\n')
        print('TYPE FIRST 3 LETTERS ONLY')
        print(('e.g.: "Jan" for January\n'))
        user_input = input().strip().capitalize()
        new_month = month_abbr.get(user_input)

        if new_month in existing_months:
            break
        elif new_month in full_months and new_month not in existing_months:
            print(f'{new_month} HAS NO CURRENT RECORD')
            print("WHAT WOULD YOU LIKE TO DO INSTEAD ?\n")
            print("1. Generate new month")
            print("2. Go back to main menu \n")
            print("Press ENTER to try again")

            choice = input().strip()
            if choice == '1':
                generate_month()
                break
            elif choice == '2':
                main()
                break
            elif choice == '':
                continue
        else:
            print('Invalid data. Please try again')


def exit_program():
    """
    Function to exit the program
    """
    clear_screen()
    typingPrint("Exiting the program")
    typingPrint("See you next time!\n")
    typingPrint("GOODBYE")
    exit()


def budget_decision(new_month):
    """
    Prompt user for the next step when previous function was completed
    """
    while True:
        print('HOPE YOU ARE HAPPY WITH WHAT YOU SEE... ')
        print('WHAT WOULD YOU LIKE TO DO NOW?\n')
        print(f'1. Show {new_month} budget breakdown')
        print('2. Go to Main Menu \n3. EXIT\n')
        try:
            choice = int(input('Enter your choice here:\n').strip())
            print("\n")
            if choice == 1:
                budget_breakdown()
                input()  # create space/pause for user to swith between pages
                main()
                break
            if choice == 2:
                main()
                break
            elif choice == 3:
                exit_program()
                break
            else:
                clear_screen()
                print('Number out of range.\n')
                print('Please enter a number from the list provided:\n')
                typingInput("Press Enter to continue...\n")
        except ValueError:
            clear_screen()
            print('Invalid data. Please enter a number from the list.\n')
            typingInput("Press Enter to continue...\n")


def income_categories(new_month):
    """
    Add income from listed categories or create a new one
    """
    clear_screen()
    while True:
        print(f"INCOME FOR {new_month.upper()}:\n")
        print("To add income to pre-set categories, select:")
        print("1. Salary")
        print("2. Sales")
        print("\nTo acess other sections, select:")
        print("3. Create additional Income category")
        print("4. Outgoings")
        print("5. Main menu")
        print("6. EXIT\n")

        try:
            choice = int(input('Enter Your Choice (1-6): \n').strip())
            if choice in [1, 2]:
                category = "Salary" if choice == 1 else "Sales"
                while True:
                    clear_screen()
                    try:
                        income = int(input(
                            f"ENTER YOUR {category.upper()} "
                            f"INCOME: \n").strip())
                        break  # break the loop once input is a number
                    except ValueError:
                        clear_screen()
                        print("Income value must be a digit.\n")
                        typingInput("Press ENTER to continue... ")
                        clear_screen()
                # append data to the summary spreadsheet
                tracker.append_row([new_month, category, income, ''])
                data.setdefault(new_month, {  # setdefault doesnt change
                        'Category': [], 'Income': [],
                        'Outgoings': []})
                data[new_month]['Category'].append(category)
                data[new_month]['Income'].append(income)
                clear_screen()
                typingPrint(f'Amount of €{income:.2f} added successfully '
                            f'to the {new_month} income.\n')
                continue
            elif choice == 3:
                add_income(new_month)
                break
            elif choice == 4:
                outgoings_categories(new_month)
                break
            elif choice == 5:
                main()
                break
            elif choice == 6:
                exit_program()
                break
            else:
                clear_screen()
                print('Number out of range.\n')
                print('Please enter a number from the list provided:\n')
                typingInput("Press Enter to continue...\n")
                clear_screen()
        except ValueError:
            clear_screen()
            print('Invalid data. Please enter a number from the list.\n')
            typingInput("Press Enter to continue...\n")
            clear_screen()


def add_income(new_month):
    """
    Append income data to the existing month
    """
    clear_screen()
    while True:
        print(f"ADDING {new_month.upper()} INCOME:\n")
        print("TYPE NAME AND THE AMOUNT (e.g.: 'Cash, 2000'): ")
        print('NOTE: Amount must be a DIGIT\n')
        try:
            user_input = input().strip().capitalize()
            if ',' in user_input:
                category, income = user_input.split(',')
                category = category.strip()
                income = income.strip()
                # making sure that input is a digit
                if not income.isdigit():
                    raise ValueError("Income amount must be a digit.")

                income = int(income)

                tracker.append_row([
                    new_month, category, income, ''
                ])

                # Create a key:value dict where key is not changing
                data.setdefault(new_month, {
                    'Category': [], 'Income': [],
                    'Outgoings': []
                })
                data[new_month]['Category'].append(category)
                data[new_month]['Income'].append(income)
                clear_screen()
                typingPrint(f'Amount: €{income:.2f} for {category} added '
                            f'successfully to the {new_month} Income.\n')
            else:
                clear_screen()
                raise ValueError("Invalid input format.")
                clear_screen()
        except ValueError as e:
            clear_screen()
            print(f'Error: {e}')
            typingInput("Press ENTER to continue... ")
            clear_screen()
            continue
        print('Press ENTER To Continue Adding...\n')
        print("To acess other sections, select:")
        print("1. Outgoings")
        print("2. Budget Summary")
        print("3. Main Menu\n")

        choice = input('Enter your choice here:\n').strip()
        clear_screen()
        if choice == '1':
            outgoings_categories(new_month)
            break
        elif choice == '2':
            budget_summary(new_month)
            break
        elif choice == '3':
            main()
            break
        clear_screen()


def outgoings_categories(new_month):
    """
    Add outgoings from listed categories or create new one.
    """
    # create list of outgoings to chose from
    outgoings_list = [
        'House Bills', 'School', 'Creche', 'Shopping', 'Cars', 'Health',
        'Entertainment', 'Holidays'
    ]
    clear_screen()
    while True:
        print(f"OUTGOINGS FOR {new_month.upper()}:\n")
        print("To add outgoings to pre-set categories, select: ")
        for i, category in enumerate(outgoings_list, 1):  # create index
            print(f'{i}. {category}')
        print("\nTo acess other sections, select:")

        print('9. Create additional Outgoings category\n10. Main Main')
        print('11. Budget Summary\n12. EXIT\n')
        try:
            choice = int(input('Enter Your Choice (1-11): \n').strip())
            if choice >= 1 and choice <= 8:
                clear_screen()
                category = outgoings_list[choice - 1]
                print(f"What is your OUTGOINGS amount for {category.upper()}?")
                outgoings = int(input().strip())
                tracker.append_row([new_month, category, '', outgoings])
                data.setdefault(new_month, {
                        'Category': [], 'Income': [], 'Outgoings': []})
                data[new_month]['Category'].append(category)
                data[new_month]['Outgoings'].append(outgoings)
                clear_screen()
                typingPrint(f'Amount of €{outgoings:.2f} added '
                            f'sucessfully to {new_month} outgoings.\n')
                continue
            elif choice == 9:
                add_outgoings(new_month)
                break
            elif choice == 10:
                main()
                break
            elif choice == 11:
                budget_summary(new_month)
                break
            elif choice == 12:
                exit_program()
                break
            else:
                clear_screen()
                print('Number out of range.\n')
                print('Please enter a number from the list provided:\n')
                typingInput("Press Enter to continue...\n")
                clear_screen()
        except ValueError:
            clear_screen()
            print('Invalid data. Please enter a number from the list.\n')
            typingInput("Press Enter to continue...\n")
            clear_screen()


def add_outgoings(new_month):
    """
    Append outgoings data to the existing month.
    """
    clear_screen()
    while True:
        print(f"ADDING {new_month.upper()} OUTGOINGS:\n")
        print("TYPE NAME AND THE AMOUNT (e.g.: 'Clothes, 200'): ")
        typingPrint('Note. Amount must be a DIGIT\n')
        try:
            user_input = input().strip().capitalize()
            if ',' in user_input:
                category, outgoings = user_input.split(',')
                category = category.strip()
                outgoings = outgoings.strip()
                if not outgoings.isdigit():
                    raise ValueError("Outgoings amount must be a digit.")
                outgoings = int(outgoings)

                tracker.append_row([
                    new_month, category, '', outgoings])

                # create a key :value dict where key is not changing
                data.setdefault(new_month, {
                        'Category': [], 'Income': [], 'Outgoings': []})
                data[new_month]['Category'].append(category)
                data[new_month]['Outgoings'].append(outgoings)
                clear_screen()
                typingPrint(f'Amount €{outgoings:.2f} for {category} added '
                            f'successfully to {new_month} Outgoings.\n')
            else:
                clear_screen()
                raise ValueError("Invalid input format.")
                clear_screen()
        except ValueError as e:
            clear_screen()
            print(f'Error: {e}')
            typingInput("Press ENTER to continue... ")
            continue
        print('Press ENTER To Continue Adding...\n')
        print("Or choose from following options:")
        print("1. Go To Budget Summary")
        print("2. Go Back to Main Menu\n")
        choice = input('Enter your choice here:\n').strip()
        if choice == '1':
            budget_summary(new_month)
            break
        elif choice == '2':
            main()
            break
        clear_screen()


def generate_month():
    """
    Confirm whether or not month exists in the tracking list.
    If not, generate a new one and append to the list.
    """
    global new_month
    clear_screen()
    while True:
        print("LET'S CREATE A NEW MONTH \n")
        print('TYPE FIRST 3 LETTERS OF THE MONTH:\n')
        print(" 'Jan' for January, 'Feb' for February etc.\n")
        try:
            user_input = input().strip().capitalize()
            new_month = month_abbr.get(user_input)
            clear_screen()
            if new_month:
                if new_month in existing_months:
                    typingPrint(f'Oopsi...{new_month} already EXISTS. ')
                    typingPrint('What would you like to do? \n')
                    print('1. Add Income or Outgoings to this month')
                    print('2. Go back to Main Menu')
                    print('3. Generate new month\n')
                    typingPrint('Please enter your choice: ')
                    choice = (input().strip())
                    if choice == '1':
                        choose_category(new_month)
                        break
                    elif choice == '2':
                        main()
                        break
                    elif choice == '3':
                        continue
                else:
                    print(f"Creating new month: {new_month}")
                    data[new_month] = {
                            "Category": [], "Income": [], "Outgoings": []}
                    typingPrint(f"{new_month} has been added sucessfully\n")
                    ("\n")
                    choose_category(new_month)
                    break
            else:
                clear_screen()
                print(f'"{user_input}" Does not match the criteria.\n')
                print("Please Try Again.\n")
                typingInput("Press Enter to continue...\n")
                clear_screen()
        except ValueError:
            clear_screen()
            print("Oops, somtheing went wrong. Please try again.\n")
            typingInput("Press Enter to continue...\n")
            clear_screen


def choose_category(new_month):
    """
    Function to let user choose between adding income or outgoings
    """
    while True:
        clear_screen()
        print(f'What would you like to do now with {new_month} ?\n')
        print('1. Add Income\n2. Add Outgoings\n3. EXIT\n')
        try:
            choice = int(input('Please Enter Your Choice: \n').strip())
            if choice == 1:
                income_categories(new_month)
                break
            elif choice == 2:
                outgoings_categories(new_month)
                break
            elif choice == 3:
                exit_program()
                break
            else:
                clear_screen()
                print('Number out of range.\n')
                print('Please enter a number from the list provided:\n')
                typingInput("Press Enter to continue...\n")
        except ValueError:
            clear_screen()
            print('Invalid data. Please enter a number from the list.\n')
            typingInput("Press Enter to continue...\n")


def budget_summary(new_month):
    """
    Filter through the data and display only one with corresponding month.
    """
    clear_screen()
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

    balance = total_income - total_outgoings
    # Check if the month already exists in the summary worksheet
    summary_months = summary.col_values(1)  # months are in the first column

    if new_month not in summary_months:
        summary.append_row([new_month, total_income, total_outgoings, balance])

    print(f"Budget Summary for {new_month}")
    print(f"Total Income: €{total_income:.2f}")  # convert into float
    print(f"Total Outgoings: €{total_outgoings:.2f}")
    print(f"Balance: €{balance:.2f}\n")
    budget_decision(new_month)


def budget_breakdown():
    """
    Display budget detailed data to the user.
    """
    global new_month
    clear_screen()
    print(f"Here is your breakdown for month of {new_month}")
    typingPrint("Press ENTER to go back to the Main Menu\n")
    print('\n')

    # display the data so that it can be acessed and deleted
    all_values = tracker.get_all_values()
    if not all_values:
        print("Data is not availabe")
        typingInput("Press Enter to continue... \n")
        return

    # skip the header row (first row)
    data_rows = all_values[1:]

    # design the table
    print("-" * 65)
    print(
        f"{'Index':<7}{'Month':<15}{'Category':<18}"
        f"{'Income':<10}{'Outgoings':<10}")
    print("-" * 65)
    for index, row in enumerate(data_rows, start=1):
        month = row[0]
        if new_month in month:
            category = row[1]
            income = row[2] if row[2] else '0'
            outgoings = row[3] if row[3] else '0'
            print(
                f'{index:<7}{month:<15}{category:<18}'
                f'{income:<10}{outgoings:<10}')


def delete_entry(new_month):
    """
    Delete data from the tracker worksheet based on user input.
    """
    all_values = tracker.get_all_values()
    while True:
        budget_breakdown()
        try:
            if not all_values:
                print("No data available to Delete")
                typingInput("Press Enter to continue... \n")
                return
            print("\n")
            index_to_delete = int(input(
                    "What line number you wish to delete?\n").strip())
            if index_to_delete > 0 and index_to_delete < len(all_values):
                tracker.delete_rows(index_to_delete + 1)  # +1indices start at1
                clear_screen()
                typingInput(f'Entry at line {
                        index_to_delete} deleted sucesfully\n')
                print("Press ENTER to go back to the Main Menu... \n")
                main()
            else:
                clear_screen()
                print("Invalid index. Enter number within the range.")
        except ValueError:
            clear_screen()
            print("Invalid input. Please enter a number.")


def main():
    """
    Display main menu to the user with the core functions
    """
    while True:
        clear_screen()
        print('Please choose from the following options: \n')
        print('1. Display budget summary')
        print('2. Generate budget')
        print("3. Add data to the existing month ")
        print('4. Delete entry')
        print('5. EXIT\n')
        try:
            choice = int(input('Please Enter a Number(1-5):\n').strip())
            if choice == 1:
                catch_month()
                budget_summary(new_month)
                break
            elif choice == 2:
                clear_screen()
                generate_month()
                break
            elif choice == 3:
                catch_month()
                choose_category(new_month)
                break
            elif choice == 4:
                catch_month()
                delete_entry(new_month)
                main()
                break
            elif choice == 5:
                clear_screen()
                exit_program()
                break
            else:
                clear_screen()
                print('Number out of range.\n')
                print('Please enter a number from the list provided:\n')
                typingInput("Press Enter to continue...\n")
        except ValueError:
            clear_screen()
            print('Invalid data. Please enter a number from the list.\n')
            typingInput("Press Enter to continue...\n")


# calling the main function
welcome_page()
main()
