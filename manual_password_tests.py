from utils import generate_password, check_password_level


def test_functions() -> None:
    """test the generate_password and
     check_password_level functions to print success or fail.

    :return: None
    """
    password_level1 = generate_password(5, 1)
    password_level2 = generate_password(5, 2)
    password_level3 = generate_password(5, 3)
    password_level4 = generate_password(5, 4)
    exception_level1 = generate_password(9, 1)
    exception_level2 = generate_password(9, 2)
    try:
        assert check_password_level(password_level1) == 1
        assert check_password_level(password_level2) == 2
        assert check_password_level(password_level3) == 3
        assert check_password_level(password_level4) == 4
        assert check_password_level(exception_level1) == 2
        assert check_password_level(exception_level2) == 3
        print('success')
    except AssertionError:
        print('fail')


if __name__ == '__main__':
    test_functions()
