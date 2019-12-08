import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()


machine = TocMachine(
        states=["user", "state1", "state2","state1_1","state1_2","state1_3","state1_4","write","write2","write3","write4"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "state1",
            "conditions": "is_going_to_state1",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "state2",
            "conditions": "is_going_to_state2",
        },
        {
            "trigger": "advance",
            "source": "state1",
            "dest": "state1_1",
            "conditions": "is_going_to_state1_1",
        },
        {
            "trigger": "advance",
            "source": "state1",
            "dest": "state1_2",
            "conditions": "is_going_to_state1_2",
        },       
        {
            "trigger": "advance",
            "source": "state1",
            "dest": "state1_3",
            "conditions": "is_going_to_state1_3",
        },       
        {
            "trigger": "advance",
            "source": "state1",
            "dest": "state1_4",
            "conditions": "is_going_to_state1_4",
        },       
        {
            "trigger":"advance",
            "source":"state1_1",
            "dest":"write",
            "conditions":"is_going_to_write",
        },
        {
            "trigger":"advance",
            "source":"state1_2",
            "dest":"write2",
            "conditions":"is_going_to_write2",
        },
        {
            "trigger":"advance",
            "source":"state1_3",
            "dest":"write3",
            "conditions":"is_going_to_write3",
        },
        {
            "trigger":"advance",
            "source":"state1_4",
            "dest":"write4",
            "conditions":"is_going_to_write4",
        },

        {"trigger": "go_back", "source": ["state1", "state2","state1_1","state1_2","state1_3","state1_4","write","write2","write3","write4"], "dest": "user"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "我看不懂你說什麼!你是不是亂輸入了喵啊啊!!!!!")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
    

