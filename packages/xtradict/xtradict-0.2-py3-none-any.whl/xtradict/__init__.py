class strg(dict):
    '''Improved dict class for better data management'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i,v in self.items():
            try: exec(f'self.{i} = v')
            except: raise Exception('Keys contain invalid characters')
    def __getitem__(self, key):
        return eval(f'self.{key}')
    def keys(self):
        return [x for x,_ in self.__dict__.items()]
