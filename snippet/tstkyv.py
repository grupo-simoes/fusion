from kivy.uix.listview import ListItemButton
from kivy.adapters.listadapter import ListAdapter


class DataItem(object):
    def __init__(self, text='', is_selected=False):
        self.text = text
        self.is_selected = is_selected

data_items = [DataItem(text='cat'),
              DataItem(text='dog'),
              DataItem(text='frog')]

list_item_args_converter = lambda row_index, obj: {'text': obj.text,
                                                   'size_hint_y': None,
                                                   'height': 25}

list_adapter = ListAdapter(data=data_items,
                           args_converter=list_item_args_converter,
                           propagate_selection_to_data=True,
                           cls=ListItemButton)

list_view = ListView(adapter=list_adapter)
