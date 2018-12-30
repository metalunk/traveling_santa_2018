from models.city import City


def test_is_prime():
    x, y = 0, 0

    c = City(0, x, y)
    assert not c.is_prime

    c = City(1, x, y)
    assert not c.is_prime

    c = City(2, x, y)
    assert c.is_prime

    c = City(3, x, y)
    assert c.is_prime

    c = City(4, x, y)
    assert not c.is_prime

    c = City(13, x, y)
    assert c.is_prime

    c = City(63, x, y)
    assert c.is_prime

    c = City(127, x, y)
    assert c.is_prime

    c = City(128, x, y)
    assert not c.is_prime
