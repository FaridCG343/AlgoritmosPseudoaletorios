from __future__ import annotations


class PseudoRandom:
    def __init__(self, seed):
        self.seed = seed

    def middle_square(self, quantity) -> list:
        # Seed must have at least 4 digits otherwise it will raise an exception
        if len(str(self.seed)) < 4:
            raise Exception("Seed must have at least 4 digits")
        # Quantity must be greater than 0 otherwise it will raise an exception
        if quantity < 1:
            raise Exception("Quantity must be greater than 0")
        list_generated = self.__middle_square(quantity)
        return list_generated

    def __middle_square(self, quantity) -> list:
        list_generated = []
        xi = self.seed  # Set the seed
        for i in range(quantity):
            xi = xi ** 2  # Square the seed
            # if the len of the seed is odd then add a zero to the left (2n + 1) else (2n)
            xi = str(xi).zfill(len(str(self.seed)) * 2)  # Fill with zeros to match the seed length
            left = len(str(self.seed)) // 2  # Get the left side of the string
            if len(str(self.seed)) % 2 != 0:
                xi = "0" + xi
                left = left + 1
            right = left + len(str(self.seed))  # Get the right side of the string
            xi = xi[left:right]  # Get the middle of the string
            xi = int(xi)  # Convert to integer
            if xi in list_generated:  # If the number is already in the list, return the list
                return list_generated
            list_generated.append(xi)  # Append the number to the list
        return list_generated

    def linear_congruential(self, quantity, a, c, m) -> list:
        if quantity < 1:
            raise Exception("Quantity must be greater than 0")
        list_generated = self.__linear_congruential(quantity, self.seed, a, c, m)
        return list_generated

    def __linear_congruential(self, quantity, xi, a, c, m, i=0, list_generated=None) -> list:
        if list_generated is None:
            list_generated = []
        if i == quantity:
            return list_generated
        xi = (a * xi + c) % m
        if xi in list_generated:
            return list_generated
        list_generated.append(xi)
        return self.__linear_congruential(quantity, xi, a, c, m, i + 1, list_generated)

    def quadratic_congruential(self, quantity, a, b, c, m) -> list:
        if quantity < 1:
            raise Exception("Quantity must be greater than 0")
        list_generated = self.__quadratic_congruential(quantity, self.seed, a, b, c, m)
        return list_generated

    def __quadratic_congruential(self, quantity, xi, a, b, c, m, i=0, list_generated=None) -> list:
        if list_generated is None:
            list_generated = []
        if i == quantity:
            return list_generated
        xi = (a * xi ** 2 + b * xi + c) % m
        if xi in list_generated:
            return list_generated
        list_generated.append(xi)
        return self.__quadratic_congruential(quantity, xi, a, b, c, m, i + 1, list_generated)
