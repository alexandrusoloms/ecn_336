import os

import time
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
#from pyvirtualdisplay import Display
import signal



class Twitter(object):

    def __init__(self):
        # for set_random_sleep
        self.MINIMUM = 2
        self.SD = 1
        self.MEAN = 2.65
        # paths and loading data
        self.__data_path = os.path.join(os.path.dirname('__file__'), '..', ) + '/data/'
        self.__output_path = os.path.join(os.path.dirname('__file__'), '..', ) + '/output/'
        self.__twitter_names = pd.read_csv(self.__data_path + 'MP_df.csv')
        self.__twitter_names = self.__twitter_names['twitter_name'].values




    @staticmethod
    def construct_twitter_url(tw_name):
        """
        making the twitter url
        """
        tw_name = tw_name.replace('@', '').strip()
        return 'https://twitter.com/{}'.format(tw_name)

    def set_random_sleep(self):
        """
        A method wich generates a random number conditioned on:
            - a mean of 'MEAN'
            - standard deviation of 'SD' and
            - a minimum of 'MINIMUM'
        It then time.sleep(s) for the random number generated
        """
        sleep_time = np.random.randn(1) * self.SD + self.MEAN
        if sleep_time < self.MINIMUM:
            sleep_time = self.MINIMUM
        time.sleep(sleep_time)

    def get_data(self, url_link):
        """
        scrolling down until a html size of 2500000
        """
        url = url_link
        #display = Display(visible=0, size=(1024, 768))
        #display.start()
        driver = webdriver.Chrome('../chromedriver 2')
        driver.get(url)

        while True:
            html = driver.page_source
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.set_random_sleep()
            html2 = driver.page_source

            if len(html) == len(html2):
               driver.close()
               driver.service.process.send_signal(signal.SIGTERM)
               driver.quit()
              # display.stop()
               return html
               break

    @staticmethod
    def get_mp_name(mp):
        return mp.replace('@', '').strip().lower()

    def writer(self, data, name_of_mp):
        """
        this will save the file to the output_path

        :data is the html of the page:
        :name_of_mp i.e.: theresamay:
        """
        with open(self.__output_path + name_of_mp + '.txt', 'wb') as handle:
            handle.write(data.encode("ascii", 'ignore'))

    def main(self):
        """
        this is the method which runs it all
        """
        for mp in self.__twitter_names:
            try:
                mp_name = self.get_mp_name(mp)
                twitter_url = self.construct_twitter_url(mp)
                data = self.get_data(twitter_url)
                self.writer(data=data, name_of_mp=mp_name)
                self.set_random_sleep()
            # logging exceptions
            except Exception as e:
                with open(self.__output_path + 'exceptions.txt', 'a') as handle:
                    handle.write(str(e))
                self.set_random_sleep()


if __name__ == '__main__':
    Twitter().main()
