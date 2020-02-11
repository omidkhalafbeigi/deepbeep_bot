import requests
import telegram
import telegram.ext
from telegram.ext import *
import os


def get_private_chat():  # handmade (this function, get chats information in private type...
    # That two update_id per every request, compare with each other. Then if they aren't equal, new message will be
    # send. With this method, repetitive message can't send...

    while True:

        json_get_update = requests.get(
            'https://api.telegram.org/bot1024213820:AAHgNbsuySh1kMM9OzfncEpIEalx6jIKozI/getupdates').json()
        bot = telegram.Bot('981511760:AAEK3hz7ACpC2Q5l7_k_7Pa8dRlKkMN-Ejo')
        json_get_update_result = json_get_update['result']  # type: list
        update_id = json_get_update_result[len(json_get_update_result) - 1]['update_id']
        message = json_get_update_result[len(json_get_update_result) - 1]['message']
        from_chat = message['from']
        chat = message['chat']
        chat_id = chat['id']  # get chat_id
        text = message['text']
        type_chat = chat['type']

        if update_id != update_id_former:

            if (type_chat == 'private') and (text == '/start'):
                bot.send_message(chat_id, "Hello!\nI'm Deep Beep bot.")
                update_id_former = json_get_update_result[len(json_get_update_result) - 1]['update_id']
            else:
                bot.send_message(chat_id, "I can't understand.")
                update_id_former = json_get_update_result[len(json_get_update_result) - 1]['update_id']
        else:
            pass


# ------------------------------------------------------

bot = telegram.Bot('1024213820:AAHgNbsuySh1kMM9OzfncEpIEalx6jIKozI')


def check_is_admin(last_index):  # In function, id akharin shakhsi ke payam ferestade ro ba id admin haye group
    # moghayese mikone
    user = result[len(result) - 1]['message']['from']['id']  # id akharin shakhsi ke payam ferestade
    get_administrators = bot.get_chat_administrators(result[len(result) - 1]['message']['chat']['id'])
    for i in get_administrators:
        if i['user']['id'] == user:
            return True
    return False


def lock_group(last_message):
    if check_is_admin(last_message):
        bot.send_message(result[len(result) - 1]['message']['chat']['id'], "Group locked!")
        print('--------------------')
        is_lock = True
        return is_lock


    else:
        bot.send_message(result[len(result) - 1]['message']['chat']['id'], "Shut up!")
        print('I said shut up :))')
        print('--------------------')
        is_lock = False
        return is_lock


# file = open(f"{os.environ['HOME']}/Desktop/Bad Words", "r")
database_badwords = ['fuck', 'shit', 'damn', 'bitch']


# file.close()
# api.telegram.org/bot1024213820:AAHgNbsuySh1kMM9OzfncEpIEalx6jIKozI/sendMessage?chat_id=<chat_id>&text=<text>

