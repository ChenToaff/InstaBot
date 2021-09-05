from Bot.insta_bot import InstaBot
from Bot.dataBase import Db
from time import sleep, time
from datetime import datetime, date
from random import randrange, choice
from settings import Password, Username, Source, Hours

FOLLOW, LIKE, SCROLL, UNFOLLOW = 0, 1, 2, 3
querys ={
    FOLLOW : """
            SELECT user_name
            FROM users
            WHERE (date_of_follow = "") AND (requsted = 0) AND (ignore = 0)  LIMIT 1;
            """,
    LIKE :"""
            SELECT user_name
            FROM users
            WHERE (date_of_follow != "") AND (liked = 0) LIMIT 1;
            """,
    UNFOLLOW : """
            SELECT user_name FROM users
            WHERE ((julianday('now') - julianday(date_of_follow)) >= 3) AND (ignore < 2) AND (following_me = 0) ORDER BY ignore ASC LIMIT 1;
            """
    }

def create_table(db):
    db.query("""
    CREATE TABLE IF NOT EXISTS users (
    user_name TEXT NOT NULL PRIMARY KEY,
    following_me BIT,
    date_of_follow TEXT,
    requsted BIT,
    liked BIT,
    ignore BIT
    );""")

def users_table(db, page_followers):
    create_table(db)
    query = "INSERT OR IGNORE INTO users (user_name,following_me,date_of_follow,requsted, liked,ignore) VALUES"
    for user in page_followers:
        query += ' ("'+user+'",0,"",0,0,0),'
    db.query(query[:-1])


def update_following(myBot, db):
    users = myBot.page_data(myBot.username, 3)
    for user in users:
        db.query("""INSERT OR IGNORE INTO users (user_name,following_me,date_of_follow,requsted, liked,ignore)
                     VALUES("{user}",0,Date("now"),0,0,0)""")
        db.query(
            f"""UPDATE users SET date_of_follow = Date("now") WHERE (user_name = '{user}') AND (date_of_follow ='');""")
    return users


def update_followers(myBot, db):
    users = myBot.page_data(myBot.username, 2)
    num = int(myBot.driver.find_element_by_xpath(
        f"//ul[not(ancestor::nav)]/li[2]/a/span").text)
    if len(users) < num * 0.93:
       print("error: followers number mismatch")
       return users

    db.query(f"""UPDATE users SET following_me = 0;""")
    for user in users:
        db.query(
            f"""UPDATE users SET following_me = 1 WHERE (user_name = '{user}');""")
    return users

def follow_func(myBot,user):
    answer = myBot.follow(user)
    return f"""UPDATE users SET {"requsted" if answer else "ignore"} = 1 WHERE (user_name = '{user}');"""

def like_func(myBot,user):
    myBot.like(user)
    return f"""UPDATE users SET liked = 1 WHERE (user_name = '{user}');"""


def unfollow_func(myBot,user):
    myBot.un_follow(user)
    return f"""UPDATE users SET ignore = ignore + 1,date_of_follow = '' WHERE (user_name = '{user}');"""

def main_loop(myBot, db):   
    limitsPerHour = {LIKE: 0,FOLLOW: 0,UNFOLLOW: 0}
    functions = {
        FOLLOW : follow_func,
        LIKE: like_func,
        UNFOLLOW: unfollow_func
    }
    # botTime:
    allowedTime = 60 * Hours
    startTime = time()
    # actions time:
    timeCounter = 0
    timeLimit = 0

    while (((time() - startTime)/60) < allowedTime):
        if((time() - timeCounter)/60 >= timeLimit):
            if timeLimit != 0:
                print("sleepig: " + datetime.now().strftime("%H:%M"))
                sleep(randrange(40, 60)*60)
                print("finished sleeping: " + datetime.now().strftime("%H:%M"))
            
            actions = [FOLLOW, LIKE, SCROLL, UNFOLLOW]
            timeLimit = randrange(50, 65)
            limitsPerHour[LIKE] = randrange(20, 30)
            limitsPerHour[FOLLOW] = randrange(15, 20)
            limitsPerHour[UNFOLLOW] = randrange(15, 20)
            update_following(myBot, db)
            update_followers(myBot, db)
            timeCounter = time()

        currentAction = choice(actions)
        if currentAction == SCROLL:
            myBot.scroll()
            continue
        
        limitsPerHour[currentAction] -= 1
        user = db.read_query(querys[currentAction])
        if(len(user) > 0):
            user = user[0][0]
            q = functions[currentAction](myBot,user)
            if(myBot.banner_on()):
                 actions.remove(currentAction)
            else:
                db.query(q)
        else:
            actions.remove(currentAction)

        if(limitsPerHour[currentAction] <= 0):
            actions.remove(currentAction)

    db.close()

if __name__ == "__main__":
    myBot = InstaBot(Username, Password)
    db = Db(f"./data/{Username}/users.db")
    check = db.read_query("""
            SELECT user_name FROM users
            WHERE (ignore = 0) AND (following_me = 0) AND (requsted = 0) AND (date_of_follow = '');""")
    if(check == None or len(check) < 300):
        page_followers = myBot.page_data(Source, 2)
        users_table(db, page_followers)

    main_loop(myBot, db)
