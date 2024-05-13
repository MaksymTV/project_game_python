### - Імпорт бібліотек для коректної роботи коду.
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window
from kivy.utils import platform
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.properties import StringProperty, NumericProperty
from random import shuffle, choice, randint
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
from kivy.uix.popup import Popup
from kivy.base import stopTouchApp
###
### - Клас який відповідає за екран меню.
class MenuScreen(Screen): 
    def __init__(self, **kw):
        super().__init__(**kw)
###
### - Функція, яка викликається при вході на екран.
    def on_enter(self, *args):
        app.save_prog
###
### - Клас який відповідає за ігровий екран меню.
class GameScreen(Screen):
    points = NumericProperty(0)
    def __init__(self, **kw):
        super().__init__(**kw)
###
### - Функція, яка викликається при вході на екран.
    def on_enter(self, *args):
        data = app.load_prog()
        self.ids.sticker.new_sticker(data) # Передача даних про стан гри для відновлення.
        return super().on_enter(*args)
###
### - Клас, що представляє Sticker's на ігровому екрані.
class Sticker(Image):
    points = NumericProperty(0)
    is_anim = False
    hp = None
    sticker = None
    sticker_index = 0
    mult = 1
###
### - Функція, яка реагує на дотик користувача до стікеру.
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and not self.is_anim:
            self.parent.parent.parent.points += (1*self.mult)
            self.points += (1*self.mult)
            Sticker.points = self.points
            self.hp -= 1
            if self.hp <= 0:
                Sticker.points = self.points
                self.break_sticker()
                app.save_prog() ### - Зберігання стану гри.
            else:
                x = self.x
                y = self.y
                size = self.size.copy()
                anim = Animation(size=(size[0]*1.2, size[1]*1.2), d=.1, t='out_back') + Animation(size=(size[0], size[1]), d=.1)
                anim.start(self)
                self.is_anim = True
                anim.on_complete = lambda *arg: setattr(self, 'is_anim', False)  
        return super().on_touch_down(touch)
###
### Функція, яка відповідає за створення нового стікеру.
    def new_sticker(self, *args,):
        Sticker.sticker = self.sticker = app.LEVELS[randint(0, len(app.LEVELS)-1)]
        self.source = app.STICKERS[self.sticker]['source']
        self.hp = app.STICKERS[self.sticker]['hp']
        self.size = app.STICKERS[self.sticker]['size']
        size = self.size.copy()
        self.size = size[0], size[1]
        self.center = self.parent.center
        anim = Animation(opacity=1, d=0.3)
        anim &= Animation(
            size=(self.size[0]/1.5, self.size[1]/1.5), d=.2, t='out_back')
        anim &= Animation(center=self.parent.center, d=.3)
        anim.start(self)
        anim.on_complete = lambda *arg: setattr(self, 'is_anim', False)
###
### - Функція, яка відповідає за руйнування стікеру.
    def break_sticker(self):
        self.is_anim = True
        anim = Animation(size=(self.size[0]*2, self.size[1]*2), d=.2)
        anim &= Animation(center=self.parent.center, d=.2)
        anim &= Animation(opacity=0, d=.3)

        anim.start(self)
        anim.on_complete = Clock.schedule_once(self.new_sticker, .5)
###
### - Клас, що відображає екран магазину.
class ShopScreen(Screen):
    pass
###
### - Головний клас програми, що наслідується від App.
class MainApp(App):
    Storage = None
    SHOP = {"mult": 1}
    LEVELS = ['LittleTurtle', 'LittlePanda', 'CatFace', 
              'WolfFace', 'ChickenRooster', 'EagleHead', 
              'RexMascot', 
              ### - NewSticker.
              'WolfFace2', 'CartoonHamster', 
              'OwlGlasses', 'CuteCat', 'CatNinja', 
              'BearMascot', 'WatercolorMascot', 'ChickenFlower', 
              'GiraffeFlowers',]
