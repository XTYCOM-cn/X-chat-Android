"""窗口位置修复程序 - 强制窗口到屏幕中央"""
import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
import os

class WindowPositionFixApp(App):
    def build(self):
        print("[POSITION_FIX] Starting window position fix")
        
        # 强制设置窗口位置到屏幕左上角
        Window.left = 0
        Window.top = 0
        print(f"[POSITION_FIX] Set window position to (0, 0)")
        
        # 设置窗口大小
        Window.size = (800, 600)
        print(f"[POSITION_FIX] Set window size to {Window.size}")
        
        # 设置背景色
        Window.clearcolor = (0, 1, 0, 1)  # 绿色背景
        print(f"[POSITION_FIX] Set clearcolor to {Window.clearcolor}")
        
        # 强制窗口显示和置顶
        try:
            Window.show()
            Window.raise_window()
            print("[POSITION_FIX] Called show() and raise_window()")
        except Exception as e:
            print(f"[POSITION_FIX] Error calling window methods: {e}")
        
        # 尝试设置窗口标题
        try:
            Window.set_title("KIVY POSITION FIX TEST - GREEN BACKGROUND")
            print("[POSITION_FIX] Set window title")
        except Exception as e:
            print(f"[POSITION_FIX] Error setting title: {e}")
        
        # 定期报告窗口状态
        Clock.schedule_interval(self.report_status, 2.0)
        
        # 延迟执行额外的位置修复
        Clock.schedule_once(self.delayed_position_fix, 1.0)
        
        label = Label(
            text='POSITION FIX TEST\nGREEN BACKGROUND\nWindow at (0,0)\nSize: 800x600',
            font_size=20,
            color=(1, 1, 1, 1),  # 白色文字
            halign='center'
        )
        label.bind(size=lambda inst, val: setattr(inst, 'text_size', val))
        
        return label
    
    def delayed_position_fix(self, dt):
        print("[POSITION_FIX] Delayed position fix")
        
        # 再次强制设置位置
        Window.left = 100
        Window.top = 100
        print(f"[POSITION_FIX] Moved window to (100, 100)")
        
        # 尝试不同的显示方法
        try:
            if hasattr(Window, '_window'):
                sdl_window = Window._window
                if hasattr(sdl_window, 'show'):
                    sdl_window.show()
                    print("[POSITION_FIX] Called SDL window show()")
                if hasattr(sdl_window, 'raise_window'):
                    sdl_window.raise_window()
                    print("[POSITION_FIX] Called SDL window raise_window()")
        except Exception as e:
            print(f"[POSITION_FIX] Error with SDL window methods: {e}")
    
    def report_status(self, dt):
        print(f"[POSITION_FIX] Status - Position: ({Window.left}, {Window.top}), Size: {Window.size}, Color: {Window.clearcolor}")
        
        # 尝试强制刷新
        try:
            Window.canvas.ask_update()
        except Exception as e:
            print(f"[POSITION_FIX] Error updating canvas: {e}")
        
        return True

if __name__ == '__main__':
    print("[POSITION_FIX] Starting window position fix app")
    print("[POSITION_FIX] This should show a GREEN window at position (0,0) then (100,100)")
    WindowPositionFixApp().run()