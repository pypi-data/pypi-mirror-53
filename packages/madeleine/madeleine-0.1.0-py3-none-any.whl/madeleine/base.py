from abc import ABCMeta, abstractmethod, abstractproperty
from collections.abc import Mapping, Iterable
from enum import Enum
from pathlib import Path
from objtools.registry import ClassRegistry
import random


class FileFormat(Enum):
    JSON = 'json'
    YAML = 'yaml'
    TOML = 'toml'


class ComponentRegistry(ClassRegistry):

    def check_value(self, value):
        assert issubclass(value, Component)


registry = ComponentRegistry()
register = registry.register
unregister = registry.unregister


class ComponentMetaclass(registry.metaclass, ABCMeta):
    pass


class Component(metaclass=ComponentMetaclass, register=False):
    """
    Describes any generator component.
    """

    def __init__(self, **data):
        self.__dict__.update(**data)

    def resolve_references(self, references):
        """
        Complex components might hold references to other components:
        they should leave them unresolved until the Generator builds all the
        components, then calls this method with all of the referencable names.
        """

    @abstractmethod
    def generate(self):
        pass

    def serialize(self):
        """
        Should return a JSON/YAML/TOML-compatible structure which can be used
        to export a component to a file.
        """
        return self.__dict__.copy()

    @abstractproperty
    def combinations(self):
        """
        Should return how many combinations a single component may have.
        Useful to perform some checks after parsing.
        """

    def __str__(self):
        return str(self.serialize())

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(
                '{}={!r}'.format(k, v)
                for k, v in self.serialize().items()
            ),
        )

    def _repr_pretty_(self, p, cycle):
        if cycle:
            p.text('{}(...)'.format(self.__class__.__name__))
        else:
            with p.group(2, '{}('.format(self.__class__.__name__), ')'):
                p.breakable('')
                for k, v in self.serialize().items():
                    p.text(k)
                    p.text('=')
                    p.pretty(v)
                    p.text(',')
                    p.breakable()

    @classmethod
    def from_path(cls, path, fmt=FileFormat.YAML):
        assert isinstance(fmt, FileFormat)
        if not isinstance(path, Path):
            path = Path(path)
        with path.open() as f:
            if fmt == FileFormat.JSON:
                import json
                data = json.load(f)
            elif fmt == FileFormat.YAML:
                try:
                    import yaml
                except ImportError as e:
                    raise ImportError(
                        '{}\n'
                        'You may need to install madeleine with YAML support: '
                        'pip install madeleine[yaml]'.format(e.message),
                    )
                data = yaml.safe_load(f)
            elif fmt == FileFormat.TOML:
                try:
                    import toml
                except ImportError as e:
                    raise ImportError(
                        '{}\n'
                        'You may need to install madeleine with TOML support: '
                        'pip install madeleine[toml]'.format(e.message),
                    )
                data = toml.load(f)
            else:
                raise NotImplementedError

            if cls is Component:
                # Guess the component type when calling Component.from_path
                return Component._make(data)
            return cls(**data)

    @staticmethod
    def _make(data):
        """
        Guess which component subclass to use for a given component data,
        then build and return the resulting components.
        """
        if isinstance(data, str):
            data = {'value': data}
        if not isinstance(data, Mapping):
            if isinstance(data, Iterable):
                return list(map(Component._make, data))
            raise ValueError('Component description should be a mapping')

        for key, component_class in registry.items():
            if key in data:
                return component_class(**data)

        raise ValueError('Could not parse component description')


class Reference(Component, key='ref'):
    """
    A component used to temporarily hold references to other components
    during the first pass of schema loading, when not all referenced names
    are available, before a second pass allows resolution of all references.
    """
    def __init__(self, **kwargs):
        self.to = None
        super().__init__(**kwargs)

    def resolve_references(self, references):
        if self.ref not in references:
            raise ValueError('Unknown reference {!r}'.format(self.ref))
        self.to = references[self.ref]

    @property
    def combinations(self):
        if not self.to:
            raise TypeError('Unresolved reference to {!r}'.format(self.ref))
        return self.to.combinations

    def generate(self):
        if not self.to:
            raise TypeError('Unresolved reference to {!r}'.format(self.ref))
        return self.to.generate()

    def serialize(self):
        return {
            'ref': self.ref,
        }


class Value(Component, key='value'):
    """
    A component that holds a string value.
    Will return the value on every generation, unless `optional` is True,
    in which case it may return None 50% of the time.
    """

    def __init__(self, value, optional=False, **kwargs):
        self.value = value
        self.optional = optional
        super().__init__(**kwargs)

    @property
    def combinations(self):
        return 1 + self.optional

    def generate(self):
        if not self.optional or random.randrange(2):
            return self.value

    def serialize(self):
        if self.optional:
            return {
                'optional': True,
                'value': self.value,
            }
        return self.value


class Include(Component, key='include'):
    """
    Automatically include another generator file.
    """

    def __init__(self, include=None, format=None, **kwargs):
        if format is None:
            format = FileFormat.YAML
        if isinstance(format, str):
            format = FileFormat(format)
        super().__init__(include=include, format=format, **kwargs)
        self.to = Component.from_path(self.include, fmt=self.format)

    def resolve_references(self, references):
        self.to.resolve_references(references)

    @property
    def combinations(self):
        return self.to.combinations

    def generate(self):
        return self.to.generate()

    def serialize(self):
        return {
            'include': self.include,
            'format': self.format,
        }
