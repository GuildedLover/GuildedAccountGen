import random, string
from faker import Faker 

fake = Faker()


def Email():
    EMAIL = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
    return EMAIL + "@gmail.com"

def Username(Realistic: bool):
    if not Realistic:
        Username = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))
    else:
        Username = fake.first_name_male() + str(random.randint(500, 50000))
    return Username
def Password():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))


def randomNumber():
    return random.randint(999, 999999)