# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 23:17:31 2018

@author: Parashar
"""

from whatsapp_utils import AutoWhatsApp
import pandas as pd
import glob


MESSAGE_TXT = """THis is a multi-line msg
line 1
line 2
line 3"""


def start_bot():

    whatsbot = AutoWhatsApp("user-data-dir=C:\\Users\\lol_user_name\\AppData\\Local\\Google\\Chrome\\User Data\\")
    
    xlsx_list   = glob.glob("excels\\*.xlsx")
    for xlsx in xlsx_list:
        xl_df = pd.read_excel(xlsx)
        phoneNumbers =  list(xl_df[xl_df.columns[len(xl_df.columns)]])
    
        for number in phoneNumbers:
            whatsbot.hit_api(str(number))
            #####################
            whatsbot.write_text_message("{}".format(MESSAGE_TXT))
            whatsbot.attach_images()
            #####################

start_bot()

