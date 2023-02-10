import csv
import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from doad import create_xl, create_csv


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
            # time.sleep(1)
        else:
            # если вопрос десятый, то нажимаю кнопку "Проверить ответы"
            action_button = browser.find_element(By.CSS_SELECTOR, 'input[id^=action-button]')
            value = action_button.get_attribute('value')
            print(value)
            action_button.click()
    time.sleep(1)

    watupro_quiz = browser.find_element(By.CSS_SELECTOR, 'div[id^=watupro_quiz]')
    watupro_choices_columns = watupro_quiz.find_elements(By.CSS_SELECTOR, 'div[class^=watupro-choices-columns]')

    # inc = 1
    start_number_question = [0, 1, 11, 21, 31, 41, 51, 61, 71, 81, 91, 101, 111, 121, 131, 141, 151, 161, 171, 191, 121, 131, ]

    data_list = [[f'Билет №{index}']]
    data_list_answer_question = []
    for item in watupro_choices_columns:
        # вопрос
        show_question_content = item.find_element(By.CSS_SELECTOR, 'div[class^=show-question-content]')
        watupro_num = show_question_content.find_element(By.CSS_SELECTOR, 'span[class^=watupro_num]')
        show_question_content = show_question_content.find_element(By.CSS_SELECTOR, 'strong')

        data_list.append([str(watupro_num.text), str(show_question_content.text)])
        # ответы
        show_question_choices = item.find_element(By.CSS_SELECTOR, 'div[class^=show-question-choices]')
        li = show_question_choices.find_elements(By.CSS_SELECTOR, 'li')
        for l in li:
            answer = l.find_element(By.CSS_SELECTOR, 'span[class^=answer]')
            type_answer = l.get_attribute('class')
            if type_answer == 'answer correct-answer' or type_answer == 'answer user-answer correct-answer':
                data_list.append(['X', str(answer.text)])
            else:
                data_list.append(['', str(answer.text)])

    create_xl(data_list)
    browser.close()


def generator_number_question():
    """
    Генерирует словарь для сквозной нумерации вопросов из всех билетов
    номер билета - это позиция в списке с началом нумерации вопросов
    например: Билет №3 generator_number_question[3] => 31
    """
    result = [0]
    for i in range(1, 1000, 10):
        result.append(i)
    return result


if __name__ == '__main__':
    # test_solution()
    start_number_question = generator_number_question()
    print(start_number_question)