import pandas as pd
import matplotlib.pyplot as plt
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Инициализация браузера
driver = webdriver.Chrome()

# URL для парсинга
url = "https://www.divan.ru/sankt-peterburg/category/divany"
driver.get(url)

# Ожидание загрузки карточек товаров
WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-testid="product-card"]')))

# Список для хранения данных
parsed_data = []

# Находим карточки с товарами
sofas = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="product-card"]')

# Перебираем карточки
for sofa in sofas:
    try:
        # Название дивана
        title_element = sofa.find_element(By.CSS_SELECTOR, 'span[itemprop="name"]')
        title = title_element.text if title_element else "Не указано"

        # Текущая цена
        current_price_element = sofa.find_elements(By.CSS_SELECTOR, 'span[data-testid="price"]')
        current_price = current_price_element[1].text.replace('руб.', '').strip().replace(" ", "") if len(current_price_element) > 0 else "0"

        # Старая цена
        old_price = current_price_element[2].text.replace('руб.', '').strip().replace(" ", "") if len(current_price_element) > 1 else "0"

        # Ссылка на товар
        link_element = sofa.find_element(By.CSS_SELECTOR, 'a.ui-GPFV8')
        link = "https://www.divan.ru" + link_element.get_attribute('href') if link_element else "Не указано"

        # Вычисляем скидку
        discount = "0%"
        if old_price != "0" and current_price != "0":
            old_price = int(old_price)
            current_price = int(current_price)
            discount = f"{round((old_price - current_price) / old_price * 100)}%"

        # Добавляем данные в список
        parsed_data.append([title, int(current_price), discount, link])
        print(f"Добавлено: {title}, {current_price}, {discount}, {link}")
    except Exception as e:
        print(f"Ошибка при парсинге карточки: {e}")
        continue

# Закрываем браузер
driver.quit()

# Сохраняем данные в CSV
csv_file = "divanru.csv"
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Название дивана', 'Цена', 'Скидка %', 'Ссылка на диван'])
    writer.writerows(parsed_data)

print(f"Данные успешно сохранены в {csv_file}")

# Обработка данных
df = pd.DataFrame(parsed_data, columns=['Название дивана', 'Цена', 'Скидка %', 'Ссылка на диван'])

# Вычисляем среднюю цену
average_price = df['Цена'].mean()
print(f"Средняя цена дивана: {average_price:.2f} руб.")

# Построение гистограммы цен
plt.figure(figsize=(10, 6))
plt.hist(df['Цена'], bins=15, color='blue', alpha=0.7)
plt.title('Распределение цен на диваны')
plt.xlabel('Цена, руб.')
plt.ylabel('Количество')
plt.grid(True)
plt.savefig("price_histogram.png")
plt.show()
