#!python3
#distutils: language = c++


__all__ = (
    "RandomValue", "TruffleShuffle", "QuantumMonty", "FlexCat",
    "CumulativeWeightedChoice", "RelativeWeightedChoice",
    "random_value", "cumulative_weighted_choice",
    "canonical", "random_float", "triangular",
    "random_below", "random_int", "random_range", "d", "dice", "ability_dice",
    "percent_true", "plus_or_minus", "plus_or_minus_linear", "plus_or_minus_gauss",
    "ZeroCool", "random_index", "quantum_monty",
    "front_gauss", "middle_gauss", "back_gauss", "quantum_gauss",
    "front_poisson", "middle_poisson", "back_poisson", "quantum_poisson",
    "front_linear", "middle_linear", "back_linear", "quantum_linear",
    "shuffle", "smart_clamp", "flatten",
)


cdef extern from "Storm.hpp":
    int           _percent_true           "Storm::percent_true"(double)
    double        _canonical              "Storm::canonical_variate"()
    double        _random_float           "Storm::uniform_real_variate"(double, double)
    double        _triangular             "Storm::triangular_variate"(double, double, double)
    long long     _random_below           "Storm::random_below"(long long)
    long long     _random_int             "Storm::uniform_int_variate"(long long, long long)
    long long     _random_range           "Storm::random_range"(long long, long long, long long)
    long long     _d                      "Storm::d"(long long)
    long long     _dice                   "Storm::dice"(long long, long long)
    long long     _ability_dice           "Storm::ability_dice"(long long)
    long long     _plus_or_minus          "Storm::plus_or_minus"(long long)
    long long     _plus_or_minus_linear   "Storm::plus_or_minus_linear"(long long)
    long long     _plus_or_minus_gauss    "Storm::plus_or_minus_gauss"(long long)
    long long     _random_index           "Storm::random_index"(long long)
    long long     _front_gauss            "Storm::front_gauss"(long long)
    long long     _middle_gauss           "Storm::middle_gauss"(long long)
    long long     _back_gauss             "Storm::back_gauss"(long long)
    long long     _quantum_gauss          "Storm::quantum_gauss"(long long)
    long long     _front_poisson          "Storm::front_poisson"(long long)
    long long     _middle_poisson         "Storm::middle_poisson"(long long)
    long long     _back_poisson           "Storm::back_poisson"(long long)
    long long     _quantum_poisson        "Storm::quantum_poisson"(long long)
    long long     _front_linear           "Storm::front_linear"(long long)
    long long     _middle_linear          "Storm::middle_linear"(long long)
    long long     _back_linear            "Storm::back_linear"(long long)
    long long     _quantum_linear         "Storm::quantum_linear"(long long)
    long long     _quantum_monty          "Storm::quantum_monty"(long long)
    long long     _smart_clamp            "Storm::GearBox::smart_clamp"(long long, long long, long long)


# Random Integer #
def random_below(number: int):
    """
    Returns a random integer in the range [0, number), or (number, 0] for negative numbers.
    Always returns 0 for input 0.
    Flat uniform distribution.
    """
    return _random_below(number)

def random_index(limit: int):
    """
    Canonical ZeroCool method.
    Returns a random integer in the range [0, number), or [number, 0) for negative numbers.
    Always returns 0 when limit is 0.
    This symmetry matches how python can index a list from the back for negative values or the front for positive values.
    Flat uniform distribution.
    """
    return _random_index(limit)

def random_int(left_limit: int, right_limit: int):
    """
    Returns a random integer in the range [left_limit, right_limit].
    Flat uniform distribution.
    """
    return _random_int(left_limit, right_limit)

def random_range(start: int, stop: int = 0, step: int = 1):
    """
    A = min(start, stop), B = max(start, stop), C = step
    Returns a random integer in the range [A, B) by increments of C.
    The sign of the step parameter controls the phase of the output.
    Negative stepping will flip the inclusively to (A, B] by C.
    Empty ranges will always return the start argument.
    When passed only one argument this function behaves like random_index.
    Flat uniform distribution.
    """
    return _random_range(start, stop, step)

