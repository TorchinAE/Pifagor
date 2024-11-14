from collections import defaultdict

# Создаем словарь с значением по умолчанию 0
default_dict = defaultdict(int)

# Пример добавления значений
default_dict['яблоко'] += 1
default_dict['банан'] += 2
default_dict['яблоко'] += 1
default_dict['яблоко'] += 1
print(default_dict)
