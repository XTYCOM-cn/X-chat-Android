"""
现代化启动界面 (Splash Screen) 模块
提供品牌标识、渐变动效和优雅的加载体验
"""

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle, Line, RoundedRectangle
from kivy.graphics import PushMatrix, PopMatrix, Rotate, Scale
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.properties import StringProperty, ObjectProperty
import math
import sys
import re

# 平台检测与文本清洗（移除Windows上不支持/显示异常的Emoji）
IS_WINDOWS = sys.platform.startswith('win')
_EMOJI_RE = re.compile(
    r"[\U0001F300-\U0001FAFF\U0001F1E6-\U0001F1FF\u2600-\u27BF\uFE0F]",
    flags=re.UNICODE
)

def sanitize_text(text: str) -> str:
    if not isinstance(text, str):
        return text
    if IS_WINDOWS:
        return _EMOJI_RE.sub('', text)
    return text


class RotatingLogo(Widget):
    """增强版旋转品牌Logo组件"""
    
    def __init__(self, **kwargs):
        super(RotatingLogo, self).__init__(**kwargs)
        self.angle = 0
        self.scale = 0.5  # 初始缩放
        self.glow_alpha = 0.0  # 发光效果透明度
        self.bind(size=self.update_graphics, pos=self.update_graphics)
        Clock.schedule_once(self.init_graphics, 0)
        
    def init_graphics(self, dt):
        self.update_graphics()
        # 启动入场动画：缩放 + 旋转
        scale_anim = Animation(scale=1.0, duration=1.0, t='out_elastic')
        scale_anim.start(self)
        
        # 发光效果动画
        glow_anim = Animation(glow_alpha=1.0, duration=0.8, t='out_expo')
        glow_anim += Animation(glow_alpha=0.3, duration=0.8, t='in_out_sine')
        glow_anim.repeat = True
        glow_anim.start(self)
        
        # 持续旋转动画
        Clock.schedule_once(self.start_rotation, 0.5)
        
    def start_rotation(self, dt):
        self.rotation_anim = Animation(angle=360, duration=2.5, t='linear')
        self.rotation_anim.repeat = True
        self.rotation_anim.bind(on_progress=self.on_rotation_progress)
        self.rotation_anim.start(self)
        
    def on_rotation_progress(self, animation, widget, progress):
        self.angle = animation.animated_properties['angle'] * progress
        self.update_graphics()
        
    def update_graphics(self, *args):
        self.canvas.clear()
        with self.canvas:
            center_x, center_y = self.center
            radius = min(self.width, self.height) * 0.25 * self.scale
            
            PushMatrix()
            Scale(self.scale, self.scale, 1, origin=(center_x, center_y))
            Rotate(angle=self.angle, axis=(0, 0, 1), origin=(center_x, center_y))
            
            # 外层发光环
            for i in range(3):
                alpha = self.glow_alpha * (0.8 - i * 0.25)
                Color(0.12, 0.53, 0.9, alpha)
                glow_radius = radius * (1.8 + i * 0.3)
                Ellipse(pos=(center_x - glow_radius, center_y - glow_radius), 
                       size=(glow_radius*2, glow_radius*2))
            
            # 主品牌环 - 12个旋转光束
            for i in range(12):
                angle = (self.angle + i * 30) * math.pi / 180
                beam_length = radius * 1.2
                start_radius = radius * 0.6
                
                start_x = center_x + math.cos(angle) * start_radius
                start_y = center_y + math.sin(angle) * start_radius
                end_x = center_x + math.cos(angle) * beam_length
                end_y = center_y + math.sin(angle) * beam_length
                
                # 渐变光束效果
                alpha = 1.0 - (i / 12.0) * 0.6
                Color(0.2, 0.7, 1.0, alpha)
                Line(points=[start_x, start_y, end_x, end_y], width=dp(4), cap='round')
            
            # 中心Logo - 增强版"X"标志
            Color(1, 1, 1, 1)
            logo_size = radius * 0.8
            line_width = dp(6)
            
            # X 的两条对角线 - 带圆角效果
            Line(points=[
                center_x - logo_size/2, center_y - logo_size/2,
                center_x + logo_size/2, center_y + logo_size/2
            ], width=line_width, cap='round')
            Line(points=[
                center_x - logo_size/2, center_y + logo_size/2,
                center_x + logo_size/2, center_y - logo_size/2
            ], width=line_width, cap='round')
            
            # 中心装饰点
            Color(0.4, 0.8, 1.0, 0.9)
            dot_radius = radius * 0.15
            Ellipse(pos=(center_x - dot_radius, center_y - dot_radius), 
                   size=(dot_radius*2, dot_radius*2))
            
            # 内圈装饰环
            Color(0.6, 0.9, 1.0, 0.4)
            inner_radius = radius * 0.4
            for angle_deg in range(0, 360, 45):
                angle_rad = math.radians(angle_deg)
                x = center_x + math.cos(angle_rad) * inner_radius
                y = center_y + math.sin(angle_rad) * inner_radius
                small_dot = dp(2)
                Ellipse(pos=(x - small_dot, y - small_dot), size=(small_dot*2, small_dot*2))
            
            PopMatrix()