def d(sides: int = 20):
    """
    Represents a single roll of a given die, d20 by default.
    The size of the die is equal to the number of sides.
    Flat uniform distribution.
    """
    return _d(sides)

def dice(rolls: int = 1, sides: int = 20):
    """
    Represents the sum of multiple rolls of the same size die.
    Geometric distribution based on the number and size of the dice rolled.
    """
    return _dice(rolls, sides)

def ability_dice(rolls: int = 4):
    """
    @parm rolls :: Number of d6 rolls. Default is 4. Clamped in range [3, 9].
    @return :: Returns the sum of the top 3 of N d(6) where N = rolls input.
    """
    return _ability_dice(rolls)

def plus_or_minus(number: int = 1):
    """ Returns a random integer in range [-number, number].
    Flat uniform distribution. """
    return _plus_or_minus(number)

def plus_or_minus_linear(number: int = 1):
    """ Returns a random integer in range [-number, number].
    Linear geometric distribution, centered on zero. """
    return _plus_or_minus_linear(number)

def plus_or_minus_gauss(number: int = 1):
    """ Returns a random integer in range [-number, number].
    Scaled gaussian distribution, centered on zero. """
    return _plus_or_minus_gauss(number)


# Random Bool #
def percent_true(truth_factor: float = 50.0) -> bool:
    """ Produces True or False based on the truth_factor, the probability of True as a percentage. """
    return _percent_true(truth_factor) == 1


# Random Floats #
def canonical() -> float:
    """ Returns a random float in range [0.0, 1.0). Inclusiveness can vary across platforms.
    Flat uniform distribution. """
    return _canonical()

def random_float(left_limit: float = 0.0, right_limit: float = 1.0) -> float:
    """ Returns a random float in range [left_limit, right_limit). Inclusiveness can vary across platforms.
    Flat uniform distribution. """
    return _random_float(left_limit, right_limit)

def triangular(low: float, high: float, mode: float) -> float:
    """ Returns a random float in range [low, high] with a linear distribution about the mode. """
    return _triangular(low, high, mode)


# Utilities #
def smart_clamp(target: int, lo: int, hi: int) -> int:
    """
    Originally intended for internal use only.

    Essentially the same as median but considerably faster.
    @return :: Returns the middle value of three integer arguments, input order does not matter.
    """
    return _smart_clamp(target, lo, hi)

def flatten(maybe_callable: object, *args, flat: bool = True, **kwargs):
    """
    Originally intended for internal use only.

    Recursively calls the input object and returns the result.
    The arguments are only passed in on the first evaluation.
    If the object is not callable it is simply returned without error.
    Essentially this is the opposite of bind, and it's recursive.
    Conceptually this is somewhat like collapsing the wave function.
    Often flatten is used as the last step in lazy evaluation.
    @param maybe_callable :: Any Object that might be callable.
    @param flat :: Boolean, default is True. Optional, keyword only.
        Disables flattening if flat is set to False, conceptually turns flatten into the identity function.
    @param *args, **kwargs :: Optional arguments used to flatten the maybe_callable object.
    @return :: Recursively Flattened Object.
    """
    if flat is False or not callable(maybe_callable):
        return maybe_callable
    else:
        try:
            return flatten(maybe_callable(*args, **kwargs))
        except TypeError:
            return maybe_callable


# Shuffle #
def shuffle(array: list):
    """
    Knuth B shuffle algorithm.
    Reverse Order Random Swap Backwards == Cache friendly!
    Destructive, in-place shuffle.
    @param array :: List of values.
    @return :: None
    """
    size = len(array) - 1
    for i in reversed(range(size)):
        j = _random_int(i, size)
        array[i], array[j] = array[j], array[i]


