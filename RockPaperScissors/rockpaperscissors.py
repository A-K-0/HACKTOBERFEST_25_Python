print('***Welcome to www.rockpaperscissors.com***')
L=[{'sahitya':'I@m12345'}]
m=['!','@','#','$','%','^','&','*','_','-','+','=',':',';','.','/','<','>',',','?']
a=int(input('''Enter 1 to Login or 2 to Sign Up..'''))

def login():
    while True:
        u=input('Enter user id:')
        print('''While entering a password, remember 3 conditions:
1. It must contain a lower case and an upper case letter.
2. It must contain a special symbol. [ ! @ # $ % ^ & * _ - + = : ; , . / < > ? ]
3. It must contain a minimum of 8 characters and not more than 15 characters.''')
        p=input('Enter password:')
        d={u:p}
        if d in L:
            print('Login Successful..')
            break
        else:
            print('Invalid user Id or password.. Please try again.')

def signup():
    while True:
        u=input('Enter user id:')
        # check if user exists without recursion
        exists=False
        for i in L:
            if u in i:
                exists=True
                break
        if exists:
            print('User Id already exists. Please try with a new user Id.')
            continue

        print('''While entering a password, remember 3 conditions:
1. It must contain a lower case and an upper case letter.
2. It must contain a special symbol. [ ! @ # $ % ^ & * _ - + = : ; , . / < > ? ]
3. It must contain a minimum of 8 characters and not more than 15 characters.''')
        p=input('Enter password:')
        c=d=e=0
        for i in p:
            if i.islower():
                c+=1
            elif i.isupper():
                d+=1
            elif i in m:
                e+=1
        # stricter check
        if c>=1 and d>=1 and e>=1 and 8<=len(p)<=15:
            print('Password Criteria Matched.')
            q=input('Confirm Password:')
            if p==q:
                dct={u:p}
                L.append(dct)
                print('Sign Up successful.. Now proceed to Login Page..')
                break
            else:
                print('Passwords not matched. Please try again.')
        else:
            print('Password Criteria not matched. Please try again.')

if a<1 or a>2:
    print('Invalid Input..')
else:
    if a==1:
        login()
    elif a==2:
        signup()
        login()

import random as r
print("Let's play Rock Paper Scissors.")
while True:
    d={1:'Rock',2:'Paper',3:'Scissors'}
    l=[1,2,3]
    x=r.choice(l)
    y=int(input('''Enter your choice as numbers: Rock=1, Paper=2, Scissors=3
Your choice:'''))
    if y in l:
        print(f'Computer chose {d[x]}. You chose {d[y]}.')
        if x==y:
            print('Game draw.')
        elif (y==1 and x==3) or (y==2 and x==1) or (y==3 and x==2):
            print('You win.')
        else:
            print('Computer wins.')
    else:
        print('Invalid Input. Enter correct choice.')
    p=input('Wanna play again? (y/Y/n/N)')
    if p in 'Nn':
        print('Have a nice day.. See you soon..')
        break
    elif p not in 'YyNn':
        print('Wrong choice entered.. Game is exiting..')
        break
