# X-chat-Android

X-chat-GPT的Android版本，使用Kivy框架开发。

## 项目结构
- `main.py`: 应用入口点
- `android/`: Android特定配置
- `assets/`: 静态资源
- `requirements.txt`: Python依赖

## 如何构建
1. 安装Python 3.8+
2. 安装依赖: `pip install -r requirements.txt`
3. 安装Buildozer: `pip install buildozer`
4. 构建APK: `buildozer android debug`