# ZeroCool #
def front_gauss(size: int):
    """ Gamma Index Distribution: Front Peak. """
    return _front_gauss(size)

def middle_gauss(size: int):
    """ Gaussian Index Distribution: Middle Peak. """
    return _middle_gauss(size)

def back_gauss(size: int):
    """ Gamma Index Distribution: Back Peak. """
    return _back_gauss(size)

def quantum_gauss(size: int):
    """ Quantum Gaussian Index Distribution: Three-way Monty. """
    return _quantum_gauss(size)

def front_poisson(size: int):
    """ Poisson Index Distribution: Front 1/3 Peak. """
    return _front_poisson(size)

def middle_poisson(size: int):
    """ Symmetric Poisson Index Distribution. """
    return _middle_poisson(size)

def back_poisson(size: int):
    """ Poisson Index Distribution: Back 1/3 Peak. """
    return _back_poisson(size)

def quantum_poisson(size: int):
    """ Quantum Poisson Index Distribution: Three-way Monty. Twin Peaks """
    return _quantum_poisson(size)

def front_linear(size: int):
    """ Linear Geometric Index Distribution: 45 Degree Front Peak. Left Triangle """
    return _front_linear(size)

def middle_linear(size: int):
    """ Linear Geometric Index Distribution: 45 Degree Middle Peak. Pyramid """
    return _middle_linear(size)

def back_linear(size: int):
    """ Linear Geometric Index Distribution: 45 Degree Back Peak. Right Triangle """
    return _back_linear(size)

def quantum_linear(size: int):
    """ Quantum Geometric Index Distribution: Three-way Monty. Saw tooth """
    return _quantum_linear(size)

def quantum_monty(size: int):
    """ Quantum Monty Index Distribution: Nine-way Monty. Quantum wave. """
    return _quantum_monty(size)


# ZeroCool Collection #
ZeroCool = {
    "random_index": random_index,
    "front_linear": front_linear,
    "middle_linear": middle_linear,
    "back_linear": back_linear,
    "quantum_linear": quantum_linear,
    "front_gauss": front_gauss,
    "middle_gauss": middle_gauss,
    "back_gauss": back_gauss,
    "quantum_gauss": quantum_gauss,
    "front_poisson": front_poisson,
    "middle_poisson": middle_poisson,
    "back_poisson": back_poisson,
    "quantum_poisson": quantum_poisson,
    "quantum_monty": quantum_monty,
}


# Fortuna Generator Functions #
def random_value(data):
    """ Equivalent to Random.choice. Flat uniform distribution.
    Also see RandomValue class for additional options.
    The function is measurably faster than the class, but the class offers far more flexibility. """
    return data[_random_index(len(data))]

def cumulative_weighted_choice(weighted_table):
    """ Similar to Random.choices with cumulative weights zipped with the corresponding values.
    Also see CumulativeWeightedChoice and RelativeWeightedChoice.
    The function is measurably faster than the classes, but the classes offer far more flexibility. """
    max_weight = weighted_table[-1][0]
    rand = _random_index(max_weight)
    for weight, value in weighted_table:
        if weight > rand:
            return value


# Fortuna Generator Classes #
class RandomValue:
    """
    @param collection :: Collection of Values.
    @param flat :: Bool. Default: True. Option to automatically flatten callable values with lazy evaluation.
    @return :: Callable Object. `Callable(*args, zero_cool=random_index, range_to=0, **kwargs) -> Value`
        @param zero_cool :: Optional ZeroCool Method, kwarg only. Default = random_index().
        @param range_to :: Optional Integer in range [-N, N] where N is the length of the Collection.
            Default = 0, kwarg only. Parameter for ZeroCool Method. `range_to=0` indicates the intent to use the whole collection.
            Negative values of range_to indicate ranging from the back of the Collection.
        @param *args, **kwargs :: Optional arguments used to flatten the return Value if Callable.
        @return Value or Value(*args, **kwargs) if Callable.

    Please refer to https://pypi.org/project/Fortuna/ for full documentation with examples.
    """
    __slots__ = ("data", "size", "flat")

    def __init__(self, collection, *, flat=True):
        self.data = tuple(collection)
        self.size = len(self.data)
        self.flat = flat
        assert self.size > 0, "Input Error, Empty Container"

    def __call__(self, *args, zero_cool: staticmethod = _random_index, range_to: int = 0, **kwargs):
        return flatten(self.data[zero_cool(range_to or self.size)], *args, flat=self.flat, **kwargs)

    def __str__(self):
        output = (
            "RandomValue(collection",
            "" if self.flat else ", flat=False",
            ")",
        )
        return "".join(output)


