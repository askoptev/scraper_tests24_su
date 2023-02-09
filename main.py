import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def test_solution():
    url = 'https://tests24.su/eb-1260-16-bilet-'
    index = 1
    browser = webdriver.Chrome()
    path = f'{url}{index}//'
    browser.get(path)

    for i in range(1, 11):
        # последовательно забираю вопросы и нажимаю чек-бокс первого варианта ответа
        question = browser.find_element(By.CSS_SELECTOR, f'div[id^=question-{i}')
        print(f'[{i}]')
        print(question.text)
        block_questions = question.find_element(By.CSS_SELECTOR, 'div[class^=question-choices]')
        block_questions.find_element(By.CSS_SELECTOR, 'input').click()
        if i != 10:
            # если вопрос не десятый, то нажимаю кнопку "Следующий"
            next_question = browser.find_element(By.CSS_SELECTOR, 'div[id^=next-question]')
            button = next_question.find_element(By.CSS_SELECTOR, 'input')
            value = button.get_attribute('value')
            print(value)
            button.click()
            time.sleep(1)
        else:
            # если вопрос десятый, то нажимаю кнопку "Проверить ответы"
            action_button = browser.find_element(By.CSS_SELECTOR, 'input[id^=action-button]')
            value = action_button.get_attribute('value')
            print(value)
            action_button.click()
        # time.sleep(5)

    watupro_choices_columns = browser.find_elements(By.CSS_SELECTOR, 'div[class^=watupro-choices-columns]')
    for column in watupro_choices_columns:
        print(column.text)

    time.sleep(10)

    browser.close()


if __name__ == '__main__':
    test_solution()
