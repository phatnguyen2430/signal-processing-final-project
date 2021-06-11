import json

class InputObject:
    image = None
    use_filter = None
    filter_type = None
    scale_in = None
    scale_out = None
    n = None
    bit_24 = None
    def __init__(self,image,use_filter = "IDEAL",filter_type = "HIGH",scale_in = 0,scale_out = 80,n = 20,bit_24 = False):
        self.image = image
        self.use_filter = use_filter
        self.filter_type = filter_type
        self.scale_in = scale_in
        self.scale_out = scale_out
        self.n = n
        self.bit_24 = bit_24
    @classmethod
    def from_json(cls, json_str):
        json_dict = json.loads(json_str)
        return cls(**json_dict)