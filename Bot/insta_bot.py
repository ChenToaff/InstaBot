from selenium import webdriver
import selenium
from time import sleep
from random import random, randrange, choice
import os
import pathlib


def sleep_rand(num):
    sleep((random() * 10) % num)


def sleep_rand_range(low, high):
    sleep(randrange(low, high))


class InstaBot:
    def __init__(self, username, pw):
        LOGIN = not os.path.isdir(f'./data/{username}')
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-insecure-localhost')
        scriptDirectory = pathlib.Path().absolute()
        options.add_argument(f"user-data-dir={scriptDirectory}/data/{username}")
        #options.add_argument(f"user-data-dir=./data/{username}")
        self.driver = webdriver.Chrome(
            "C:/webdrivers/chromedriver.exe", options=options)

        self.url = "https://instaram.com/"
        self.username = username
        self.pw = pw
        self.driver.get(self.url)
        if(LOGIN):
            sleep(2)
            self.login()
        self.dismiss_notNow()

    def login(self):
        self.driver.find_element_by_xpath(
            "//input[@name=\"username\"]").send_keys(self.username)
        self.driver.find_element_by_xpath(
            "//input[@name=\"password\"]").send_keys(self.pw)
        self.driver.find_element_by_xpath('//button[@type="submit"]').click()

    def scroll_box(self):
        sleep(3)
        scrollBox = self.driver.find_element_by_xpath(
            "//div[@role='dialog']//ul/..")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep_rand_range(3, 5)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight);
                return arguments[0].scrollHeight;
                """, scrollBox)
        return scrollBox

    def dismiss_notNow(self):
        self.click_xpath("//button[contains(text(),'Not Now')]")

    def page_data(self, account, action):
        """self, account, action (2 = followers, 3 = following)"""
        self.driver.get(self.url + account)
        sleep(2)
        self.driver.find_element_by_xpath(
            f"//ul[not(ancestor::nav)]/li[{str(action)}]/a").click()
        scrollBox = self.scroll_box()
        links = scrollBox.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        # close button
        self.driver.find_element_by_xpath(
            "//div[@role='dialog']/div[1]//button[1]").click()
        return names

    def click_xpath(self, path):
        sleep_rand_range(3, 5)
        btn = self.driver.find_elements_by_xpath(path)
        try:
            if len(btn) > 0:
                btn[0].click()
        except:
            btn = None
        return btn

    def follow(self, account):
        self.driver.get(self.url + account)
        return self.click_xpath("//button[contains(text(),'Follow')]")

    def like(self, account):
        self.driver.get(self.url + account)
        posts = self.driver.find_elements_by_xpath(
            "//a[starts-with(@href, '/p/')]")
        if(len(posts) > 0):
            sleep_rand_range(3, 5)
            if(len(posts) > 2):
                posts[choice(range(0, 3))].click()  # image
            else:
                posts[0].click()  # image

            lBtn = self.click_xpath(
                "//*[name()='svg'][@aria-label='Like']/..")  # likeBtn
            cBtn = self.click_xpath(
                "//*[name()='svg'][@aria-label='Close']/..")  # closeBtn
            if not (lBtn and cBtn):
                print("failed liking: " + account)

    def banner_on(self):
        opt = ["OK", "Report a Problem"]
        isOn = self.click_xpath(
            f"//button[contains(text(),'{opt[choice([0, 1])]}')]")
        if isOn:
            print(f"banner on")
        return isOn

    def un_follow(self, account):
        self.driver.get(self.url + account)
        if self.click_xpath("//span[@aria-label='Following']/../.."):
            if self.click_xpath("//button[contains(text(),'Unfollow')]"):
                return
        print("failed unfollowing: " + account)

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
