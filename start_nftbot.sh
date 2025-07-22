#!/bin/bash

# مجلد المشروع
PROJECT_DIR="nftbot"
cd ~/$PROJECT_DIR || { echo "❌ مجلد المشروع $PROJECT_DIR غير موجود!"; exit 1; }

# تثبيت الحزم إذا لم تكن مثبتة
if [ ! -d "node_modules" ]; then
  echo "🔄 تثبيت الحزم..."
  npm install || { echo "❌ فشل تثبيت الحزم"; exit 1; }
else
  echo "✅ الحزم مثبتة مسبقًا"
fi

# شغل السيرفر
nohup node index.js > api.log 2>&1 &
echo "✅ API server started."

# شغل البوت
nohup node bot.js > bot.log 2>&1 &
echo "🤖 Bot started."

# انتظر 5 ثواني لفتح ngrok
sleep 5

# جلب رابط ngrok
NGROK_URL=$(curl -s http://127.0.0.1:4040/api/tunnels | grep -o 'https://[a-zA-Z0-9./?=_-]*')

if [ -n "$NGROK_URL" ]; then
  echo "🔗 رابط ngrok العام: $NGROK_URL"
else
  echo "❌ لم يتم العثور على رابط ngrok، تحقق من تشغيل ngrok."
fi