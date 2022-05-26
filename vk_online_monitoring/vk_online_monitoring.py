import csv
from datetime import datetime
from time import sleep

import vk_api

my_file = "unique_online_log.csv"

group_id = "cmctvc"
group_file = f"unique_online_group_log.csv"


class VKconnector():
    def __init__(self, login, password):
        def auth_handler():
            key = input("Enter authentication code: ")
            remember_device = True
            return key, remember_device

        self.vk_session = vk_api.VkApi(login, password, auth_handler=auth_handler)
        while 1:
            try:
                self.vk_session.auth(token_only=True)
                break
            except vk_api.AuthError as error_msg:
                print(error_msg)

        self.friends_fieldnames = ('datetime', *self.get_friends_ids())
        self.group_fieldnames = 'datetime', *[i['id'] for i in self.get_group_users()['items']]

    def get_friends_ids(self):
        api = self.vk_session.get_api()
        return api.friends.get()['items']

    def get_friends_ids_online(self):
        api = self.vk_session.get_api()
        return api.friends.getOnline()

    def get_group_users(self):
        while 1:
            try:
                tools = vk_api.VkTools(self.vk_session)
                group = tools.get_all_slow(
                    'groups.getMembers',
                    1000,   # можно попробовать и больше, этот метод должен позволять,
                            # но у меня были проблемы, да и мне не надо
                    {'group_id': group_id,
                     'fields': 'online'}
                )
                break
            except:
                pass
        sleep(1)
        return group

    def get_friends_online(self):
        return {i: True for i in self.get_friends_ids_online()}

    def get_group_online(self):
        return {i['id']: True for i in self.get_group_users()['items'] if i['online']}


def write_headers(file, names):
    with open(file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=names)
        writer.writeheader()


def write_row(file, fields, data):
    with open(file, 'a+', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, extrasaction='ignore', fieldnames=fields)
        writer.writerow(data)


if __name__ == "__main__":
    login, password = open('../../vk_login_pass.txt', 'r').read().split()
    vk_conn = VKconnector(login, password)

    write_headers(my_file, vk_conn.friends_fieldnames)
    write_headers(group_file, vk_conn.group_fieldnames)

    activities = (
        (my_file, vk_conn.friends_fieldnames, vk_conn.get_friends_online),
        (group_file, vk_conn.group_fieldnames, vk_conn.get_group_online)
    )

    while 1:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(now, end="\t")
        for i in activities:
            try:
                online=i[2]()
                write_row(i[0], i[1], {'datetime': now, **online})
                print(len(online), end="\t")
            except Exception as e:
                print(e)
        print()
        sleep(60)
