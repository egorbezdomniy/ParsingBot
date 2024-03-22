import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By


def scroll(driver, scroll_time=20, first_scroll=1000, default_scroll=400):
    y = first_scroll
    for timer in range(scroll_time * 2):
        driver.execute_script("window.scrollTo(0, " + str(y) + ")")
        y += default_scroll
        time.sleep(0.5)


def more(driver, pages: int, delay=2):
    for i in range(pages):
        try:
            show_more_button = driver.find_element(By.CLASS_NAME, 'catalog-items-list__show-more')
            show_more_button.click()
            time.sleep(delay)
        except NoSuchElementException as e:
            print(f"Ошибка при попытке нажатия кнопки 'Показать больше': {e}")
            break


def parse(driver,
          needed_percent=0,
          parental_element_class='catalog-item',
          amount_element='item-price',
          bonus_amount_element='bonus-percent',
          bonus_percent_element='bonus-amount',
          name_element='item-title'
          ):
    offers = []

    elements = driver.find_elements(By.CLASS_NAME, parental_element_class)
    for element in elements:
        try:
            price = element.find_element(By.CLASS_NAME, amount_element).text
            name = element.find_element(By.CLASS_NAME, name_element).text
            url = element.find_element(By.TAG_NAME, 'a').get_attribute('href')
            bonus_percent = element.find_element(By.CLASS_NAME, bonus_amount_element).text
            bonus_amount = element.find_element(By.CLASS_NAME, bonus_percent_element).text
            bonus_percent = int(bonus_percent.removesuffix('%'))
            if bonus_percent >= needed_percent:
                offers.append({'url': url, 'name': name, 'price': price, 'bonus_percent': bonus_percent,
                               'bonus_amount': bonus_amount})
        except:
            pass

    return offers
