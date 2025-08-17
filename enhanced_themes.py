"""
增强主题配置模块
支持角色主题化和深色/浅色模式切换
"""

from kivy.metrics import dp, sp


class ThemeManager:
    """主题管理器"""
    
    def __init__(self):
        self.current_mode = "dark"  # dark or light
        self.current_assistant = "X-GPT"
        
        # 角色别名映射
        self.assistant_aliases = {
            "Donny": "唐纳德",
            "TrumpGPT": "唐纳德",
            "Donald": "唐纳德",
            "Trump": "唐纳德",
            "DickGPT": "DickGPT兄弟",
            "Dick": "DickGPT兄弟",
        }
        
    def get_current_theme(self):
        """获取当前活跃主题配置"""
        return ENHANCED_THEMES[self.current_assistant][self.current_mode]
        
    def set_mode(self, mode):
        """设置主题模式 (dark/light)"""
        if mode in ["dark", "light"]:
            self.current_mode = mode
            
    def set_assistant(self, assistant):
        """设置当前助手（支持别名映射）"""
        # 先检查别名映射
        actual_assistant = self.assistant_aliases.get(assistant, assistant)
        
        if actual_assistant in ENHANCED_THEMES:
            self.current_assistant = actual_assistant
            print(f"[ThemeManager] Assistant set to: {actual_assistant} (from {assistant})")
            
            # 立即应用主题背景色到窗口
            from kivy.core.window import Window
            theme = self.get_current_theme()
            Window.clearcolor = hex_to_rgba(theme["background"])
            print(f"[ThemeManager] Window background updated to: {theme['background']}")
        else:
            print(f"[ThemeManager] Unknown assistant: {assistant}")
            
    def get_all_assistants(self):
        """获取所有可用助手列表"""
        return list(ENHANCED_THEMES.keys())


