import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from linebot.models import (
    TemplateSendMessage, ButtonsTemplate, MessageTemplateAction,
    PostbackAction, MessageAction, ImageSendMessage,
    URIAction, AltUri, DatetimePickerAction,
    ConfirmTemplate, CarouselTemplate, CarouselColumn,
    ImageCarouselTemplate, ImageCarouselColumn
)
from transitions.extensions import GraphMachine

from utils import send_text_message
from utils import send_image_url

cred=credentials.Certificate('linebot-1708b.json')
firebase_admin.initialize_app(cred)
db=firestore.client()

#doc_ref = db.collection("BOT").document("user1")
doc_path="BOT/user1"
doc_ref=db.document(doc_path)
class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_state1(self, event):
        text = event.message.text
        return text.lower() == "記帳"

    def is_going_to_state2(self, event):
        text = event.message.text
        return text.lower() == "我的帳本"
    def is_going_to_write(self,event):
        text =event.message.text
        flag=text.isdigit()
        global u1
        u1=0
        global value
        try:
            value=int(text)
            if value>=0:
                flag=1
            else:
                flag=0
        except:
            flag=0
        if text=="清空":
            u1=1
            flag=1
        return flag

    def is_going_to_write2(self,event):
        text =event.message.text
        flag=text.isdigit()
        global u2
        u2=0
        global value2
        try:
            value2=int(text)
            if value2>=0:
                flag=1
            else:
                flag=0
        except:
            flag=0
        if text=="清空":
            u2=1
            flag=1
        return flag
        

    def is_going_to_write3(self,event):
        text =event.message.text
        flag=text.isdigit()
        global value3
        global u3
        u3=0
        try:
            value3=int(text)
            if value3>=0:
                flag=1
            else:
                flag=0
        except:
            flag=0
        if text=="清空":
            u3=1
            flag=1
        return flag

    def is_going_to_write4(self,event):
        text =event.message.text
        flag=text.isdigit()
        global value4
        global u4
        u4=0
        try:
            value4=int(text)
            if value4>=0:
                flag=1
            else:
                flag=0
        except:
            flag=0
        if text=="清空":
            u4=1
            flag=1
        return flag

    def is_going_to_state1_1(self,event):
        text = event.message.text
        return text.lower()=="餐費"
    def is_going_to_state1_2(self,event):
        text = event.message.text
        return text.lower()=="娛樂"
    def is_going_to_state1_3(self,event):
        text = event.message.text
        return text.lower()=="交通"
    def is_going_to_state1_4(self,event):
        text = event.message.text
        return text.lower()=="其他"

    def on_enter_state1(self, event):
        print("I'm entering state1")

        reply_token = event.reply_token
        send_text_message(reply_token, "喵喵喵~\n輸入想要記的項目~\n[餐費]  [娛樂]  [交通]  [其他]")
        #self.go_back()

    def on_enter_state1_1(self,event):
        reply_token=event.reply_token
        send_text_message(reply_token,"喵嗚嗚~\n輸入費用/或想刪除請輸入[清空]")

    def on_enter_state1_2(self,event):
        reply_token=event.reply_token
        send_text_message(reply_token,"喵嗚嗚~\n輸入費用/或想刪除請輸入[清空]")

    def on_enter_state1_3(self,event):
        reply_token=event.reply_token
        send_text_message(reply_token,"喵嗚嗚~\n請輸入費用/或想刪除請輸入[清空]")

    def on_enter_state1_4(self,event):
        reply_token=event.reply_token
        send_text_message(reply_token,"喵嗚嗚~\n請輸入費用/或想刪除請輸入[清空]")
            
       
    def on_enter_write(self,event):
        reply_token=event.reply_token
        send_text_message(reply_token,"好的已經記好了喵~\n想看完整的要輸入[我的帳本]\n我就會幫你打開了窩~")
        getdoc=doc_ref.get()
        d=getdoc.to_dict()['food_money']
        if u1==1:
            content={'food_money':0}
        else:
            content={'food_money':d+value}
        doc_ref.update(content)
        self.go_back()

    def on_enter_write2(self,event):
        reply_token=event.reply_token
        send_text_message(reply_token,"好的已經記好了喵~\n想看完整的要輸入[我的帳本]\n我就會幫你打開了窩~")
        getdoc=doc_ref.get()
        d=getdoc.to_dict()['entertainment']
        if u2==1:
            content={'entertainment':0}
        else:
            content={'entertainment':d+value2}
        doc_ref.update(content)
        self.go_back()    

    def on_enter_write3(self,event):
        reply_token=event.reply_token
        send_text_message(reply_token,"好的已經記好了喵~\n想看完整的要輸入[我的帳本]\n我就會幫你打開了窩~")
        getdoc=doc_ref.get()
        d=getdoc.to_dict()['traffic']
        if u3==1:
            content={'traffic':0}
        else:
            content={'traffic':d+value3}
        doc_ref.update(content)
        self.go_back()

    def on_enter_write4(self,event):
        reply_token=event.reply_token
        send_text_message(reply_token,"好的已經記好了喵~\n想看完整的要輸入[我的帳本]\n我就會幫你打開了窩~")
        getdoc=doc_ref.get()
        d=getdoc.to_dict()['other']
        if u4==1:
            content={'other':0}
        else:
            content={'other':d+value4}
        doc_ref.update(content)
        self.go_back()  

    # def on_exit_state1(self):
    #    print("Leaving state1")

    def on_enter_state2(self, event):
        print("I'm entering state2")
        doc = doc_ref.get()
        total=doc.to_dict()['entertainment']+doc.to_dict()['food_money']+doc.to_dict()['traffic']+doc.to_dict()['other']

        reply_token = event.reply_token
        send_text_message(reply_token,"喵哈哈!!來看看你都花了多少錢吧~\n"+"餐費:"+str(doc.to_dict()['food_money'])
                +"\n"+"娛樂費:"+str(doc.to_dict()['entertainment'])+"\n"+"交通費:"+str(doc.to_dict()['traffic'])
                +"\n"+"其他:"+str(doc.to_dict()['other'])+"\n"+"總支出:"+str(total))
        user_id=event.source.user_id
        img=ImageSendMessage(
                original_content_url = 'https://i.imgur.com/RV5O2Sz.jpg',
                preview_image_url = 'https://i.imgur.com/RV5O2Sz.jpg'
                )
        send_image_url(user_id,img)
        self.go_back()

   # def on_exit_state2(self):
    #    print("Leaving state2")
