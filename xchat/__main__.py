import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.animation import Animation
from kivy.clock import Clock
import threading
import requests
import random
import os
import sys
import re
from kivy.core.text import LabelBase
from kivy.uix.floatlayout import FloatLayout

# 添加父目录到sys.path以导入根目录模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 添加增强主题管理器导入，支持角色主题化
from enhanced_themes import ThemeManager, ENHANCED_THEMES, hex_to_rgba
from splash_screen import SplashScreen  # 导入启动界面

# Window配置 - 移动端适配
Window.softinput_mode = "below_target"
Window.keyboard_anim_args = {'d': .2, 't': 'in_out_expo'}
Window.keyboard_mode = 'managed'

# 配置区
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")  # 从环境变量读取，默认为空
USER_NAME = "用户"

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

# 为XChatAndroidApp类添加主题管理
class XChatAndroidApp(App):
    def __init__(self, **kwargs):
        super(XChatAndroidApp, self).__init__(**kwargs)
        self.theme_manager = ThemeManager()
        self.assistant_type = self.theme_manager.current_assistant  # 保持兼容性
        self.splash_shown = False
        print("[XChat] App initialized. splash_shown=False, assistant=", self.assistant_type)
        
    def build(self):
        print("[XChat] build() called. splash_shown=", self.splash_shown)
        # 确保先注册中文字体（Windows/Android/Linux）
        try:
            register_cjk_fonts()
            print("[XChat] CJK fonts registered")
        except Exception as e:
            print("[XChat] register_cjk_fonts failed:", e)
        
        # 首次启动显示启动页
        if not self.splash_shown:
            self.splash_shown = True
            print("[XChat] Returning SplashScreen as root")
            return SplashScreen(title=sanitize_text("X-chat-GPT"), subtitle=sanitize_text("智能对话助手"), on_complete=self.on_splash_complete)
        
        # 应用增强主题配色
        theme = self.theme_manager.get_current_theme()
        print(f"[XChat] Current theme keys: {list(theme.keys())}")
        print(f"[XChat] Background color: {theme.get('background', 'NOT FOUND')}")
        Window.clearcolor = hex_to_rgba(theme["background"])
        print("[XChat] Building main UI with theme:", self.assistant_type, self.theme_manager.current_mode)
        print(f"[XChat] Current window size: {Window.size}")

        # 主布局
        main_layout = BoxLayout(orientation="vertical", spacing=dp(8), padding=dp(10))
        
        # 主布局背景绘制
        with main_layout.canvas.before:
            from kivy.graphics import Color, Rectangle
            bg_color = hex_to_rgba(theme["background"])
            print(f"[XChat] Main layout bg color: {bg_color}")
            self._bg_color_instr = Color(*bg_color)
            self._bg_rect = Rectangle(pos=main_layout.pos, size=main_layout.size)
        
        # 绑定背景矩形跟随布局变化
        def update_bg_rect(instance, value):
            self._bg_rect.pos = instance.pos
            self._bg_rect.size = instance.size
        main_layout.bind(pos=update_bg_rect, size=update_bg_rect)
        
        # 窗口设置一个最小尺寸
        try:
            if hasattr(Window, 'minimum_width'):
                Window.minimum_width = 640.0
                Window.minimum_height = 480.0
                print(f"[XChat] Set minimum window size: {Window.minimum_width}x{Window.minimum_height}")
        except Exception as e:
            print(f"[XChat] Failed to set minimum window size: {e}")
        
        # 标题栏 - 应用主题颜色
        title_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(60), spacing=dp(10))
        
        role_icon_display = theme['role_icon'] if not IS_WINDOWS else ''
        title_label = Label(
            text=f"[color={theme['primary']}]" + sanitize_text(role_icon_display) + f"[/color] [b]{sanitize_text(theme['role_name'])}[/b]",
            markup=True,
            color=hex_to_rgba(theme['text_primary']),
            font_size=theme['title_size'],
            size_hint_x=0.7,
            text_size=(None, None),
            halign="left", valign="middle",
            font_name='Roboto'
        )
        self.title_label = title_label
        title_layout.add_widget(title_label)
        
        print(f"[XChat] Title label created with color: {hex_to_rgba(theme['text_primary'])}")
        
        # 角色选择器 - 主题化外观
        self.assistant_spinner = Spinner(
            text=self.assistant_type,
            values=list(ENHANCED_THEMES.keys()),
            size_hint=(0.3, 1),
            color=hex_to_rgba(theme['button_text']),
            background_color=hex_to_rgba(theme['primary']),
            font_name='Roboto'
        )
        self.assistant_spinner.bind(text=self.on_assistant_change)
        title_layout.add_widget(self.assistant_spinner)
        main_layout.add_widget(title_layout)
        
        # 聊天历史区域 - 应用主题背景
        self.chat_history = ChatHistory()
        main_layout.add_widget(self.chat_history)
        print("[XChat] Chat history added")
        
        # 输入区域 - 使用主题化样式并增强视觉效果
        input_layout = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(10))
        
        # 创建输入框容器以支持边框效果
        input_container = BoxLayout(
            size_hint_x=0.8,
            padding=dp(2)
        )
        
        self.input_box = TextInput(
            hint_text="输入消息...",
            font_size=sp(16),
            background_color=hex_to_rgba(theme['input_bg']),
            foreground_color=hex_to_rgba(theme['text_primary']),
            cursor_color=hex_to_rgba(theme['primary']),
            multiline=False,
            padding=[dp(15), dp(15)],
            font_name='Roboto'
        )
        
        # 添加输入框边框效果
        with input_container.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            self.input_border_color = Color(*hex_to_rgba(theme['input_border']))
            self.input_border = RoundedRectangle(
                pos=input_container.pos,
                size=input_container.size,
                radius=[dp(8)]
            )
        def _update_input_border(self, instance, value=None):
            """在输入容器移动或尺寸变化时，更新其圆角边框的位置和大小。"""
            try:
                if hasattr(self, 'input_border') and self.input_border is not None:
                    self.input_border.pos = instance.pos
                    self.input_border.size = instance.size
            except Exception as e:
                print(f"[XChat] _update_input_border error: {e}")
        # 将局部函数赋给实例属性，供Kivy绑定使用
        self._update_input_border = _update_input_border
        input_container.bind(pos=self._update_input_border, size=self._update_input_border)
        try:
            # 立即同步一次，避免初始阶段在(0,0)出现残留色块
            self._update_input_border(input_container)
        except Exception:
            pass
        
        input_container.add_widget(self.input_box)
        self.input_box.bind(on_text_validate=self.send_message)
        input_layout.add_widget(input_container)

        # 发送按钮 - 增强视觉效果
        self.send_btn = Button(
            text="发送",
            font_size=sp(16),
            background_color=hex_to_rgba(theme['primary']),
            background_normal='',  # 移除默认背景
            color=hex_to_rgba(theme['button_text']),
            size_hint_x=0.2,
            font_name='Roboto'
        )
        self.send_btn.bind(on_press=self.send_message)
        input_layout.add_widget(self.send_btn)

        main_layout.add_widget(input_layout)

        # 初始欢迎消息
        Clock.schedule_once(lambda dt: self.chat_history.add_message(
            "系统", 
            theme['greeting'], 
            hex_to_rgba(theme['secondary']), 
            animate=True
        ), 0.5)

        print("[XChat] Main UI built")
        return main_layout

    def on_splash_complete(self):
        print("[XChat] Splash complete callback invoked")
        # 直接替换根部件，遵循Kivy推荐做法
        try:
            new_root = self.build()
            self.root = new_root
            print("[XChat] Root replaced with main UI")
        except Exception as e:
            print("[XChat] Failed to replace root:", e)
            try:
                # 兜底：尝试在现有root中清空后加入
                if self.root:
                    self.root.clear_widgets()
                    self.root.add_widget(self.build())
                    print("[XChat] Fallback: embedded new UI into existing root")
            except Exception as e2:
                print("[XChat] Fallback failed:", e2)
        
        # 在UI替换后，强制刷新一次画布，避免黑屏
        try:
            if self.root:
                self.root.canvas.ask_update()
                for child in self.root.walk():
                    if hasattr(child, 'canvas'):
                        child.canvas.ask_update()
                print("[XChat] Canvases refreshed after root replacement")
        except Exception as e:
            print("[XChat] Canvas refresh error:", e)
        
        # 启动页完成后，切换到主界面（安全地替换根部件）
        # [REMOVED obsolete _switch_root implementation]

    def on_assistant_change(self, spinner, text):
        self.assistant_type = text  # 与主题管理器同步
        self.theme_manager.set_assistant(text)
        theme = self.theme_manager.get_current_theme()
        Window.clearcolor = hex_to_rgba(theme["background"])  # 更新窗口背景颜色
        print("[XChat] Assistant changed to:", text)
        
        # 更新根背景画布颜色
        if hasattr(self, '_bg_color_instr'):
            try:
                self._bg_color_instr.rgba = hex_to_rgba(theme['background'])
            except Exception as e:
                print('[XChat] update bg color failed:', e)
        
        # 更新标题和按钮颜色
        role_icon_display = theme['role_icon'] if not IS_WINDOWS else ''
        self.title_label.text = f"[color={theme['primary']}]" + sanitize_text(role_icon_display) + f"[/color] [b]{sanitize_text(theme['role_name'])}[/b]"
        self.title_label.color = hex_to_rgba(theme['text_primary'])
        # 修复属性名错误：send_button -> send_btn
        if hasattr(self, 'send_btn'):
            self.send_btn.background_color = hex_to_rgba(theme['primary'])
            self.send_btn.color = hex_to_rgba(theme['button_text'])
        # 同步更新 Spinner 与输入框样式
        if hasattr(self, 'assistant_spinner'):
            self.assistant_spinner.background_color = hex_to_rgba(theme['primary'])
            self.assistant_spinner.color = hex_to_rgba(theme['button_text'])
        if hasattr(self, 'input_box'):
            self.input_box.background_color = hex_to_rgba(theme['input_bg'])
            self.input_box.foreground_color = hex_to_rgba(theme['text_primary'])
            self.input_box.cursor_color = hex_to_rgba(theme['primary'])
        if hasattr(self, 'input_border_color'):
            try:
                self.input_border_color.rgba = hex_to_rgba(theme['input_border'])
            except Exception as e:
                print('[XChat] update input border color failed:', e)

    def send_message(self, instance):
        user_text = self.input_box.text.strip()
        if not user_text:
            return

        theme = self.theme_manager.get_current_theme()
        print(f"[XChat] User sent: {user_text}")
        
        # 添加用户消息到聊天历史
        self.chat_history.add_message(USER_NAME, user_text, hex_to_rgba(theme['user_bubble']))
        self.input_box.text = ""
        
        # 立即显示正在思考的消息
        self.chat_history.add_message("系统", "🤔 正在思考中...", hex_to_rgba(theme['system_bubble']))
        
        # 异步获取API响应
        threading.Thread(target=self.get_api_response, args=(user_text,), daemon=True).start()

    def get_api_response(self, user_input):
        theme = self.theme_manager.get_current_theme()
        try:
            print(f"[XChat] Getting API response for: {user_input}")
            
            # 调用API获取响应
            response_text = self.call_deepseek_api(user_input)
            print(f"[XChat] API response received: {response_text[:100]}...")
            
            # 使用Clock.schedule_once确保UI更新在主线程执行
            Clock.schedule_once(lambda dt: self.chat_history.add_message(
                theme['role_name'], 
                response_text, 
                hex_to_rgba(theme['bot_bubble'])
            ), 0)

        except Exception as e:
            print(f"[XChat] API error: {str(e)}")
            # 错误消息也需要在主线程更新
            Clock.schedule_once(lambda dt: self.chat_history.add_message(
                "系统", 
                f"❌ 获取回复失败: {str(e)}", 
                hex_to_rgba(theme['error'])
            ), 0)

    def call_deepseek_api(self, prompt):
        try:
            headers = {
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            }

            # 根据角色切换不同的系统提示词
            system_prompts = {
                "TrumpGPT": "You are Donald Trump. Speak in a confident and assertive tone.",
                "DickGPT": "You are an energetic and playful assistant.",
                "X-GPT": "你是一个认真负责的中文AI助手，请使用简洁、直观、友好的语气回答用户的问题。",
            }
            system_prompt = system_prompts.get(self.assistant_type, "你是一个AI助手，请用中文回答。")

            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            }

            # 优化超时和重试策略 - 减少超时时间提升响应性能
            max_retries = 2
            retry_count = 0
            timeout = 15  # 从30秒优化为15秒
            response = None

            while retry_count <= max_retries:
                try:
                    response = requests.post(
                        "https://api.deepseek.com/v1/chat/completions",
                        headers=headers,
                        json=payload,
                        timeout=timeout
                    )
                    response.raise_for_status()
                    break
                except requests.exceptions.Timeout as e:
                    retry_count += 1
                    if retry_count > max_retries:
                        raise requests.exceptions.Timeout("API响应超时，请检查网络连接或稍后重试")
                except requests.exceptions.RequestException as e:
                    raise

            if not response or not response.json().get("choices") or len(response.json()["choices"]) == 0:
                return "❌ API响应错误，请稍后重试"

            raw_response = response.json()["choices"][0]["message"]["content"]
            return raw_response

        except requests.exceptions.Timeout:
            return "⏰ 请求超时(15秒)，请检查网络连接或稍后重试"
        except requests.exceptions.ConnectionError:
            return "🌐 网络连接失败，请检查网络设置"
        except requests.exceptions.HTTPError as e:
            if "401" in str(e):
                return "🔑 API密钥无效，请检查配置"
            elif "429" in str(e):
                return "⏳ API调用频率限制，请稍后重试"
            else:
                return f"❌ HTTP错误: {str(e)}"
        except Exception as e:
            return f"❌ API请求失败: {str(e)}"

