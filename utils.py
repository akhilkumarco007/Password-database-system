import random  # https://docs.python.org/3.6/library/random.html
import sqlite3  # https://docs.python.org/3.6/library/sqlite3.html
import string  # https://docs.python.org/3.6/library/string.html
import re  # https://docs.python.org/3.6/howto/regex.html
import urllib.request as url_request  # https://docs.python.org/3.6/library/urllib.request.html#module-urllib.request
import json  # https://docs.python.org/3.6/library/json.html
import os  # https://docs.python.org/3.6/library/os.html


def password_shuffler(password_list: list) -> str:
    """Shuffle the given password list and joins the password

    :param password_list: password characters
    :return: joined password
    """
    random.shuffle(password_list)
    return ''.join(ch for ch in password_list)


def generate_password(length: int, complexity: int) -> str:
    """Generate a random password with given length and complexity

    Complexity levels:
        Complexity == 1: return a password with only lowercase chars
        Complexity ==  2: Previous level plus at least 1 digit
        Complexity ==  3: Previous levels plus at least 1 uppercase char
        Complexity ==  4: Previous levels plus at least 1 punctuation char

    :param length: number of characters
    :param complexity: complexity level
    :returns: generated password
    """
    punct = string.punctuation
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    digits = string.digits
    if complexity == 1:
        if length > 0:
            password_list = [ch for ch in random.choices(lower, k=length)]
            return password_shuffler(password_list)
        else:
            raise ValueError('Length should be greater than 0 for level 1!')
    elif complexity == 2:
        if length > 1:
            password_list = random.choices(lower + digits, k=length - 2)
            password_list.append(random.choice(lower))
            password_list.append(random.choice(digits))
            return password_shuffler(password_list)
        else:
            raise ValueError('Length should be greater than 1 for level 2!')
    elif complexity == 3:
        if length > 2:
            password_list = random.choices(lower + digits +
                                           upper, k=length - 3)
            password_list.append(random.choice(lower))
            password_list.append(random.choice(digits))
            password_list.append(random.choice(upper))
            return password_shuffler(password_list)
        else:
            raise ValueError('Length should be greater than 2 for level 3!')
    elif complexity == 4:
        if length > 3:
            password_list = random.choices(lower + digits +
                                           upper + punct, k=length - 4)
            password_list.append(random.choice(lower))
            password_list.append(random.choice(digits))
            password_list.append(random.choice(upper))
            password_list.append(random.choice(punct))
            return password_shuffler(password_list)
        else:
            raise ValueError('Length should be greater than 3 for level 4!')
    else:
        raise ValueError('Complexity should be one of 1, 2, 3, 4!')


def check_password_level(password: str) -> int:
    """Return the password complexity level for a given password

    Complexity levels:
        Return complexity 1: If password has only lowercase chars
        Return complexity 2: Previous level condition and at least 1 digit
        Return complexity 3: Previous levels condition and at least 1 uppercase char
        Return complexity 4: Previous levels condition and at least 1 punctuation

    Complexity level exceptions (override previous results):
        Return complexity 2: password has length >= 8 chars and only lowercase chars
        Return complexity 3: password has length >= 8 chars and only lowercase and digits

    :param password: password
    :returns: complexity level
    """
    if password:
        for ch in password:
            if ch not in string.punctuation + \
                    string.digits + string.ascii_uppercase + \
                    string.ascii_lowercase:
                raise ValueError('Password has invalid characters')
        if not re.findall('\W', password) and \
                not re.findall('[A-Z0-9]', password) and \
                re.findall('[a-z]', password):
            if len(password) >= 8:
                return 2
            else:
                return 1
        elif not re.findall('\W', password) and \
                not re.findall('[A-Z]', password) and \
                re.findall('[0-9]', password) and \
                re.findall('[a-z]', password):
            if len(password) >= 8:
                return 3
            else:
                return 2
        elif not re.findall('\W', password) and not re.findall('_', password) and \
                re.findall('[A-Z]', password) and \
                re.findall('[0-9]', password) and \
                re.findall('[a-z]', password):
            return 3
        elif (re.findall('\W', password) or re.findall('_', password)) and \
                re.findall('[A-Z]', password) and \
                re.findall('[0-9]', password) and \
                re.findall('[a-z]', password):
            return 4
        else:
            raise ValueError('Password not in format, please check the rules!')
    else:
        raise ValueError('Password length should be greater than 0')


def retrieve_user(url: str) -> tuple:
    """Retrieve the full name and email from the given url

    :param url: web page address
    :return: full name and email
    """
    with url_request.urlopen(url) as web_page:
        data = json.loads(web_page.read().decode())
        person_info = data['results'][0]
        name_dict = person_info['name']
        email = person_info['email']
        full_name = name_dict['first'] + ' ' + name_dict['last']
    return full_name, email


def create_user(db_path: str) -> None:  # you may want to use: http://docs.python-requests.org/en/master/
    """Retrieve a random user from https://randomuser.me/api/
    and persist the user (full name and email) into the given SQLite db

    :param db_path: path of the SQLite db file (to do: sqlite3.connect(db_path))
    :return: None
    """
    full_name, email = retrieve_user('https://randomuser.me/api/')
    if not os.path.isfile(db_path):
        with sqlite3.connect(db_path) as connection:
            cursor = connection.cursor()
            cursor.execute('''CREATE TABLE person_information (id INTEGER PRIMARY KEY AUTOINCREMENT,
             full_name, email)''')
            cursor.execute("INSERT INTO person_information (full_name, email) VALUES (?, ?)",
                           (full_name, email))
            connection.commit()
    else:
        with sqlite3.connect(db_path) as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO person_information (full_name, email) VALUES (?, ?)",
                           (full_name, email))
            connection.commit()
