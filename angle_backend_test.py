"""ANGLE后端测试程序 - 使用DirectX而非OpenGL"""
import os
import sys

# 在导入Kivy之前设置环境变量
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
os.environ['KIVY_WINDOW'] = 'sdl2'

print("[ANGLE_TEST] Set KIVY_GL_BACKEND to angle_sdl2")
print("[ANGLE_TEST] Set KIVY_WINDOW to sdl2")

import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock

class AngleBackendTestApp(App):
    def build(self):
        print("[ANGLE_TEST] Starting ANGLE backend test")
        
        # 设置窗口属性
        Window.left = 50
        Window.top = 50
        Window.size = (600, 400)
        Window.clearcolor = (1, 1, 0, 1)  # 黄色背景
        
        print(f"[ANGLE_TEST] Window position: ({Window.left}, {Window.top})")
        print(f"[ANGLE_TEST] Window size: {Window.size}")
        print(f"[ANGLE_TEST] Window clearcolor: {Window.clearcolor}")
        
        # 强制显示窗口
        try:
            Window.show()
            Window.raise_window()
            Window.set_title("ANGLE BACKEND TEST - YELLOW BACKGROUND")
            print("[ANGLE_TEST] Window setup completed")
        except Exception as e:
            print(f"[ANGLE_TEST] Error setting up window: {e}")
        
        # 定期状态报告
        Clock.schedule_interval(self.status_report, 3.0)
        
        # 创建UI
        label = Label(
            text='ANGLE BACKEND TEST\nYELLOW BACKGROUND\nUsing DirectX instead of OpenGL\nPosition: (50, 50)\nSize: 600x400',
            font_size=18,
            color=(0, 0, 0, 1),  # 黑色文字
            halign='center'
        )
        label.bind(size=lambda inst, val: setattr(inst, 'text_size', val))
        
        return label
    
    def status_report(self, dt):
        print(f"[ANGLE_TEST] Status - Backend working, Position: ({Window.left}, {Window.top}), Size: {Window.size}")
        return True

if __name__ == '__main__':
    print("[ANGLE_TEST] Starting ANGLE backend test app")
    print("[ANGLE_TEST] This uses DirectX instead of OpenGL to bypass graphics driver issues")
    print("[ANGLE_TEST] Should show a YELLOW window at position (50, 50)")
    
    try:
        AngleBackendTestApp().run()
    except Exception as e:
        print(f"[ANGLE_TEST] Error running app: {e}")
        print("[ANGLE_TEST] ANGLE backend may not be available")
        
        # 回退到默认后端
        print("[ANGLE_TEST] Falling back to default backend...")
        os.environ.pop('KIVY_GL_BACKEND', None)
        
        class FallbackApp(App):
            def build(self):
                Window.clearcolor = (1, 0, 1, 1)  # 紫色背景
                return Label(text='FALLBACK TEST\nPURPLE BACKGROUND', font_size=20, color=(1, 1, 1, 1))
        
        FallbackApp().run()