class TruffleShuffle:
    """
    @param collection :: Collection of Values. Any list-like object, a Set is recommended but not required.
    @param flat :: Bool. Default: True. Option to automatically flatten callable values with lazy evaluation.
    @return :: Callable Object. `Callable(*args, **kwargs) -> Value`
        @param *args, **kwargs :: Optional arguments used to flatten the return Value (below) if Callable.
        @return :: Value or Value(*args, **kwargs) if Callable.
        Random value from the collection with a Wide Uniform Distribution.

    Wide Uniform Distribution: "Wide" refers to the average distance between consecutive occurrences of the same value.
    The average width of the output distribution will naturally scale up with the size of the collection.
    The goal of this type of distribution is to keep the output sequence free of clumps or streaks of the same value,
    while maintaining randomness and uniform probability. This is not the same as a flat uniform distribution.
    The two distributions over time will be statistically similar for any given set,
    but the repetitiveness of the output sequence will be very different.

    Please refer to https://pypi.org/project/Fortuna/ for full documentation with examples.
    """
    __slots__ = ("flat", "data")

    def __init__(self, collection, flat=True):
        self.flat = flat
        self.data = list(collection)
        assert len(self.data) > 0, "Input Error, Empty Container"
        shuffle(self.data)

    def __call__(self, *args, **kwargs):
        result = self.data.pop()
        self.data.insert(_front_poisson(len(self.data) - 1), result)
        return flatten(result, *args, flat=self.flat, **kwargs)

    def __str__(self):
        output = (
            "TruffleShuffle(collection",
            "" if self.flat else ", flat=False",
            ")",
        )
        return "".join(output)


