import random
import string


def generate_random_word(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

# Generar un número aleatorio
def generate_random_number(start, end):
    return random.randint(start, end)
