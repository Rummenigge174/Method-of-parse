# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from lesson_7.instaparser.items import InstaparserItem
import re
import json
from urllib.parse import urlencode
from copy import deepcopy


class InstagramSpider(scrapy.Spider):
    #атрибуты класса
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    insta_login = 'Jora_Morata1554'
    insta_pwd = '#PWD_INSTAGRAM_BROWSER:9:1595940187:AVdQADbY6hhWstiKaZfRfGp4oJ1ZdmXQCS6L56BQ7mszUg8DE/7Kk2i2Hc67FRU5gCrgnxg2LE6XALE/pss9ERKgxU0n+x9UXKIFu0OCLOOuRMY7ZBsv8sJH7DrVswFhI/ss2MBoxD8K552D+XuCZ4/qNQ=='
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    parse_users = ['i_am_vi_ola','krapiva_k']      #Пользователь, у которого собираем посты. Можно указать список
    # ai_machine_learning kravtsov1723 fialki_mini  krapiva_k 'krapiva_k',
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    follower_hash = 'c76146de99bb02f6415203be841dd25a'  #hash для получения данных по постах с главной страницы
    subscribe_hash = 'd04b0a864b4b54837c0d870b0e77e076'

    def parse(self, response: HtmlResponse):             #Первый запрос на стартовую страницу
        csrf_token = self.fetch_csrf_token(response.text)   #csrf token забираем из html
        yield scrapy.FormRequest(                   #заполняем форму для авторизации
            self.inst_login_link,
            method='POST',
            callback=self.user_parse,
            formdata={'username': self.insta_login, 'enc_password': self.insta_pwd},
            headers={'X-CSRFToken': csrf_token}
        )

    def user_parse(self, response: HtmlResponse):
        j_body = json.loads(response.text)
        if j_body['authenticated']:
            for parse_user in self.parse_users:         #Проверяем ответ после авторизации
                yield response.follow(                  #Переходим на желаемую страницу пользователя. Сделать цикл для кол-ва пользователей больше 2-ух
                    f'/{parse_user}',
                    callback=self.user_data_parse,
                    cb_kwargs={'username': parse_user}
                )

    def user_data_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)       #Получаем id пользователя
        variables = {'id': user_id,                                    #Формируем словарь для передачи даных в запрос
                     'first': 50}                                      #12 постов. Можно больше (макс. 50)
        url_followers = f'{self.graphql_url}query_hash={self.follower_hash}&{urlencode(variables)}'    #Формируем ссылку для получения данных о постах
        yield response.follow(
            url_followers,
            callback=self.user_followers_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'variables': deepcopy(variables)}         #variables ч/з deepcopy во избежание гонок
        )
        url_subscribes = f'{self.graphql_url}query_hash={self.subscribe_hash}&{urlencode(variables)}'  # Формируем ссылку для получения данных о постах
        yield response.follow(
            url_subscribes,
            callback=self.user_subscribes_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'variables': deepcopy(variables)}  # variables ч/з deepcopy во избежание гонок
        )


    def user_subscribes_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = json.loads(response.text)
        page_info = j_data.get('data').get('user').get('edge_follow').get('page_info')
        if page_info.get('has_next_page'):  # Если есть следующая страница
            variables['after'] = page_info['end_cursor']  # Новый параметр для перехода на след. страницу
            url_posts = f'{self.graphql_url}query_hash={self.subscribe_hash}&{urlencode(variables)}'
            yield response.follow(
                url_posts,
                callback=self.user_subscribes_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)}
            )
        subscribes = j_data.get('data').get('user').get('edge_follow').get('edges')  # Сами посты
        for subscribe in subscribes:  # Перебираем посты, собираем данные
            item = InstaparserItem(
                _id=subscribe['node']['id'],  # id подписчика
                username=username,
                user_id=user_id,
                username_follower=subscribe['node']['username'],
                full_name=subscribe['node']['full_name'],
                is_private=subscribe['node']['is_private'],
                photo=subscribe['node']['profile_pic_url'],
                follow_data=subscribe['node'],
                follower=False,
                subscribe=True)
            yield item

    def user_followers_parse(self, response: HtmlResponse, username, user_id, variables):   #Принимаем ответ. Не забываем про параметры от cb_kwargs
        j_data = json.loads(response.text)
        page_info = j_data.get('data').get('user').get('edge_followed_by').get('page_info')
        if page_info.get('has_next_page'):                                          #Если есть следующая страница
            variables['after'] = page_info['end_cursor']                            #Новый параметр для перехода на след. страницу
            url_posts = f'{self.graphql_url}query_hash={self.follower_hash}&{urlencode(variables)}'
            yield response.follow(
                url_posts,
                callback=self.user_followers_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)}
            )
        followers = j_data.get('data').get('user').get('edge_followed_by').get('edges')     #Сами посты
        for follow in followers:                                                                      #Перебираем посты, собираем данные
            item = InstaparserItem(
                _id=follow['node']['id'], #id подписчика
                username=username,
                user_id=user_id,
                username_follower=follow['node']['username'],
                full_name=follow['node']['full_name'],
                is_private=follow['node']['is_private'],
                photo=follow['node']['profile_pic_url'],
                follow_data=follow['node'],
                follower=True,
                subscribe=False)
            yield item                  #В пайплайн

    #Получаем токен для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    #Получаем id желаемого пользователя
    def fetch_user_id(self, text, username):
        matched = re.search('{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text).group()
        return json.loads(matched).get('id')

