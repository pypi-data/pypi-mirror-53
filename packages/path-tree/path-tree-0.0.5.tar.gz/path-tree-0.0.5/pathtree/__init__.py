import os
import glob
from pathlib import Path


class PathTree(object):
    '''

    TODO:
     - how do you manage in both representations (flattened and hierarchical)
        - first step - manage in compiled view - assume unmutable
     - partial string substitution
     -

    -------

    paths = PathSpec.define('./blah/logs', {
        '{log_id}': {
            'model.h5': 'model',
            'model_spec.pkl': 'model_spec',
            'plots': {
                '{step_name}': {
                    '{plot_name}.png': 'plot'
                }
            }
        }
    })

    paths = paths.format(root='logs', log_id='adfasdfasdf', step_name='epoch_100')

    paths['model'] # logs/adfasdfasdf/model.h5
    paths['plot'] # logs/adfasdfasdf/plots/epoch_100/{plot_name}.png

    plot_files = glob.glob(paths['plots'].format(plot_name='*'))

    '''

    def __init__(self, paths, data=None):
        self._paths = paths
        self.data = {} if data is None else data

    @staticmethod
    def define(root, paths):
        '''Build paths from hierarchy'''
        data = {'root': root}
        return PathTree({
            v: PathItem(*k, data=data)
            for k, v in get_keys({'{root}': paths})
        }, data)

    def __repr__(self):
        return '<PathTree data={} \n{}\n>'.format(self.data, '\n'.join([
            '\t{} : {}'.format(name, self[name].maybe_format())
            for name in self._paths
        ]))

    def update(self, **kw):
        '''Update in place'''
        self.data.update(kw)
        for name in self._paths:
            self._paths.update(**kw)
        return self

    def specify(self, **kw):
        '''Return new PathTree with added variables'''
        return PathTree({
            name: self._paths[name].specify(**kw)
            for name in self._paths
        }, {**self.data, **kw})

    def format(self, **kw):
        return {
            name: self._paths[name].maybe_format(**kw)
            for name in self._paths
        }

    def __iter__(self):
        return iter(self._paths)

    def __getitem__(self, name):
        return self._paths[name]

    def get(self, name, **kw):
        '''Get a path with possibly'''
        return self._paths[name].specify(**kw)

    def parse(self, path, name):
        return self[name].parse(path)


class PathItem:
    '''



    '''
    def __init__(self, *path, data=None):
        self.path = os.path.join(*path)
        self.data = {} if data is None else data


    def update(self, **kw):
        self.data.update(**kw)

    def specify(self, **kw):
        return PathItem(self.path, data={**self.data, **kw})

    @property
    def fully_specified(self):
        try:
            self.format()
            return True
        except KeyError:
            return False

    def __str__(self):
        '''Return path with all variables inserted. Will fail if variables are missing.
        There's no good way to do partial formatting - stackoverflow answers suck.
        '''
        # TODO: make print work - partial formatting is key !!
        try:
            return self.format()
        except KeyError:
            return repr(self)

    def __repr__(self):
        return '<PathItem "{}" data={}>'.format(self.path, self.data)

    @property
    def str(self):
        return str(self)

    def maybe_format(self, **kw):
        p = self.specify(**kw)
        try:
            return p.format()
        except KeyError:
            return p

    def format(self, **kw):
        '''Works like string format.'''
        return self.path.format(**{**self.data, **kw})

    def parse(self, path):
        '''Extract variables from a compiled path'''
        from parse import parse
        r = parse(self.path, path)
        return r.fixed, r.named




def get_keys(data, keys=None):
    keys = tuple(keys or ())
    for key, value in data.items():
        keys_ = keys + (key,)
        if isinstance(value, dict):
            for keys_, value in get_keys(value, keys_):
                yield keys_, value
        else:
            yield keys_, value


if __name__ == '__main__':
    paths = PathTree.define('./blah/logs', {
        '{log_id}': {
            'model.h5': 'model',
            'model_spec.pkl': 'model_spec',
            'plots': {
                '{step_name}': {
                    '{plot_name}.png': 'plot'
                }
            }
        }
    })

    paths = paths.specify(root='logs', log_id='a')
    p = paths.format()

    print(p)
    print(p['model'], p['model_spec'])
    assert p['model'] == 'logs/a/model.h5'
    assert p['model_spec'] == 'logs/a/model_spec.pkl'


    p2 = paths.format(root='logs', log_id='b')
    assert p['model'] == 'logs/a/model.h5'
    assert p2['model_spec'] == 'logs/b/model_spec.pkl'
    # assert paths['plot'] == 'logs/adfasdfasdf/plots/epoch_100/{plot_name}.png'

    plot_f = p['plot'].specify(step_name='epoch_100')
    for n in 'abcde':
        f = plot_f.format(plot_name=n)
        print(n, f)
        assert f == 'logs/a/plots/epoch_100/{}.png'.format(n)

    plot_files = glob.glob(plot_f.format(plot_name='*'))
    print(plot_files)
