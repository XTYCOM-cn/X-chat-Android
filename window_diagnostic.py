"""窗口诊断程序 - 检查窗口属性和显示状态"""
import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
import sys
import os

class WindowDiagnosticApp(App):
    def build(self):
        print("[DIAGNOSTIC] Starting window diagnostic")
        
        # 设置窗口属性
        Window.clearcolor = (1, 0, 0, 1)  # 红色背景
        
        # 强制窗口到前台
        Window.raise_window()
        Window.show()
        
        # 诊断窗口属性
        self.diagnose_window()
        
        # 定期诊断
        Clock.schedule_interval(self.periodic_diagnosis, 3.0)
        
        label = Label(
            text='WINDOW DIAGNOSTIC\nCheck console for details',
            font_size=24,
            color=(1, 1, 1, 1)
        )
        
        return label
    
    def diagnose_window(self):
        print("\n" + "="*50)
        print("[DIAGNOSTIC] WINDOW PROPERTIES REPORT")
        print("="*50)
        
        # 基本窗口信息
        print(f"Window size: {Window.size}")
        print(f"Window clearcolor: {Window.clearcolor}")
        print(f"Window position: {getattr(Window, 'left', 'N/A')}, {getattr(Window, 'top', 'N/A')}")
        
        # 窗口状态
        try:
            print(f"Window minimized: {getattr(Window, 'minimized', 'N/A')}")
            print(f"Window maximized: {getattr(Window, 'maximized', 'N/A')}")
            print(f"Window fullscreen: {getattr(Window, 'fullscreen', 'N/A')}")
            print(f"Window borderless: {getattr(Window, 'borderless', 'N/A')}")
            print(f"Window resizable: {getattr(Window, 'resizable', 'N/A')}")
        except Exception as e:
            print(f"Error getting window state: {e}")
        
        # SDL窗口信息
        try:
            if hasattr(Window, '_window'):
                sdl_window = Window._window
                print(f"SDL Window object: {sdl_window}")
                if hasattr(sdl_window, 'get_window_info'):
                    info = sdl_window.get_window_info()
                    print(f"SDL Window info: {info}")
        except Exception as e:
            print(f"Error getting SDL window info: {e}")
        
        # 系统信息
        print(f"\nSystem platform: {sys.platform}")
        print(f"Python version: {sys.version}")
        
        # 环境变量检查
        relevant_env_vars = ['KIVY_WINDOW', 'KIVY_GL_BACKEND', 'SDL_VIDEODRIVER']
        print("\nRelevant environment variables:")
        for var in relevant_env_vars:
            value = os.environ.get(var, 'Not set')
            print(f"  {var}: {value}")
        
        # OpenGL信息
        try:
            from kivy.graphics.opengl import gl_get_extensions, gl_get_version
            print(f"\nOpenGL version: {gl_get_version()}")
            extensions = gl_get_extensions()
            print(f"OpenGL extensions count: {len(extensions) if extensions else 0}")
        except Exception as e:
            print(f"Error getting OpenGL info: {e}")
        
        print("="*50)
        print("[DIAGNOSTIC] End of report\n")
    
    def periodic_diagnosis(self, dt):
        print(f"[DIAGNOSTIC] Periodic check - Window size: {Window.size}, clearcolor: {Window.clearcolor}")
        
        # 尝试强制刷新
        try:
            Window.canvas.ask_update()
            if hasattr(Window, '_window') and hasattr(Window._window, 'flip'):
                Window._window.flip()
        except Exception as e:
            print(f"[DIAGNOSTIC] Error during refresh: {e}")
        
        return True

if __name__ == '__main__':
    print("[DIAGNOSTIC] Starting window diagnostic app")
    WindowDiagnosticApp().run()