class QuantumMonty:
    """
    @param collection :: Collection of Values.
    @param flat :: Bool. Default is True. Option to automatically flatten callable values with lazy evaluation.
    @return :: Callable Object with Monty Methods for producing various distributions of the collection.
        @param *args, **kwargs :: Optional arguments used to flatten the return Value (below) if Callable.
        @return :: Random value from the collection.

    Please refer to https://pypi.org/project/Fortuna/ for full documentation with examples.
    """
    __slots__ = ("flat", "size", "data", "truffle_shuffle")

    def __init__(self, collection, flat=True):
        self.flat = flat
        self.data = tuple(collection)
        self.size = len(self.data)
        assert self.size > 0, "Input Error, Empty Container"
        self.truffle_shuffle = TruffleShuffle(self.data, flat)

    def __call__(self, *args, **kwargs):
        return self.quantum_monty(*args, **kwargs)

    def dispatch(self, monty):
        """ Internal dispatch method. Prefer to use the methods by name if possible. """
        return {
            "flat_uniform": self.flat_uniform,
            "truffle_shuffle": self.truffle_shuffle,
            "front_linear": self.front_linear,
            "middle_linear": self.middle_linear,
            "back_linear": self.back_linear,
            "quantum_linear": self.quantum_linear,
            "front_gauss": self.front_gauss,
            "middle_gauss": self.middle_gauss,
            "back_gauss": self.back_gauss,
            "quantum_gauss": self.quantum_gauss,
            "front_poisson": self.front_poisson,
            "middle_poisson": self.middle_poisson,
            "back_poisson": self.back_poisson,
            "quantum_poisson": self.quantum_poisson,
            "quantum_monty": self.quantum_monty,
        }[monty]

    def flat_uniform(self, *args, **kwargs):
        return flatten(self.data[_random_index(self.size)], *args, flat=self.flat, **kwargs)

    def front_linear(self, *args, **kwargs):
        return flatten(self.data[_front_linear(self.size)], *args, flat=self.flat, **kwargs)

    def middle_linear(self, *args, **kwargs):
        return flatten(self.data[_middle_linear(self.size)], *args, flat=self.flat, **kwargs)

    def back_linear(self, *args, **kwargs):
        return flatten(self.data[_back_linear(self.size)], *args, flat=self.flat, **kwargs)

    def quantum_linear(self, *args, **kwargs):
        return flatten(self.data[_quantum_linear(self.size)], *args, flat=self.flat, **kwargs)

    def front_gauss(self, *args, **kwargs):
        return flatten(self.data[_front_gauss(self.size)], *args, flat=self.flat, **kwargs)

    def middle_gauss(self, *args, **kwargs):
        return flatten(self.data[_middle_gauss(self.size)], *args, flat=self.flat, **kwargs)

    def back_gauss(self, *args, **kwargs):
        return flatten(self.data[_back_gauss(self.size)], *args, flat=self.flat, **kwargs)

    def quantum_gauss(self, *args, **kwargs):
        return flatten(self.data[_quantum_gauss(self.size)], *args, flat=self.flat, **kwargs)

    def front_poisson(self, *args, **kwargs):
        return flatten(self.data[_front_poisson(self.size)], *args, flat=self.flat, **kwargs)

    def middle_poisson(self, *args, **kwargs):
        return flatten(self.data[_middle_poisson(self.size)], *args, flat=self.flat, **kwargs)

    def back_poisson(self, *args, **kwargs):
        return flatten(self.data[_back_poisson(self.size)], *args, flat=self.flat, **kwargs)

    def quantum_poisson(self, *args, **kwargs):
        return flatten(self.data[_quantum_poisson(self.size)], *args, flat=self.flat, **kwargs)

    def quantum_monty(self, *args, **kwargs):
        return flatten(self.data[_quantum_monty(self.size)], *args, flat=self.flat, **kwargs)

    def __str__(self):
        output = (
            "QuantumMonty(collection",
            "" if self.flat else ", flat=False",
            ")",
        )
        return "".join(output)


class FlexCat:
    """
    FlexCat is a lot like a multi dimensional QuantumMonty, or a QuantumMonty of QuantumMontys.

    The constructor takes two optional keyword arguments to specify the algorithms to be used to make random selections.
    The algorithm specified for selecting a key need not be the same as the one for selecting values.
    An optional key may be provided at call time to bypass the random key selection.
    Keys passed in this way must exactly match a key in the Matrix.

    By default, FlexCat will use key_bias="front_linear" and val_bias="truffle_shuffle",
    this will make the top of the data structure geometrically more common than the bottom and it will truffle shuffle
    the sequence values. This config is known as TopCat, it produces a descending-step, micro-shuffled distribution sequence.
    Many other combinations are available.

    Please refer to https://pypi.org/project/Fortuna/ for full documentation with examples.
    """
    __slots__ = ("random_cat", "random_selection")

    def __init__(self, matrix_data: dict, key_bias="front_linear", val_bias="truffle_shuffle", flat=True):
        """
        @param matrix_data :: Dictionary of Value Sequences.
        @parm key_bias :: Default is "front_linear". String indicating the name of the algorithm to use for random key selection.
        @parm val_bias :: Default is "truffle_shuffle". String indicating the name of the algorithm to use for random value selection.
        @param flat :: Bool. Default is True. Option to automatically flatten callable values with lazy evaluation.
        @return :: Callable Instance
        """
        self.random_cat = QuantumMonty(tuple(matrix_data.keys()), flat=False).dispatch(key_bias)
        self.random_selection = {
            key: QuantumMonty(tuple(seq), flat=flat).dispatch(val_bias) for key, seq in matrix_data.items()
        }

    def __call__(self, cat_key=None, *args, **kwargs):
        """
        @param cat_key :: Optional String. Default is None. Key selection by name.
            If specified, this will override the key_bias for a single call.
        @param *args, **kwargs :: Optional arguments used to flatten the return Value (below) if Callable.
        @return :: Value. Returns a random value generated with val_bias from a random sequence generated with key_bias.
        """
        monty = self.random_selection
        key = cat_key if cat_key is not None else self.random_cat()
        return monty[key](*args, **kwargs)

    def __str__(self):
        return "FlexCat(matrix_data, key_bias, val_bias, flat)"


