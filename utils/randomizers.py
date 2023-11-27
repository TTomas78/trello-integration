import random
import string


def generate_random_word(length):
    """
    Generate a random string of fixed length
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def generate_random_number(start, end):
    """
    Generate a random number between start and end
    """
    return random.randint(start, end)
