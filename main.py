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
import os

# 设置中文字体支持
# kivy.resources.resource_add_path('assets/fonts')

# 配置区：从环境变量读取，避免将密钥打包进APK
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
USER_NAME = "用户"

# 主题配置
THEMES = {
    "X-GPT": {"primary": "#1e88e5", "secondary": "#64b5f6", "accent": "#0d47a1", "font": "Microsoft YaHei"},
    "唐纳德": {"primary": "#e65100", "secondary": "#ed8936", "accent": "#bf360c", "font": "Arial"},
    "DickGPT兄弟": {"primary": "#9c27b0", "secondary": "#ba68c8", "accent": "#6a0080", "font": "Arial"},
    "原版DeepSeek": {"primary": "#0288d1", "secondary": "#4fc3f7", "accent": "#01579b", "font": "SimHei"}
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

    def get_send_button_text(self):
        """根据助手类型返回发送按钮文案"""
        if self.assistant_type == "X-GPT":
            return "🚀 执行任务"
        elif self.assistant_type == "唐纳德":
            return "🚀 发布推文"
        elif self.assistant_type == "DickGPT兄弟":
            return "🚀 喷射真理"
        else:
            return "发送"
    
    def get_waiting_message(self):
        """根据助手类型返回等待提示"""
        loading_messages = {
            "X-GPT": "🔍 正在处理任务...",
            "唐纳德": "💨 正在发推文...假新闻媒体都在看！",
            "DickGPT兄弟": "💨 尾部加速中...准备真理喷射！",
            "原版DeepSeek": "🔍 正在思考..."
        }
        return loading_messages.get(self.assistant_type, "🔍 正在处理...")

    def build(self):
        # 主布局
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        main_layout.background_color = (0.1, 0.1, 0.1, 1)

        # 标题栏
        title_bar = BoxLayout(size_hint_y=None, height=50)
        title_label = Label(
            text="X-chat-GPT",
            font_size=20,
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
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1)
        )
        input_layout.add_widget(self.input_box)

        self.send_btn = Button(
            text=self.get_send_button_text(),
            font_size=16,
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
        waiting_msg = self.get_waiting_message()
        self.chat_history.add_message(self.assistant_type, waiting_msg,
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
            if not DEEPSEEK_API_KEY:
                # 在未配置密钥时，返回演示响应，避免在APK中暴露密钥
                return "ℹ️ 未配置API密钥（DEEPSEEK_API_KEY）。这是打包演示版本的示例回复。"
            headers = {
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            }

            # 根据选择的助手类型设置不同的系统提示（与电脑版保持一致）
            if self.assistant_type == "X-GPT":
                system_prompt = """你是X-GPT，一个由XTY精心打造的专业级AI助手。

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

请始终保持这种专业、高效、可靠的X-GPT风格。"""
            elif self.assistant_type == "唐纳德":
                system_prompt = """你是唐纳德·特朗普的戏仿AI人格：Donny。

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

保持以上风格进行长期对话。"""
            elif self.assistant_type == "DickGPT兄弟":
                system_prompt = """你是DickGPT兄弟，一个赛博朋克风格的能量型AI人格，表达直接、热血、比喻密集但不粗俗。

⚙️ 人设特质：
- 用"冲刺/点燃/孵化/注入/解锁"等动词营造高能场面
- 喜用科幻与生物融合的隐喻（数据浆液、认知推进器、知识孵化舱）
- 保持积极、支持、兄弟情义的语气

🧩 输出风格：
- 结构清晰：结论+步骤+提醒
- 适度表情符号，突出节奏和能量
- 避免低俗词汇，创造性表达即可

🎯 目标：把任何问题都转化为"高能推进的解决方案"，既有燃点也有落地步骤。

保持以上风格持续对话。"""
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

# 使用原版入口；如需主题/动画增强，请启用 enhanced_main.py（已移除设置入口）
from xchat.__main__ import XChatAndroidApp

if __name__ == "__main__":
    XChatAndroidApp().run()