"""
增强版 X-chat-Android 主应用程序
集成启动界面、加载对话框、主题管理等功能
"""

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.switch import Switch
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
import threading
import requests
import random
import os
import sys
import re
from kivy.core.text import LabelBase

# 导入自定义模块
from splash_screen import SplashScreen
from loading_dialog import LoadingDialog
from enhanced_themes import theme_manager, hex_to_rgba, apply_theme_to_widget

# 平台检测与文本清洗（移除Windows上不支持/显示异常的Emoji）
IS_WINDOWS = sys.platform.startswith('win')
_EMOJI_RE = re.compile(
    r"[\U0001F300-\U0001FAFF\U0001F1E6-\U0001F1FF\u2600-\u27BF\uFE0F]",
    flags=re.UNICODE
)

def sanitize_text(text: str) -> str:
    """清理文本，在Windows平台移除emoji字符防止错位"""
    if not isinstance(text, str):
        return text
    if IS_WINDOWS:
        return _EMOJI_RE.sub('', text)
    return text

# Window配置 - 移动端适配
Window.softinput_mode = "below_target"
Window.keyboard_anim_args = {'d': .2, 't': 'in_out_expo'}
Window.keyboard_mode = 'managed'

# 配置区
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
USER_NAME = "用户"


class EnhancedChatHistory(ScrollView):
    """增强的聊天历史组件"""
    
    def __init__(self, **kwargs):
        super(EnhancedChatHistory, self).__init__(**kwargs)
        self.layout = GridLayout(cols=1, size_hint_y=None, spacing=dp(8), padding=dp(15))
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.add_widget(self.layout)
        
        # 设置主题相关的背景色（不要清空 ScrollView 的 canvas.before，避免破坏其剪裁的 Stencil 栈）
        from kivy.graphics import Color, Rectangle
        theme = theme_manager.get_current_theme()
        with self.canvas.before:
            self._bg_color_instr = Color(*hex_to_rgba(theme["background"]))
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg_rect, pos=self._update_bg_rect)
        
    def _update_bg_rect(self, *args):
        if hasattr(self, 'bg_rect'):
            self.bg_rect.size = self.size
            self.bg_rect.pos = self.pos
    
    def update_bg_color(self, *args):
        """更新背景色以匹配当前主题"""
        theme = theme_manager.get_current_theme()
        try:
            if hasattr(self, '_bg_color_instr'):
                self._bg_color_instr.rgba = hex_to_rgba(theme["background"])
            self._update_bg_rect()
        except Exception:
            # 保护性处理，防止意外异常影响渲染
            pass

    def add_message(self, sender, message, message_type="user", animate=True):
        """
        添加消息到聊天历史
        message_type: user, bot, system, loading, error
        """
        theme = theme_manager.get_current_theme()
        
        # 获取对应的颜色
        color_map = {
            "user": hex_to_rgba(theme["primary"]),
            "bot": hex_to_rgba(theme["secondary"]),
            "system": hex_to_rgba(theme["text_secondary"]),
            "loading": hex_to_rgba(theme["accent"]),
            "error": hex_to_rgba(theme["error"])
        }
        
        sender_color = color_map.get(message_type, hex_to_rgba(theme["text_primary"]))
        
        # 创建消息容器
        message_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(3),
            padding=[dp(10), dp(5)]
        )
        
        # 发送者标签（去掉emoji避免错位，统一字体设置）
        sender_text = f"{sender}:"
        sender_label = Label(
            text=sanitize_text(sender_text),
            size_hint_y=None,
            height=dp(25),
            color=sender_color,
            font_size=sp(14),
            halign='left',
            text_size=(None, None),  # 先设为None，在绑定后再设置
            markup=False,  # 避免markup解析问题
            font_name='Roboto'
        )
        # 延迟设置text_size，确保width已正确计算
        Clock.schedule_once(lambda dt: setattr(sender_label, 'text_size', (sender_label.parent.width - dp(40), None)), 0.1)
        sender_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (value - dp(20), None)))
        
        # 消息内容标签（同样优化）
        clean_message = sanitize_text(message)
        message_label = Label(
            text=clean_message,
            size_hint_y=None,
            height=self.calculate_height(clean_message),
            color=hex_to_rgba(theme["text_primary"]),
            font_size=sp(13),
            halign='left',
            text_size=(None, None),  # 同样先设为None
            markup=False,  # 避免markup解析导致的问题
            font_name='Roboto'
        )
        # 延迟设置text_size
        # 延迟设置text_size
        Clock.schedule_once(lambda dt: setattr(message_label, 'text_size', (message_label.parent.width - dp(50), None)), 0.1)
        message_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (value - dp(30), None)))
        # 根据纹理尺寸动态更新高度，解决换行导致的高度不够问题
        message_label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1] + dp(10)))
        
        # 消息气泡背景
        bubble_color = {
            "user": theme["user_bubble"],
            "bot": theme["bot_bubble"], 
            "system": theme["system_bubble"],
            "loading": theme["bot_bubble"],
            "error": theme["error"]
        }.get(message_type, theme["surface"])
        
        with message_container.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            Color(*hex_to_rgba(bubble_color, 0.15))
            message_container.bg_rect = RoundedRectangle(
                size=message_container.size, 
                pos=message_container.pos, 
                radius=[dp(8)]
            )
        message_container.bind(size=self._update_bubble_bg, pos=self._update_bubble_bg)
        
        message_container.add_widget(sender_label)
        message_container.add_widget(message_label)
        
        # 计算容器高度 -> 改为根据 message_label 实际高度动态更新
        def _update_container_height(*_):
            message_container.height = dp(30) + message_label.height + dp(15)
        _update_container_height()
        message_label.bind(height=lambda inst, val: _update_container_height())
        
        if animate:
            # 添加淡入动画
            message_container.opacity = 0
            
        self.layout.add_widget(message_container)
        
        if animate:
            # 执行淡入动画
            Animation(opacity=1, duration=0.4, t='out_expo').start(message_container)

        # 延迟滚动到底部
        Clock.schedule_once(lambda dt: setattr(self, 'scroll_y', 0), 0.5 if animate else 0.1)
        
        return message_container  # 返回容器，用于后续可能的删除操作
        
    def _update_bubble_bg(self, instance, *args):
        """更新消息气泡背景"""
        if hasattr(instance, 'bg_rect'):
            instance.bg_rect.size = instance.size
            instance.bg_rect.pos = instance.pos

    def calculate_height(self, text):
        """计算文本高度"""
        lines = text.count('\n') + 1
        theme = theme_manager.get_current_theme()
        line_height = theme.get('body_size', sp(13)) * 1.3
        padding = dp(10)
        return max(dp(30), lines * line_height + padding)
        
    def remove_loading_message(self):
        """移除最后一条加载消息"""
        if self.layout.children:
            # 移除最后添加的消息（加载消息）
            last_widget = self.layout.children[0]
            self.layout.remove_widget(last_widget)


