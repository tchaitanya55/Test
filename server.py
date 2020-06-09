import requests as requests
from selenium import webdriver
import json


url = "http://studentscorner.vardhaman.org/"
driver = webdriver.Chrome("C:\\Users\\rks15\\OneDrive\\Desktop\\chromedriver")





def mid1_marks():
    update = last_update(url)
    send_message(get_chat_id(update), 'enter roll no')
    un=get_message_text(update)
    send_message(get_chat_id(update), 'enter password')
    pas=get_message_text(update)
    driver.get(url)
    driver.find_element_by_id("username").send_keys(un)
    driver.find_element_by_id("login-pass").send_keys(pas)
    driver.find_element_by_class_name("ok").click()

    driver.find_element_by_link_text('Internal Marks').click()

    row = len(driver.find_elements_by_xpath("/html/body/table[3]/tbody/tr"))
    col = len(driver.find_elements_by_xpath("/html/body/table[3]/tbody/tr[3]/th"))
    # print(row)
    # print(col)
    dict = {}
    l1 = []
    l2 = []
    for i in range(3, row + 1):

        for j in range(3, 4):
            val = driver.find_element_by_xpath("/html/body/table[3]/tbody/tr[" + str(i) + "]/th[" + str(j) + "]").text
            l1.append(val)
    for i in range(3, row + 1):

        for j in range(4, 5):
            val = driver.find_element_by_xpath("/html/body/table[3]/tbody/tr[" + str(i) + "]/th[" + str(j) + "]").text
            l2.append(val)
    for i in range(0, len(l1)):
        dict[l1[i]] = int(l2[i])
    # print(dict)
    marks_json = json.dumps(dict)
    send_message(get_chat_id(update), marks_json)


url = "https://api.telegram.org/bot1225689665:AAE30R2XKLjs1zutn4lJMb6xqi_Z5lGK1RU/"


# create func that get chat id
def get_chat_id(update):
    chat_id = update['message']["chat"]["id"]
    return chat_id


# create function that get message text
def get_message_text(update):
    message_text = update["message"]["text"]
    return message_text


# create function that get last_update
def last_update(req):
    response = requests.get(req + "getUpdates")
    response = response.json()
    result = response["result"]
    total_updates = len(result) - 1
    return result[total_updates]  # get last record message update


# create function that let bot send message to user
def send_message(chat_id, message_text):
    params = {"chat_id": chat_id, "text": message_text}
    response = requests.post(url + "sendMessage", data=params)
    return response


# create main function for navigate or reply message back
def main():
    update_id = last_update(url)["update_id"]
    while True:
        update = last_update(url)
        if update_id == update["update_id"]:
            if get_message_text(update).lower() == "/start" or get_message_text(update).lower() == "hi":
                send_message(get_chat_id(update), 'enter 1 as input')
            elif get_message_text(update).lower() == "1":
                send_message(get_chat_id(update), mid1_marks())
            else:
                send_message(get_chat_id(update), "Sorry :(")
            update_id += 1


# call the function to make it reply
main()
