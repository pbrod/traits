from traits.api import HasTraits, Tuple


class Test(HasTraits):
    var = Tuple(1, 2, 3)


obj = Test()
obj.var = "5"  # {ERR}
obj.var = 5  # {ERR}

obj.var = False  # {ERR}
obj.var = 5.5  # {ERR}

obj.var = 5 + 4j  # {ERR}
obj.var = True  # {ERR}

obj.var = (True,)