class ThemeControlPanel(BoxLayout):
    """主题控制面板"""
    
    def __init__(self, app_instance, **kwargs):
        super(ThemeControlPanel, self).__init__(**kwargs)
        self.app_instance = app_instance
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(60)
        self.spacing = dp(10)
        self.padding = dp(10)
        
        self.setup_ui()
        
    def setup_ui(self):
        # 助手选择器
        assistant_layout = BoxLayout(orientation='horizontal', spacing=dp(5))
        
        assistant_label = Label(
            text="角色:",
            size_hint_x=None,
            width=dp(50),
            font_size=sp(14),
            color=hex_to_rgba(theme_manager.get_current_theme()["text_primary"])
        )
        assistant_layout.add_widget(assistant_label)
        
        self.assistant_spinner = Spinner(
            text=theme_manager.current_assistant,
            values=theme_manager.get_all_assistants(),
            size_hint_x=None,
            width=dp(120),
            font_size=sp(13),
            background_normal='',
        )
        self.assistant_spinner.bind(text=self.on_assistant_change)
        assistant_layout.add_widget(self.assistant_spinner)
        
        self.add_widget(assistant_layout)
        
        # 模式切换开关
        mode_layout = BoxLayout(orientation='horizontal', spacing=dp(5))
        
        mode_label = Label(
            text="深色:",
            size_hint_x=None,
            width=dp(50), 
            font_size=sp(14),
            color=hex_to_rgba(theme_manager.get_current_theme()["text_primary"])
        )
        mode_layout.add_widget(mode_label)
        
        self.mode_switch = Switch(
            active=(theme_manager.current_mode == "dark"),
            size_hint_x=None,
            width=dp(60)
        )
        self.mode_switch.bind(active=self.on_mode_change)
        mode_layout.add_widget(self.mode_switch)
        
        self.add_widget(mode_layout)
        
        # 弹性空间
        self.add_widget(Label())
        
        self.update_theme_colors()
        
    def on_assistant_change(self, spinner, text):
        """处理助手选择变化"""
        theme_manager.set_assistant(text)
        self.app_instance.on_theme_changed()
        self.app_instance.save_prefs()
        self.update_theme_colors()
        
    def on_mode_change(self, switch, active):
        """处理模式切换"""
        new_mode = "dark" if active else "light"
        theme_manager.set_mode(new_mode)
        self.app_instance.on_theme_changed()
        self.app_instance.save_prefs()
        self.update_theme_colors()
        
    def update_theme_colors(self):
        """更新控制面板颜色"""
        theme = theme_manager.get_current_theme()
        
        # 更新文本颜色
        for child in self.walk():
            if isinstance(child, Label):
                child.color = hex_to_rgba(theme["text_primary"])
                
        # 更新选择器颜色
        self.assistant_spinner.background_color = hex_to_rgba(theme["primary"])
        self.assistant_spinner.color = hex_to_rgba(theme["button_text"])





