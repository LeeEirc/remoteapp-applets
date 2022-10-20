class DictObj:
    def __init__(self, in_dict: dict):
        assert isinstance(in_dict, dict)
        for key, val in in_dict.items():
            if isinstance(val, (list, tuple)):
                setattr(self, key, [DictObj(x) if isinstance(x, dict) else x for x in val])
            else:
                setattr(self, key, DictObj(val) if isinstance(val, dict) else val)


class User(DictObj):
    id: str
    name: str
    username: str


class CategoryProperty(DictObj):
    autofill: str
    username_selector: str
    password_selector: str
    submit_selector: str
    script: list


class Category(DictObj):
    value: str
    label: str


class Asset(DictObj):
    id: str
    name: str
    address: str
    protocols: list
    category: Category
    category_property: CategoryProperty


class Account(DictObj):
    id: str
    name: str
    username: str
    secret: str


class Platform(DictObj):
    charset: str
