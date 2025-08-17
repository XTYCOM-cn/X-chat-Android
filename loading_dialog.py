"""
等待响应对话框模块
提供类似微信/QQ的加载动画体验
"""

from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, PushMatrix, PopMatrix, Rotate
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp, sp
import math


class SpinnerWidget(Widget):
    """旋转加载指示器"""
    
    def __init__(self, **kwargs):
        super(SpinnerWidget, self).__init__(**kwargs)
        self.angle = 0
        self.animation = None
        self.bind(size=self.update_graphics, pos=self.update_graphics)
        Clock.schedule_once(self.init_graphics, 0)
        
    def init_graphics(self, dt):
        self.update_graphics()
        self.start_animation()
        
    def start_animation(self):
        if self.animation:
            self.animation.stop(self)
        self.animation = Animation(angle=360, duration=1.2, t='linear')
        self.animation.repeat = True
        self.animation.bind(on_progress=self.on_animation_progress)
        self.animation.start(self)
        
    def stop_animation(self):
        if self.animation:
            self.animation.stop(self)
            self.animation = None
            
    def on_animation_progress(self, animation, widget, progress):
        self.angle = animation.animated_properties['angle'] * progress
        self.update_graphics()
        
    def update_graphics(self, *args):
        self.canvas.clear()
        with self.canvas:
            center_x, center_y = self.center
            radius = min(self.width, self.height) * 0.35
            
            # 绘制旋转的圆弧
            PushMatrix()
            Rotate(angle=self.angle, axis=(0, 0, 1), origin=(center_x, center_y))
            
            # 主圆弧 - 模仿Material Design spinner
            for i in range(8):
                alpha = 1.0 - (i / 8.0) * 0.8
                Color(0.12, 0.53, 0.9, alpha)
                
                start_angle = i * 45
                end_angle = start_angle + 30
                
                # 绘制圆弧线段
                points = []
                for angle in range(int(start_angle), int(end_angle), 2):
                    x = center_x + math.cos(math.radians(angle)) * radius
                    y = center_y + math.sin(math.radians(angle)) * radius
                    points.extend([x, y])
                
                if len(points) >= 4:
                    Line(points=points, width=dp(3), cap='round')
            
            PopMatrix()


class PulsingDots(Widget):
    """脉冲点动画 - 备用加载样式"""
    
    def __init__(self, **kwargs):
        super(PulsingDots, self).__init__(**kwargs)
        self.dot_scales = [1.0, 0.7, 0.4]
        self.bind(size=self.update_graphics, pos=self.update_graphics)
        Clock.schedule_once(self.init_animation, 0)
        
    def init_animation(self, dt):
        self.update_graphics()
        Clock.schedule_interval(self.animate_dots, 0.3)
        
    def animate_dots(self, dt):
        # 循环缩放模式
        self.dot_scales = [self.dot_scales[-1]] + self.dot_scales[:-1]
        self.update_graphics()
        
    def update_graphics(self, *args):
        self.canvas.clear()
        with self.canvas:
            center_x, center_y = self.center
            dot_spacing = dp(20)
            
            for i, scale in enumerate(self.dot_scales):
                Color(0.12, 0.53, 0.9, 0.3 + scale * 0.7)
                radius = dp(4) * scale
                x = center_x + (i - 1) * dot_spacing
                Ellipse(pos=(x - radius, center_y - radius), size=(radius*2, radius*2))


