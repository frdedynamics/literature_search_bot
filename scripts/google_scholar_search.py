#!/usr/bin/env python3

from sys import exit
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class Search:

    def __init__(self, search_terms_exact, search_terms_at_least_one, search_year) -> None:
        self.search_terms_exact = ''
        self.search_terms_at_least_one = ''
        for term in search_terms_exact:
            self.search_terms_exact = self.search_terms_exact+'+'+term
        #self.search_terms_exact = self.search_terms_exact[1:]
        
        for term in search_terms_at_least_one:
            self.search_terms_at_least_one = self.search_terms_at_least_one+'+'+term
        #self.search_terms_at_least_one = self.search_terms_at_least_one[1:]
        
        self.search_year = str(search_year)


    def search(self, mode):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        if mode == 0: # without
            search_term = "https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&as_ylo=2017&as_yhi=2017&q=%22"+self.search_terms_exact+"%22+AND"+self.search_terms_at_least_one+"&as_eq=&as_occt=any&as_sauthors=&as_publication=&as_ylo="+self.search_year+"&as_yhi="+self.search_year+"&hl=en&as_sdt=0%2C5"
        elif mode == 1: # with IMU
            search_term = "https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&as_ylo=2017&as_yhi=2017&q=%22"+self.search_terms_exact+"%22+AND+imu+AND"+self.search_terms_at_least_one+"&as_eq=&as_occt=any&as_sauthors=&as_publication=&as_ylo="+self.search_year+"&as_yhi="+self.search_year+"&hl=en&as_sdt=0%2C5"
        else: # with camera
            search_term = "https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&as_ylo=2017&as_yhi=2017&q=%22"+self.search_terms_exact+"%22+AND+camera+AND"+self.search_terms_at_least_one+"&as_eq=&as_occt=any&as_sauthors=&as_publication=&as_ylo="+self.search_year+"&as_yhi="+self.search_year+"&hl=en&as_sdt=0%2C5"


        self.driver.get(search_term)
        text = self.driver.find_elements(By.CLASS_NAME, "gs_ab_mdw")
        # search_number_xpath = "/html/body/div/div[9]/div[3]/div/text()[1]"
        # text = self.driver.find_element("xpath", search_number_xpath)
        if text[1].text.split()[0] == "About":
            self.found_number = text[1].text.split()[1].replace(",","")
        else:
            self.found_number = text[1].text.split()[0].replace(",","")
        # #print(self.found_number)
        # #print(search_term)


    def close_search(self):
        self.driver.close()

    def robot_manual_check(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome() # this opens GUI

        search_term = "https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&as_ylo=2017&as_yhi=2017&q=%22"+self.search_terms_exact+"%22+AND"+self.search_terms_at_least_one+"&as_eq=&as_occt=any&as_sauthors=&as_publication=&as_ylo="+self.search_year+"&as_yhi="+self.search_year+"&hl=en&as_sdt=0%2C5"
        self.driver.get(search_term)
        temp = input()
        exit()

    
    @staticmethod
    def test_df(df):
        df.loc[len(df.index)] = [2017, 2210,1090, 123]
        df.loc[len(df.index)] = [2018, 2210,2090, 223]
        df.loc[len(df.index)] = [2019, 3210,3090, 323]
        df.loc[len(df.index)] = [2020, 5210,4090, 423]
        df.loc[len(df.index)] = [2021, 6210,5090, 523]
        return df

    @staticmethod
    def plot(df):
        fig, ax = plt.subplots()
        width = 0.8

        ax.bar(df['year'], df['found'], width, label='all search', color='bisque')
        ax.bar(df['year'], df['found_camera'], width, bottom=df['found'], label='filter:"camera', color='darkturquoise')
        ax.bar(df['year'], df['found_imu'], width, bottom=df['found_camera']+df['found'], label='filter:"IMU', color='salmon')

        ax.set(xticks=df['year'], xlabel='Publication year', ylabel='Number of articles')

        # ANNOTATE WITH ARROW
        # ax. annotate('Starting', xy =(2020, 5000),
        #      xytext =(2020, 5000),
        #      arrowprops = dict(facecolor ='green',
        #                        shrink = 0.05),   )

        text_offset = 0.2
        for index, row in df.iterrows():
            ax. annotate(row['found'], xy=(row['year']-text_offset, row['found']/2))
            ax. annotate(row['found_camera'], xy=(row['year']-text_offset, row['found']+row['found_camera']/2))
            ax. annotate(row['found_camera'], xy=(row['year']-text_offset, row['found']+row['found_camera']+row['found_imu']/2))

        plt.title('Number of publications on HRC or HRI over the last two decades based on Google Scholar', fontsize=20, fontweight=20)
        plt.show()



if __name__ == "__main__":
    search_terms_exact = ['human','robot']
    search_terms_at_least_one = ['interaction', 'cooperation', 'collaboration']
    search_years = np.arange(2013, 2023)

    # # ------------Uncomment here if "I am not a robot" occurs. Might need VPN ------------ # #
    # search_year = '2020'
    # my_search = Search(search_terms_exact, search_terms_at_least_one, search_year)
    # my_search.robot_manual_check()
   
    # # ------------ Uncomment here to redo the search ------------ # #
    # # max 10 years otherwise bot recognition
    # df = pd.DataFrame(columns=[["year", "found","found_camera", "found_imu"]])
    # # df = Search.test_df(df)
    # # Search.plot(df)

    # for year in search_years:
    #     search_year = str(year)
    #     for i in range(3):
    #         my_search = Search(search_terms_exact, search_terms_at_least_one, search_year)
    #         my_search.search(i)
    #         sleep(0.1)
    #         if i == 0:
    #             found_number = my_search.found_number
    #         elif i == 1:
    #             found_number_imu = my_search.found_number
    #         else:
    #             found_number_camera = my_search.found_number
    #     my_search.close_search()
    #     df.loc[len(df.index)] = [year, found_number, found_number_camera, found_number_imu]
    #     print(year, "--", found_number, "--", found_number_camera, "--", found_number_imu)
    # df.to_csv('~/Insync/giat@hvl.no/Onedrive/Workspaces/PythonWS/google-search-automation/df_2013_2023.csv', index=False)

    df = pd.read_csv ('~/Insync/giat@hvl.no/Onedrive/Workspaces/PythonWS/google-search-automation/df.csv')   
    
    Search.plot(df)
    print(df.tail(10))
