from models.city import City


def test_is_prime():
    x, y = 0, 0
    prime_cities = City.sieve_of_eratosthenes(128)

    c = City(0, x, y, prime_cities)
    assert not c.is_prime

    c = City(1, x, y, prime_cities)
    assert not c.is_prime

    c = City(2, x, y, prime_cities)
    assert c.is_prime

    c = City(3, x, y, prime_cities)
    assert c.is_prime

    c = City(4, x, y, prime_cities)
    assert not c.is_prime

    c = City(13, x, y, prime_cities)
    assert c.is_prime

    c = City(63, x, y, prime_cities)
    assert not c.is_prime

    c = City(127, x, y, prime_cities)
    assert c.is_prime

    c = City(128, x, y, prime_cities)
    assert not c.is_prime
