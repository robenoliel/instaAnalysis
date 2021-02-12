# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 18:44:39 2020

@author: roben
"""

from bs4 import BeautifulSoup                         #Tratamento do texto HTML
import selenium.webdriver as webdriver                #Acesso a página web
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep                                #Criação de intervalos
import pandas as pd                                   #Métodos e classes de análise de dados
import pickle

class instaReader:
    
    def __init__(self, driver, login, password):
        self.driver = driver
        self.username = login
        self.df_posts = pd.DataFrame(columns = ['user','code','date','likes','popularity','text'])
        self.df_users = pd.DataFrame(columns = ['user','followers'])
        
        url = 'https://www.instagram.com/accounts/login/'       #URL do insta do PELS/IAS

        try:
            self.driver.get(url)
        except:
            raise Exception('An Error has occured while opening the instagram page, \
                            please verify your webdriver.')
            
        sleep(3)
        
        try:
            logField = driver.find_element_by_name("username")
            passField = driver.find_element_by_name("password")
        
            logField.send_keys(login)
            passField.send_keys(password)
        
            sleep(0.5)
        
            driver.find_elements_by_tag_name("button")[1].click()
            sleep(3)
            try:
                driver.find_element_by_xpath("//button[contains(@class, 'sqdOP') and contains(@class, 'L3NKy') and contains(@class, 'y3zKF')]").click()
                sleep(3)
            except:
                pass
            try:
                driver.find_element_by_xpath("//button[contains(@class, 'aOOlW') and contains(@class, 'HoLwm')]").click()
                sleep(3)
            except:
                pass
            
            print('Log in successfull.')
            
        except:
            raise Exception('An Error has occured while logging in instagram, \
                            please verify your username and password.')
                
    def scrapPosts(self, number_of_posts = 0, user = '', keep_data = True):
        
        sleep(3)
        
        if user == '': user = self.username
        
        searchField = self.driver.find_element_by_xpath("//input[contains(@class, 'XTCLo') and contains(@class, 'x3qfX')]")
        searchField.send_keys(user)    
        
        sleep(2)
        
        self.driver.find_element_by_xpath("//div[contains(@class, 'z556c')]").click()
        
        sleep(3)
        
        try:
            result = self.driver.find_element_by_xpath("h2//[contains(@class, '_7UhW9') and contains(@class, 'fKFbl') \
                                              and contains(@class, 'yUEEX') and contains(@class, 'KV-D4') \
                                              and contains(@class, 'fDxYl')]").text
            assert(result == user)
        except:
            Exception("We couldn't find the user you're looking for!")

        sleep(2)
        
        followers = int(self.driver.find_element_by_xpath("//span[contains(@class, 'g47SY')]").text)
        
        df_posts = pd.DataFrame(columns = ['code','date','likes','text','popularity'])
        lastOne = None
        step = 1000
        start = 0
        count = 0
        while True:
            sleep(2)
            self.driver.execute_script("window.scrollTo("+str(start)+", "+str(start+step)+");")
            sleep(1)
            new_posts = self.driver.find_elements_by_class_name("v1Nh3")
            for element in new_posts:
                code = element.find_element_by_tag_name('a').get_attribute('href')[28:-1]
                df_posts = df_posts.append({'code':code}, ignore_index=True)
            start+=step
            if new_posts[-1] == lastOne:
                count+=1
                if count == 3:
                    break
            else:
                count = 0
                lastOne = new_posts[-1]
                
        df_posts = pd.DataFrame.drop_duplicates(df_posts).reset_index(drop = True)

        url = 'https://www.instagram.com/p/'
        if number_of_posts == 0: number_of_posts = len(df_posts)
        df_posts = df_posts.iloc[0:number_of_posts,:]
        for i, row in df_posts.iterrows():
            self.driver.get(url+row['code'])
            sleep(2)
            try:
                content = self.driver.find_element_by_xpath("//div[contains(@class, 'C4VMK')]").find_elements_by_tag_name('span')[-1].get_attribute('innerHTML')
                row['text'] = BeautifulSoup(content, "lxml").text
            except:
                pass
            try:
                like_content = self.driver.find_element_by_xpath("//div[contains(@class, 'Nm9Fw')]")
                liked_by_x = len(like_content.find_elements_by_tag_name('span'))-1
                and_other_x_people = int(like_content.find_elements_by_tag_name('span')[-1].text)
                row['likes'] = liked_by_x + and_other_x_people
                row['popularity'] = (liked_by_x + and_other_x_people)/followers
            except:
                pass
            
            row['date'] = self.driver.find_element_by_tag_name('time').get_attribute('datetime')
        
        if keep_data:
            self.df_posts = self.df_posts.append(df_posts.insert(0, 'user', user), ignore_index = True)
            self.df_users = self.df_users.append({'user':user, 'followers':followers})
        return df_posts
    
    def get_users(users = []):
        if users == []:
            return self.df_users
        return self.df_users[self.df_users.isin(users)]
    
    def get_posts(users = []):
        if users == []:
            return self.df_posts
        return self.df_posts[self.df_posts.isin(users)]
        
            

