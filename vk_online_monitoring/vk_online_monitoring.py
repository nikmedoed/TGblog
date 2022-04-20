import vk_api
from time import sleep
from datetime import datetime


def auth_handler():
    key = input("Enter authentication code: ")
    remember_device = True
    return key, remember_device


login, password = open('../../vk_login_pass.txt', 'r').read().split() # replace with your 'login', 'pass'
vk_session = vk_api.VkApi(login, password, auth_handler=auth_handler)

try:
    vk_session.auth(token_only=True)
except vk_api.AuthError as error_msg:
    print(error_msg)

while 1:
    api = vk_session.get_api()
    friends = len(api.friends.getOnline())
    while 1:
        try:
            tools = vk_api.VkTools(vk_session)
            cmctvc = tools.get_all_slow('groups.getMembers', 500, {'group_id': "cmctvc", 'fields': 'online'})
            break
        except:
            pass
        sleep(1)
    try:
        cmctvc = len([i for i in cmctvc['items'] if i['online']])
        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\t{friends}\t{cmctvc}')
        with open('log.csv', "a+", encoding="utf8") as f:
            f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\t{friends}\t{cmctvc}\n')
    except Exception as e:
        print(e)
    sleep(60)
