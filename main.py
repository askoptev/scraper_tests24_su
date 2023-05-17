import csv
import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from doad import create_xl, create_csv, append_xl


def test_solution(var: int):
    """
    Парсит сайт tests24.su
    """
    list_url = {
        1: 'https://tests24.su/eb-1254-15-bilet-',
        2: 'https://tests24.su/eb-1255-15-bilet-',
        3: 'https://tests24.su/eb-1256-15-bilet-',
        4: 'https://tests24.su/eb-1257-14-bilet-',
        5: 'https://tests24.su/eb-1258-15-bilet-',
        6: 'https://tests24.su/eb-1259-15-bilet-',
        7: 'https://tests24.su/eb-1260-17-bilet-',
    }
    list_value_tickets = {
        1: 10,
        2: 10,
        3: 22,
        4: 24,
        5: 30,
        6: 39,
        7: 41,
    }
    groups = {
        1: '2_low',
        2: '2_high',
        3: '3_low',
        4: '3_high',
        5: '4_low',
        6: '4_high',
        7: '5_high',
    }
    url = list_url[var]
    all_data = []
    for j in range(1, list_value_tickets[var] + 1):
        index = j
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
        try:
            watupro_quiz = browser.find_element(By.CSS_SELECTOR, 'div[id^=watupro_quiz]')
            watupro_choices_columns = watupro_quiz.find_elements(By.CSS_SELECTOR, 'div[class^=watupro-choices-columns]')
        except Exception as er:
            print(er)
            watupro_choices_columns = browser.find_elements(By.CSS_SELECTOR, 'div[class^=watupro-choices-columns]')

        inc = 0
        start_number_question = generator_number_question()

        data_list = [[f'Билет №{index}']]
        data_list_answer_question = []
        for item in watupro_choices_columns:
            # вопрос
            show_question_content = item.find_element(By.CSS_SELECTOR, 'div[class^=show-question-content]')
            watupro_num = show_question_content.find_element(By.CSS_SELECTOR, 'span[class^=watupro_num]')
            show_question_content = show_question_content.find_element(By.CSS_SELECTOR, 'strong')

            data_list.append([str(watupro_num.text), str(show_question_content.text)])
            data_list_answer_question.append([start_number_question[index] + inc, str(show_question_content.text)])
            all_data.append([start_number_question[index] + inc, str(show_question_content.text)])
            inc += 1
            # ответы
            show_question_choices = item.find_element(By.CSS_SELECTOR, 'div[class^=show-question-choices]')
            li = show_question_choices.find_elements(By.CSS_SELECTOR, 'li')
            for l in li:
                answer = l.find_element(By.CSS_SELECTOR, 'span[class^=answer]')
                type_answer = l.get_attribute('class')
                if type_answer == 'answer correct-answer' or type_answer == 'answer user-answer correct-answer':
                    data_list.append(['X', str(answer.text)])
                    data_list_answer_question.append(['', str(answer.text)])
                    all_data.append(['', str(answer.text)])
                else:
                    data_list.append(['', str(answer.text)])

        create_xl(data_list, f'ticket_{groups[var]}_{index}')
        # create_xl(data_list_answer_question, f'{groups[var]}_{index}')
        # append_xl(data_list_answer_question, f'append')
        browser.close()
    # create_xl(all_data, f'all')


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
    choise = """
    Выберите необходимую группу:
    1. II группа до 1000В
    2. II группа до и выше 1000В   
    3. III группа до 1000В 
    4. III группа до и выше 1000В
    5. IV группа до 1000В 
    6. IV группа до и выше 1000В
    7. V группа до и выше 1000В    
    """
    print(choise)
    var = input()
    var = int(var)
    test_solution(var=var)
