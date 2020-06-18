from Bot.insta_bot import InstaBot
from Bot.dataBase import Db
from time import sleep, time
from datetime import datetime, date
from random import randrange, choice
from settings import Password, Username, Source, Hours


def users_table(db, page_followers):
    db.query("""
    CREATE TABLE IF NOT EXISTS users (
    user_name TEXT NOT NULL PRIMARY KEY,
    following_me BIT
    date_of_follow TEXT,
    requsted BIT,
    liked BIT
    ignore BIT
    );""")

    query = "INSERT OR IGNORE INTO users (user_name,following_me,date_of_follow,requsted, liked,ignore) VALUES"
    for user in page_followers:
        query += ' ("'+user+'",0,"",0,0,0),'
    db.query(query[:-1])


def update_following(myBot, db):
    users = myBot.page_data(myBot.username, 3)
    for user in users:
        db.query(
            f"""UPDATE users SET date_of_follow = Date("now") WHERE (user_name = '{user}') AND (date_of_follow ='');""")
    return users


def update_followers(myBot, db):
    users = myBot.page_data(myBot.username, 2)
    num = int(myBot.driver.find_element_by_xpath(
        f"//ul[not(ancestor::nav)]/li[2]/a/span").text)
    if len(users) < num:
        raise Exception('followers error')

    db.query(f"""UPDATE users SET following_me = 0;""")
    for user in users:
        db.query(
            f"""UPDATE users SET following_me = 1 WHERE (user_name = '{user}');""")
    return users


def main_loop(myBot, db):
    update_following(myBot, db)
    update_followers(myBot, db)
    # botTime:
    allowedTime = 60 * 6
    startTime = time()
    # actions time:
    timeCounter = time()
    timeLimit = randrange(50, 65)
    FOLLOW, LIKE, SCROLL, UNFOLLOW = 0, 1, 2, 3
    actions = [FOLLOW, LIKE, SCROLL, UNFOLLOW]
    #actions =  [LIKE, SCROLL,UNFOLLOW]

    while (((time() - startTime)/60) < allowedTime):
        if((time() - timeCounter)/60 >= timeLimit):
            print("sleepig: " + datetime.now().strftime("%H:%M"))
            sleep(randrange(40, 60)*60)
            print("finished sleeping: " + datetime.now().strftime("%H:%M"))
            timeLimit = randrange(50, 65)
            timeCounter = time()
            actions = [FOLLOW, LIKE, SCROLL, UNFOLLOW]
            #actions =  [LIKE, SCROLL,UNFOLLOW]

        currentAction = choice(actions)
        #currentAction = 3
        if(currentAction == FOLLOW):
            user = db.read_query("""
            SELECT user_name
            FROM users
            WHERE (date_of_follow = "") AND (requsted = 0) AND (ignore = 0)  LIMIT 1;
            """)
            if(len(user) > 0):
                user = user[0][0]
                answer = myBot.follow(user)
                if(myBot.banner_on()):
                    actions.remove(FOLLOW)
                elif(answer):
                    db.query(
                        f"""UPDATE users SET requsted = 1 WHERE (user_name = '{user}');""")
                else:
                    db.query(
                        f"""UPDATE users SET ignore = 1 WHERE (user_name = '{user}');""")

        elif currentAction == LIKE:
            user = db.read_query("""
            SELECT user_name
            FROM users
            WHERE (date_of_follow != "") AND (liked = 0) LIMIT 1;
            """)
            if(len(user) > 0):
                user = user[0][0]
                myBot.like(user)
                if(myBot.banner_on()):
                    actions.remove(LIKE)
                else:
                    db.query(
                        f"""UPDATE users SET liked = 1 WHERE (user_name = '{user}');""")
        elif(currentAction == UNFOLLOW):
            for i in [0, 1]:
                user = db.read_query(f"""
                SELECT user_name FROM users
                WHERE ((julianday('now') - julianday(date_of_follow)) >= 3) AND (ignore = {i}) AND (following_me = 0) LIMIT 1;
                """)
                if(len(user) > 0):
                    user = user[0][0]
                    myBot.un_follow(user)
                    if(myBot.banner_on()):
                        actions.remove(UNFOLLOW)
                    else:
                        db.query(
                            f"""UPDATE users SET ignore = {i+1},date_of_follow = '' WHERE (user_name = '{user}');""")
                    break
        elif currentAction == SCROLL:
            myBot.scroll()

    db.close()


if __name__ == "__main__":
    myBot = InstaBot(Username, Password)
    db = Db(f"./data/{Username}/users.db")
    check = db.read_query("""
            SELECT user_name FROM users
            WHERE (ignore = 0) AND (following_me = 0) AND (requsted = 0) AND (date_of_follow = '');""")
    if(len(check) < 300):
        page_followers = myBot.page_data(Source, 2)
        users_table(db, page_followers)

    main_loop(myBot, db)
