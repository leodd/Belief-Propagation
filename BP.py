from itertools import product


class BP:
    # loopy belief propagation

    def __init__(self, g=None, max_prod=False):
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
                res = max(f.potential.get(x) * m, res)
            else:
                res += f.potential.get(x) * m

        return res

    @staticmethod
    def normalize_message(message):
        z = 0
        for k, v in message.items():
            z = z + v
        for k, v in message.items():
            message[k] = v / z

    def belief(self, x, rv):
        b = 1
        for nb in rv.nb:
            b *= self.message[(nb, rv)][x]
        return b

    def map(self, rv):
        return max(self.points[rv], key=lambda x: self.belief(x, rv))

    def run(self, iteration=10):
        self.points = self.init_points()
        self.message = dict()

        # init message
        for f in self.g.factors:
            for rv in f.nb:
                m = {k: 1 for k in self.points[rv]}
                self.message[(f, rv)] = m
                self.message[(rv, f)] = m

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
