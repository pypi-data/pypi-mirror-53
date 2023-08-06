class strg(dict):
    '''Improved dict class for better data management'''
    def __init__(self, *args, **kwargs):
        for i, v in kwargs.items():
            exec(f'self.{i} = v')
    def __getitem__(self, key):
        return eval(f'self.{key}')
    def keys(self):
        return [x for x,_ in self.__dict__.items()]
