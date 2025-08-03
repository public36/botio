from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# جلب الأرقام من موقع smsreceivefree.com
def fetch_numbers():
    url = "https://smsreceivefree.com/country/usa"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    numbers = []
    for div in soup.find_all('div', class_='number-boxes-item'):
        num = div.find('h4').text.strip()
        link = div.a['href']
        numbers.append({'number': num, 'link': link})
    return numbers

# جلب الرسائل لرقم معين
def fetch_messages(link_path):
    url = f"https://smsreceivefree.com{link_path}"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    messages = []
    rows = soup.find_all('tr')
    for row in rows[1:]:
        cols = row.find_all('td')
        if len(cols) >= 4:
            sender = cols[0].text.strip()
            msg = cols[1].text.strip()
            time = cols[3].text.strip()
            messages.append({'from': sender, 'text': msg, 'time': time})
    return messages

@app.route('/')
def index():
    return jsonify({'message': '✅ API يعمل! استخدم /numbers لرؤية الأرقام'})

@app.route('/numbers')
def get_numbers():
    return jsonify(fetch_numbers())

@app.route('/messages/<path:link>')
def get_messages(link):
    link = '/' + link  # تصحيح الرابط
    return jsonify(fetch_messages(link))

if __name__ == '__main__':
    app.run(debug=True)
