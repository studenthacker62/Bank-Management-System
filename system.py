import json

accounts = []
account_numbers = set()
try:
    with open("data.json", "r") as f:
        accounts = json.load(f)
except FileNotFoundError:
    accounts = []


def create_account(account_numbers, accounts):
    while True:

        account_number = input("Enter account number (or press [0] to go back): ")
        if account_number == "0":
            return None

        if account_number == "":
            print("Enter valid account number!")
            continue
        elif account_number in account_numbers:
            print("Account number already exists!")
            continue  # start loop again

        name = input("Enter your name: ")
        if name == "":
            print("Enter valid username!")
            continue

        try:
            age = int(input("Enter your age: "))
            if not (18 <= age <= 70):
                print("Enter valid age!")
                continue
        except ValueError:
            print("Age must be in digits!")
            continue

        try:
            initial_deposit = int(input("Enter your intitial deposit: "))
            if not (initial_deposit >= 1000):
                print("Enter valid initial deposit!")
                continue
        except ValueError:
            print("initial deposit must be in digits!")
            continue

        account = {
            "Account_No": account_number,
            "Name": name,
            "Age": age,
            "Balance": initial_deposit,
            "Transactions": [],
        }

        accounts.append(account)
        account_numbers.add(account_number)
        return accounts


def search_account(accounts, account_number):
    for account in accounts:
        if account_number == account["Account_No"]:
            return account
    return None


def deposit_money(account_number):
    account = search_account(accounts, account_number)
    if account is not None:
        try:
            money = int(input("Enter amount to deposit: "))
            if money > 0:
                account["Balance"] += money
                account["Transactions"].append({"Type": "Deposit", "Amount": money})
            else:
                print("\nDeposit amount must be positive.\n")
        except ValueError:
            print("\nInvalid data type\n")
    elif account is None:
        print("\nAccount not found.\n")


def withdraw_money(account_number):
    account = search_account(accounts, account_number)
    if account is not None:
        try:
            money = int(input("Enter amount to withdraw: "))
            if 0 < money <= account["Balance"]:
                account["Balance"] -= money
                account["Transactions"].append({"Type": "Withdraw", "Amount": money})
            else:
                print(
                    "\nWithdraw amount must be positive and less then actual balance.\n"
                )
        except ValueError:
            print("\nInvalid data type\n")
    elif account is None:
        print("\nAccount not found.\n")


def transfer_funds(accounts):

    sender_number = input("Enter sender account number: ")
    receiver_number = input("Enter receiver account number: ")

    if sender_number == receiver_number:
        print("\nCannot transfer to the same account.\n")
        return
    else:
        sender_account = search_account(accounts, sender_number)
        receiver_account = search_account(accounts, receiver_number)

        if sender_account is not None and receiver_account is not None:
            try:
                money = int(input("Enter amount to Transfer: "))
            except ValueError:
                print("\nInvalid data type")
                return

            if 0 < money <= sender_account["Balance"]:
                sender_account["Balance"] -= money
                sender_account["Transactions"].append(
                    {"Type": "Transfer Out", "Amount": money, "To": receiver_number}
                )
                receiver_account["Balance"] += money
                receiver_account["Transactions"].append(
                    {"Type": "Transfer In", "Amount": money, "From": sender_number}
                )

            else:
                print(
                    "\nTransfer amount must be positive and less then actual balance."
                )

        else:
            print("\nAccounts not found.\n")


def show_transaction_history(accounts):
    if accounts == []:
        print("\nNo accounts created yet")

    for account in accounts:
        print(f"\nAccount: {account['Account_No']}")

        if account["Transactions"] != []:
            for transaction in account["Transactions"]:
                print(f"{transaction}")

        else:
            print("No transactions yet")
            continue


def display_all_accounts(accounts):
    if accounts == []:
        print("\nNo accounts created yet")
    for account in accounts:
        print("\n--------------------------------\n")
        print(f"Account_No: {account['Account_No']}")
        print(f"Age: {account['Age']}")
        print(f"Name: {account['Name']}")
        print(f"Balance: {account['Balance']}")
        print(f"Transactions: {account['Transactions']}\n")
        print("--------------------------------")


def bank_statistics(accounts):
    if accounts != []:
        total_accounts = len(accounts)
        bank_balance = 0
        heighest_balance = 0
        lowest_balance = accounts[0]["Balance"]
        for account in accounts:
            bank_balance += account["Balance"]
            if account["Balance"] > heighest_balance:
                heighest_balance = account["Balance"]
            if account["Balance"] < lowest_balance:
                lowest_balance = account["Balance"]

        average_balance = bank_balance / total_accounts

        print("\n--------------------------------")
        print(f"Total Accounts: {total_accounts}")
        print(f"Highest Balance: {heighest_balance}")
        print(f"Lowest Balance: {lowest_balance}")
        print(f"Total Bank balance: {bank_balance}")
        print(f"Average Balnce: {average_balance}")
        print("--------------------------------")
    else:
        print("\nNo accounts created yet")


def save_data(accounts):
    with open("data.json", "w") as f:
        json.dump(accounts, f)
    print("\nData saved successfuly")


def erase_data(accounts):
    accounts.clear()
    with open("data.json", "w") as f:
        json.dump(
            accounts,
            f,
        )
    print("\nData erased succssfully")


def startup_menu(account_numbers, accounts):
    while True:
        print("\n-->MENU:-\n")
        print("1.Create account")
        print("2.Search account")
        print("3.Deposit money")
        print("4.Withdraw money")
        print("5.Display all accounts")
        print("6.Transfer funds")
        print("7.Show transaction history")
        print("8.Bank statistics")
        print("9.Save data")
        print("10.Erase data")
        print("11.Exit Menu\n")

        try:
            option = int(input("Select an option: "))
        except ValueError:
            print("Choose valid option!")
            continue

        if option == 1:
            result = create_account(account_numbers, accounts)
            if result is None:
                print("\n//Account creation cancelled.\n")
            else:
                print("\n//Account created successfully.\n")

        elif option == 2:
            account_number = input("Enter account number: ")
            result = search_account(accounts, account_number)
            if result is None:
                print("\nAccount not found.\n")
            else:
                print(f"\n{result}\n")

        elif option == 3:
            account_number = input("Enter account number: ")
            deposit_money(account_number)

        elif option == 4:
            account_number = input("Enter account number: ")
            withdraw_money(account_number)

        elif option == 5:
            display_all_accounts(accounts)

        elif option == 6:
            transfer_funds(accounts)

        elif option == 7:
            show_transaction_history(accounts)

        elif option == 8:
            bank_statistics(accounts)

        elif option == 9:
            save_data(accounts)

        elif option == 10:
            erase_data(accounts)

        elif option == 11:
            break
        else:
            print("//Enter options from below\n")


startup_menu(account_numbers, accounts)
