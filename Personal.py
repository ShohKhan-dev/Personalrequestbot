import requests
import datetime



class BotHandler:
    def __init__(self, token):
            self.token = token
            self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=0, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp
    
    def send_me(self, name, user_name, ID, user_text):
        if user_name == "Unknown username":
            text = "Name: " +name+ "\nUsername: " +user_name+ "\nID: " +str(ID)+ "\n\nText: " +user_text
        else:
            text = "Name: " +name+ "\nUsername: @" +user_name+ "\nID: " +str(ID)+ "\n\nText: " +user_text

        params = {'chat_id': "Your Chat_id", 'text': text, 'parse_mode': 'HTML'}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp
        

token = '<Bot token>' 
murojat_bot = BotHandler(token) 



def main():
    new_offset = 0
    while True:
        all_updates=murojat_bot.get_updates(new_offset)

        if len(all_updates) > 0:
            for current_update in all_updates:
                #print(current_update)
                first_update_id = current_update['update_id']
                if 'text' not in current_update['message']:
                    first_chat_text='Unknown message'
                else:
                    first_chat_text = current_update['message']['text']
                first_chat_id = current_update['message']['chat']['id']
                if 'first_name' in current_update['message']:
                    first_chat_name = current_update['message']['chat']['first_name']
                    if 'username' in current_update['message']['chat']:
                        username = current_update['message']['chat']['username']
                    else:
                        username = 'Unknown username'
                elif 'from' in current_update['message']:
                    first_chat_name = current_update['message']['from']['first_name']
                    if 'username' in current_update['message']['from']:
                        username = current_update['message']['from']['username']
                    else:
                        username = 'Unknown username'
                else:
                    first_chat_name = "Unknown"
                    username = 'Unknown username'
                

                if first_chat_text == 'Unknown message':
                    murojat_bot.send_message(first_chat_id, 'Iltimos faqat matnli habar yuboring, boshqa turdagi habarlar qabul qilinmaydi!!!')
                else:
                    if first_chat_id != <your chat_id>:
                        murojat_bot.send_me(first_chat_name, username, first_chat_id, first_chat_text)
                        murojat_bot.send_message(first_chat_id, 'Sizning habaringiz yuborildi. Iltimos! Javobni kuting')
                    else:
                        if 'reply_to_message' in current_update['message']:
                            sms = current_update['message']['reply_to_message']['text']
                            tex = sms.split()
                            if 'ID:' in tex:
                                ind = tex.index('ID:')
                                IDI = tex[ind+1:ind+2]
                                murojat_bot.send_message(IDI, first_chat_text)
                            
                new_offset = first_update_id + 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
