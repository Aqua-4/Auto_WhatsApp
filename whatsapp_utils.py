from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import glob


class AutoWhatsApp:

    OVERFLOW_CNT = 3
    OVERFLOW_LIMIT = 10

    def __init__(self, user_profile_path=""):

        self.options = webdriver.ChromeOptions()
        self.options.add_argument(user_profile_path)
        self.driver = webdriver.Chrome(
            executable_path="chromedriver", chrome_options=self.options)

    # def reset_counter(self):
    #     self.OVERFLOW_CNT = 0

    def chk_counter(self, bool_reset=False):
        if bool_reset:
            self.OVERFLOW_CNT = 0
        self.OVERFLOW_CNT += 1
        print(self.OVERFLOW_CNT)
        time.sleep(self.OVERFLOW_CNT)

        if self.OVERFLOW_CNT >= self.OVERFLOW_LIMIT:
            return False
        else:
            return True

    def format_number(self, phone_number):
        phone_number = phone_number.replace(" ", "").replace("+", "").strip()
        if len(phone_number) == 10:
            phone_number = "91{}".format(phone_number)
        print(phone_number)
        return phone_number

    def hit_api(self, phone_number):
        phone_number = self.format_number(phone_number)
        self.driver.get(
            "https://api.WhatsApp.com/send?phone={}".format(phone_number))

        self.accept_alert()
        self.click_to_message()

    def accept_alert(self):
        try:
            self.driver.switch_to_alert().accept()
        except:
            pass

    def click_to_message(self):
        print("clcik msg")
        try:
            self.driver.find_element_by_xpath(
                "//a[contains(text(),'Message')]").send_keys(Keys.ENTER)
            self.chk_counter(True)
            time.sleep(5)
        except:
            if self.chk_counter():
                self.click_to_message()

    def write_text_message(self, msg_text="This is an automated text message"):
        try:
            while self.check_loader():
                time.sleep(self.OVERFLOW_CNT)
            msg_box = self.driver.find_element_by_xpath(
                "//div[text()='Type a message']")
            msg_box = msg_box.find_element_by_xpath("..")
            time.sleep(5)
            for _line in msg_text.split("\n"):
                msg_box.send_keys(Keys.ENTER,Keys.LEFT_SHIFT)
            self.send_message(msg_box)
        except:
            print("Failed sending message")

    def send_message(self):
        try:
            self.driver.find_element_by_xpath("//span[@data-icon='send']").click()
        except:
            self.driver.find_element_by_xpath("//span[@data-icon='send-light']").click()
        time.sleep(5)

    def attach_images(self, image_folder_path="images"):
        while self.check_loader():
            time.sleep(self.OVERFLOW_CNT)
        try:
            self.driver.find_element_by_xpath(
                "//span[@data-icon='clip']").click()
            # self.driver.find_element_by_xpath("//span[@data-icon='image']").find_element_by_xpath("..").click()
            for image in glob.glob("{}\\*".format(image_folder_path)):
                self.upload_image(image)
            # insert text
            time.sleep(2)
            import pdb
            pdb.set_trace()
            self.send_message()
        except:
            if self.chk_counter():
                self.attach_images(image_folder_path)

    def check_loader(self):
        """<progress value="96" max="100" dir="ltr"></progress>"""
        try:
            self.driver.find_element_by_tag_name("progress")
            print("Loading")
            time.sleep(2)
            return True
        except:
            time.sleep(2)
            return False
            # self.check_loader()

    def upload_image(self, image_name):
        image_object = self.driver.find_element_by_xpath(
            "//input[@type='file']")
        image_abs_path = "{}\\{}".format(os.getcwd(), image_name)
        image_object.send_keys(image_abs_path)
        time.sleep(2)

    def __del__(self):
        print("Shutting down chrome")
        self.driver.close()


# <progress value = "96" max = "100" dir = "ltr" > </progress >