class ChatHistory(ScrollView):
    def __init__(self, **kwargs):
        super(ChatHistory, self).__init__(**kwargs)
        self.layout = GridLayout(cols=1, size_hint_y=None, spacing=dp(5), padding=dp(10))
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.add_widget(self.layout)

    def add_message(self, sender, message, color, animate=True):
        # 文本清洗，避免Windows下Emoji显示异常
        sender = sanitize_text(str(sender))
        message = sanitize_text(str(message))
        
        # 添加发送者标签 - 使用更明确的颜色对比
        sender_label = Label(
            text=f"● {sender}",
            size_hint_y=None,
            height=dp(25),
            color=color,
            font_size=sp(14),
            halign='left',
            text_size=(self.width - dp(20), None),
            font_name='Roboto',
            markup=True
        )
        sender_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (value - dp(20), None)))
        
        # 添加消息内容 - 增强对比度
        message_color = (0.95, 0.95, 0.95, 1) if sender != "系统" else (0.8, 0.8, 0.8, 1)
        
        message_label = Label(
            text=message,
            size_hint_y=None,
            height=self.calculate_height(message),
            color=message_color,
            font_size=sp(13),
            halign='left',
            text_size=(self.width - dp(40), None),
            markup=True,
            font_name='Roboto'
        )
        message_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (value - dp(40), None)))
        
        if animate:
            # 添加淡入动画
            sender_label.opacity = 0
            message_label.opacity = 0
            
        self.layout.add_widget(sender_label)
        self.layout.add_widget(message_label)
        
        if animate:
            # 执行淡入动画
            Animation(opacity=1, duration=0.3).start(sender_label)
            Animation(opacity=1, duration=0.3, t='out_expo').start(message_label)

        # 延迟滚动到底部，确保动画完成后滚动
        Clock.schedule_once(lambda dt: setattr(self, 'scroll_y', 0), 0.35 if animate else 0.1)

    def calculate_height(self, text):
        # 更精确的文本高度计算
        lines = text.count('\n') + 1
        line_height = sp(16)
        padding = dp(10)
        return max(dp(30), lines * line_height + padding)

# 使用系统内置中文字体作为 Kivy 默认字体（覆盖 Roboto），避免中文显示为未知符号
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

if __name__ == "__main__":
    # 直接运行原版应用，避免加载增强版入口
    register_cjk_fonts()
    XChatAndroidApp().run()