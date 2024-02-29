from PseudoRandom import PseudoRandom

if __name__ == "__main__":
    # rnd = PseudoRandom(315534645654)
    # print(len(rnd.middle_square(1000)))
    # print(rnd.linear_congruential(10, 3, 5, 19))
    # print(rnd.quadratic_congruential(10, 3, 5, 7, 19))
    x = '12345'
    xi = '1234567890'
    left = len(x) // 2
    if len(x) % 2 != 0:
        xi = '0' + xi
        left = left + 1
    right = left + len(x)
    print(xi[left:right], xi[:left], xi[right:])
