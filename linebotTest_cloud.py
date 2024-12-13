from flask import Flask
app = Flask(__name__)

from flask import request, abort
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import google.generativeai as genai
import os

line_bot_api = LineBotApi(os.environ.get('Line_bot_token'))
handler = WebhookHandler(os.environ.get('Line_bot_secret'))

genai.configure(api_key=os.environ.get('gemini_api_key'))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_prompt=event.message.text
    model = genai.GenerativeModel("gemini-1.5-flash")#版本
    response = model.generate_content(user_prompt)#裡面內容就是我要跟AI對話的內容
    result=response.text
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=result))#AI回覆我們的訊息

if __name__ == '__main__':
    app.run()
