import pyodbc
import time
from datetime import datetime
# MSSQL veritabanına bağlan
connection = pyodbc.connect(
    'Driver={SQL Server};'
    'Server=OSMAN\SQLEXPRESS01;'
    'Database=bank;'
    'UID=osman;'  # Kullanıcı adı
    'PWD=osman1234;'  # Şifre
)


def start():
    global datetime
    time = datetime.now()
    hour_minute_second = time.strftime("%H:%M:%S")
    date = time.strftime("%Y/%m/%d")
    print("  --- WELCOME TO HALIC BANK ---")
    print("    --------------------------")
    print("           ISTANBUL       ")
    print("     ""— " + date + " " + hour_minute_second + " —")
    print("    -----------------—-------")
    print("1. Login\n2. Exit")
    choice = int(input(">>> "))

    if choice == 1:
        login_choice()
    else:
        print("Good bye!")


def login_choice():
    print("""What do you want to login as:
1. User
2. Go Back
""")
    choice = int(input(">>> "))
    if choice == 1:
        login()

    elif choice == 2:
        start()

    else:
        print("Please enter a valid number as input.")
        login_choice()


def login():
    username = input("Username: ")
    password = input("Password: ")

    cursor = connection.cursor()
    query = "SELECT * FROM Users WHERE Username = ? AND Userpass = ?"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    if result:
        mainmenu(username, password)
    else:
        print("Incorrect username or password. Access denied.")
        login()




def mainmenu(username, password):

    print(username + " Welcome to Ozer Bank")
    print("Please enter the number of the service:")
    print("""
1. Withdraw Money
2. Deposit Money
3. Transfer Money
4. My Account Information
5. Account Settings
6. Logout""")
    choice = int(input(">>> "))

    if choice == 1:
        withdraw_funds(username)
        mainmenu(username, password)
    if choice == 2:
        deposit_funds(username)
    if choice == 3:
        transfer_funds(username)
        mainmenu(username, password)
    if choice == 4:
        zaman = datetime.now()
        saat = zaman.strftime("%H:%M:%S")
        tarih = zaman.strftime("%Y/%m/%d")
        print("—— Ozer Bank ——")
        print("— " + tarih + " " + saat + " —")
        print("———————————–")
        account_information(username)
        mainmenu(username, password)
    if choice == 5:
        pass
    if choice == 6:
        login_choice()


def account_information(username):
    cursor = connection.cursor()
    query = "SELECT Amount FROM Users WHERE Username = ?"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    if result:
        Amount = result[0]
        print(f"Username: {username}")
        print(f"Balance: {Amount} USD")
    else:
        print("User not found.")


def transfer_funds(username):

    cursor = connection.cursor()

    
    recipient_username = input("Enter the recipient's username: ")
    transfer_amount = int(input("Enter the transfer amount: "))

   
    cursor.execute("SELECT Amount FROM Users WHERE Username = ?", username)
    sender_balance = cursor.fetchone()[0]

    if transfer_amount > sender_balance:
        print("Insufficient funds for transfer. Transfer failed.")
    else:
     
        cursor.execute(
            "SELECT Amount FROM Users WHERE Username = ?", recipient_username)
        recipient_balance = cursor.fetchone()[0]

     
        new_sender_balance = sender_balance - transfer_amount
        new_recipient_balance = recipient_balance + transfer_amount

       
        cursor.execute("UPDATE Users SET Amount = ? WHERE Username = ?",
                       (new_sender_balance, username))

        # Alıcının bakiyesini güncelle
        cursor.execute("UPDATE Users SET Amount = ? WHERE Username = ?",
                       (new_recipient_balance, recipient_username))

        connection.commit()
        print(
            f"Transfer successful. Your new balance: {new_sender_balance:.2f} USD")


def withdraw_funds(username):

    cursor = connection.cursor()

    
    withdraw_amount = int(input("Enter the amount to withdraw: "))

    
    cursor.execute("SELECT Amount FROM Users WHERE Username = ?", username)
    user_balance = cursor.fetchone()[0]

    if withdraw_amount > user_balance:
        print("Insufficient funds. Withdrawal failed.")
    else:
        
        new_balance = user_balance - withdraw_amount
        cursor.execute(
            "UPDATE Users SET Amount = ? WHERE Username = ?", (new_balance, username))
        connection.commit()
        print(
            f"Withdrawal successful. Your new balance: {new_balance:.2f} USD")
4


def deposit_funds(username):

    cursor = connection.cursor()

   
    deposit_amount = int(input("Enter the amount to deposit: "))

    
    cursor.execute("SELECT Amount FROM Users WHERE Username = ?", username)
    user_balance = cursor.fetchone()[0]

  
    new_balance = user_balance + deposit_amount
    cursor.execute("UPDATE Users SET Amount = ? WHERE Username = ?",
                   (new_balance, username))
    connection.commit()
    print(f"Deposit successful. Your new balance: {new_balance:.2f} USD")






start()