class WeightedChoice:
    """
    Base Class, internal only.

    Weighted Choice offers two strategies for selecting random values from a sequence where programmable rarity is desired.
    RelativeWeightedChoice & CumulativeWeightedChoice
    Both produce a custom distribution of values based on the weights of the values.

    The choice to use one strategy over the other is purely about which one suits you or your data best.
    Relative weights are easier to understand at a glance.
    However, many RPG Treasure Tables map rather nicely to a cumulative weighted strategy.

    Please refer to https://pypi.org/project/Fortuna/ for full documentation with examples.
    """
    __slots__ = ("flat", "max_weight", "data")

    def __call__(self, *args, **kwargs):
        """
        @param *args, **kwargs :: Optional arguments used to flatten the return Value (below) if Callable.
        @return :: Random value from the weighted_table, distribution based on the weights of the values.
        """
        rand = _random_below(self.max_weight)
        for weight, value in self.data:
            if weight > rand:
                return flatten(value, *args, flat=self.flat, **kwargs)


class RelativeWeightedChoice(WeightedChoice):
    __slots__ = ("flat", "max_weight", "data")

    def __init__(self, weighted_table, flat=True):
        """
        @param weighted_table :: Table of weighted pairs. [ (w1, v1), (w2, v2), (w3, v3)... ] or zip(weights, values)
        @param flat :: Bool. Default: True. Option to automatically flatten callable values with lazy evaluation.
        @return :: Callable Instance
        """
        self.flat = flat
        optimized_data = sorted([list(itm) for itm in weighted_table], key=lambda x: x[0], reverse=True)
        cum_weight = 0
        for w_pair in optimized_data:
            cum_weight += w_pair[0]
            w_pair[0] = cum_weight
        self.max_weight = optimized_data[-1][0]
        self.data = tuple(tuple(itm) for itm in optimized_data)

    def __str__(self):
        output = (
            "RelativeWeightedChoice(weighted_table",
            "" if self.flat else ", flat=False",
            ")",
        )
        return "".join(output)


class CumulativeWeightedChoice(WeightedChoice):
    __slots__ = ("flat", "max_weight", "data")

    def __init__(self, weighted_table, flat=True):
        """
        @param weighted_table :: Table of weighted pairs.
        @param flat :: Bool. Default: True. Option to automatically flatten callable values with lazy evaluation.
        @return :: Callable Instance

        Note: Logic dictates Cumulative Weights must be unique! This is not checked.
        """
        self.flat = flat
        data = sorted([list(itm) for itm in weighted_table], key=lambda x: x[0])
        prev_weight = 0
        for w_pair in data:
            w_pair[0], prev_weight = w_pair[0] - prev_weight, w_pair[0]
        optimized_data = sorted(data, key=lambda x: x[0], reverse=True)
        cum_weight = 0
        for w_pair in optimized_data:
            cum_weight += w_pair[0]
            w_pair[0] = cum_weight
        self.max_weight = optimized_data[-1][0]
        self.data = tuple(tuple(itm) for itm in optimized_data)

    def __str__(self):
        output = (
            "CumulativeWeightedChoice(weighted_table",
            "" if self.flat else ", flat=False",
            ")",
        )
        return "".join(output)
