from selenium import webdriver
import selenium
from time import sleep
from random import random, randrange, choice
import os


def sleep_rand(num):
    sleep((random() * 10) % num)


def sleep_rand_range(low, high):
    sleep(randrange(low, high))


class InstaBot:
    def __init__(self, username, pw):
        LOGIN = not os.path.isdir(f'./{username}')
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-insecure-localhost')
        options.add_argument(f"user-data-dir=./{username}")
        self.driver = webdriver.Chrome(
            "C:/webdrivers/chromedriver.exe", options=options)

        self.url = "https://instaram.com/"
        self.username = username
        self.pw = pw
        self.driver.get(self.url)
        if(LOGIN):
            sleep(2)
            self.login()

    def login(self):
        self.driver.find_element_by_xpath(
            "//input[@name=\"username\"]").send_keys(self.username)
        self.driver.find_element_by_xpath(
            "//input[@name=\"password\"]").send_keys(self.pw)
        self.driver.find_element_by_xpath('//button[@type="submit"]').click()
        sleep(4)
        self.driver.find_element_by_xpath(
            "//button[contains(text(),'Not Now')]").click()

    def scroll_box(self):
        sleep(3)
        scrollBox = self.driver.find_element_by_xpath(
            "//div[@role='dialog']/div[2]")

        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep_rand_range(3, 5)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight);
                return arguments[0].scrollHeight;
                """, scrollBox)
        return scrollBox

    def page_follow(self, account, action):
        """self, account, action (2 = followers, 3 = following)"""
        self.driver.get(self.url + account)
        sleep(2)
        self.driver.find_element_by_xpath(
            f"/html/body/div[1]/section/main/div/header/section/ul/li[{str(action)}]/a").click()
        scrollBox = self.scroll_box()
        links = scrollBox.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        # close button
        self.driver.find_element_by_xpath(
            "//div[@role='dialog']/div[1]//button[1]").click()
        return names

    def follow(self, account):
        FOLLOWING, ERROR = 0, 404
        self.driver.get(self.url + account)
        try:
            mainDiv = self.driver.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/header/section/div[1]")
            followBt = mainDiv.find_elements_by_xpath(
                "//button[contains(text(),'Follow')]")
            if len(followBt) > 0:
                followBt[0].click()
        except Exception as e:
            print(e)
            return ERROR
        return FOLLOWING

    def like(self, account):
        self.driver.get(self.url + account)
        try:
            result = self.driver.find_elements_by_xpath("//a")
            posts = []
            for i in result:
                if("/p/" in i.get_attribute("href")):
                    posts.append(i)
            if(len(posts) > 0):
                sleep_rand(1)
                if(len(posts) > 2):
                    posts[choice(range(0, 3))].click()  # image
                else:
                    posts[0].click()  # image
                sleep_rand(5)
                self.driver.find_element_by_xpath(
                    "/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[1]/button").click()  # likeBtn
                sleep_rand(3)
                self.driver.find_element_by_xpath(
                    "/html/body/div[4]/div[3]/button").click()  # closeBtn
        except Exception as e:
            print("account: " + account)
            print(e)
            return 0
        return 1

    def banner_on(self):
        sleep(3)
        on = False
        try:
            opt = ["OK", "Report a Problem"]
            btn = self.driver.find_element_by_xpath(
                f"//button[contains(text(),'{opt[choice([0, 1])]}')]")
            sleep_rand(1)
            btn.click()
            on = True
        except Exception as e:

            pass
        if(on):
            print(f"banner on")
        return on

    def un_follow(self, account):
        self.driver.get(self.url + account)
        try:
            sleep_rand(2)
            self.driver.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/header/section/div[1]/div[2]/span/span[1]/button").click()
            bt = self.driver.find_elements_by_xpath(
                "//button[contains(text(),'Unfollow')]")
            if len(bt) > 0:
                sleep_rand(2)
                bt[0].click()
            return 1
        except Exception as e:
            print(e)
            return 404

    def scroll(self):
        if(choice([1, 2]) == 1):
            self.driver.get(self.url + "explore/")
        else:
            self.driver.get(self.url)
        # number of scolls to do
        numOf = randrange(15, 20)
        sleep_rand(2)
        for i in range(numOf):
            scrollAmount = randrange(600, 800)
            self.driver.execute_script(f"window.scrollBy(0,{scrollAmount})")
            sleep_rand_range(3, 5)
