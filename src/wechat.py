import itchat
import time
import yaml


def login_callback():
    print("Login successful")

def logout_callback():
    print("Logout")
    itchat.auto_login(hotReload=True, statusStorageDir="itchat.pkl", enableCmdQR=2,
                      loginCallback=login_callback, exitCallback=logout_callback)

def wechat_login():
    itchat.auto_login(hotReload=True, statusStorageDir="itchat.pkl", enableCmdQR=2,
                      loginCallback=login_callback, exitCallback=logout_callback)

def search_chatrooms(chatroom_name: str):
    found_chatroom = None
    start_time = time.time()
    while not found_chatroom and time.time() - start_time < 10:
        found_chatroom = itchat.search_chatrooms(name=chatroom_name)
    if found_chatroom:
        print(f"Chatroom \"{chatroom_name}\" found.")
        return found_chatroom[0]
    else:
        print(f"Chatroom \"{chatroom_name}\" not found!")
        return None

def send_message_to_chatroom(message: str, chatroom_name: str):
    try:
        chatroom = search_chatrooms(chatroom_name)
        chatroom.send(message)
        print("Message sent.")
    except IndexError:
        print("Message not sent!")


# Login wechat at startup
# Check if all chatrooms in reminder_list.yml are found
# Remember to set in wechat app the groupchat setting "Save to Contacts"
if __name__ == "__main__":
    wechat_login()

    print("Checking chatrooms...")
    with open("reminder_list.yml", "r") as file:
        reminders = yaml.load(file, Loader=yaml.FullLoader)
        chatrooms = set(reminder["chatroom"] for reminder in reminders.values())
    for chatroom in chatrooms:
        search_chatrooms(chatroom)