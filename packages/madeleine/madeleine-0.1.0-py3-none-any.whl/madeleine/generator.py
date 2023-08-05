from collections.abc import Mapping
from madeleine import Component


class Generator(Component, key='main'):

    def __init__(self, **data):
        assert 'version' in data, 'Missing generator spec version'
        assert data['version'] == '1', 'Incompatible generator spec version'
        assert 'main' in data, 'Missing main component'
        data.setdefault('components', {})
        assert isinstance(data['components'], Mapping), \
            'Components should be a mapping'

        self.version = data['version']
        self.components = {}
        for k, v in data['components'].items():
            self.components[k] = Component._make(v)

        self.main = Component._make(data['main'])
        # Allows components to reference the main component
        self.components.setdefault('main', self.main)

        # Let components resolve all their references
        for k in self.components:
            self.components[k].resolve_references(self.components)
        self.main.resolve_references(self.components)

    @property
    def combinations(self):
        return self.main.combinations

    def generate(self):
        return self.main.generate()

    def serialize(self):
        return {
            'version': self.version,
            'components': {
                name: component.serialize()
                for name, component in self.components.items()
            },
            'main': self.main.serialize()
        }
