from copy import deepcopy


class RequestedObject:
    def from_json(self, json):
        self.__dict__.update(json)

    def stringify(self):
        raise NotImplementedError

    def __getitem__(self, item):
        return self.__dict__[item]


class StrictRequestedObject(RequestedObject):
    def stringify(self):
        raise NotImplementedError

    def from_json(self, json):
        for key, value in json.items():
            if key in self.__dict__:
                self.__dict__[key] = value


class List(RequestedObject):
    def __init__(self, subclass):
        self.subclass = subclass

        self.items = []

    def from_json(self, json):
        for subitem in json:
            new_item = deepcopy(self.subclass)
            new_item.from_json(subitem)
            self.items.append(new_item)

    def __iter__(self):
        return iter(self.items)

    def __len__(self):
        return len(self.items)

    def __getitem__(self, item):
        return self.items[item]

    def stringify(self):
        return_string = ""

        for item in self.items:
            return_string += item.stringify() + "\n"

        return return_string


class Dict(RequestedObject):
    def __init__(self, subclass_dict):
        self._subclass_dict = subclass_dict

    def from_json(self, json):
        for key, subclass in self._subclass_dict.items():
            new_item = deepcopy(subclass)
            new_item.from_json(json[key])
            self.__dict__[key] = new_item

            del json[key]

        super().from_json(json)

    def stringify(self):
        return_string = ""
        for key, value in self.__dict__.items():
            if not key.startswith("_"):

                return_string += "<b>" + str(key) + "</b>\n"
                try:
                    return_string += value.stringify()
                except AttributeError:
                    return_string += str(value)

        return return_string

class StrictDict(Dict, StrictRequestedObject):
    pass


class PageableObject(List):
    # TODO: Include next
    def __init__(self, subclass):
        List.__init__(self, subclass)

    def from_json(self, json):
        List.from_json(self, json["items"])

        del json["items"]
        RequestedObject.from_json(self, json)