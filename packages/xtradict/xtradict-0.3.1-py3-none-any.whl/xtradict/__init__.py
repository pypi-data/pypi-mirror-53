class strg(dict):
    '''Improved dict class for better data management'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i,v in self.items():
            try: exec(f'self.{i.replace(" ", "_")} = v')
            except: raise Exception('Keys contain invalid characters')
    def keys(self):
        return [x for x,_ in self.items()]
