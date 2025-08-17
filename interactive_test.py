"""交互式Kivy测试程序 - 通过键盘确认程序运行状态"""
import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
import random

class InteractiveTestApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.counter = 0
        self.colors = [(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1), (1, 1, 0, 1), (1, 0, 1, 1)]
        
    def build(self):
        print("[INTERACTIVE] Building interactive test app")
        Window.clearcolor = (1, 0, 0, 1)  # 红色背景
        print(f"[INTERACTIVE] Window size: {Window.size}")
        print(f"[INTERACTIVE] Window clearcolor: {Window.clearcolor}")
        
        self.label = Label(
            text='INTERACTIVE TEST\nPress SPACE to change color\nPress ESC to exit\nCounter: 0',
            font_size=24,
            color=(1, 1, 1, 1),  # 白色文字
            halign='center'
        )
        self.label.bind(size=lambda inst, val: setattr(inst, 'text_size', val))
        
        # 绑定键盘事件
        Window.bind(on_key_down=self.on_key_down)
        
        # 自动变色循环
        Clock.schedule_interval(self.auto_change_color, 2.0)
        
        print("[INTERACTIVE] Interactive test ready - press SPACE or wait for auto color change")
        return self.label
    
    def on_key_down(self, window, key, scancode, codepoint, modifier):
        print(f"[INTERACTIVE] Key pressed: {key} (scancode: {scancode})")
        
        if key == 32:  # SPACE键
            self.change_color()
        elif key == 27:  # ESC键
            print("[INTERACTIVE] ESC pressed - exiting")
            self.stop()
    
    def change_color(self):
        self.counter += 1
        color = random.choice(self.colors)
        Window.clearcolor = color
        self.label.text = f'INTERACTIVE TEST\nPress SPACE to change color\nPress ESC to exit\nCounter: {self.counter}\nColor: {color}'
        print(f"[INTERACTIVE] Color changed to {color}, counter: {self.counter}")
    
    def auto_change_color(self, dt):
        self.change_color()
        return True  # 继续调度

if __name__ == '__main__':
    print("[INTERACTIVE] Starting interactive Kivy test")
    print("[INTERACTIVE] Instructions: Press SPACE to change colors, ESC to exit")
    InteractiveTestApp().run()