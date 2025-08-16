import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import threading
import requests
import random

# 配置区
DEEPSEEK_API_KEY = "sk-24f56defebb149a9a7c356d39296af07"  # 替换为你的API密钥
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
        self.layout = GridLayout(cols=1, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.add_widget(self.layout)

    def add_message(self, sender, message, color):
        # 添加发送者标签
        sender_label = Label(
            text=f"{sender}:\n",
            size_hint_y=None,
            height=30,
            color=color,
            font_size=14,
            # 移除 font_name 以使用默认字体
            halign='left'
        )
        self.layout.add_widget(sender_label)

        # 添加消息内容
        message_label = Label(
            text=f"{message}\n\n",
            size_hint_y=None,
            height=self.calculate_height(message),
            color=(1, 1, 1, 1),
            font_size=12,
            # 移除 font_name 以使用默认字体
            halign='left',
            text_size=(self.width - 20, None)
        )
        self.layout.add_widget(message_label)

        # 滚动到底部
        self.scroll_y = 0

    def calculate_height(self, text):
        # 简单估算文本高度
        lines = text.count('\n') + 1
        return max(30, lines * 20)

class XChatAndroidApp(App):
    def __init__(self, **kwargs):
        super(XChatAndroidApp, self).__init__(**kwargs)
        self.assistant_type = "X-GPT"

    def build(self):
        # 主布局
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        main_layout.background_color = (0.1, 0.1, 0.1, 1)

        # 标题栏
        title_bar = BoxLayout(size_hint_y=None, height=50)
        title_label = Label(
            text="X-chat-GPT",
            font_size=20,
            # 移除 font_name 以使用默认字体
            color=(1, 1, 1, 1)
        )
        title_bar.add_widget(title_label)
        title_bar.background_color = tuple(int(THEMES[self.assistant_type]["primary"][i:i+2], 16)/255 for i in (1, 3, 5)) + (1,)
        main_layout.add_widget(title_bar)

        # 聊天历史
        self.chat_history = ChatHistory(size_hint_y=1)
        main_layout.add_widget(self.chat_history)

        # 输入区域
        input_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        self.input_box = TextInput(
            hint_text="输入消息...",
            font_size=16,
            # 移除 font_name 以使用默认字体
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1)
        )
        input_layout.add_widget(self.input_box)

        self.send_btn = Button(
            text="发送",
            font_size=16,
            # 移除 font_name 以使用默认字体
            background_color=tuple(int(THEMES[self.assistant_type]["primary"][i:i+2], 16)/255 for i in (1, 3, 5)) + (1,),
            color=(1, 1, 1, 1)
        )
        self.send_btn.bind(on_press=self.send_message)
        input_layout.add_widget(self.send_btn)

        main_layout.add_widget(input_layout)

        # 初始消息
        self.chat_history.add_message("系统", "你好！欢迎使用X-chat-GPT。请输入您的问题。", (0.6, 0.2, 0.8, 1))

        return main_layout

    def send_message(self, instance):
        user_input = self.input_box.text.strip()
        if not user_input:
            return

        # 添加用户消息
        self.chat_history.add_message(USER_NAME, user_input, (0.2, 0.8, 0.2, 1))
        self.input_box.text = ""

        # 显示加载状态
        loading_messages = {
            "X-GPT": "🔍 正在处理任务...",
            "唐纳德": "💨 正在发推文...假新闻媒体都在看！",
            "DickGPT兄弟": "💨 尾部加速中...准备真理喷射！",
            "原版DeepSeek": "🔍 正在思考..."
        }
        self.chat_history.add_message(self.assistant_type, loading_messages.get(self.assistant_type, "🔍 正在处理..."),
                                      tuple(int(THEMES[self.assistant_type]["secondary"][i:i+2], 16)/255 for i in (1, 3, 5)) + (1,))

        # 在单独的线程中调用API
        threading.Thread(target=self.get_api_response, args=(user_input,), daemon=True).start()

    def get_api_response(self, user_input):
        try:
            response = self.call_deepseek_api(user_input)
            self.chat_history.add_message(self.assistant_type, response,
                                          tuple(int(THEMES[self.assistant_type]["secondary"][i:i+2], 16)/255 for i in (1, 3, 5)) + (1,))
        except Exception as e:
            error_messages = {
                "X-GPT": f"❌ 任务处理失败: {str(e)}",
                "唐纳德": f"💥 获取响应失败: 这肯定是假新闻媒体的错！{str(e)}",
                "DickGPT兄弟": f"💥 获取响应失败: {str(e)}",
                "原版DeepSeek": f"❌ 请求失败: {str(e)}"
            }
            self.chat_history.add_message(self.assistant_type, error_messages.get(self.assistant_type, f"❌ 任务处理失败: {str(e)}"),
                                          (1, 0, 0, 1))

    def call_deepseek_api(self, prompt):
        """调用DeepSeek API并返回响应"""
        try:
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

            # 添加超时参数和重试机制
            max_retries = 2
            retry_count = 0
            timeout = 30
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
                        raise
                except requests.exceptions.RequestException as e:
                    raise

            if not response or not response.json().get("choices") or len(response.json()["choices"]) == 0:
                return "❌ API响应错误"

            raw_response = response.json()["choices"][0]["message"]["content"]
            return raw_response

        except Exception as e:
            return f"❌ API请求失败: {str(e)}"

if __name__ == "__main__":
    XChatAndroidApp().run()