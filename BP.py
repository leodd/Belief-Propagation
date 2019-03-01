from itertools import product
from math import log, e


class BP:
    # loopy belief propagation

    def __init__(self, g, max_prod=False):
        self.g = g
        self.message = dict()
        self.points = dict()
        self.max_prod = max_prod

    def init_points(self):
        points = dict()
        for rv in self.g.rvs:
            if rv.value is None:
                points[rv] = rv.domain.values
            else:
                points[rv] = (rv.value,)
        return points

    def message_rv_to_f(self, x, rv, f):
        if rv.value is None:
            res = 1
            for nb in rv.nb:
                if nb != f:
                    res *= self.message[(nb, rv)][x]
            return res
        else:
            return 1

    def message_f_to_rv(self, x, f, rv, max_prod=False):
        res = 0
        param = []

        for nb in f.nb:
            if nb == rv:
                param.append((x,))
            else:
                param.append(self.points[nb])

        for joint_x in product(*param):
            m = 1
            for i, rv_ in enumerate(f.nb):
                if rv_ != rv:
                    m *= self.message[(rv_, f)][joint_x[i]]
            if max_prod:
                res = max(f.potential.get(joint_x) * m, res)
            else:
                res += f.potential.get(joint_x) * m

        return res

    @staticmethod
    def normalize_message(message):
        z = 0
        for k, v in message.items():
            z = z + v
        if z == 0:
            return
        for k, v in message.items():
            message[k] = v / z

    def belief(self, x, rv):
        b = 1
        for nb in rv.nb:
            b *= self.message[(nb, rv)][x]
        return b

    def factor_belief(self, x, f):
        b = f.potential.get(x)
        for i, nb in enumerate(f.nb):
            b *= self.message_rv_to_f(x[i], nb, f)
        return b

    def map(self, rv):
        return max(self.points[rv], key=lambda x: self.belief(x, rv))

    def prob(self, rv):
        p = dict()
        for x in self.points[rv]:
            p[x] = self.belief(x, rv)
        self.normalize_message(p)
        return p

    def factor_prob(self, f):
        p = dict()
        param = tuple(map(lambda rv: self.points[rv], f.nb))
        for x in product(*param):
            p[x] = self.factor_belief(x, f)
        self.normalize_message(p)
        return p

    def partition(self):
        z = 0

        rvs_p = dict()
        for rv in self.g.rvs:
            rvs_p[rv] = self.prob(rv)

        for f in self.g.factors:
            param = tuple(map(lambda rv: self.points[rv], f.nb))
            f_p = self.factor_prob(f)
            for joint_x in product(*param):
                b = 1
                for i, nb in enumerate(f.nb):
                    b *= rvs_p[nb][joint_x[i]]
                f_b = f_p[joint_x]
                if f_b != 0:
                    z += f_b * log(f.potential.get(joint_x) * b / f_b)

        for rv in self.g.rvs:
            for x in self.points[rv]:
                b = rvs_p[rv][x]
                z -= b * log(b)

        return e ** z

    def run(self, iteration=10):
        self.points = self.init_points()
        self.message = dict()

        # init message
        for f in self.g.factors:
            for rv in f.nb:
                m = {k: 1 for k in self.points[rv]}
                self.message[(f, rv)] = m

        # BP iteration
        for i in range(iteration):
            # message from rv to f
            for rv in self.g.rvs:
                for f in rv.nb:
                    m = dict()
                    for x in self.points[rv]:
                        m[x] = self.message_rv_to_f(x, rv, f)
                    self.normalize_message(m)
                    self.message[(rv, f)] = m

            # message from f to rv
            for f in self.g.factors:
                for rv in f.nb:
                    m = dict()
                    for x in self.points[rv]:
                        m[x] = self.message_f_to_rv(x, f, rv, max_prod=self.max_prod)
                    self.normalize_message(m)
                    self.message[(f, rv)] = m
