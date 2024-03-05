import requests
import os
import zipfile
import random
import heapq
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import Keys, ActionChains
import time


# region ''' DICTIONARY '''

dictionary = {
    "77078221234": "ZZ",
    "dobryan72@bk.ru": "XXX",
    "77016534225": "ZEDFE",
    "77022451626": "FWRFRW",
    "77018043811": "FWEFEW",
}
# endregion

# region  ''' PROXY WITH AUTHENTICATION '''
PROXY_HOST = '178.124.218.181'  # rotating proxy
PROXY_PORT = 7030
PROXY_USER = 'zfmidmzt'
PROXY_PASS = 'ikyvfgor'


manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
          singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
          },
          bypassList: ["localhost"]
        }
      };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

# '''''' CREATE_CHROME_OPTOINS_TO_GET_NEXT_PROXY ''''''
path = os.path.dirname(os.path.abspath(__file__))
chrome_options = webdriver.ChromeOptions()
pluginfile = 'proxy_auth_plugin.zip'
with zipfile.ZipFile(pluginfile, 'w') as zp:
    zp.writestr("manifest.json", manifest_json)
    zp.writestr("background.js", background_js)
chrome_options.add_extension(pluginfile)

# endregion

# region ''' OPTOINS '''

options = webdriver.ChromeOptions()

#  ''' User_Agent '''
def get_user_agent():
    with open("UserAgents", "r") as f:
        for line in f:
            useragent = line.strip()
            print(f"New_User_Agent: {useragent}")
            yield useragent
iterator = get_user_agent()


# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36")

options.add_experimental_option('excludeSwitches', ['enable-logging'])

options.add_argument("--disable-blink-features=AutomationControlled")

options.add_argument("--no-sandbox")

options.add_argument("--start-maximized")

options.add_argument("--window-size=1920,1080")

# options.add_argument('--headless=new')

options.add_argument('--disable-setuid-sandbox')

options.add_argument('--disable-dev-shm-usage')

options.add_argument("--disable-popup-blocking")

options.add_argument('--disable-gpu')

options.page_load_strategy = "eager"

options.add_experimental_option('useAutomationExtension', False)

# ''' IF_USE_SELENOID_DOCKER '''
# options.add_argument("--browser-version=121.0")
# options.add_argument("--platform=linux")
# driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', options=options)


# ''' URL '''
url1 = "https://vk.com/"
url2 = "https://vk.com/club223860964/"


# endregion