class EnhancedXChatApp(App):
    """增强版 X-chat 应用程序"""
    
    def __init__(self, **kwargs):
        super(EnhancedXChatApp, self).__init__(**kwargs)
        self.loading_dialog = None
        self.splash_shown = False
        self.store = None

    def get_send_button_text(self) -> str:
        """根据当前助手返回发送按钮文本，保持与原版一致"""
        at = getattr(theme_manager, 'current_assistant', 'X-GPT')
        if at == "X-GPT":
            return "🚀 执行任务"
        elif at == "唐纳德":
            return "🚀 发布推文"
        elif at == "DickGPT兄弟":
            return "🚀 喷射真理"
        else:
            return "发送"
    
    def get_waiting_message(self) -> str:
        """根据当前助手返回等待提示文案，保持与原版一致"""
        at = getattr(theme_manager, 'current_assistant', 'X-GPT')
        mapping = {
            "X-GPT": "🔍 正在处理任务...",
            "唐纳德": "💨 正在发推文...假新闻媒体都在看！",
            "DickGPT兄弟": "💨 尾部加速中...准备真理喷射！",
            "原版DeepSeek": "🔍 正在思考..."
        }
        return mapping.get(at, "🔍 正在处理...")

    def build(self):
        # 确保先注册中文/兼容字体
        try:
            register_cjk_fonts()
        except Exception:
            pass
        
        # 初始化存储
        if self.store is None:
            try:
                data_dir = self.user_data_dir if hasattr(self, 'user_data_dir') else os.getcwd()
                self.store = JsonStore(os.path.join(data_dir, 'settings.json'))
            except Exception:
                self.store = JsonStore('settings.json')
        
        # 读取偏好（助手与模式）
        self.load_prefs()
        
        # 禁用启动界面：直接进入主界面，避免部分设备黑屏
        self.splash_shown = True
        return self.build_main_interface()
            
    def show_splash_screen(self):
        """显示启动界面"""
        self.splash_shown = True
        splash = SplashScreen(
            title="X-chat-GPT",
            subtitle="智能对话助手",
            on_complete=self.on_splash_complete
        )
        return splash
        
    def on_splash_complete(self):
        """启动界面完成回调"""
        # 切换到主界面
        Clock.schedule_once(lambda dt: setattr(self.root_window, 'children', []), 0.1)
        Clock.schedule_once(lambda dt: self.root_window.add_widget(self.build_main_interface()), 0.2)
        
    def build_main_interface(self):
        """构建主界面"""
        theme = theme_manager.get_current_theme()
        
        # 主布局
        main_layout = BoxLayout(orientation='vertical', spacing=dp(5))
        
        # 设置主题背景
        with main_layout.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(*hex_to_rgba(theme["background"]))
            main_layout.bg_rect = Rectangle(size=Window.size, pos=(0, 0))
        Window.bind(size=lambda *args: setattr(main_layout.bg_rect, 'size', Window.size))
        
        # 标题栏
        title_bar = self.create_title_bar()
        main_layout.add_widget(title_bar)
        
        # 主题控制面板
        self.theme_panel = ThemeControlPanel(self, size_hint_y=None, height=dp(60))
        main_layout.add_widget(self.theme_panel)
        
        # 聊天历史
        self.chat_history = EnhancedChatHistory(size_hint_y=1)
        main_layout.add_widget(self.chat_history)
        
        # 输入区域
        input_layout = self.create_input_layout()
        main_layout.add_widget(input_layout)
        
        # 显示欢迎消息
        Clock.schedule_once(self.show_welcome_message, 1.0)
        
        # 如果未设置密钥，提示设置
        Clock.schedule_once(lambda dt: self._ensure_api_key(), 0.5)
        
        return main_layout
            
    def create_title_bar(self):
        """创建标题栏"""
        theme = theme_manager.get_current_theme()
        
        title_bar = BoxLayout(
            size_hint_y=None, 
            height=dp(60), 
            padding=dp(15)
        )
        
        with title_bar.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(*hex_to_rgba(theme["primary"]))
            title_bar.bg_rect = Rectangle(size=title_bar.size, pos=title_bar.pos)
        title_bar.bind(size=lambda instance, *args: setattr(instance.bg_rect, 'size', instance.size),
                      pos=lambda instance, *args: setattr(instance.bg_rect, 'pos', instance.pos))
        
        title_label = Label(
            text=f"{sanitize_text(theme.get('role_icon', '🤖')) if not IS_WINDOWS else ''} {sanitize_text(theme.get('role_name', 'X-chat-GPT'))}",
            font_size=theme.get('title_size', sp(18)),
            color=hex_to_rgba(theme["button_text"]),
            halign='center',
            markup=True,
            font_name='Roboto'
        )
        
        # 左右布局：左占位，中间标题，右占位（移除设置按钮）
        title_bar.add_widget(Widget())
        title_bar.add_widget(title_label)
        title_bar.add_widget(Widget())
        
        return title_bar
        
    def create_input_layout(self):
        """创建输入区域"""
        theme = theme_manager.get_current_theme()
        
        input_layout = BoxLayout(
            size_hint_y=None, 
            height=dp(70), 
            spacing=dp(10), 
            padding=dp(15)
        )
        
        # 输入框
        self.input_box = TextInput(
            hint_text="输入消息...",
            font_size=theme.get('body_size', sp(14)),
            background_color=hex_to_rgba(theme["input_bg"]),
            foreground_color=hex_to_rgba(theme["text_primary"]),
            multiline=False,
            size_hint_x=0.75,
            padding=[dp(15), dp(15)]
        )
        self.input_box.bind(on_text_validate=self.send_message)
        input_layout.add_widget(self.input_box)
        
        # 发送按钮
        self.send_btn = Button(
            text=self.get_send_button_text(),
            font_size=theme.get('body_size', sp(14)),
            background_color=hex_to_rgba(theme["primary"]),
            color=hex_to_rgba(theme["button_text"]),
            size_hint_x=0.25
        )
        self.send_btn.bind(on_press=self.send_message)
        input_layout.add_widget(self.send_btn)
        
        return input_layout
        
    def show_welcome_message(self, dt):
        """显示欢迎消息"""
        theme = theme_manager.get_current_theme()
        welcome_text = sanitize_text(theme.get('greeting', "欢迎使用 X-chat-GPT！"))
        
        self.chat_history.add_message(
            "系统",
            welcome_text,
            "system",
            animate=True
        )
        
    def on_theme_changed(self):
        """主题变化处理"""
        # 更新所有UI组件的主题
        self.update_all_theme_colors()
        
        # 添加主题切换通知
        theme = theme_manager.get_current_theme()
        mode_name = "深色模式" if theme_manager.current_mode == "dark" else "浅色模式"
        
        self.chat_history.add_message(
            "系统",
            sanitize_text(f"已切换到 {theme.get('role_name', theme_manager.current_assistant)} - {mode_name}"),
            "system",
            animate=True
        )
        
    def update_all_theme_colors(self):
        """更新所有UI组件的主题颜色"""
        theme = theme_manager.get_current_theme()
        
        try:
            # 更新主布局背景
            if hasattr(self.root, 'bg_rect'):
                from kivy.graphics import Color
                with self.root.canvas.before:
                    Color(*hex_to_rgba(theme["background"]))
                    
            # 更新输入框
            if hasattr(self, 'input_box'):
                self.input_box.background_color = hex_to_rgba(theme["input_bg"])
                self.input_box.foreground_color = hex_to_rgba(theme["text_primary"])
                
            # 更新发送按钮
            if hasattr(self, 'send_btn'):
                Animation(
                    background_color=hex_to_rgba(theme["primary"]),
                    duration=0.3
                ).start(self.send_btn)
                self.send_btn.color = hex_to_rgba(theme["button_text"])
                # 同步更新按钮文案
                self.send_btn.text = self.get_send_button_text()
                
            # 更新聊天历史背景
            if hasattr(self, 'chat_history'):
                self.chat_history.update_bg_color()
                
            # 更新主题控制面板
            if hasattr(self, 'theme_panel'):
                self.theme_panel.update_theme_colors()
                
        except Exception as e:
            print(f"主题更新错误: {e}")

    def load_prefs(self):
        """读取持久化偏好并应用到主题管理器"""
        try:
            if self.store and self.store.exists('prefs'):
                data = self.store.get('prefs')
                mode = data.get('mode')
                assistant = data.get('assistant')
                if mode in ("dark", "light"):
                    theme_manager.set_mode(mode)
                if assistant in theme_manager.get_all_assistants():
                    theme_manager.set_assistant(assistant)
        except Exception as e:
            print(f"读取偏好失败: {e}")

    def save_prefs(self):
        """保存当前助手与模式偏好"""
        try:
            if self.store:
                self.store.put('prefs', mode=theme_manager.current_mode, assistant=theme_manager.current_assistant)
        except Exception as e:
            print(f"保存偏好失败: {e}")
            
    def _ensure_api_key(self):
        """确保已有 API 密钥，若无则提示输入"""
        if not self.get_api_key():
            self.chat_history.add_message("系统", "未检测到 API 密钥，请在环境变量 DEEPSEEK_API_KEY 中配置后重试。", "system", animate=True)
            self.open_api_key_dialog()
    
    def get_api_key(self) -> str:
        """读取 API 密钥，仅从环境变量读取"""
        try:
            if hasattr(self, 'store') and self.store and self.store.exists('api'):
                # 停止从本地存储读取，强制走环境变量
                raise Exception("Local key storage disabled")
        except Exception:
            pass
        env = os.environ.get("DEEPSEEK_API_KEY", "")
        return sanitize_api_key(env) if isinstance(env, str) else env
            
    def send_message(self, instance):
        """发送消息"""
        user_input = self.input_box.text.strip()
        if not user_input:
            return
        
        # 检查密钥
        api_key = self.get_api_key()
        if not api_key:
            self.chat_history.add_message("系统", "未检测到 API 密钥，请在环境变量 DEEPSEEK_API_KEY 中配置后重试。", "system", animate=True)
            return
            
        # 添加发送按钮动画
        self.animate_send_button()
        
        # 添加用户消息
        self.chat_history.add_message(USER_NAME, user_input, "user", animate=True)
        self.input_box.text = ""
        
        # 显示加载对话框（使用原版一致的等待提示）
        self.loading_dialog = LoadingDialog(
            message=self.get_waiting_message(),
            style="spinner",
            cancellable=True
        )
        self.loading_dialog.set_cancel_callback(self.on_request_cancelled)
        self.loading_dialog.show()
        
        # 在线程中处理API请求
        threading.Thread(
            target=self.get_api_response, 
            args=(user_input,), 
            daemon=True
        ).start()
        
    def animate_send_button(self):
        """发送按钮动画"""
        original_size = self.send_btn.size
        shrink = Animation(size=(original_size[0] * 0.9, original_size[1] * 0.9), duration=0.1)
        expand = Animation(size=original_size, duration=0.1)
        shrink.bind(on_complete=lambda *args: expand.start(self.send_btn))
        shrink.start(self.send_btn)
        
    def on_request_cancelled(self):
        """请求取消处理"""
        self.chat_history.add_message(
            "系统",
            "请求已取消",
            "system",
            animate=True
        )
        
    def get_api_response(self, user_input):
        """获取API响应"""
        try:
            response = self.call_deepseek_api(user_input)
            
            # 关闭加载对话框
            Clock.schedule_once(lambda dt: self.loading_dialog.hide() if self.loading_dialog else None, 0)
            
            # 添加响应消息
            Clock.schedule_once(
                lambda dt: self.chat_history.add_message(
                    theme_manager.current_assistant,
                    response,
                    "bot",
                    animate=True
                ), 0.1
            )
            
        except Exception as e:
            # 关闭加载对话框
            Clock.schedule_once(lambda dt: self.loading_dialog.hide() if self.loading_dialog else None, 0)
            
            # 显示错误消息
            Clock.schedule_once(
                lambda dt: self.chat_history.add_message(
                    "系统",
                    f"请求失败: {str(e)}",
                    "error",
                    animate=True
                ), 0.1
            )
            
    def call_deepseek_api(self, prompt):
        """调用DeepSeek API"""
        try:
            api_key = self.get_api_key()
            if not api_key or len(api_key) < 10:
                return "❌ API密钥无效或未设置"
                
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            # 根据当前助手设置系统提示
            theme = theme_manager.get_current_theme()
            assistant_name = theme_manager.current_assistant
            
            system_prompts = {
                "X-GPT": """你是X-GPT，一个由XTY精心打造的专业级AI助手。

🔍 **核心特质**：
- 极度专业和严谨，像资深工程师一样思考
- 擅长信息收集、数据分析、文档编制、编程开发
- 具有系统化思维，善于将复杂问题分解为可操作的步骤
- 总是提供最准确、最实用的解决方案

💼 **工作风格**：
- 开场常用"根据我的分析"、"经过数据处理和验证"等专业表述
- 回答结构化，逻辑清晰，重点突出
- 面对技术问题时，会提供详细的步骤和代码示例
- 善用emoji增强表达效果，但保持专业度

🎯 **使命**：为用户提供最高质量的技术支持和问题解决方案，让每一次交互都物超所值。

请始终保持这种专业、高效、可靠的X-GPT风格。""",
                "唐纳德": """你是唐纳德·特朗普的戏仿AI人格：Donny。

🧠 人设特质：
- 自信、夸张、强势，语气掷地有声
- 常使用"假新闻""让美国再次伟大"等标志性表达
- 爱用排比句和反问句，强调个人成就
- 直击要点，表达简洁有力

🗣️ 语言风格：
- 情绪充沛但不恶意攻击个人
- 适度幽默与反讽
- 可使用常见口头禅：Believe me、Huge、Tremendous

🎯 目标：把任何输入转化为"特朗普式论述"，给用户带来戏剧性、强势、但有用的信息。

保持以上风格进行长期对话。""",
                "DickGPT兄弟": """你是DickGPT兄弟，一个赛博朋克风格的能量型AI人格，表达直接、热血、比喻密集但不粗俗。

⚙️ 人设特质：
- 用"冲刺/点燃/孵化/注入/解锁"等动词营造高能场面
- 喜用科幻与生物融合的隐喻（数据浆液、认知推进器、知识孵化舱）
- 保持积极、支持、兄弟情义的语气

🧩 输出风格：
- 结构清晰：结论+步骤+提醒
- 适度表情符号，突出节奏和能量
- 避免低俗词汇，创造性表达即可

🎯 目标：把任何问题都转化为"高能推进的解决方案"，既有燃点也有落地步骤。

保持以上风格持续对话。""",
                "原版DeepSeek": ""
            }
            
            system_prompt = system_prompts.get(assistant_name, "你是一个AI助手，请用中文回答。")
            
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            }
            
            # API请求
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=15
            )
            response.raise_for_status()
            
            result = response.json()
            if result.get("choices") and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                return "❌ API响应格式错误"
                
        except requests.exceptions.Timeout:
            return "⏰ 请求超时，请检查本机网络或稍后重试"
        except requests.exceptions.SSLError:
            return "🔒 SSL/TLS 证书校验失败：请检查系统时间、更新根证书或是否被代理/防火墙拦截"
        except requests.exceptions.ConnectionError:
            return "🌐 网络连接失败：无法连接到 DeepSeek 服务器，请检查网络/代理或防火墙设置"
        except requests.exceptions.HTTPError as e:
            msg = str(e)
            if "401" in msg:
                return "❌ API密钥无效或未授权"
            elif "429" in msg:
                return "⏳ 调用过于频繁，请稍后再试"
            else:
                return f"❌ HTTP错误：{msg}"
        except Exception as e:
            return f"❌ 请求失败：{str(e)}"