class LoadingDialog(ModalView):
    """现代化加载对话框"""
    
    def __init__(self, message="正在处理...", style="spinner", cancellable=True, **kwargs):
        super(LoadingDialog, self).__init__(**kwargs)
        
        # 对话框属性设置
        self.size_hint = (None, None)
        self.size = (dp(280), dp(200))
        self.auto_dismiss = False
        self.background_color = (0, 0, 0, 0.7)  # 半透明背景
        
        self.message_text = message
        self.loading_style = style
        self.is_cancellable = cancellable
        self.on_cancel_callback = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # 主容器
        main_layout = BoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(15)
        )
        
        # 对话框背景
        with main_layout.canvas.before:
            Color(0.15, 0.15, 0.2, 0.95)  # 深色半透明背景
            from kivy.graphics import RoundedRectangle
            self.bg_rect = RoundedRectangle(size=main_layout.size, pos=main_layout.pos, radius=[dp(15)])
        main_layout.bind(size=self._update_bg, pos=self._update_bg)
        
        # 加载指示器区域
        indicator_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=0.6,
            spacing=dp(10)
        )
        
        # 选择加载样式
        if self.loading_style == "spinner":
            self.loading_widget = SpinnerWidget(
                size_hint=(None, None),
                size=(dp(50), dp(50)),
                pos_hint={'center_x': 0.5}
            )
        else:  # dots
            self.loading_widget = PulsingDots(
                size_hint=(None, None),
                size=(dp(80), dp(20)),
                pos_hint={'center_x': 0.5}
            )
            
        indicator_layout.add_widget(Widget())  # 上方间隔
        indicator_layout.add_widget(self.loading_widget)
        indicator_layout.add_widget(Widget())  # 下方间隔
        
        main_layout.add_widget(indicator_layout)
        
        # 消息文本
        self.message_label = Label(
            text=self.message_text,
            font_size=sp(16),
            color=(0.9, 0.9, 0.9, 1),
            halign='center',
            valign='middle',
            text_size=(dp(240), None),
            size_hint_y=0.3
        )
        main_layout.add_widget(self.message_label)
        
        # 取消按钮（可选）
        if self.is_cancellable:
            button_layout = BoxLayout(
                size_hint_y=0.2,
                padding=[dp(20), 0]
            )
            
            self.cancel_btn = Button(
                text="取消",
                font_size=sp(14),
                background_color=(0.8, 0.3, 0.3, 1),
                color=(1, 1, 1, 1),
                size_hint=(None, None),
                size=(dp(80), dp(35)),
                pos_hint={'center_x': 0.5}
            )
            self.cancel_btn.bind(on_press=self.on_cancel_pressed)
            
            button_layout.add_widget(Widget())  # 左侧间隔
            button_layout.add_widget(self.cancel_btn)
            button_layout.add_widget(Widget())  # 右侧间隔
            
            main_layout.add_widget(button_layout)
        
        self.add_widget(main_layout)
        
    def _update_bg(self, *args):
        if hasattr(self, 'bg_rect'):
            self.bg_rect.size = self.children[0].size
            self.bg_rect.pos = self.children[0].pos
            
    def update_message(self, new_message):
        """更新加载消息"""
        self.message_text = new_message
        if hasattr(self, 'message_label'):
            self.message_label.text = new_message
            
    def set_cancel_callback(self, callback):
        """设置取消回调函数"""
        self.on_cancel_callback = callback
        
    def on_cancel_pressed(self, instance):
        """处理取消按钮点击"""
        if self.on_cancel_callback:
            self.on_cancel_callback()
        self.dismiss()
        
    def show(self):
        """显示对话框"""
        self.open()
        
    def hide(self):
        """隐藏对话框"""
        if hasattr(self.loading_widget, 'stop_animation'):
            self.loading_widget.stop_animation()
        self.dismiss()


class ProgressDialog(LoadingDialog):
    """带进度条的加载对话框"""
    
    def __init__(self, message="正在处理...", **kwargs):
        self.progress_value = 0
        super(ProgressDialog, self).__init__(message=message, style="progress", **kwargs)
        
    def setup_ui(self):
        # 基础UI设置
        super(ProgressDialog, self).setup_ui()
        
        # 添加进度条
        self.progress_bar = Widget(
            size_hint=(1, None),
            height=dp(4)
        )
        self.progress_bar.bind(size=self.update_progress_bar, pos=self.update_progress_bar)
        
        # 将进度条插入到消息标签之前
        if len(self.children[0].children) >= 2:
            self.children[0].add_widget(self.progress_bar, index=1)
            
    def update_progress_bar(self, *args):
        """更新进度条显示"""
        self.progress_bar.canvas.clear()
        with self.progress_bar.canvas:
            # 背景条
            Color(0.3, 0.3, 0.3, 1)
            from kivy.graphics import Rectangle
            Rectangle(pos=self.progress_bar.pos, size=self.progress_bar.size)
            
            # 进度条
            Color(0.12, 0.53, 0.9, 1)  # 主题色
            progress_width = self.progress_bar.width * (self.progress_value / 100.0)
            Rectangle(pos=self.progress_bar.pos, size=(progress_width, self.progress_bar.height))
            
    def set_progress(self, value):
        """设置进度值 (0-100)"""
        self.progress_value = max(0, min(100, value))
        self.update_progress_bar()
        
        # 更新消息文本显示进度
        base_message = self.message_text.split(' (')[0]  # 移除之前的进度信息
        self.update_message(f"{base_message} ({self.progress_value}%)")