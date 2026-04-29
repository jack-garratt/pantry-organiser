import kivy
kivy.require('2.3.1') # replace with your current kivy version !
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex
from db_utils import generate_items,add_item
from item import Item

Window.size = (540, 1170)
Window.clearcolor = get_color_from_hex("#1C1C1Cff")

class Header(BoxLayout):
    def __init__(self, **kwargs):
        super(Header,self).__init__(**kwargs)
        self.add_widget(Label(text = "Stock Counter", bold = True, font_size = 72))

class ItemFrame(BoxLayout):
    def __init__(self, item, **kwargs):
        super(ItemFrame,self).__init__(**kwargs)
        self.item = item
        with self.canvas.before:
            Color(0.18, 0.18, 0.18, 1)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius = (10,10,10,10))
            self.bind(size=self._update_rect, pos=self._update_rect)
        self.add_widget(Label(text = self.item.get_name(), font_size = 64))
        self.remove_button = Button(text = "-" ,font_size = 32, size_hint = (0.08,1))
        self.remove_button.bind(on_press=self.decrement_command)
        self.add_button = Button(text = "+", font_size = 32, size_hint = (0.08,1))
        self.add_button.bind(on_press=self.increment_command)
        self.quantity_label = Label(text = str(self.item.get_quantity()), font_size = 32, size_hint = (0.2,1))
        self.add_widget(self.remove_button)
        self.add_widget(self.quantity_label)
        self.add_widget(self.add_button)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def increment_command(self, instance):
        self.item.increment_quantity()
        self.quantity_label.text = str(self.item.get_quantity())

    def decrement_command(self, instance):
        self.item.decrement_quantity()
        if self.item.get_quantity() >= 0:
            self.quantity_label.text = str(self.item.get_quantity())
        else:
            self.parent.remove_widget(self)

class Body(ScrollView):
    def __init__(self, items, **kwargs):
        super(Body,self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing = 20, padding = 20)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        for item in items:
            self.add_item_widget(item)
        self.add_widget(self.layout)

    def add_item_widget(self, item):
        self.layout.add_widget(ItemFrame(item, height = 75, size_hint_y = None, padding = 8))


class Footer(BoxLayout):
    def __init__(self, body, **kwargs):
        super(Footer,self).__init__(**kwargs)
        self.body = body
        self.name_feild = TextInput(size_hint = (0.8,1), font_size = 62, multiline = False)
        self.add_widget(self.name_feild)
        self.add_button = Button(text = "+", font_size = 50, size_hint = (0.2,1))
        self.add_widget(self.add_button)
        self.add_button.bind(on_press=self.add_item_local)

    def add_item_local(self,instance):
        item = Item(self.name_feild.text, 1)
        self.body.add_item_widget(item)
        add_item(self.name_feild.text)
        self.name_feild.text = ""

class Root(BoxLayout):
    def __init__(self, items,**kwargs):
        super(Root, self).__init__(**kwargs)
        header = Header(size_hint = (1, 0.1))
        body = Body(items)
        footer = Footer(body,size_hint = (1, 0.075),padding = 16, spacing = 8 )
        self.add_widget(header)
        self.add_widget(body)
        self.add_widget(footer)



class MyApp(App):
    def build(self):
        items = generate_items()
        return Root(items, orientation = "vertical")

if __name__ == '__main__':
    MyApp().run()