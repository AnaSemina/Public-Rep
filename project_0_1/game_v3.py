"""Игра Угадай число Компьютер сам загадывает и сам угадывает за менее, чем 20 попыток
"""

import numpy as np

def random_predict(number:int=1) -> int:
    """_summary_

    Args:
        number (int, optional): загаданное число. Defaults to 1.

    Returns:
        int: число попыток
    """
    count = 0
    predict = np.random.randint(1, 101)
    
    while number != predict:

      count += 1

      if len(str(number-predict)) == 2: #подбираем сначала десяток
        if number > predict:
          predict += 10
        elif number < predict:
          predict -= 10
          
      else:                         #подбираем единицы
        if number > predict:
          predict += 1
        elif number < predict:
          predict -= 1

    return(count)   

def score_game(random_predict) -> int:
    """За какое количество попыток в среднем за 1000 подходов угадывает

    Args:
        random_predict (_type_): функция угадывания

    Returns:
        int: среднее количество попыток
    """
    count_ls = []
    np.random.seed(1) #фиксируем сид для воспроизводимости
    random_array = np.random.randint(1,101,size = (1000)) #загадали список чисел
    for number in random_array:
        count_ls.append(random_predict(number))
    score = int(np.mean(count_ls))
    print(f'Ваш алгоритм угадывает число в среднем за: {score} попыток')
    return(score) 

#RUN

if __name__ == '__main__':
    score_game(random_predict)