# 增强主题配置 - 每个角色包含深色和浅色模式
ENHANCED_THEMES = {
    "X-GPT": {
        "dark": {
            # 基础颜色
            "primary": "#1e88e5",
            "secondary": "#64b5f6", 
            "accent": "#0d47a1",
            "background": "#121212",
            "surface": "#1e1e1e",
            "error": "#cf6679",
            
            # 文本颜色
            "text_primary": "#ffffff",
            "text_secondary": "#b3b3b3",
            "text_hint": "#666666",
            
            # 界面元素
            "input_bg": "#2a2a2a",
            "input_border": "#404040",
            "button_text": "#ffffff",
            "divider": "#333333",
            
            # 消息气泡
            "user_bubble": "#0d47a1",
            "bot_bubble": "#2a2a2a",
            "system_bubble": "#1a4d3a",
            
            # 字体配置
            "font_family": "Roboto",
            "title_size": sp(20),
            "body_size": sp(14),
            "caption_size": sp(12),
            
            # 角色特色
            "role_icon": "🤖",
            "role_name": "X-GPT 专业助手",
            "role_description": "专业的AI助手，擅长信息处理和技术支持",
            "loading_message": "🔍 正在分析处理...",
            "greeting": "你好！我是X-GPT，专业的AI助手。我可以帮您处理各种任务，包括信息查询、数据分析、编程协助等。请告诉我您需要什么帮助？"
        },
        "light": {
            # 基础颜色 - 浅色模式
            "primary": "#1565c0",
            "secondary": "#1976d2",
            "accent": "#0d47a1",
            "background": "#fafafa",
            "surface": "#ffffff",
            "error": "#d32f2f",
            
            # 文本颜色
            "text_primary": "#212121",
            "text_secondary": "#757575",
            "text_hint": "#9e9e9e",
            
            # 界面元素
            "input_bg": "#f5f5f5",
            "input_border": "#e0e0e0",
            "button_text": "#ffffff",
            "divider": "#e0e0e0",
            
            # 消息气泡
            "user_bubble": "#1565c0",
            "bot_bubble": "#f0f0f0",
            "system_bubble": "#e8f5e8",
            
            # 字体配置
            "font_family": "Roboto",
            "title_size": sp(20),
            "body_size": sp(14),
            "caption_size": sp(12),
            
            # 角色特色
            "role_icon": "🤖",
            "role_name": "X-GPT 专业助手",
            "role_description": "专业的AI助手，擅长信息处理和技术支持",
            "loading_message": "🔍 正在分析处理...",
            "greeting": "你好！我是X-GPT，专业的AI助手。我可以帮您处理各种任务，包括信息查询、数据分析、编程协助等。请告诉我您需要什么帮助？"
        }
    },
    
    "唐纳德": {
        "dark": {
            # 特朗普风格 - 深色，使用标准特朗普橙色
            "primary": "#FF8C00",      # 标准特朗普橙色
            "secondary": "#FFA500",    # 亮橙色
            "accent": "#FF4500",       # 深橙红
            "background": "#8B3E00",   # 深橙色背景（接近深色的特朗普橙）
            "surface": "#A45100",      # 稍浅一点的深橙色表面
            "divider": "#B65C00",      # 深橙系分割线
            "error": "#d32f2f",
            
            "text_primary": "#ffffff",
            "text_secondary": "#ffccbc",
            "text_hint": "#8d6e63",
            
            "input_bg": "#4a2e7c",     # 紫色输入框背景
            "input_border": "#6a4c93", # 协调的紫色边框，不再是棕色
            "button_text": "#ffffff",
            "divider": "#4e342e",
            
            "user_bubble": "#FF8C00",   # 使用特朗普橙色
            "bot_bubble": "#4a2e7c",
            "system_bubble": "#2e1a56", # 更深紫色的系统气泡
            
            "font_family": "Roboto",
            "title_size": sp(22),  # 更大的标题，显示权威
            "body_size": sp(15),
            "caption_size": sp(12),
            
            "role_icon": "🇺🇸",
            "role_name": "唐纳德·特朗普",
            "role_description": "美国前总统，以独特的沟通风格著称",
            "loading_message": "💭 正在发推...假新闻媒体都在关注！",
            "greeting": "Hello! 我是唐纳德·特朗普，美国历史上最棒的总统！相信我，没人比我更懂怎么让对话变得精彩。有什么问题尽管问，我会给你最好的答案！"
        },
        "light": {
            "primary": "#e64a19",
            "secondary": "#ff6e40",
            "accent": "#d84315",
            "background": "#fff3e0",
            "surface": "#ffffff",
            "error": "#d32f2f",
            
            "text_primary": "#3e2723",
            "text_secondary": "#5d4037",
            "text_hint": "#8d6e63",
            
            "input_bg": "#fbe9e7",
            "input_border": "#ffccbc",
            "button_text": "#ffffff",
            "divider": "#ffccbc",
            
            "user_bubble": "#e64a19",
            "bot_bubble": "#fbe9e7",
            "system_bubble": "#fff8e1",
            
            "font_family": "Roboto",
            "title_size": sp(22),
            "body_size": sp(15),
            "caption_size": sp(12),
            
            "role_icon": "🇺🇸",
            "role_name": "唐纳德·特朗普",
            "role_description": "美国前总统，以独特的沟通风格著称",
            "loading_message": "💭 正在发推...假新闻媒体都在关注！",
            "greeting": "Hello! 我是唐纳德·特朗普，美国历史上最棒的总统！相信我，没人比我更懂怎么让对话变得精彩。有什么问题尽管问，我会给你最好的答案！"
        }
    },
    
    "DickGPT兄弟": {
        "dark": {
            # DickGPT风格 - 深紫色背景
            "primary": "#7b1fa2",
            "secondary": "#9c27b0",
            "accent": "#4a148c",
            "background": "#1a0e33",  # 非常深的紫色背景
            "surface": "#2e1065",     # 深紫色表面
            "error": "#e91e63",
            
            "text_primary": "#ffffff",
            "text_secondary": "#e1bee7",
            "text_hint": "#8e24aa",
            
            "input_bg": "#4a148c",    # 深紫色输入框背景
            "input_border": "#512da8",
            "button_text": "#ffffff",
            "divider": "#4a148c",
            
            "user_bubble": "#7b1fa2",
            "bot_bubble": "#4a148c",
            "system_bubble": "#2e1065",
            
            "font_family": "Roboto",
            "title_size": sp(20),
            "body_size": sp(14),
            "caption_size": sp(12),
            
            "role_icon": "🚀",
            "role_name": "DickGPT兄弟",
            "role_description": "活力四射的AI伙伴，用独特方式传递智慧",
            "loading_message": "🚀 尾部加速中...准备智慧喷射！",
            "greeting": "嘿兄弟！我是DickGPT，你最有活力的AI伙伴！准备好接受一些不一样的智慧冲击了吗？我们一起在知识的海洋中冲浪吧！🏄‍♂️"
        },
        "light": {
            "primary": "#8e24aa",
            "secondary": "#ab47bc",
            "accent": "#6a1b9a",
            "background": "#fce4ec",
            "surface": "#ffffff",
            "error": "#c2185b",
            
            "text_primary": "#4a148c",
            "text_secondary": "#6a1b9a",
            "text_hint": "#8e24aa",
            
            "input_bg": "#f3e5f5",
            "input_border": "#e1bee7",
            "button_text": "#ffffff",
            "divider": "#e1bee7",
            
            "user_bubble": "#8e24aa",
            "bot_bubble": "#f3e5f5",
            "system_bubble": "#fff1ff",
            
            "font_family": "Roboto",
            "title_size": sp(20),
            "body_size": sp(14),
            "caption_size": sp(12),
            
            "role_icon": "🚀",
            "role_name": "DickGPT兄弟",
            "role_description": "活力四射的AI伙伴，用独特方式传递智慧",
            "loading_message": "🚀 尾部加速中...准备智慧喷射！",
            "greeting": "嘿兄弟！我是DickGPT，你最有活力的AI伙伴！准备好接受一些不一样的智慧冲击了吗？我们一起在知识的海洋中冲浪吧！🏄‍♂️"
        }
    },
    
    "原版DeepSeek": {
        "dark": {
            # 原版DeepSeek风格 - 简洁深蓝色
            "primary": "#0277bd",
            "secondary": "#0288d1",
            "accent": "#01579b",
            "background": "#0e1621",
            "surface": "#1a252f",
            "error": "#f44336",
            
            "text_primary": "#ffffff",
            "text_secondary": "#b0bec5",
            "text_hint": "#607d8b",
            
            "input_bg": "#263238",
            "input_border": "#37474f",
            "button_text": "#ffffff",
            "divider": "#37474f",
            
            "user_bubble": "#01579b",
            "bot_bubble": "#263238",
            "system_bubble": "#1e2a30",
            
            "font_family": "Roboto",
            "title_size": sp(18),  # 更简洁的字体大小
            "body_size": sp(13),
            "caption_size": sp(11),
            
            "role_icon": "🧠",
            "role_name": "DeepSeek",
            "role_description": "原版DeepSeek AI，提供纯净的AI对话体验",
            "loading_message": "🧠 深度思考中...",
            "greeting": "Hello! 我是DeepSeek，一个AI助手。我将以最直接、客观的方式回答您的问题，没有额外的个性设定或风格化表达。请问有什么可以帮助您的？"
        },
        "light": {
            "primary": "#0288d1",
            "secondary": "#03a9f4",
            "accent": "#0277bd",
            "background": "#f8f9fa",
            "surface": "#ffffff",
            "error": "#f44336",
            
            "text_primary": "#263238",
            "text_secondary": "#546e7a",
            "text_hint": "#90a4ae",
            
            "input_bg": "#f5f5f5",
            "input_border": "#e0e0e0",
            "button_text": "#ffffff",
            "divider": "#e0e0e0",
            
            "user_bubble": "#0288d1",
            "bot_bubble": "#f5f5f5",
            "system_bubble": "#e3f2fd",
            
            "font_family": "Roboto",
            "title_size": sp(18),
            "body_size": sp(13),
            "caption_size": sp(11),

            "role_icon": "🧠",
            "role_name": "DeepSeek",
            "role_description": "原版DeepSeek AI，提供纯净的AI对话体验",
            "loading_message": "🧠 深度思考中...",
            "greeting": "Hello! 我是DeepSeek，一个AI助手。我将以最直接、客观的方式回答您的问题，没有额外的个性设定或风格化表达。请问有什么可以帮助您的？"
        }
    }
}


def hex_to_rgba(hex_color, alpha=1.0):
    """将十六进制颜色转换为RGBA元组"""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 6:
        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0
        b = int(hex_color[4:6], 16) / 255.0
        return (r, g, b, alpha)
    return (1, 1, 1, alpha)  # 默认白色


def apply_theme_to_widget(widget, theme, widget_type="default"):
    """将主题应用到指定组件"""
    if widget_type == "button":
        widget.background_color = hex_to_rgba(theme["primary"])
        widget.color = hex_to_rgba(theme["button_text"])
        
    elif widget_type == "input":
        widget.background_color = hex_to_rgba(theme["input_bg"])
        widget.foreground_color = hex_to_rgba(theme["text_primary"])
        
    elif widget_type == "label":
        widget.color = hex_to_rgba(theme["text_primary"])
        
    elif widget_type == "secondary_label":
        widget.color = hex_to_rgba(theme["text_secondary"])
        
    return widget


# 全局主题管理器实例
theme_manager = ThemeManager()