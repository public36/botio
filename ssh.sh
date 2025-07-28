#!/bin/bash

echo "🔧 Generating new SSH key..."

# تحديد البريد الإلكتروني
default_email="mbomadian23@gmail.com"
read -p "📧 دخل الإيميل ولا خليه فارغ باش نستعمل الافتراضي [$default_email]: " user_email
user_email=${user_email:-$default_email}

# توليد مفتاح SSH جديد
ssh-keygen -t ed25519 -C "$user_email" -f ~/.ssh/id_ed25519 -N ""

# تعيين الصلاحيات
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub

# تشغيل SSH Agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# إضافة المفتاح اللي عطيتيني إلى ملف المفتاح العمومي
echo 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIN9EGJGHRk//Ut5srxzKY+3kOTBtj3OW6+ztXSpMmXWc mbomadian23@gmail.com' >> ~/.ssh/id_ed25519.pub

echo ""
echo "🚀 Public Key (اللي تقدر تضيفه لـ GitHub أو السيرفر):"
cat ~/.ssh/id_ed25519.pub

echo ""
echo "📋 انسخو ولسقو فحساب GitHub ولا فالسيرفر:"
echo "🔗 GitHub: https://github.com/settings/ssh/new"