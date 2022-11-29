#Импорт необходимых библиотек нахуй
import time
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import telebot

#Токен бота и айди тг канала
bot_token = "5983451174:AAHXRmGlzXk_sEufMi6zo3VbVCi_2ruOg98"
id_channel = "@invest_tl"

#Объект бота
bot = telebot.TeleBot(bot_token)

#URL дзен канала
url = "https://dzen.ru/id/5f9495ed1c757132502a4a09"
#Подрубаем selenium в переменную driver
driver = webdriver.Chrome()
#И даем ему наш url адрес
driver.get(url)

#Функция проверяет существует ли в поле видимости элемент
def is_element_exist(text):
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, text)))
    except TimeoutException:
        return False

#Функция парсинга
def parsing(prev_post):
    post = driver.find_element(By.CLASS_NAME, "card-image-compact-view__content")
    post_text = post.text

    if post_text != prev_post:
        href = post.find_element(By.CLASS_NAME, "zen-ui-card-title-clamp")
        description = post.find_element(By.CLASS_NAME, "card-layer-snippet-view").text.strip()
        hrefUrl = href.get_attribute("href")
        href_title = href.text.strip()

        info_description = (description[:100] + '...') if len(description) > 100 else description
        return f"{href_title}\n\n{info_description}\n\n{hrefUrl}", post_text
    else:
        return None, post_text


prev_post = None
#Бесконечный цикл в котором проверяется вышла ли новая статья, не парсили ли мы уже такую.
#Если нет то парсим
while True:
    while True:
        #Если статей не прогружено, мотаем страницу вниз, прогружая элементы ( и статьи )
        while is_element_exist("zen-ui-card-title-clamp") == False:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        break
    #Ебашим дальше, браузер обновляется каждые n секунд чтобы новые статьи отобразились и если они есть - парсим
    post_return = parsing(prev_post)
    prev_post = post_return[1]
    driver.refresh()
    time.sleep(30)
    if post_return[0] != None:
        bot.send_message(id_channel, post_return[0])
        time.sleep(30)

bot.polling()