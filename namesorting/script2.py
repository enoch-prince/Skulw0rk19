import re

questions = []


# with open('RomeoAndJuliet.txt') as f:
#     text = f.read()


# sentences = re.split(r' *[\.\?!][\'"\)\]]* *', text)



with open('RomeoAndJuliet.txt') as f:
    for line in f:
        if '?' in line and len(line.split()) < 6: # checks for questions with the word limit
            questions.append(line.strip()) # line.strip() removes trailing space before and after the question

print(questions)


    