class LoadingDots(Widget):
    """增强版加载点动画组件"""
    
    def __init__(self, **kwargs):
        super(LoadingDots, self).__init__(**kwargs)
        self.dots_data = [
            {'scale': 1.0, 'alpha': 1.0, 'y_offset': 0},
            {'scale': 0.7, 'alpha': 0.7, 'y_offset': 0},
            {'scale': 0.4, 'alpha': 0.4, 'y_offset': 0}
        ]
        self.animation_phase = 0
        self.bind(size=self.update_graphics, pos=self.update_graphics)
        Clock.schedule_once(self.init_animation, 0.5)
        
    def init_animation(self, dt):
        self.update_graphics()
        Clock.schedule_interval(self.animate_dots, 0.35)
        
    def animate_dots(self, dt):
        # 波浪式动画效果
        self.animation_phase = (self.animation_phase + 1) % 9
        
        for i in range(3):
            phase_offset = (self.animation_phase + i * 3) % 9
            if phase_offset < 3:
                # 上升阶段
                self.dots_data[i]['scale'] = 0.6 + (phase_offset / 3) * 0.8
                self.dots_data[i]['alpha'] = 0.5 + (phase_offset / 3) * 0.5
                self.dots_data[i]['y_offset'] = (phase_offset / 3) * dp(5)
            elif phase_offset < 6:
                # 保持阶段
                self.dots_data[i]['scale'] = 1.4
                self.dots_data[i]['alpha'] = 1.0
                self.dots_data[i]['y_offset'] = dp(5)
            else:
                # 下降阶段
                progress = (phase_offset - 6) / 3
                self.dots_data[i]['scale'] = 1.4 - progress * 0.8
                self.dots_data[i]['alpha'] = 1.0 - progress * 0.5
                self.dots_data[i]['y_offset'] = dp(5) - progress * dp(5)
                
        self.update_graphics()
        
    def update_graphics(self, *args):
        self.canvas.clear()
        with self.canvas:
            center_x, center_y = self.center
            dot_spacing = dp(18)
            
            for i, dot_data in enumerate(self.dots_data):
                Color(1, 1, 1, dot_data['alpha'])
                radius = dp(3) * dot_data['scale']
                x = center_x + (i - 1) * dot_spacing
                y = center_y + dot_data['y_offset']
                Ellipse(pos=(x - radius, y - radius), size=(radius*2, radius*2))


