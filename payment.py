

import psycopg2
import uuid
import random



def generate_account_number():
    number=random.randint(1000000000,9999999999)
    return number
# payment cli terminal

conn=psycopg2.connect(host='Your host name',dbname='Your database name',user='Your username',password='Your password',port='your port number')
cur=conn.cursor()
cur.execute('''
CREATE TABLE IF NOT EXISTS payment(account_no VARCHAR(10),Bal VARCHAR(10),password VARCHAR(10),name VARCHAR(1000));
''')
conn.commit()
def bank_payment():
    print('Welcome to zenith payment Cli\nAlready have an account,Press 1\nNeed an account,Press 2')
    print('-'*20)
    user_input=input('1 or 2:')
    if user_input == '1':
        print('Enter your  username and password')
        account=input('Your account number:')
        pass_=input('Your Password:')
        cur.execute('SELECT account_no,bal,name FROM payment WHERE account_no= %s AND password= %s;',(account,pass_))
        result=cur.fetchone()
        if result == None:
            print(f'No account found with this number-{account},Press 2 to create account')
            print('-'*20)
            print('-'*20)
            bank_payment()
        else:
            # cur.execute(f'''
            #              INSERT INTO  payment(account_no,Bal,password) VALUES ('{account_no}',000,'{pass_}');
            #              ''')
            # conn.commit()
            print('*'*50)
            print('Account Info:\n1-Transfer\n2-Check Balance\n3-change Password\n4-Top Up')
            print('*'*50)
            user_input=input('Select an option:')
            if user_input == '1':
                print('TRANSFER:\nEnter destination account number')
                account_no=input("Client account number:")
                cur.execute('SELECT account_no,name FROM payment WHERE account_no= %s ;',(account_no,))
                client_account=cur.fetchone()
                if client_account == None:
                    print(f'No user with this account number-{account_no} is found')
                else:
                    print(client_account)
                    print('How much do you want to send')
                    amount=input('Amount:')
                    if int(amount) <= 0:
                        print("Invalid transaction")
                    elif int(amount) > 0:
                        if int(amount) <= int(result[1]):
                            if result[0] == client_account[0]:
                                print("You can't send to your own account")
                            user_update_bal=int(result[1])-int(amount)
                            user_client_bal=int(result[1]) + int(amount)
                            cur.execute('UPDATE payment SET bal=%s where account_no=%s ;',(str(user_client_bal),client_account[0]))
                            conn.commit()


                            cur.execute('UPDATE payment SET bal=%s where account_no=%s ;',(str(user_update_bal),result[0],))
                            conn.commit()
                            
                            
                            print('*'*50)
                            print('Transaction Successful......')
                            cur.execute('SELECT bal FROM payment WHERE account_no= %s ;',(result[0],))
                            new_bal=cur.fetchone()
                            print(f'You just sent {amount} to {client_account[1]}-{client_account[0]}\nYour account balance is {new_bal[0]}')
                        else:
                            print('Insufficient funds....Credit your account')
            elif user_input == '2':
                print(f'Your current balance is {result[1]}')
            elif user_input == '3':
                previous_password=input('Enter your current password:')
                new_password=input('Enter new password:')
                if previous_password == new_password:
                    cur.execute('UPDATE payment SET password = %s WHERE account_no=%s',(new_password,result[0]))
                    conn.commit()
                    print('Your Password has been updated...')
                else:
                    print('Both passwords does not match')
            elif user_input == '4':
                top_up_amount=input('Top up amount amount:')
                if int(top_up_amount) > 1000:
                    print('Maximum amount is 1000')
                else:
                    new_amount=int(result[1]) + int(top_up_amount)
                    cur.execute('UPDATE payment SET bal=%s WHERE account_no=%s;',(str(new_amount),result[0]))
                    conn.commit()
                    print(f'Your new balance is {new_amount}')
    elif user_input == '2':
        user_name=input('Enter you name:')
        user_password=input('Enter a password:')
        confirm_password=input('Confirm Password:')
        if user_password == confirm_password:
            cur.execute('SELECT * FROM payment WHERE name=%s;',(user_name,))
            result=cur.fetchone()
            if result == None:
                cur.execute('INSERT INTO payment VALUES(%s,%s,%s,%s);',(str(generate_account_number()),'1000',user_password,user_name))
                conn.commit()
                cur.execute('SELECT account_no FROM payment WHERE password=%s;',(confirm_password,))
                get_user_account=cur.fetchall()[0]
                print(f'Your account number is {get_user_account},Press 2 to login and transact')
                print('*'*50)
                print('*'*50)
                print('*'*50)
                bank_payment()
                
    else:
        print('Thanks for your time')



bank_payment()
# generate_account_number()


