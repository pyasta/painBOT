from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import json

dev = [5422543182] 
token = "6671054872:AAFLCso0Sc42CZU86mR0Pj_UVT9n641LnT4" 
app = Client('bot',9398500,'ad2977d673006bed6e5007d953301e13',bot_token=token)

import os
import sys



# Create a dictionary to store user actions
user_actions = {}

@app.on_message(filters.command("start") & filters.private ,group=1)
def start(client, message):
   if message.from_user.id in dev: 
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("اضف اسم", callback_data="add_name"),
         InlineKeyboardButton("مسح اسم", callback_data="delete_name")],
        [InlineKeyboardButton("🏝️", callback_data="aa"),
        ],
        [InlineKeyboardButton("جلب جميع الأسماء", callback_data="get_all_names"),
         InlineKeyboardButton("مسح جميع الأسماء", callback_data="delete_all_names")]
    ])
    message.reply(f"**مرحبا بك {message.from_user.mention} في مركز الاستخبارات**\n\nاختر الإجراء الذي تريده:", reply_markup=markup)



@app.on_callback_query()
def button(client, query):
    if query.data == "add_name":
        query.message.reply("الرجاء إرسال الاسم الذي تريد إضافته.")
        user_actions[query.from_user.id] = "add_name"
    elif query.data == "delete_name":
        query.message.reply("الرجاء إرسال الاسم الذي تريد حذفه.")
        user_actions[query.from_user.id] = "delete_name"
    elif query.data == "get_all_names":
        names = get_all_names()
        if names:
            query.message.reply("\n".join(names))
        else:
            query.message.reply("لم يتم العثور على أسماء في الملف.")
    elif query.data == "delete_all_names":
        delete_all_names()
        query.message.reply("تم مسح جميع الأسماء من الملف.")

@app.on_message(filters.all,group=2)
def handle_message(client, message):
    action = user_actions.get(message.from_user.id)
    if action == "add_name":
        name = message.text
        add_name(name)
        message.reply(f"تم حفظ الاسم {name} في قاعدة البيانات.")
    elif action == "delete_name":
        name = message.text
        delete_name(name)
        message.reply(f"تم مسح الاسم {name} من الملف.")
    user_actions.pop(message.from_user.id, None)

def add_name(name):
    names = get_all_names()
    names.append(name)
    save_names(names)

def delete_name(name):
    names = get_all_names()
    names = [n for n in names if n != name]
    save_names(names)

def get_all_names():
    names = load_names()
    return names

def save_names(names):
    with open("names.json", "w", encoding="utf-8") as file:
        json.dump(names, file, ensure_ascii=False)

def load_names():
    try:
        with open("names.json", "r", encoding="utf-8") as file:
            names = json.load(file)
        return names
    except FileNotFoundError:
        return []

def delete_all_names():
    with open("names.json", "w", encoding="utf-8") as file:
        json.dump([], file, ensure_ascii=False)

@app.on_message(filters.text,group=3)
async def check_user_message(client, message):
    keywords = get_all_names()
    for keyword in keywords:
        if keyword in message.text:
           id = message.from_user.id
           men = message.from_user.mention
           c = message.chat.title
           mi = message_ids=message.id
           lin = await app.export_chat_invite_link(message.chat.id)
           chat_id = message.chat.id
           chat_info = await app.get_chat(chat_id) 
           chat_user = chat_info.username
           ciaid = chat_info.id
           cias = str(ciaid)
           ci = cias[4:]
           usern = await app.get_users(message.from_user.id)
           us = usern.username
           user_message = message.text 

    
    link_message = f"https://t.me/c/{ci}/{mi}" 
    ll = f"[اضغط هنا 🏝️.]({link_message})"
    
    for keyword in keywords:
        if keyword in user_message:
            await app.send_message(chat_id=5422543182,text= f"**مشتبه به استعمل احد الكلمات المراقبة\n\nالمشتبه به : ( {men} )\nمعرف المشتبه به : ( @{us} )\nايدي المشتبه به : ( `{id}` )\nالمعرف الخاص بالمجموعة : ( @{chat_user} )\nاسم المجموعة المشتبه بها : ( `{c}` )\nرابط الرسالة :( {ll} )\n\nالرسالة :( {user_message} )\n\nرابط دعوى الى المجموعة :\n( {lin} )  \n\nالرسالة المحولة 👇👇.**",disable_web_page_preview=True)
            await app.forward_messages(
       chat_id=5422543182, from_chat_id=message.chat.id, message_ids=message.id)
            if message.text == 'تحديث':
             await message.reply(quote=True, text=f' تم تحديث الملفات')
             python = sys.executable
             os.execl(python, python, *sys.argv)

app.run()

