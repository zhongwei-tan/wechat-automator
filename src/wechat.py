import itchat


def login_callback():
    print('Login successful')

def logout_callback():
    print('Logout')
    itchat.auto_login(hotReload=True, loginCallback=login_callback, exitCallback=logout_callback)

def wechat_login():
    itchat.auto_login(hotReload=True, statusStorageDir='itchat.pkl', enableCmdQR=2,
                      loginCallback=login_callback, exitCallback=logout_callback)

def send_message_to_chatroom(message: str, chatroom_name: str):
    try:
        chatroom = itchat.search_chatrooms(name=chatroom_name)[0]
        chatroom.send(message)
        print('Message sent!')
    except IndexError:
        print('Chatroom {} is not found'.format(chatroom_name))