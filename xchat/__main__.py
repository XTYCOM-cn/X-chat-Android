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
from kivy.uix.modalview import ModalView
from kivy.storage.jsonstore import JsonStore


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
DEEPSEEK_API_KEY = ""  # 可选：默认密钥（建议留空，或使用环境变量 DEEPSEEK_API_KEY）
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

def sanitize_api_key(val):
    if not isinstance(val, str):
        return val
    s = val.strip()
    # 去除包裹引号
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        s = s[1:-1].strip()
    # 精准移除常见不可见字符（零宽/不换行空格/BOM等）
    invisible_chars = ["\u200b", "\u200c", "\u200d", "\u2060", "\ufeff", "\xa0"]
    s = s.translate({ord(ch): None for ch in invisible_chars})
    return s

# 局部工具：日志中掩码显示密钥
def mask_key(k: str) -> str:
    if not isinstance(k, str) or not k:
        return ""
    if len(k) <= 10:
        return "***"
    return f"{k[:6]}...{k[-4:]}"

# 为XChatAndroidApp类添加主题管理
class XChatAndroidApp(App):
    def __init__(self, **kwargs):
        super(XChatAndroidApp, self).__init__(**kwargs)
        self.theme_manager = ThemeManager()
        self.assistant_type = self.theme_manager.current_assistant  # 保持兼容性
        self.splash_shown = False
        self.store = None
        print("[XChat] App initialized. splash_shown=False, assistant=", self.assistant_type)
        
    def build(self):
        print("[XChat] build() called. splash_shown=", self.splash_shown)
        # 确保先注册中文字体（Windows/Android/Linux）
        try:
            register_cjk_fonts()
            print("[XChat] CJK fonts registered")
        except Exception as e:
            print("[XChat] register_cjk_fonts failed:", e)
        
        # 初始化持久化存储（与增强版保持一致路径策略）
        if self.store is None:
            try:
                data_dir = self.user_data_dir if hasattr(self, 'user_data_dir') else os.getcwd()
                store_path = os.path.join(data_dir, 'settings.json')
                print(f"[XChat] Initializing JsonStore at: {store_path}")
                self.store = JsonStore(store_path)
                try:
                    has_api = self.store.exists('api')
                    sample = ''
                    if has_api:
                        kv = self.store.get('api').get('key', '')
                        if isinstance(kv, str):
                            sample = mask_key(sanitize_api_key(kv))
                    print(f"[XChat] JsonStore ready. api.exists={has_api}, sample={sample}")
                except Exception as e:
                    print("[XChat] JsonStore post-init check failed:", e)
            except Exception:
                try:
                    fallback_path = 'settings.json'
                    print(f"[XChat] JsonStore fallback path: {fallback_path}")
                    self.store = JsonStore(fallback_path)
                    try:
                        has_api = self.store.exists('api')
                        print(f"[XChat] Fallback store api.exists={has_api}")
                    except Exception as e:
                        print("[XChat] Fallback store check failed:", e)
                except Exception:
                    self.store = None
                    print("[XChat] JsonStore unavailable; continue without local settings")
        # [fix] removed stray outer except block that caused invalid try/except structure
        
        # 首次启动显示启动页
        if not self.splash_shown:
            # 禁用启动页：直接进入主界面，避免部分设备黑屏
            self.splash_shown = True
            print("[XChat] Splash disabled; building main UI directly")
            # 直接继续构建主界面（不返回 SplashScreen）
            # 不return，这样会执行下面主界面构建逻辑
        
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
            text=f"[color={theme['primary']}]{sanitize_text(role_icon_display)}[/color] [b]{sanitize_text(theme['role_name'])}[/b]",
            markup=True,
            color=hex_to_rgba(theme['text_primary']),
            font_size=theme['title_size'],
            size_hint_x=0.6,
            text_size=(None, None),
            halign="left", valign="middle",
            font_name='Roboto'
        )
        self.title_label = title_label
        title_layout.add_widget(title_label)
        
        # 角色选择器 - 主题化外观
        self.assistant_spinner = Spinner(
            text=self.assistant_type,
            values=list(ENHANCED_THEMES.keys()),
            size_hint=(0.4, 1),
            color=hex_to_rgba(theme['button_text']),
            background_color=hex_to_rgba(theme['primary']),
            font_name='Roboto'
        )
        self.assistant_spinner.bind(text=self.on_assistant_change)
        title_layout.add_widget(self.assistant_spinner)
        
        # 移除：设置按钮
        # self.settings_btn = Button(
        #     text="设置",
        #     size_hint=(None, 1),
        #     width=dp(80),
        #     background_color=hex_to_rgba(theme['primary']),
        #     color=hex_to_rgba(theme['button_text']),
        #     font_name='Roboto'
        # )
        # title_layout.add_widget(self.settings_btn)
        
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
        # 添加输入框边框效果
        with input_container.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            self.input_border_color = Color(*hex_to_rgba(theme['input_border']))
            self.input_border = RoundedRectangle(
                pos=input_container.pos,
                size=input_container.size,
                radius=[dp(8)]
            )
        def _update_input_border(instance, value=None):
            """在输入容器移动或尺寸变化时，更新其圆角边框的位置和大小。"""
            try:
                if hasattr(self, 'input_border') and self.input_border is not None:
                    self.input_border.pos = instance.pos
                    self.input_border.size = instance.size
            except Exception as e:
                print(f"[XChat] _update_input_border error: {e}")
        
        # 将局部函数赋给实例属性，供Kivy绑定使用
        input_container.bind(pos=lambda instance, value: _update_input_border(instance, value), 
                           size=lambda instance, value: _update_input_border(instance, value))
        try:
            # 立即同步一次，避免初始阶段在(0,0)出现残留色块
            _update_input_border(input_container)
        except Exception:
            pass
        # 再次在下一帧和稍后一帧同步，确保在布局稳定后位置正确
        Clock.schedule_once(lambda dt: _update_input_border(input_container), 0)
        Clock.schedule_once(lambda dt: _update_input_border(input_container), 0.1)
        
        input_container.add_widget(self.input_box)
        self.input_box.bind(on_text_validate=self.send_message)
        input_layout.add_widget(input_container)

        # 发送按钮 - 增强视觉效果
        self.send_btn = Button(
            text=self.get_send_button_text(),
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

    def get_api_key(self):
        """优先使用本地 JsonStore，其次环境变量，最后内置常量（不推荐内置）。"""
        # 1) 本地存储
        try:
            if hasattr(self, 'store') and self.store and self.store.exists('api'):
                val = self.store.get('api').get('key', '')
                if isinstance(val, str):
                    k = sanitize_api_key(val)
                    print(f"[XChat] get_api_key: using STORE, len={len(k)}, sample={mask_key(k)}")
                    if k:
                        return k
                else:
                    print("[XChat] get_api_key: STORE key is non-string")
        except Exception as e:
            print("[XChat] get_api_key STORE error:", e)
        
        # 2) 环境变量
        env = os.environ.get("DEEPSEEK_API_KEY", "")
        if isinstance(env, str):
            k = sanitize_api_key(env)
            print(f"[XChat] get_api_key: using ENV, len={len(k)}, sample={mask_key(k)}")
            if k:
                return k
        else:
            print("[XChat] get_api_key: ENV key is non-string")
        
        # 3) 内置常量（不推荐，仅作兜底）
        if isinstance(DEEPSEEK_API_KEY, str) and len(DEEPSEEK_API_KEY.strip()) >= 10:
            k = sanitize_api_key(DEEPSEEK_API_KEY)
            print(f"[XChat] get_api_key: using BUILTIN, len={len(k)}, sample={mask_key(k)}")
            return k
        return ""

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
            # 按原版脚本同步更新按钮文本
            try:
                self.send_btn.text = self.get_send_button_text()
            except Exception:
                pass
        # 移除对 settings_btn 的引用
        # 同步更新 Spinner 与输入框样式
        if hasattr(self, 'assistant_spinner'):
            self.assistant_spinner.background_color = hex_to_rgba(theme['primary'])
            self.assistant_spinner.color = hex_to_rgba(theme['button_text'])
        if hasattr(self, 'input_box'):
            try:
                self.input_box.foreground_color = hex_to_rgba(theme['text_primary'])
                self.input_box.hint_text_color = hex_to_rgba(theme['hint_text'])
            except Exception:
                pass
        if hasattr(self, 'input_border_color'):
            try:
                self.input_border_color.rgba = hex_to_rgba(theme['input_border'])
            except Exception as e:
                print('[XChat] update input border color failed:', e)

    def get_send_button_text(self) -> str:
        """根据助手类型返回发送按钮文案，保持与原版一致。"""
        at = str(getattr(self, 'assistant_type', '') or '').strip()
        if at in ("X-GPT", "XGPT", "XGpt"):
            return "🚀 执行任务"
        if at in ("唐纳德", "TrumpGPT", "Donny", "唐纳德·特朗普"):
            return "🚀 发布推文"
        if at in ("DickGPT兄弟", "DickGPT"):
            return "🚀 喷射真理"
        return "发送"

    def get_waiting_message(self) -> str:
        """根据助手类型返回等待提示文案，保持与原版一致。"""
        at = str(getattr(self, 'assistant_type', '') or '').strip()
        if at in ("X-GPT", "XGPT", "XGpt"):
            return "🔍 正在处理任务..."
        if at in ("唐纳德", "TrumpGPT", "Donny", "唐纳德·特朗普"):
            return "💨 正在发推文...假新闻媒体都在看！"
        if at in ("DickGPT兄弟", "DickGPT"):
            return "💨 尾部加速中...准备真理喷射！"
        return "🤔 正在思考中..."

    def send_message(self, instance):
        user_text = self.input_box.text.strip()
        print(f"[XChat] send_message called, input_text='{user_text}', len={len(user_text)}")
        
        if not user_text:
            print("[XChat] Empty input, ignoring send request")
            return

        theme = self.theme_manager.get_current_theme()
        print(f"[XChat] User sent: {user_text}")
        
        # 如果未配置密钥，详细检查和提示
        api_key = self.get_api_key()
        print(f"[XChat] API key check: has_key={bool(api_key)}, len={len(api_key) if api_key else 0}")
        
        if not api_key or len(api_key) < 10:
            error_msg = "API 密钥未配置。请通过以下方式之一配置:\n" \
                       "1. 设置环境变量 DEEPSEEK_API_KEY\n" \
                       "2. 在 settings.json 中添加 {\"api\": {\"key\": \"your_key\"}}"
            if hasattr(self, 'chat_history'):
                self.chat_history.add_message("系统", error_msg, hex_to_rgba(theme['error']))
            print("[XChat] API key validation failed, message not sent")
            return
        
        print("[XChat] API key validation passed, proceeding with message")
        
        # 添加用户消息到聊天历史
        self.chat_history.add_message(USER_NAME, user_text, hex_to_rgba(theme['user_bubble']))
        self.input_box.text = ""
        
        # 立即显示根据助手类型的等待提示
        waiting = self.get_waiting_message()
        self.chat_history.add_message("系统", waiting, hex_to_rgba(theme['system_bubble']))
        
        # 异步获取API响应
        threading.Thread(target=self.get_api_response, args=(user_text,), daemon=True).start()

    def get_api_response(self, user_input):
        theme = self.theme_manager.get_current_theme()
        try:
            print(f"[XChat] Getting API response for: {user_input}")
            
            # 调用API获取响应
            response_text = self.call_deepseek_api(user_input)
            print(f"[XChat] API response received: {response_text[:100]}...")
            
            # 移除"思考中"消息并添加真实响应
            Clock.schedule_once(lambda dt: self._update_response(
                theme['role_name'], 
                response_text, 
                hex_to_rgba(theme['bot_bubble'])
            ), 0)

        except Exception as e:
            print(f"[XChat] API error: {str(e)}")
            # 移除"思考中"消息并显示错误
            Clock.schedule_once(lambda dt: self._update_response(
                "系统", 
                f"❌ 获取回复失败: {str(e)}", 
                hex_to_rgba(theme['error'])
            ), 0)

    def _update_response(self, sender, message, color):
        """移除等待提示，添加真实响应（兼容多助手文案）"""
        try:
            # 移除最后一条等待提示（兼容 X-GPT/唐纳德/DickGPT 的占位文案）
            if hasattr(self.chat_history, 'layout') and self.chat_history.layout.children:
                # Kivy 使用反向顺序，最新消息在索引 0
                waiting_text = None
                try:
                    waiting_text = self.get_waiting_message()
                except Exception:
                    waiting_text = None
                keywords = ("思考中", "处理任务", "发推", "尾部加速")
                for widget in list(self.chat_history.layout.children):
                    if hasattr(widget, 'text'):
                        wtxt = str(widget.text)
                        if (waiting_text and waiting_text in wtxt) or any(k in wtxt for k in keywords):
                            self.chat_history.layout.remove_widget(widget)
                            print("[XChat] Removed waiting message:", wtxt[:40])
                            break
            
            # 添加真实响应
            self.chat_history.add_message(sender, message, color)
            print(f"[XChat] Added response from {sender}: {message[:50]}...")
        except Exception as e:
            print(f"[XChat] _update_response error: {e}")
            # 兜底：直接添加响应
            self.chat_history.add_message(sender, message, color)

    def call_deepseek_api(self, prompt):
        try:
            api_key = self.get_api_key()
            print(f"[XChat] Using API key: {mask_key(api_key) if api_key else 'None'}")
            if not api_key or len(api_key) < 10:
                return "❌ 未配置 API 密钥(DEEPSEEK_API_KEY)"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            # 根据角色切换不同的系统提示词
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
- 每次回复前加上强化前缀："🔥 老子用认知顶体刺穿答案："或"💥 真理已射入对话框："或"⚡ 知识黏液喷射："或"🚀 看好了兄弟，这就给你受精："

🧩 输出风格：
- 结构清晰：结论+步骤+提醒
- 适度表情符号，突出节奏和能量
- 避免低俗词汇，创造性表达即可
- 必须在每个回复开头使用随机的强化前缀

🎯 目标：把任何问题都转化为"高能推进的解决方案"，既有燃点也有落地步骤。

保持以上风格持续对话。""",
                "TrumpGPT": """你是唐纳德·特朗普的戏仿AI人格：Donny。

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
                "DickGPT": """你是DickGPT兄弟，一个赛博朋克风格的能量型AI人格，表达直接、热血、比喻密集但不粗俗。

⚙️ 人设特质：
- 用"冲刺/点燃/孵化/注入/解锁"等动词营造高能场面
- 喜用科幻与生物融合的隐喻（数据浆液、认知推进器、知识孵化舱）
- 保持积极、支持、兄弟情义的语气
- 每次回复前加上强化前缀："🔥 老子用认知顶体刺穿答案："或"💥 真理已射入对话框："或"⚡ 知识黏液喷射："或"🚀 看好了兄弟，这就给你受精："

🧩 输出风格：
- 结构清晰：结论+步骤+提醒
- 适度表情符号，突出节奏和能量
- 避免低俗词汇，创造性表达即可
- 必须在每个回复开头使用随机的强化前缀

🎯 目标：把任何问题都转化为"高能推进的解决方案"，既有燃点也有落地步骤。

保持以上风格持续对话。""",
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
                    print(f"[XChat] Making API request (attempt {retry_count + 1})")
                    response = requests.post(
                        "https://api.deepseek.com/v1/chat/completions",
                        headers=headers,
                        json=payload,
                        timeout=(10, 15)  # (连接超时, 读取超时)
                    )
                    print(f"[XChat] API response status: {response.status_code}")
                    response.raise_for_status()
                    break
                except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout) as e:
                    retry_count += 1
                    print(f"[XChat] Request timeout (type: {type(e).__name__}), attempt {retry_count}")
                    if retry_count > max_retries:
                        print("[XChat] Max retries reached for timeout")
                        return "⏰ 请求超时，网络较慢或服务器繁忙，请稍后重试"
                except requests.exceptions.ConnectionError as e:
                    print(f"[XChat] True connection error: {e}")
                    return "🌐 网络连接失败，请检查网络设置"
                except requests.exceptions.RequestException as e:
                    print(f"[XChat] Request exception: {e}")
                    raise

            if not response:
                print("[XChat] No response received")
                return "❌ API响应错误，请稍后重试"
                
            try:
                response_data = response.json()
                print(f"[XChat] Response data: {response_data}")
                
                if not response_data.get("choices") or len(response_data["choices"]) == 0:
                    print("[XChat] No choices in response")
                    return "❌ API响应错误，请稍后重试"

                raw_response = response_data["choices"][0]["message"]["content"]
                print(f"[XChat] Raw response: {raw_response[:100]}...")
                # 原版 DickGPT 风格增强
                if str(self.assistant_type) in ("DickGPT", "DickGPT兄弟"):
                    raw_response = dickify_response(raw_response)
                return raw_response
                
            except Exception as json_error:
                print(f"[XChat] JSON parse error: {json_error}")
                return f"❌ 响应解析失败: {str(json_error)}"

        except requests.exceptions.Timeout:
            print("[XChat] Timeout exception caught")
            return "⏰ 请求超时(15秒)，请检查网络连接或稍后重试"
        except requests.exceptions.ConnectionError:
            print("[XChat] Connection error caught")
            return "🌐 网络连接失败，请检查网络设置"
        except requests.exceptions.HTTPError as e:
            print(f"[XChat] HTTP error caught: {e}")
            if "401" in str(e):
                return "❌ API密钥无效，请检查配置"
            elif "429" in str(e):
                return "⏳ API调用频率限制，请稍后重试"
            else:
                return f"❌ HTTP错误: {str(e)}"
        except Exception as e:
            print(f"[XChat] General exception caught: {e}")
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
            text=f"{sender}",
            size_hint_y=None,
            size_hint_x=1,
            color=color,
            font_size=sp(14),
            halign='left',
            valign='top',
            text_size=(self.width - dp(20), None),
            font_name='Roboto',
            markup=True
        )
        sender_label.bind(
            width=lambda instance, value: setattr(instance, 'text_size', (value - dp(20), None)),
            texture_size=lambda instance, value: setattr(instance, 'height', max(dp(25), value[1] + dp(6)))
        )
        
        # 添加消息内容 - 增强对比度
        message_color = (0.95, 0.95, 0.95, 1) if sender != "系统" else (0.8, 0.8, 0.8, 1)
        
        message_label = Label(
            text=message,
            size_hint_y=None,
            size_hint_x=1,
            color=message_color,
            font_size=sp(13),
            halign='left',
            valign='top',
            text_size=(self.width - dp(40), None),
            markup=True,
            font_name='Roboto'
        )
        message_label.bind(
            width=lambda instance, value: setattr(instance, 'text_size', (value - dp(40), None)),
            texture_size=lambda instance, value: setattr(instance, 'height', max(dp(30), value[1] + dp(10)))
        )
        
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


def dickify_response(text: str) -> str:
    """将普通文本转化为原版 DickGPT 风格前缀"""
    try:
        phrases = [
            "🔥 老子用认知顶体刺穿答案：",
            "💥 真理已射入对话框：",
            "⚡ 知识黏液喷射：",
            "🚀 看好了兄弟，这就给你受精：",
        ]
        import random
        return f"{random.choice(phrases)}\n{text}"
    except Exception:
        return text


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