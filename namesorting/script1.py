"""
Logic
-----

Loop through the text:
    => For loops
    => While Loops
    => List comprehensions


"""

import re

pattern = "[А-Я]+[а-я]+\s+[А-Я]+\.+[А-Я]+\."

text = input("Copy and paste text here: ")

match = re.findall(pattern, text)

print(match)

surnames = [name.split()[0] for name in match]

print(f"Unsorted => {surnames}")

surnames.sort()

print(f"Sorted => {surnames}")



#"Студент Вася вспомнил, что на своей лекции Балакшин П.В. упоминал про старшекурсников, которые будут ему помогать: Анищенко А.А. и Машина Е.А."