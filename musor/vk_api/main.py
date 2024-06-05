import vk_api
import os
from dotenv import load_dotenv


def two_factor():
    code = input('Code? ')
    return code, 0

def captcha_handler(captcha):
    """ При возникновении капчи вызывается эта функция и ей передается объект
        капчи. Через метод get_url можно получить ссылку на изображение.
        Через метод try_again можно попытаться отправить запрос с кодом капчи
    """

    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()

    # Пробуем снова отправить запрос с капчей
    return captcha.try_again(key)

def initApi(login, captcha_handler, auth_handler, app_id, token):
    vk = vk_api.VkApi(login, captcha_handler= captcha_handler, auth_handler=auth_handler, app_id= app_id, token= token)

    try:
        vk.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    api = vk.get_api()

    

    return api



def main():
    load_dotenv()
    login = os.getenv("LOGIN")
    token = os.getenv("TOKEN")
    app_id = os.getenv("APP_ID")

    print(login, app_id, token)

    api = initApi(login, captcha_handler, two_factor, app_id, token)

    api.wall.get()
    
    


if __name__ == '__main__':
    main()