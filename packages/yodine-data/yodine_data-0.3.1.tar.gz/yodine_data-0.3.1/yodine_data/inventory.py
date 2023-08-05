import typing
import collections


class MethodSpec(object):
    def __init__(self, name: str, default_value: typing.Any = None):
        self.name = name
        self.default_value = default_value

    def __repr__(self):
        return "[{} {} [{}]]".format(type(self).__name__, self.name, self.default_value)

    def __call__(self, item_type, *args, **kwargs):
        if hasattr(item_type, self.name) and hasattr(getattr(item_type, self.name), '__call__'):
            return getattr(item_type, self.name)(*args, **kwargs)

        elif hasattr(self.default_value, '__call__'):
            return self.default_value(*args, **kwargs)

        else:
            return self.default_value

class ItemType(object):

    def __repr__(self):
        return "ItemType<{}>".format(type(self).__name__)

class ItemTypes(object):
    types = {}

    @staticmethod
    def register(itype):
        ItemTypes.types[itype.__name__] = itype
        return itype

    @staticmethod
    def get_type(iname):
        return ItemTypes.types[iname]

class ItemContainer(object): # aka an inventory!
    def __init__(self):
        self.items = {}
        self.reset_item_updates()

    def reset_item_updates(self):
        self.item_updates = collections.OrderedDict()

    def give_items(self, inv_type: ItemType, count: int) -> None:
        if inv_type in self.items:
            self.items[inv_type.__name__] += count

        else:
            self.items[inv_type.__name__] = count

        self.update_item(inv_type)

    def take_items(self, inv_type: ItemType, count: int) -> int:
        if inv_type in self.items:
            if self.items[inv_type] >= count:
                self.items[inv_type] -= count

                if self.items[inv_type] == 0:
                    del self.items[inv_type]

                return 0 # no debt

            else:
                count -= self.items[inv_type]
                del self.items[inv_type]

                return count # partial debt

        else:
            return count # full debt

        self.update_item(inv_type)

    def update_item(self, inv_type):
        self.item_updates[inv_type.__name__] = self.items.get(inv_type.__name__, 0)
