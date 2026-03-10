# Task 1
def caching_fibonacci():
    cache = {}

    def fibonacci(n):
        if not isinstance(n, int):
            raise TypeError("n must be an integer")

        if n < 0:
            raise ValueError("n must be >= 0")

        # base cases
        if n in (0, 1):
            return n

        # check cache
        if n in cache:
            return cache[n]

        # compute and store
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci


# Example usage
fib = caching_fibonacci()

print(fib(10))  # 55

# Task 2
import re
from typing import Callable, Generator

def generator_numbers(text: str) -> Generator[float, None, None]:

    # Регулярний вираз: шукаємо числа, оточені пробілами (або на початку/в кінці рядка)
    # \d+\.\d+ — знаходить числа з десятковою частиною
    # \b\d+\b — знаходить цілі числа
    # Використовуємо паттерн для дійсних чисел, враховуючи вимогу про відокремлення пробілами
    pattern = r'(?<=\s)\d+\.\d+(?=\s)|(?<=\s)\d+(?=\s)'
    for word in text.split():
        try:
            # Пробуємо перетворити слово на число
            yield float(word)
        except ValueError:
            # Якщо це не число (наприклад, "дохід,"), просто ігноруємо
            continue

def sum_profit(text: str, func: Callable[[str], Generator[float, None, None]]) -> float:
   
    total = 0.0
    # Ітеруємося по генератору, який повертає функція generator_numbers
    for number in func(text):
        total += number
    return total


