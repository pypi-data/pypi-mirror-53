from functools import reduce, partial
from itertools import combinations, combinations_with_replacement
from madeleine import Component
from madeleine.helpers import binom
import operator
import random


class Repeat(Component, key='repeat'):
    """
    Repeat another component N times. The amount of times a component should
    be repeated can be defined exactly using the `n` parameter, or be generated
    randomly at each generation with a `min` and `max`.
    Setting `unique` to True will ensure every item in the result is unique.
    CAUTION: Ensure that the repeated component can return enough different
    values to fill the unique constraint, or the generator will end up in an
    infinite loop.
    """

    def __init__(self,
                 repeat,
                 n=None,
                 min=0,
                 max=None,
                 unique=False,
                 separator=' ',
                 **kwargs):
        self.repeat = Component._make(repeat)
        assert (n is not None) ^ (max is not None), 'Either set `n` or `max`'
        self.n = n
        self.min = min
        self.max = max
        self.unique = unique
        self.separator = separator
        super().__init__(**kwargs)

    def resolve_references(self, references):
        self.repeat.resolve_references(references)

    @property
    def combinations(self):
        if self.n is None:
            base_combinations = self.repeat.combinations
            if self.unique:
                return sum(binom(base_combinations, k)
                           for k in range(self.min, self.max+1))
            else:
                return sum(base_combinations ** k
                           for k in range(self.min, self.max+1))
        else:
            if self.unique:
                return binom(self.repeat.combinations, self.n)
            else:
                return self.repeat.combinations ** self.n

    def generate(self):
        amount = self.n
        if amount is None:
            amount = random.randint(self.min, self.max)
        results = []
        while len(results) < amount:
            result = self.repeat.generate()
            if self.unique and result in results:
                continue
            results.append(result)
        return self.separator.join(results)


class CompoundComponent(Component, register=False):
    """
    Abstract component for all components which hold multiple child components.
    """
    items_key = None

    def __init__(self, **data):
        assert self.items_key, \
            'Missing {}.items_key attribute'.format(self.__class__.__name__)
        self.items = list(map(Component._make, data.pop(self.items_key)))
        super().__init__(**data)

    def resolve_references(self, references):
        for item in self.items:
            item.resolve_references(references)

    def serialize(self):
        data = super().serialize()
        del data['items']
        data[self.items_key] = [
            child.serialize() for child in self.items
        ]
        return data


class AllOf(CompoundComponent, key='allOf'):
    """
    Component which simply joins all of its child components.
    """
    items_key = 'allOf'

    def __init__(self, separator=' ', **data):
        self.separator = separator
        super().__init__(**data)

    @property
    def combinations(self):
        return reduce(operator.mul, map(
            operator.attrgetter('combinations'),
            self.items,
        ))

    def generate(self):
        return self.separator.join(
            filter(None, [c.generate() for c in self.items])
        )


class Pick(CompoundComponent, key='pick'):
    """
    Component which randomly picks N of its child components.
    """
    items_key = 'pick'

    def __init__(self,
                 separator=' ',
                 unique=False,
                 n=None,
                 min=0,
                 max=None,
                 **data):
        assert (n is not None) ^ (max is not None), 'Either set `n` or `max`'
        self.n = n
        self.min = min
        self.max = max
        self.unique = unique
        self.separator = separator
        super().__init__(**data)

    @property
    def combinations(self):
        child_combinations = tuple(
            map(operator.attrgetter('combinations'), self.items)
        )
        method = combinations if self.unique else combinations_with_replacement
        if self.n is None:
            pick_range = range(max(self.min, 1), self.max)
        else:
            pick_range = (self.n, )
        # There probably is a neat formula to compute the combinations
        # with(out) replacement and include the combinations of the subsequent
        # draws, knowing each item has a different number of combinations,
        # but this goes well above my understanding of Wikiversity's
        # combinatorics course.
        # For each possible amount k of picks, multiply the combinations of
        # each combination of k items with(out) remplacement.
        return sum(
            sum(map(
                partial(reduce, operator.mul),
                method(child_combinations, k),
            ))
            for k in pick_range
        ) + (self.n is None and self.min == 0)  # Add 1 if it can pick zero

    def generate(self):
        amount = self.n
        if amount is None:
            amount = random.randint(self.min, self.max)
        method = random.sample if self.unique else random.choices
        return self.separator.join(
            filter(None, [
                c.generate() for c in method(self.items, k=amount)
            ]),
        )


class OneOf(CompoundComponent, key='oneOf'):
    """
    Component which randomly picks one of its child components.
    """
    items_key = 'oneOf'

    @property
    def combinations(self):
        return sum(map(operator.attrgetter('combinations'), self.items))

    def generate(self):
        return random.choice(self.items).generate()