class SplashScreen(FloatLayout):
    """X-chat-GPT 启动画面 - 品牌化增强版本"""
    
    title = StringProperty("X-chat-GPT")
    subtitle = StringProperty("智能对话助手") 
    on_complete = ObjectProperty(None)
    
    def __init__(self, title=None, subtitle=None, on_complete=None, **kwargs):
        super(SplashScreen, self).__init__(**kwargs)
        
        # 文本清洗，提升Windows兼容性
        self.title = sanitize_text(title or self.title)
        self.subtitle = sanitize_text(subtitle or self.subtitle)
        self.on_complete = on_complete
        
        # 延迟初始化，避免在字体注册前创建Label
        Clock.schedule_once(self.init_ui, 0.1)
        
    def init_ui(self, dt):
        """延迟初始化UI，确保字体已注册"""
        self.setup_ui()
        Clock.schedule_once(self.start_sequence, 0.2)
        
    def setup_ui(self):
        """构建启动界面UI组件"""
        # 渐变背景画布
        with self.canvas.before:
            # 深蓝渐变背景
            Color(0.1, 0.15, 0.25, 1)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
            
            # 添加渐变效果模拟
            Color(0.05, 0.1, 0.2, 0.3)
            self.gradient_rect = Rectangle(size=self.size, pos=self.pos)
            
        self.bind(size=self._update_bg, pos=self._update_bg)
        
        # 旋转Logo组件
        self.logo = RotatingLogo(
            size_hint=(None, None),
            size=(dp(160), dp(160)),
            pos_hint={'center_x': 0.5, 'center_y': 0.62}
        )
        self.add_widget(self.logo)
        
        # 应用标题 - 增强视觉效果
        self.title_label = Label(
            text=self.title,
            font_size=sp(32),
            color=(1, 1, 1, 0),
            pos_hint={'center_x': 0.5, 'center_y': 0.42},
            size_hint=(None, None),
            size=(dp(280), dp(50)),
            markup=True,
            font_name='Roboto'
        )
        # 添加标题阴影效果
        with self.title_label.canvas.before:
            Color(0, 0, 0, 0.5)
            self.title_shadow = Rectangle(size=self.title_label.size, pos=(self.title_label.pos[0] + 2, self.title_label.pos[1] - 2))
        self.add_widget(self.title_label)
        
        # 副标题 - 更精致的样式
        self.subtitle_label = Label(
            text=self.subtitle,
            font_size=sp(16),
            color=(0.8, 0.9, 1.0, 0),
            pos_hint={'center_x': 0.5, 'center_y': 0.36},
            size_hint=(None, None),
            size=(dp(200), dp(30)),
            italic=True,
            font_name='Roboto'
        )
        self.add_widget(self.subtitle_label)
        
        # 加载指示器 - 更动感
        self.loading_dots = LoadingDots(
            size_hint=(None, None),
            size=(dp(80), dp(30)),
            pos_hint={'center_x': 0.5, 'center_y': 0.22}
        )
        self.add_widget(self.loading_dots)
        
        # 品牌标语
        self.tagline_label = Label(
            text=sanitize_text("智能对话 · 无限可能"),
            font_size=sp(12),
            color=(0.6, 0.7, 0.9, 0),
            pos_hint={'center_x': 0.5, 'center_y': 0.16},
            size_hint=(None, None),
            size=(dp(150), dp(20)),
            font_name='Roboto'
        )
        self.add_widget(self.tagline_label)
        
        # 版本信息 - 更低调
        self.version_label = Label(
            text="v1.2.0 Enhanced",
            font_size=sp(9),
            color=(0.4, 0.5, 0.7, 0),
            pos_hint={'center_x': 0.5, 'center_y': 0.08},
            size_hint=(None, None),
            size=(dp(100), dp(18)),
            font_name='Roboto'
        )
        self.add_widget(self.version_label)
        
    def _update_bg(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos
        # Ensure gradient overlay follows window size/pos as well to avoid static dark block
        if hasattr(self, 'gradient_rect') and self.gradient_rect is not None:
            self.gradient_rect.size = self.size
            self.gradient_rect.pos = self.pos
        
    def start_sequence(self, dt=None):
        """启动增强版渐入动画序列"""
        Clock.schedule_once(self.animate_title, 1.0)    # Logo动画后显示标题
        Clock.schedule_once(self.animate_subtitle, 1.4)  # 0.4秒后副标题
        Clock.schedule_once(self.animate_tagline, 1.8)   # 品牌标语
        Clock.schedule_once(self.animate_version, 2.2)   # 版本信息
        Clock.schedule_once(self.complete_splash, 3.8)   # 4秒总时长
        
    def animate_title(self, dt):
        # 标题淡入 + 轻微上浮效果
        title_anim = Animation(color=(1, 1, 1, 1), duration=0.8, t='out_expo')
        title_anim &= Animation(pos_hint={'center_x': 0.5, 'center_y': 0.44}, duration=0.8, t='out_expo')
        title_anim.start(self.title_label)
        
    def animate_subtitle(self, dt):
        Animation(color=(0.8, 0.9, 1.0, 1), duration=0.6, t='out_expo').start(self.subtitle_label)
        
    def animate_tagline(self, dt):
        Animation(color=(0.6, 0.7, 0.9, 1), duration=0.6, t='out_expo').start(self.tagline_label)
        
    def animate_version(self, dt):
        Animation(color=(0.4, 0.5, 0.7, 1), duration=0.5, t='out_expo').start(self.version_label)
        
    def complete_splash(self, dt):
        """完成启动界面，执行优雅退出动画"""
        # 整体淡出 + 轻微缩放效果
        fade_out = Animation(opacity=0, duration=0.7, t='in_expo')
        scale_out = Animation(size=(self.width * 0.95, self.height * 0.95), duration=0.7, t='in_expo')
        
        combined_anim = fade_out & scale_out
        combined_anim.bind(on_complete=self._on_fade_complete)
        combined_anim.start(self)
        
    def _on_fade_complete(self, animation, widget):
        """淡出动画完成，调用回调"""
        if self.on_complete:
            self.on_complete()