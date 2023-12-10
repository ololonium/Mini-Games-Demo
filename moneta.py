# Бросок монеты
# Подбрасывает монету 100 раз и сообщает сколько раз выпал орел\решка
import random
max_tries = int(input('Введите количество бросков: '))
side1 = 0
side2 = 0
tries = 1

while tries <= max_tries:
    x = random.randint(1, 2)
    if x == 1:
        side1 += 1
        print('Орёл!')
    elif x == 2:
        side2 += 1
        print('Решка!')
    tries += 1
print('Орёл выпал ', side1, 'раз(-а).', 'Решка выпала ', side2, 'раз(-а).')
input('\n\nНажмите Enter, чтобы выйти.')
