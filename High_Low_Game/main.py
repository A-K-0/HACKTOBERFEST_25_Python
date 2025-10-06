from art import logo, vs
from game_data import data
import random
from replit import clear

# select two dictionaries data
def choose():
    a = random.choice(data)
    return a

# compare followers
def followers(a, b, wrongs, points):
    select=input("Who has more followers? Type 'A' or 'B': ")
    oney = a['follower_count']
    twoy = b['follower_count']
    clear()
    if select == 'A':
        if oney >= twoy:
            points+=1
            print(f"You're right! Current Score: {points}") 
        else:
            wrongs+=1
            print(f"Sorry, that's wrong. Final Score: {points}")
    else:
        if oney <= twoy:
            points+=1
            print(f"You're right! Current Score: {points}") 
        else:
            wrongs+=1
            print(f"Sorry, that's wrong. Final Score: {points}")

    return wrongs, points
# game
def game():
    clear()
    print(logo)
    # print(a)
    # print(b)
    wrongs = 0
    points = 0
    while wrongs == 0:
        a = choose()
        b = choose()
        print(f"Compare A: {a['name']}, a {a['description']}, from {a['country']}.")
        print(vs)
        print(f"Against B: {b['name']}, a {b['description']}, from {b['country']}.")
        wrongs, points = followers(a, b, wrongs, points)
        if wrongs > 0:
            return
        
game()



