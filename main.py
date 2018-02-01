import pickle
import pathlib
import random
import time
import os, sys
import urllib.request


from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By


user_login = 'anastasya280789@mail.ru'
user_password = 'Jzz2ryGF'
output_folder = 'output'


def get_current_folder():
    return os.path.dirname(sys.modules['__main__'].__file__)


def get_output_folder():
    return get_current_folder() + "/" + output_folder


def wait(wait_period=6):
    if wait_period is None:
        wait_time = int(random.random() * wait_period) + 2
    else:
        wait_time = wait_period
    time.sleep(wait_time)


def check_auth_from_cookies(driver):
    my_file = Path("cookies.pkl")
    auth_from_cookies = False

    if my_file.is_file():
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
            auth_from_cookies = True

    return auth_from_cookies


def load_to_cosmetic_ru(driver):
    url = 'https://www.cosmeticru.com/'

    # get file with cookies
    driver.get(url)
    wait(5)

    if not check_auth_from_cookies():
        found_login_but = None

        found_login_but = driver.find_element_by_xpath(
            "//a[text()='Вход' and contains(@class,'button') and @href='#popup-login' and @data-type='text']")

        if found_login_but is None:
            print("Error: cant find Login Button")
            exit()

        wait()
        found_login_but.click()

        user_name_elem = None;
        user_password_elem = None;

        user_name_elem = driver.find_element_by_name("user[email]")
        user_password_elem = driver.find_element_by_name("user[password]")

        if user_name_elem is None:
            print('Error: login field not found')
            exit()

        if user_password_elem is None:
            print('Error: password field not found')
            exit()

        user_name_elem.send_keys(user_login)
        user_password_elem.send_keys(user_password)

        submit_but = None
        submit_but = driver.find_element_by_xpath(
            "//button[text()='Войти' and contains(@class, 'button') and @type='submit']")

        if submit_but is None:
            print('Error: submit button not found')
            exit()

        submit_but.click()
        wait()


def login_to_sikorsky_acdm(driver):
    url_courses = 'https://www.sikorsky.academy/'

    driver.get(url_courses)
    check_auth = check_auth_from_cookies(driver)
    driver.get(url_courses)
    driver.execute_script("")
    wait()

    cosm_but = None
    try:
        cosm_but = driver.find_element_by_xpath("//a[text()='Косметология ВИП']")
    except:
        cosm_but = None

    if cosm_but is None or check_auth == False:

        user_name_elem = None;
        user_password_elem = None;

        user_name_elem = driver.find_element_by_id("user_email")
        user_password_elem = driver.find_element_by_id("user_password")

        if user_name_elem is None:
            print('Error: login field not found')
            exit()

        if user_password_elem is None:
            print('Error: password field not found')
            exit()

        user_name_elem.send_keys(user_login)
        user_password_elem.send_keys(user_password)
        wait()

        submit_but = None
        submit_but = driver.find_element_by_xpath("//input[@type='submit']")

        if submit_but is None:
            print('Error: submit button not found')
            exit()

        submit_but.click()
        wait()

        pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))


def create_folders(name):
    new_path = get_output_folder() + "/" + name
    folder = Path(new_path)

    if not folder.is_dir():
        pathlib.Path(new_path).mkdir(parents=True, exist_ok=True)

    return new_path


def check_folder_finished(folder_name):
    path = Path(folder_name + "/finished")
    return path.is_file()


def save_images(driver, path):
    fotorama__img_class = driver.find_element_by_xpath("//img[ contains(@class,'fotorama__img')]")

    if fotorama__img_class is None:
        print("Error: cant find fotorama__img_class")
        return


    num = 1

    # download the image
    while num <= 1000:
        src = fotorama__img_class.get_attribute('src')
        res = src[- src[::-1].find(".") - 1:]
        file_name = path+"/picture"+str(1)+res
        urllib.request.urlretrieve(src, file_name)
        wait()

        next_button = driver.find_element_by_xpath( "//div[ contains(@class,'fotorama__arr fotorama__arr--next')]")
        attr = next_button.get_attribute("disabled")

        if attr is not None and attr =='disabled':
            break;

        if next_button is None:
            print("Error: cant find fotorama__arr fotorama__arr--next")
            return

        next_button.click()
        wait()

        num = num + 1


#def Myclick(driver,webElement):
   # driver.executeScript("arguments[0].scrollIntoView(true);", webElement)
   # webElement.click();

def main():
    driver = webdriver.Chrome()
    login_to_sikorsky_acdm(driver)
    lectures_list = []

    cosm_but = driver.find_element_by_xpath("//a[text()='Косметология ВИП']")

    if cosm_but is None:
        print("Error: cant find Космитология ВИП кнопка")
        exit()

    cosm_but.click()
    wait()

    # nav_menu = driver.find_element_by_xpath("//ul[@class='lections_nav']")

    # if nav_menu is None:
    #    print('Error: cant found navigation panel')
    #    exit()

    blocks = driver.find_elements_by_xpath("//li[contains(@class,'nav_block')]")

    if blocks is None:
        print('Error: cant found menu blocks panel')
        exit()

    for j in blocks:
        j.click()
        wait()

        block_name = j.find_element_by_xpath(".//div[@class='block_name']").text
        block_name = block_name[0:block_name.find("\n")]
        lections = j.find_elements_by_xpath(".//li[@class='lections-li']")
        print(block_name)

        if lections is None:
            print('Error: cant found lections class in blocks panel')
            continue

        for lec_id in lections:
            lec_a = lec_id.find_element_by_xpath(".//a")
            lec_div_tooltip = lec_id.find_element_by_xpath(".//div[@class='tooltip']")
            #lec_div_tooltip_id = lec_div_tooltip.id

            #if lec_div_tooltip_id is not None and lec_div_tooltip_id != '':
            #    driver.execute_script('document.getElementById('+str(lec_div_tooltip_id)+').remove();')

            lec_name = lec_id.find_element_by_xpath(".//a").text
            print("   " + lec_name)

            new_folder_name = block_name + '/' + lec_name

            new_path = create_folders(new_folder_name)

            if check_folder_finished(new_path):
                lectures_list.append((lec_a, 1))
            else:
                lectures_list.append((lec_a, 0))

            try:
                lec_a.click()
                wait()
            except:
                try:
                    y = lec_a.getLocation().y
                except:
                    y = 0
                driver.execute_script("window.scrollTo(0," + str(y) + ")");
                driver.find_element(By.LINK_TEXT, lec_name).click()

            wait()
            save_images(driver,new_path)

    driver.close()


if __name__ == "__main__":
    # execute only if run as a script
    main()