def check_message(last_index, is_lock):  # last_message = result[len(result_json) - 1]
    # print(last_message)
    if ('callback_query' not in last_index) and (last_index['message']['chat']['type'] == 'private'):
        about_message = 'Hi.\nI am protector of your group!\nI can kick members, ' \
                        'say welcome to new members, lock and unlock your dear group and supergroup, filter bad words ' \
                        'and everything ' \
                        'you want.\nTo use these features with great support, contact with my programmer: ' \
                        '@Omid_KHB\nThanks my friend :) '
        keyboard = [[telegram.InlineKeyboardButton(text='About', url='',
                                                   callback_data='Hi.\nI am protector of your group!'),
                     telegram.InlineKeyboardButton(text='Features', url='',
                                                   callback_data='-Lock and unlock group, supergroup\n-Filter bad words\n-...'),
                     telegram.InlineKeyboardButton(text='Buy', url='',
                                                   callback_data='Contact to @Omid_KHB')]]
        markup = telegram.InlineKeyboardMarkup(keyboard)
        chat_id = last_index['message']['chat']['id']
        bot.send_message(chat_id, text='Hey my friend!\nClick one of these buttons:', reply_markup=markup)

    elif ('callback_query' in last_index) and (last_index['callback_query']['message']['chat']['type'] == 'private'):
        bot.send_message(last_index['callback_query']['message']['chat']['id'], last_index['callback_query']['data'])

    elif (last_index['message']['chat']['type'] == 'supergroup') or (last_index['message']['chat']['type'] == 'group'):
        if 'text' in last_index['message']:
            if last_index['message']['text'] == '/lock':  # command
                is_lock = lock_group(last_index)
                if is_lock == True:
                    print("Group locked")
                    print(f'Lock2: {is_lock}')
                    print('--------------------')
                    return is_lock
                else:
                    return is_lock



            elif last_index['message']['text'] == "/unlock":  # command
                if check_is_admin(last_index):
                    bot.send_message(result[len(result) - 1]['message']['chat']['id'], "Group unlocked!")
                    is_lock = False
                    print("Group unlocked...")
                    print(f'Lock2: {is_lock}')
                    print('--------------------')
                    return is_lock
                else:
                    bot.send_message(result[len(result) - 1]['message']['chat']['id'], "Shut up!")
                    print('I said shut up :))')
                    print('--------------------')
                    return is_lock


            elif last_index['message']['text'] == "/bot_off":  # command
                bot.send_message(result[len(result) - 1]['message']['chat']['id'], "Bot turned off...")
                return "off"


            else:
                if is_lock:
                    if check_is_admin(last_index):  # Check who wrote that, is admin or not
                        is_lock = True
                        print('Is admin...')
                        print('--------------------')
                        return is_lock
                    else:
                        print("deleted!")
                        print('--------------------')
                        bot.delete_message(result[len(result) - 1]['message']['chat']['id'],
                                           result[len(result) - 1]['message']['message_id'])
                        is_lock = True
                        return is_lock
                else:
                    print("Isn't important...")
                    print(f"Lock: {is_lock}")
                    print("------------------")



        elif (('new_chat_participant' in last_index['message']) or ('new_chat_member' in last_index['message']) or (
                'new_chat_members' in last_index['message']) or ('group_chat_created' in last_index['message'])):
            username = last_index['message']['new_chat_participant']['username']
            bot.send_message(last_index['message']['chat']['id'],
                             f'{username} entered to group...\nWelcome our friend :)')
            print(f"{username} entered to group...\nWelcome our friend :)")
            print("------------------")

        elif ('left_chat_participant' in last_index['message']) or ('left_chat_member' in last_index['message']):
            username = last_index['message']['left_chat_participant']['username']
            bot.send_message(last_index['message']['chat']['id'], f'{username} left the group...')
            print(f"{username}  left the group...")
            print("------------------")

        elif str(last_index['message']['text']).startswith("/kick") and check_is_admin(
                last_index):  # check in list of all members,
            # then delete it.
            # Test mode (not completed)
            username = str(last_index).split(' ')[1]
            counter = -1
            for i in result:
                if i['message']['from']['username'] == username:
                    bot.kick_chat_member(i['message']['chat']['id'], i['message']['from']['id'])
                    bot.send_message(result[len(result) - 1]['message']['chat']['id'],
                                     f"User {str(last_index).split(' ')[1]} kicked by admin!")
                    break
                else:
                    counter += 1
            if counter == len(result):  # if user cant be find, counter will be equal to chats number
                bot.send_message(result[len(result) - 1]['message']['chat']['id'],
                                 f"User not found!")
        else:  # If that wasn't any of above
            if is_lock:
                if check_is_admin(last_index):  # Check who wrote that, is admin or not
                    is_lock = True
                    return is_lock
                else:
                    print("deleted!")
                    bot.delete_message(result[len(result) - 1]['message']['chat']['id'],
                                       result[len(result) - 1]['message']['message_id'])
                    is_lock = True
                    return is_lock
            else:
                for i in str(last_index).split(' '):
                    if str(i).lower() in database_badwords:
                        bot.delete_message(result[len(result) - 1]['message']['chat']['id'],
                                           result[len(result) - 1]['message']['message_id'])
                        bot.send_message(result[len(result) - 1]['message']['chat']['id'],
                                         "Bad word deleted")
                        print("Bad word deleted")

                is_lock = False
                return is_lock


is_lock = False

while True:
    json_get_update = requests.get(
        'https://api.telegram.org/bot1024213820:AAHgNbsuySh1kMM9OzfncEpIEalx6jIKozI/getupdates').json()
    result_json = json_get_update['result']
    if len(result_json) > 0:
        offset = result_json[len(result_json) - 1]['update_id']
        print(offset)
        while True:
            json_get_update = requests.get(
                f'https://api.telegram.org/bot1024213820:AAHgNbsuySh1kMM9OzfncEpIEalx6jIKozI/getupdates?offset={offset}').json()
            result = json_get_update['result']
            if len(result) > 0:
                for i in range(0, len(result), 1):
                    last_index = result[len(result_json) - 1]
                    offset += 1
                    print(f'Lock1: {is_lock}')
                    print('In checking...')
                    is_lock = check_message(last_index, is_lock)
                    if is_lock == "off":
                        break
            else:
                print('Message not found...')
                print('--------------------')
    else:
        print('Message not found...')
        print('--------------------')
