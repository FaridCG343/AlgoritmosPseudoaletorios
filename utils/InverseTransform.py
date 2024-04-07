import math


class InverseTransform:
    def __init__(self, data: list):
        if len(data) < 1:
            raise Exception("La cantidad de datos debe ser mayor a 0.")
        self.data = data

    def uniform(self, a: float, b: float):
        if a > b:
            raise Exception("El valor de a debe ser menor a b.")
        formula = lambda x: a + (b - a) * x
        return [{"i": i, "F-1(Xi)": formula(x), "Xi": x} for i, x in enumerate(self.data)]

    def exponential(self, lambd: float):
        if lambd <= 0:
            raise Exception("El valor de lambda debe ser mayor a 0.")
        formula = lambda x: -1 * (1 / lambd) * math.log(1 - x)
        return [{"i": i, "F-1(Xi)": formula(x), "Xi": x} for i, x in enumerate(self.data)]
