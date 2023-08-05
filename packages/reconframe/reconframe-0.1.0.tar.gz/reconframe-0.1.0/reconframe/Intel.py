class Information():
    def __init__(self, key, value, test):
        if(test(value)):
            self.key = key
            self.value = value
            self.children = {}
        else:
            raise Exception("Test Failed!")

    def __repr__(self):
        return "{%s: %s} Total Children: %s" % (self.key, self.value, len(self.children))

    def add_child(self, key, value):
        if(type(value) == Information):
            try:
                self.children[key]
                exception = Exception("Key already exists!")
            except:
                self.children.update({key: value})
                return
        else:
            exception = Exception('"%s" is not an instance of Information!' % value )
        raise exception

    def remove_child(self, key):
        self.children.pop(key)
        return True

def information(info):
    if type(info) is not Information:
        return Information(0, info, lambda x: True)

    return info



# "IP Address": "192.168.0.1"
# "belongs_to": "https://"

# {
#     "url": "some_url",
#     "ip" : "192.168.0.1",
#     "ports": [
#         80,
#         500,
#         10065,
#         6553,
#         125,
#         012
#     ]
# }

# "key": "value",
# "trust": [] 
