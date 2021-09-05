import requests
from bs4 import BeautifulSoup
import telegram
# from apscheduler.schedulers.blocking import BlockingScheduler
import schedule
import time

# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.jobstores.base import JobLookupError
# import pytz
# from datetime import datetime
# datetime.utcnow().replace(tzinfo=pytz.utc)

search_word = '특징주'
# search_word = ['주당 1주', '주당 2주', '액면분할']

token = "1827855613:AAHoQ7oqaEeQ6rN5ZzyUN0oK5cT9iFvM01I"
bot = telegram.Bot(token=token)
# sched = BlockingScheduler()
old_links = []

def extract_links(old_links=[]):
    url = f'https://m.search.naver.com/search.naver?where=m_news&sm=mtb_jum&query={search_word}'
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    search_result = soup.select_one('#news_result_list')
    news_list = search_result.select('.bx>.news_wrap>a')

    links = []
    for news in news_list[:5]:
        link = news['href']
        links.append(link)

    new_links = []
    for link in links:
        if link not in old_links:
            new_links.append(link)

    return new_links

def send_links():
    global old_links
    new_links = extract_links(old_links)
    if new_links:
        for link in new_links:
            bot.sendMessage(chat_id='1543214589', text=link)
    # else:

    old_links += new_links.copy()
    old_links = list(set(old_links))


send_links()
# sched.add_job(send_links, 'interval', hours=1)
# sched.start()
schedule.every(5).minutes.do(send_links)

while True:
    schedule.run_pending()
    time.sleep(1)
