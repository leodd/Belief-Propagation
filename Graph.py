from abc import ABC, abstractmethod


class Domain:
    def __init__(self, values):
        self.values = tuple(values)

    def __hash__(self):
        return hash(self.values)

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and
            self.values == other.values
        )


class Potential(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get(self, parameters):
        pass


class RV:
    def __init__(self, domain, value=None):
        self.domain = domain
        self.value = value
        self.nb = []


class F:
    def __init__(self, potential, nb=None):
        self.potential = potential
        if nb is None:
            self.nb = []
        else:
            self.nb = nb


class Graph:
    def __init__(self, rvs, factors):
        self.rvs = rvs
        self.factors = factors
        self.init_nb()

    def init_nb(self):
        for rv in self.rvs:
            rv.nb = []
        for f in self.factors:
            for rv in f.nb:
                rv.nb.append(f)
