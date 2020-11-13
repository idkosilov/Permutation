from random import shuffle


class Permutation:
    def __init__(self, s):
        try:
            if type(s) is str:
                self.permutation = tuple(i for i in s.replace('(', '').replace(')', '').split(' '))
            elif type(s) is tuple:
                self.permutation = s
            elif type(s) is int:
                li = [i + 1 for i in range(s)]
                shuffle(li)
                self.permutation = tuple(li)
        except ValueError:
            print("Incorrect data")

    def __str__(self):
        return str(self.permutation).replace(',', '')

    def __mul__(self, *args):
        mul = self.permutation
        for arg in args:
            if isinstance(arg, CyclicPermutation):
                mul = tuple(arg.transform_permutation().permutation[el - 1] for el in mul)
            else:
                mul = tuple(arg.permutation[el - 1] for el in mul)
        return Permutation(mul)

    def __pow__(self, other):
        k = self
        for i in range(int(other) - 1):
            k = k * self
        return k

    def decrement(self):
        k = self.transform_cyclic_permutation()
        return k.N - len(k.c_permutation)

    def sgn(self):
        if self.decrement() % 2 == 0:
            return 1
        else:
            return 0

    def transform_cyclic_permutation(self):
        li = []
        elements = []
        for i in self.permutation:
            x = i
            s = [x]
            if self.permutation[x - 1] in elements:
                continue
            else:
                while i != self.permutation[x - 1]:
                    s.append(self.permutation[x - 1])
                    x = self.permutation[x - 1]
                li.append(s)
                for element in s:
                    elements.append(element)
        return CyclicPermutation(li, len(self.permutation))


class CyclicPermutation:
    def __init__(self, *args):
        if type(args[0]) == list:
            self.c_permutation = args[0]
            self.N = args[1]
        elif type(args[0]) == str:
            k = [[j for j in i.split(' ')] for i in [i.replace('(', '') for i in args[0].split(')')][:-1]]
            n = 0
            for j in [i.replace('(', '') for i in args[0].split(')')][:-1]:
                for i in j.split(' '):
                    n = n + 1
            self.c_permutation = k
            self.N = n

    def __mul__(self, *args):
        mul = self.transform_permutation()
        for arg in args:
            if isinstance(arg, CyclicPermutation):
                mul = mul * (arg.transform_permutation())
            else:
                mul = mul * arg
        return mul.transform_cperm()

    def __pow__(self, other):
        k = self.transform_permutation()
        return (k ** other).transform_cperm()

    def decrement(self):
        return self.N - len(self.c_permutation)

    def sgn(self):
        if self.decrement() % 2 == 0:
            return 1
        else:
            return 0

    def __str__(self):
        s = ''
        for li in self.c_permutation:
            s = s + str(li).replace('[', '(').replace(']', ')').replace(',', '')
        return s

    def transform_permutation(self):
        cycles = self.c_permutation
        perm = [0] * self.N
        for cycle in cycles:
            for i in range(len(cycle)):
                perm[(cycle[i] - 1) % self.N] = cycle[(i + 1) % len(cycle)]
        return Permutation(tuple(perm))