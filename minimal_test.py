"""最简单的Kivy测试程序 - 验证基础渲染管线"""
import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window

class MinimalTestApp(App):
    def build(self):
        print("[MINIMAL] Building minimal test app")
        Window.clearcolor = (1, 0, 0, 1)  # 红色背景
        print(f"[MINIMAL] Window size: {Window.size}")
        print(f"[MINIMAL] Window clearcolor: {Window.clearcolor}")
        
        return Label(
            text='HELLO WORLD TEST',
            font_size=30,
            color=(1, 1, 1, 1)  # 白色文字
        )

if __name__ == '__main__':
    print("[MINIMAL] Starting minimal Kivy test")
    MinimalTestApp().run()