from telethon.sync import TelegramClient from telethon.sessions import StringSession
 
api_id = 7081826639  # ← دخّل API ID ديالك هنا api_hash = 'abcd1234abcd1234abcd1234abcd1234'  # ← دخّل API HASH ديالك هنا
 
with TelegramClient(StringSession(), api_id, api_hash) as client: print("Login successful") print("Here is your session string:") print(client.session.save())
 