# ''' START SCRIPT WITH NEW LOGIN/PASS && USERAGENT && PROXY '''
for vk_phone, vk_password in dictionary.items():
    try:
        # ''' NEW SESSION && NEW USERAGENT '''
        useragent = next(iterator)
        options = webdriver.ChromeOptions()
        options.add_argument(f"--user-agent={useragent}")
        driver = webdriver.Chrome(os.path.join(path, 'chromedriver'), options=options, chrome_options=chrome_options)
        action = ActionChains(driver)

        # ''' NEW PROXY '''
        # Отправка запроса
        time.sleep(50)
        requests.get("http://178.124.218.181:8881/changeip/vlanudpclrgnnikg")
        time.sleep(15)

        # ''' START '''
        print("Start")
        driver.get(url=url1)
        driver.maximize_window()
        driver.execute_script("document.body.style.zoom = 0.9;")

        # ''' INPUT LOGIN '''
        print("Input_login")
        input_login = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "index_email")))
        input_login.clear()
        input_login.send_keys(vk_phone)
        time.sleep(2)
        input_login.send_keys(Keys.RETURN)

        # ''' HOW TO ENTRY IN PROFILE: PASSWORD OR CODE '''
        try:
            print("Entry_by_password_1")
            by_password_1 = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@class='vkuiButton__in']")))
            by_password_1.click()

            print("Entry_by_password_2")
            by_password_2 = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@data-test-id='verificationMethod_password']")))
            by_password_2.click()
        except:
            pass

        # ''' INPUT PASSWORD '''
        print("Input_password")
        input_password = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.NAME, 'password')))
        input_password.clear()
        input_password.send_keys(vk_password)
        input_password.send_keys(Keys.RETURN)
        time.sleep(5)

        # ''' GO TO THE PUBLIC '''
        print("Go_to_the_public")
        driver.get(url=url2)
        time.sleep(5)
        action.key_down(Keys.ESCAPE).key_up(Keys.ESCAPE).perform()

        # ''' CHECKING SUBSCRIPTION ON THIS CHANNEL'''
        try:
            print("Check_subs")
            check_subs_text = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="redesigned-group-subscribed redesigned-group-subscribed--button"]'))).text
            if check_subs_text == "Вы подписаны":
                print("(+)")
        except Exception:
            pass
            print("(-)")

            # ''' CLICK SUBSCRIPTION '''
            print("Start_subs")
            subs = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[@id="join_button"]')))
            action.click(subs).perform()
            print("Finish_subs")

        # ''' GO TO THE NEXT POST AFTER NEEDING '''
        # Найти пост с ID "post-223860964_38"
        initial_post_element = driver.find_element(By.XPATH, '//div[@id="post-223860964_38"]')

        # Найти "дедушку" этого поста
        wall_element = driver.find_element(By.XPATH, '//div[@id="wide_column"]')

        # Найти все посты на стене
        all_posts_elements = wall_element.find_elements(By.XPATH, './/div[@data-post-author-id="-223860964"]')

        # Найти индекс начального поста
        initial_post_index = all_posts_elements.index(initial_post_element)

        # Если начальный пост не последний, найти следующий
        if initial_post_index < len(all_posts_elements) - 1:
            next_post_element = all_posts_elements[initial_post_index + 1]
        else:
            next_post_element = None

        # GO to the next post element
        if next_post_element:
            print("Go_to_the_next_post")
            action.move_to_element(next_post_element).perform()
            time.sleep(2)
            action.scroll_by_amount(0, -225).perform()
            time.sleep(5)
        else:
            print("Next_post_not_found")

        # ''' CHECK AND CLICK LIKE '''
        print("Check_like")
        check_like = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, '//div[@id="post-223860964_38"]//div[contains(@aria-label, "реакцию «Нравится»")]')))
        time.sleep(2)
        if check_like == 'Убрать реакцию «Нравится»':
            print("(+)")
        else:
            print("(-)")
            check_like.click()
            print("Rlick_like")

        # ''' REPOST POST ON THE OWN WALL '''
        print("Repost_1")
        repost_1 = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="post-223860964_38"]//div[@title="Поделиться"]')))
        repost_1.click()
        time.sleep(5)

        try:
            print("Repost_2")
            repost_2 = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="like_share_my"]')))
            repost_2.click()
        except TimeoutException:
            print("Repost_1__second_attempt")
            time.sleep(5)
            repost_1 = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="post-223860964_38"]//div[@title="Поделиться"]')))
            repost_1.click()
            time.sleep(5)
            print("Repost_2__second_attempt")
            repost_2 = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="like_share_my"]')))
            repost_2.click()

        print("Repost_3")
        repost_3 = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[@id="like_share_send"]')))
        repost_3.click()
        time.sleep(3)

        # ''' OPEN COMMENTS '''
        print("Open_comments")
        open_comments = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="post-223860964_38"]//div[@title="Комментарий"]')))
        open_comments.click()
        time.sleep(2)

        # ''' SCROLL DOWN '''
        action = ActionChains(driver)
        action.key_down(Keys.CONTROL).send_keys(Keys.END).perform()
        action.key_up(Keys.CONTROL).perform()
        time.sleep(2)

        # ''' CLICK SHOW ALL COMMENTS '''
        try:
            while True:
                # Поиск кнопки
                button = driver.find_element(By.XPATH, "//span[@class='js-replies_next_label replies_next_label']")
                # Если кнопка найдена
                if button:
                    button.click()
                    print("Click_show_all_comments")
                    time.sleep(1)
        # Если кнопка не найдена
        except:
            pass


        # region ''' ACTIONS TO FIND RIGHT COMMENT '''

        print("Start_to_find_comment")

        # Получаем все элементы, содержащие текст комментариев
        all_posts = driver.find_elements(By.XPATH,'//div[@class="wl_replies"]/descendant::div[@class="reply_wrap _reply_content _post_content clear_fix"]//div[@class="wall_reply_text"]')

        # Проверяет, есть ли комментарий с заданным числом в списке постов
        def has_comment(all_posts, number):

            for post in all_posts:
                if str(number) in post.text:
                    return True
            return False

        # Функция для безопасного преобразования текста в число
        def try_parse_int(text):

            if not text or not text.strip():
                return None  # Обрабатываем пустой текст
            try:
                return int(text)
            except ValueError:
                # Обрабатываем нечисловые символы
                print(f"Error: Could not convert '{text}' to int")
                return -1  # Пример: возвращаем специальное значение


        # Получаем список чисел из комментариев
        numbers = [try_parse_int(post.text) for post in all_posts]

        # Находим три наибольших числа
        max_number, second_max_number, third_max_number = heapq.nlargest(3, numbers)

        # Проверка условия
        if max_number is not None:
            if has_comment(all_posts, max_number - 1) and has_comment(all_posts, max_number - 2):
                new_result = max_number + 1
                last_result = max_number
            elif has_comment(all_posts, second_max_number - 1) and has_comment(all_posts, second_max_number - 2):
                new_result = second_max_number + 1
                last_result = max_number
            elif has_comment(all_posts, third_max_number - 1) and has_comment(all_posts, third_max_number - 2):
                new_result = third_max_number + 1
                last_result = max_number
        else:
            new_result = None

        # endregion


        # ''' WRITE RESULT '''
        print(f'''Last_comment={last_result}''')
        print(f'''New_comment={new_result}''')

        # ''' SCROLL DOWN TO WRITE COMMENT '''
        print("Scrool_Down_again_to_see_comment")
        action.scroll_by_amount(0, 5000).perform()
        time.sleep(2)

        # ''' SEND COMMENT '''
        print("Send_comment")
        send_comment = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="wk_content"]//div[@role="textbox"]')))
        send_comment.click()
        send_comment.clear()
        send_comment.send_keys(new_result)
        time.sleep(0.5)
        send_comment.send_keys(Keys.RETURN)
        time.sleep(2)
        print("FINISH!!!!!")

        # ''' WAIT RANDOM TIME '''
        random_time = random.uniform(10, 11)
        hours = round(random_time // 3600)
        minutes = round((random_time % 3600) // 60)
        print(f"Waiting {hours} hours {minutes} minites...")

        # ''' SCROLL IN THIS TIME '''
        scroll_frequency = 5
        while random_time > 0:
            action.scroll_by_amount(0, -20).perform()
            time.sleep(scroll_frequency)
            random_time -= scroll_frequency


    except Exception as ex:
        print(ex)
    finally:
        driver.quit()
        print("New_iteration...\n\n")