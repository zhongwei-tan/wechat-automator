import itchat
import requests


def login_callback():
    print('Login successful')

def logout_callback():
    print('Logout')

def wechat_login():
    itchat.originInstance.s.close()
    itchat.originInstance.s = requests.Session()
    itchat.auto_login(hotReload=True, statusStorageDir='itchat.pkl', enableCmdQR=2,
                      loginCallback=login_callback)

def send_message_to_chatroom(message: str, chatroom_name: str):
    try:
        chatroom = itchat.search_chatrooms(name=chatroom_name)[0]
        chatroom.send(message)
        print('Message sent!')
    except IndexError:
        print('Chatroom {} is not found'.format(chatroom_name))


# Login wechat at startup
if __name__ == "__main__":
    wechat_login()