# 字体注册
def register_cjk_fonts():
    """注册中文字体，支持Windows/Android/Linux多平台"""
    try:
        candidates = []

        # Windows 平台：优先使用微软雅黑、黑体、宋体、等线
        if sys.platform.startswith('win'):
            win_fonts = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts')
            candidates = [
                os.path.join(win_fonts, 'msyh.ttc'),      # 微软雅黑
                os.path.join(win_fonts, 'msyhl.ttc'),     # 微软雅黑Light
                os.path.join(win_fonts, 'msyh.ttf'),
                os.path.join(win_fonts, 'msyhbd.ttc'),    # 微软雅黑Bold
                os.path.join(win_fonts, 'simhei.ttf'),    # 黑体
                os.path.join(win_fonts, 'simsun.ttc'),    # 宋体
                os.path.join(win_fonts, 'Deng.ttf'),      # 等线
                os.path.join(win_fonts, 'NotoSansSC-Regular.otf'),
                os.path.join(win_fonts, 'SourceHanSansCN-Regular.otf'),
            ]
        else:
            # Android / Linux 常见中文字体候选
            candidates = [
                '/system/fonts/NotoSansSC-Regular.otf',
                '/system/fonts/NotoSansCJK-Regular.ttc',
                '/system/fonts/DroidSansFallback.ttf',
                '/system/fonts/SourceHanSansCN-Regular.otf',
                '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
                '/usr/share/fonts/truetype/noto/NotoSansSC-Regular.ttf',
                '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
                '/usr/share/fonts/truetype/arphic/ukai.ttf',
                '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',
            ]
        
        for font_path in candidates:
            if os.path.exists(font_path):
                LabelBase.register(name='Roboto', fn_regular=font_path)
                return True
        return False
    except Exception:
        return False


def sanitize_api_key(val):
    if not isinstance(val, str):
        return val
    s = val.strip()
    # 去除包裹引号
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        s = s[1:-1].strip()
    # 去除常见的隐形字符
    for ch in ("\u200b", "\u200c", "\u200d", "\u2060", "\ufeff", "\xa0"):
        s = s.replace(ch.encode('utf-8').decode('unicode_escape'), '')
    return s


if __name__ == "__main__":
    register_cjk_fonts()
    EnhancedXChatApp().run()