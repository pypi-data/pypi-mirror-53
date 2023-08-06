"""
Column generators, as defined in Table-Schema specification
https://frictionlessdata.io/specs/table-schema/#types-and-formats
"""

import string
from random import Random
from typing import Optional, Tuple

import numpy as np
from dsfaker.generators.date import RandomDatetime
from dsfaker.generators.distributions import Randint, Uniform
from numpy.random import seed
from rstr import Rstr

from tsfaker import tstype
from tsfaker.exceptions import InvalidConstraint
from tsfaker.generator.foreign_key import ForeignKeyGenerator

DEFAULT_MAXIMUM_NUMBER = 10 ** 10


class AbstractColumnGenerator:
    """
    Abstract column generator.

    This class avoid a direct coupling with dsfaker library
    """

    def __init__(self, nrows: int, *args, random_seed: int = 42, **kwargs):
        self.nrows = nrows
        self.random_seed = random_seed

    def _get_1d_array(self) -> np.array:
        """
        Abstract generator of a numpy array of shape (nrows, ) - 1 dimension
        """
        raise NotImplementedError("_get_batch not implemented")

    def get_2d_array(self) -> np.array:
        """
        Generate a numpy array column of shape (nrows, 1) - 2 dimension
        """
        return np.reshape(self._get_1d_array(), (self.nrows, 1))


class Enum(AbstractColumnGenerator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enum = np.array(kwargs.get('enum'))
        self.type = kwargs.get('type')

    def _get_1d_array(self):
        seed(self.random_seed)
        random_choice = np.random.choice(self.enum, self.nrows)
        if self.type == tstype.INTEGER:
            return np.char.mod('%d', random_choice)

        return random_choice


class ForeignKey(AbstractColumnGenerator):
    def __init__(self, field: str, foreign_key_generator: ForeignKeyGenerator):
        super().__init__(foreign_key_generator.nrows)
        self.field = field
        self.foreign_key_generator = foreign_key_generator

    def _get_1d_array(self) -> np.array:
        return self.foreign_key_generator.get_column(self.field)


class Bounded(AbstractColumnGenerator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.minimum, self.maximum = manage_missing_bounds(kwargs.get('minimum'), kwargs.get('maximum'),
                                                           self.DEFAULT_MINIMUM, self.DEFAULT_MAXIMUM)


class Collection(AbstractColumnGenerator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.minLength, self.maxLength = manage_missing_bounds(kwargs.get('minLength'), kwargs.get('maxLength'),
                                                               self.DEFAULT_MIN_LENGTH, self.DEFAULT_MAX_LENGTH)
        if self.minLength < 0:
            raise InvalidConstraint('minLengh should be greater than 0')
        if self.maxLength < 1:
            raise InvalidConstraint('maxLengh should be greater than 1')


class String(Collection):
    """
    String column generator
    """
    DEFAULT_MIN_LENGTH = 0
    DEFAULT_MAX_LENGTH = 20
    DEFAULT_CHARACTERS = string.ascii_letters  # string.printable

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rstr = Rstr(Random(self.random_seed))

    def _get_single(self):
        return self.rstr.rstr(self.DEFAULT_CHARACTERS, start_range=self.minLength, end_range=self.maxLength)

    def _get_1d_array(self):
        if self.nrows == 0:
            return np.empty((0, 1), np.unicode_)
        values = [self._get_single() for _ in range(self.nrows)]
        return np.asarray(values)


class Any(String):
    """
    Any column generator
    """


class Integer(Bounded):
    """
    Integer column generator
    """
    DEFAULT_MINIMUM = -DEFAULT_MAXIMUM_NUMBER
    DEFAULT_MAXIMUM = DEFAULT_MAXIMUM_NUMBER

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _get_1d_array(self):
        # Adding 1 to maximum to include boundary in discrete range
        random_integer = Randint(self.minimum, self.maximum + 1, seed=self.random_seed).get_batch(self.nrows)
        return np.char.mod('%d', random_integer)


class Number(Bounded):
    """
    Number (float) column generator
    """
    DEFAULT_MINIMUM = -DEFAULT_MAXIMUM_NUMBER
    DEFAULT_MAXIMUM = DEFAULT_MAXIMUM_NUMBER
    DEFAULT_DECIMALS = 4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.decimals = kwargs.get('decimals', self.DEFAULT_DECIMALS)

    def _get_1d_array(self):
        column = Uniform(self.minimum, self.maximum, seed=self.random_seed).get_batch(self.nrows)
        return np.around(column, decimals=self.decimals)


class AbstractDatetime(Bounded):
    """
    Base datetime column generator
    """

    DEFAULT_MINIMUM = "1900-01-01"
    DEFAULT_MAXIMUM = "2030-01-01"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.minimum = np.datetime64(self.minimum, self.unit)
        self.maximum = np.datetime64(self.maximum, self.unit)

    def _get_1d_array(self) -> np.array:
        if self.minimum == self.maximum:
            column = np.full(self.nrows, self.minimum)
        else:
            generator = RandomDatetime(Uniform(0, 1, seed=self.random_seed),
                                       start=self.minimum,
                                       # Adding 1 to maximum to include boundary in discrete range
                                       end=self.maximum + np.timedelta64(1, self.unit),
                                       unit=self.unit)
            column = generator.get_batch(self.nrows)
        return np.datetime_as_string(column, unit=self.unit, timezone='UTC')


class Datetime(AbstractDatetime):
    """
    Datetime column generator
    """

    def __init__(self, *args, **kwargs):
        self.unit = 's'
        super().__init__(*args, **kwargs)


class Date(AbstractDatetime):
    """
    Datetime column generator
    """

    def __init__(self, *args, **kwargs):
        self.unit = 'D'
        super().__init__(*args, **kwargs)


class Yearmonth(AbstractDatetime):
    """
    Year column generator
    """

    def __init__(self, *args, **kwargs):
        self.unit = 'M'
        super().__init__(*args, **kwargs)


class Year(AbstractDatetime):
    """
    Year column generator
    """

    def __init__(self, *args, **kwargs):
        self.unit = 'Y'
        super().__init__(*args, **kwargs)


tstype_to_generator_class = {
    tstype.STRING: String,
    tstype.NUMBER: Number,
    tstype.INTEGER: Integer,
    # tstype.BOOLEAN: Boolean,
    # tstype.OBJECT: Object,
    # tstype.ARRAY: Array,
    tstype.DATE: Date,
    # tstype.TIME: Time,
    tstype.DATETIME: Datetime,
    tstype.YEAR: Year,
    tstype.YEARMONTH: Yearmonth,
    # tstype.DURATION: Duration,
    # tstype.GEOPOINT: Geopoint,
    # tstype.GEOJSON: Geojson,
    tstype.ANY: Any,
}


def manage_missing_bounds(minimum: Optional[int], maximum: Optional[int],
                          default_minimum: int, default_maximum: int) -> Tuple[int, int]:
    """ Manage missing minimum and/or maximum bounds, using default values

    :param minimum:
    :param maximum:
    :param default_minimum:
    :param default_maximum:
    :return: minimum, maximum
    """
    if minimum is None:
        if maximum is None:
            return default_minimum, default_maximum
        elif maximum < default_minimum:
            # Use maximum as minimum
            return maximum, maximum
        else:
            return default_minimum, maximum
    else:
        if maximum is None:
            if minimum > default_maximum:
                # Use minimum as maximum
                return minimum, minimum
            else:
                return minimum, default_maximum
        else:
            return minimum, maximum
