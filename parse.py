from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


# Функция для формирования URL на основе бренда, модели и года
def get_avito_url(brand, model, year):
    urls = {
        ('Toyota', 'Corolla',
         '2006'): 'https://www.avito.ru/samara/avtomobili/toyota/corolla/ix_restayling-ASgBAgICA0Tgtg20mSjitg2woijqtg389Sg?cd=1&radius=0&searchRadius=0',
        ('Toyota', 'Corolla',
         '2020'): 'https://www.avito.ru/samara/avtomobili/toyota/corolla/xii-ASgBAgICA0Tgtg20mSjitg2woijqtg2k8TE?cd=1&radius=0&searchRadius=0',
        ('Toyota', 'Camry',
         '2006'): 'https://www.avito.ru/samara/avtomobili/toyota/camry/xv30-ASgBAgICA0Tgtg20mSjitg3UoCjqtg229Sg?cd=1&radius=0&searchRadius=0',
        ('Toyota', 'Camry',
         '2020'): 'https://www.avito.ru/samara/avtomobili/toyota/camry/xv70_restayling-ASgBAgICA0Tgtg20mSjitg3UoCjqtg2sr1s?cd=1&radius=0&searchRadius=0',
        ('Toyota', 'Land Cruiser Prado',
         '2006'): 'https://www.avito.ru/samara/avtomobili/toyota/land_cruiser_prado/120_restayling-ASgBAgICA0Tgtg20mSjitg34qCjqtg3K9yg?cd=1&radius=0&searchRadius=0',
        ('Toyota', 'Land Cruiser Prado',
         '2020'): 'https://www.avito.ru/samara/avtomobili/toyota/land_cruiser_prado/150_restayling_2-ASgBAgICA0Tgtg20mSjitg34qCjqtg2W~yg?cd=1&radius=0&searchRadius=0',
        ('Toyota', 'Land Cruiser',
         '2006'): 'https://www.avito.ru/samara/avtomobili/toyota/land_cruiser/100_restayling_2-ASgBAgICA0Tgtg20mSjitg32qCjqtg2~9yg?cd=1&radius=0&searchRadius=0',
        ('Toyota', 'Land Cruiser',
         '2020'): 'https://www.avito.ru/samara/avtomobili/toyota/land_cruiser/200_restayling_2-ASgBAgICA0Tgtg20mSjitg32qCjqtg3q~Sg?cd=1&radius=0&searchRadius=0'
    }

    return urls.get((brand, model, year), None)


# Функция парсинга цен
def scrape_item_prices(url):
    if not url:
        print("URL не найден")
        return 0

    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)
        print("Страница загружена")

        item_prices = []
        while len(item_prices) < 5:  # Изменим условие для сбора 5 цен
            try:
                prices = driver.find_elements(By.CLASS_NAME, 'iva-item-priceStep-uq2CQ')
                for price in prices:
                    price_text = price.text.strip()
                    if price_text and price_text.startswith('от'):
                        continue
                    price_value = int(''.join(filter(str.isdigit, price_text)))
                    item_prices.append(price_value)
                    if len(item_prices) >= 5:  # Собрали 5 цен
                        break
            except Exception:
                print("Нужно решить капчу")
                input("Нажмите Enter после решения капчи")

        avg_price = sum(item_prices) / len(item_prices)  # Рассчитываем среднюю цену
        print(f"Средняя цена: {avg_price}")
        return avg_price

    finally:
        driver.quit()