###
### - Персонажі. 
    STICKERS = {
        'LittleTurtle': {"source": 'img/vecteezy_little-turtle-sticker-with_24558435.png', 'hp': 1, "size": (375, 375)},
        'LittlePanda': {"source": 'img/vecteezy_little-panda-sticker-with_24558432.png', 'hp': 2, "size": (375, 375)},
        'CatFace': {"source": 'img/vecteezy_colorful-cat-face-illustration-sticker_24855184.png', 'hp': 3, "size": (375, 375)},
        'WolfFace': {"source": 'img/vecteezy_wolf-face-logo-mascot-illustration-with-ai-generative_24856242.png', 'hp': 4, "size": (375, 375)},
        'ChickenRooster': {"source": 'img/vecteezy_chicken-rooster-logo-with-ai-generative_24684312.png', 'hp': 5, "size": (375, 375)},
        'EagleHead': {"source": 'img/vecteezy_illustration-of-eagle-head-logo-with_24684356.png', 'hp': 6, "size": (375, 375)},
        'RexMascot': {"source": 'img/vecteezy_tyrano-rex-logo-mascot-with_24684376.png', 'hp': 7, "size": (375, 375)},
        ### - NewSticker.
        'WolfFace2': {"source": 'img/vecteezy_beauty-wolf-face-sticker-ai-generative_26792717.png', 'hp': 8, "size": (375, 375)},
        'CartoonHamster': {"source": 'img/vecteezy_sticker-cartoon-of-cute-hamster-ai-generative_26792719.png', 'hp': 9, "size": (375, 375)},
        'OwlGlasses': {"source": 'img/vecteezy_cute-owl-wearing-glasses-and-headset-a-fun-colorful-design_23401364.png', 'hp': 8, "size": (375, 375)},
        'CuteCat': {"source": 'img/vecteezy_cute-cat-wearing-glasses-and-headset-fun-colorful-concept_23401371.png', 'hp': 6, "size": (375, 375)},
        'CatNinja': {"source": 'img/vecteezy_cat-ninja-t-shirt-design-illustration-with-ai-generative_29890667.png', 'hp': 5, "size": (375, 375)},
        'BearMascot': {"source": 'img/vecteezy_bear-mascot-wear-headphone-logo-ai-generative_29322367.png', 'hp': 4, "size": (375, 375)},
        'WatercolorMascot': {"source": 'img/vecteezy_watercolor-illustration-of-reindeer-head-mascot-with-ai_25277557.png', 'hp': 3, "size": (375, 375)},
        'ChickenFlower': {"source": 'img/vecteezy_chicken-chick-with-fantasy-flower-sticker-with_24558419.png', 'hp': 2, "size": (375, 375)},
        'GiraffeFlowers': {"source": 'img/vecteezy_giraffe-with-flowers-sticker_24558402.png', 'hp': 1, "size": (375, 375)},
        ###
    }
###
### - Функція, яка відповідає за збереження стану гри.
    def save_prog(self):
        print(Sticker.points)
        app.storage.put('progress', sticker=Sticker.sticker,
                        hp=Sticker.hp,
                        sticker_index=Sticker.sticker_index,
                        mult=Sticker.mult,
                        points=Sticker.points)
###
### - Функція, яка відповідає за побудову інтерфейсу, і взаємодіє із кнопками. 
    def build(self):
        global storage
        self.storage = JsonStore(self.user_data_dir+"storage.json")
        storage = self.storage
        sm = ScreenManager(transition=FadeTransition(duration=1))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(ShopScreen(name='shop'))
        return sm
###
### - Функція, яка відповідає за завантаження стану гри.
    def load_prog(self):
        if self.storage.exists("progress"):  # перевіряємо, чи існує ключ "progress"
            return self.storage.get("progress")
        else:
            print("Key 'progress' does not exist in JsonStore.")
            print("Available keys:", self.storage.keys())
            return None  # якщо ключ не існує, повертаємо None

### - Задавання розміру екрану.
if platform != 'android':
    Window.size = (400, 800)
    Window.left = 750
    Window.top = 100
###
app = MainApp()
app.run()
