class Dict:
    def __init__(self, structure):
        self.dict = structure

    def __new__(cls, structure):
        self = super(Dict, cls).__new__(cls)
        self.dict = structure
        if type(structure) is dict:
            self.__dict__ = {key: Dict(structure[key]) for key in structure}
        elif type(structure) is list:
            self = [Dict(item) for item in structure]
        else:
            self = structure
        return self

    def __str__(self):
        return str(self.dict)
