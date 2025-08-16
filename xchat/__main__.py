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

# Window配置 - 移动端适配
Window.softinput_mode = "below_target"
Window.keyboard_anim_args = {'d': .2, 't': 'in_out_expo'}
Window.keyboard_mode = 'managed'

# 配置区
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "sk-24f56defebb149a9a7c356d39296af07")  # 优先从环境变量读取
USER_NAME = "用户"

# 主题配置 - 使用Android兼容字体
THEMES = {
    "X-GPT": {"primary": "#1e88e5", "secondary": "#64b5f6", "accent": "#0d47a1", "font": "Roboto"},
    "唐纳德": {"primary": "#e65100", "secondary": "#ed8936", "accent": "#bf360c", "font": "Roboto"},
    "DickGPT兄弟": {"primary": "#9c27b0", "secondary": "#ba68c8", "accent": "#6a0080", "font": "Roboto"},
    "原版DeepSeek": {"primary": "#0288d1", "secondary": "#4fc3f7", "accent": "#01579b", "font": "Roboto"}
}

class ChatHistory(ScrollView):
    def __init__(self, **kwargs):
        super(ChatHistory, self).__init__(**kwargs)
        self.layout = GridLayout(cols=1, size_hint_y=None, spacing=dp(5), padding=dp(10))
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.add_widget(self.layout)

    def add_message(self, sender, message, color, animate=True):
        # 添加发送者标签
        sender_label = Label(
            text=f"{sender}:",
            size_hint_y=None,
            height=dp(25),
            color=color,
            font_size=sp(14),
            halign='left',
            text_size=(self.width - dp(20), None)
        )
        sender_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (value - dp(20), None)))
        
        # 添加消息内容
        message_label = Label(
            text=message,
            size_hint_y=None,
            height=self.calculate_height(message),
            color=(1, 1, 1, 1),
            font_size=sp(12),
            halign='left',
            text_size=(self.width - dp(40), None),
            markup=True
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

class XChatAndroidApp(App):
    def __init__(self, **kwargs):
        super(XChatAndroidApp, self).__init__(**kwargs)
        self.assistant_type = "X-GPT"

    def build(self):
        # 主布局 - 使用dp单位
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        main_layout.background_color = (0.1, 0.1, 0.1, 1)

        # 标题栏 - 使用dp和sp单位
        title_bar = BoxLayout(size_hint_y=None, height=dp(50), padding=dp(10))
        title_label = Label(
            text="X-chat-GPT",
            font_size=sp(20),
            color=(1, 1, 1, 1),
            halign='center'
        )
        title_bar.add_widget(title_label)
        title_bar.background_color = tuple(int(THEMES[self.assistant_type]["primary"][i:i+2], 16)/255 for i in (1, 3, 5)) + (1,)
        main_layout.add_widget(title_bar)

        # 助手选择器区域 - 使用dp和sp单位
        selector_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10), padding=[dp(5), 0])
        selector_label = Label(
            text="选择回答者:",
            size_hint_x=None,
            width=dp(100),
            color=(1, 1, 1, 1),
            font_size=sp(14)
        )
        selector_layout.add_widget(selector_label)

        self.assistant_spinner = Spinner(
            text=self.assistant_type,
            values=list(THEMES.keys()),
            size_hint_x=None,
            width=dp(180),
            background_normal='',
            background_color=tuple(int(THEMES[self.assistant_type]["primary"][i:i+2], 16)/255 for i in (1, 3, 5)) + (1,),
            color=(1, 1, 1, 1),
            font_size=sp(14)
        )
        self.assistant_spinner.bind(text=self.on_assistant_change)
        selector_layout.add_widget(self.assistant_spinner)
        
        # 添加一些弹性空间
        selector_layout.add_widget(Label())
        main_layout.add_widget(selector_layout)

        # 聊天历史
        self.chat_history = ChatHistory(size_hint_y=1)
        main_layout.add_widget(self.chat_history)

        # 输入区域 - 使用dp和sp单位，优化移动端体验
        input_layout = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(10), padding=[0, dp(5)])
        self.input_box = TextInput(
            hint_text="输入消息...",
            font_size=sp(16),
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            multiline=False,
            size_hint_x=0.8,
            padding=[dp(10), dp(10)]
        )
        # 绑定回车键发送消息
        self.input_box.bind(on_text_validate=self.send_message)
        input_layout.add_widget(self.input_box)

        self.send_btn = Button(
            text="发送",
            font_size=sp(16),
            background_color=tuple(int(THEMES[self.assistant_type]["primary"][i:i+2], 16)/255 for i in (1, 3, 5)) + (1,),
            color=(1, 1, 1, 1),
            size_hint_x=0.2
        )
        self.send_btn.bind(on_press=self.send_message)
        input_layout.add_widget(self.send_btn)

        main_layout.add_widget(input_layout)

        # 初始消息
        Clock.schedule_once(lambda dt: self.chat_history.add_message(
            "系统", 
            "你好！欢迎使用X-chat-GPT。选择一个回答者，然后输入您的问题。", 
            (0.6, 0.2, 0.8, 1), 
            animate=True
        ), 0.5)

        return main_layout

    def on_assistant_change(self, spinner, text):
        """处理助手选择变化 - 添加动画效果"""
        self.assistant_type = text
        
        # 更新UI主题颜色 - 添加颜色变化动画
        primary_color = tuple(int(THEMES[self.assistant_type]["primary"][i:i+2], 16)/255 for i in (1, 3, 5)) + (1,)
        
        # 按钮颜色变化动画
        Animation(background_color=primary_color, duration=0.3, t='out_expo').start(self.assistant_spinner)
        Animation(background_color=primary_color, duration=0.3, t='out_expo').start(self.send_btn)
        
        # 添加切换通知消息
        assistant_names = {
            "X-GPT": "X-GPT 专业助手",
            "唐纳德": "特朗普风格助手",
            "DickGPT兄弟": "DickGPT 兄弟",
            "原版DeepSeek": "原版 DeepSeek"
        }
        
        secondary_color = tuple(int(THEMES[self.assistant_type]["secondary"][i:i+2], 16)/255 for i in (1, 3, 5)) + (1,)
        Clock.schedule_once(lambda dt: self.chat_history.add_message(
            "系统", 
            f"已切换到 {assistant_names.get(text, text)}，准备为您服务！", 
            secondary_color,
            animate=True
        ), 0.3)
        
    def send_message(self, instance):
        user_input = self.input_box.text.strip()
        if not user_input:
            return

        # 添加发送按钮按压动画
        original_size = self.send_btn.size
        shrink_anim = Animation(size=(original_size[0] * 0.9, original_size[1] * 0.9), duration=0.1)
        expand_anim = Animation(size=original_size, duration=0.1)
        shrink_anim.bind(on_complete=lambda *args: expand_anim.start(self.send_btn))
        shrink_anim.start(self.send_btn)

        # 添加用户消息
        self.chat_history.add_message(USER_NAME, user_input, (0.2, 0.8, 0.2, 1), animate=True)
        self.input_box.text = ""

        # 显示加载状态
        loading_messages = {
            "X-GPT": "🔍 正在处理任务...",
            "唐纳德": "💨 正在发推文...假新闻媒体都在看！",
            "DickGPT兄弟": "💨 尾部加速中...准备真理喷射！",
            "原版DeepSeek": "🔍 正在思考..."
        }
        
        Clock.schedule_once(lambda dt: self.chat_history.add_message(
            self.assistant_type, 
            loading_messages.get(self.assistant_type, "🔍 正在处理..."),
            tuple(int(THEMES[self.assistant_type]["secondary"][i:i+2], 16)/255 for i in (1, 3, 5)) + (1,),
            animate=True
        ), 0.2)

        # 在单独的线程中调用API
        threading.Thread(target=self.get_api_response, args=(user_input,), daemon=True).start()

    def get_api_response(self, user_input):
        try:
            response = self.call_deepseek_api(user_input)
            Clock.schedule_once(lambda dt: self.chat_history.add_message(
                self.assistant_type, 
                response,
                tuple(int(THEMES[self.assistant_type]["secondary"][i:i+2], 16)/255 for i in (1, 3, 5)) + (1,),
                animate=True
            ), 0)
        except Exception as e:
            error_messages = {
                "X-GPT": f"❌ 任务处理失败: {str(e)}",
                "唐纳德": f"💥 获取响应失败: 这肯定是假新闻媒体的错！{str(e)}",
                "DickGPT兄弟": f"💥 获取响应失败: {str(e)}",
                "原版DeepSeek": f"❌ 请求失败: {str(e)}"
            }
            Clock.schedule_once(lambda dt: self.chat_history.add_message(
                self.assistant_type, 
                error_messages.get(self.assistant_type, f"❌ 任务处理失败: {str(e)}"),
                (1, 0, 0, 1),
                animate=True
            ), 0)

    def call_deepseek_api(self, prompt):
        """调用DeepSeek API并返回响应"""
        try:
            # API密钥校验
            if not DEEPSEEK_API_KEY or len(DEEPSEEK_API_KEY) < 10:
                return "❌ API密钥无效或未设置。请配置环境变量 DEEPSEEK_API_KEY 或检查配置。"
            
            headers = {
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            }

            # 根据选择的助手类型设置不同的系统提示
            if self.assistant_type == "X-GPT":
                system_prompt = "你是x，一个由XTY创建的AI X-GPT，擅长信息收集、数据处理、文档编制、编程开发等任务。请使用中文作为工作语言，提供专业、准确的回答。"
            elif self.assistant_type == "唐纳德":
                system_prompt = f"用特朗普风格回复（使用'假新闻'、'中国'、'让美国再次伟大'等关键词，自信夸张的语气），对象是{USER_NAME}。"
            elif self.assistant_type == "DickGPT兄弟":
                system_prompt = f"用DickGPT风格回复（冲刺/受精/孵化等比喻），对象是{USER_NAME}。"
            elif self.assistant_type == "原版DeepSeek":
                system_prompt = ""  # 无任何预设，完全根据用户输入生成回复
            else:
                system_prompt = "你是一个AI助手，请使用中文回答用户的问题。"

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

if __name__ == "__main__":
    XChatAndroidApp().run()