# X-chat-GPT 安卓应用构建指南

## 前提条件
1. 安装 Python 3.7 或更高版本
2. 安装 Git
3. 确保已安装必要的依赖: `pip install --upgrade pip setuptools virtualenv`

## Buildozer 安装步骤
在 Windows 环境下，打开 PowerShell 并执行以下命令:

```powershell
# 安装必要的依赖
pip install cython==0.29.33 wheel

# 安装 buildozer
pip install buildozer
```

## 构建 APK
1. 打开 PowerShell，导航到项目目录:
   ```powershell
   cd v:\代码\X-chat-Android
   ```

2. 初始化 buildozer (如果已有 buildozer.spec 文件可跳过):
   ```powershell
   buildozer init
   ```

3. 构建 APK 文件:
   ```powershell
   buildozer android debug
   ```

## 常见问题解决
1. **SDK/NDK 缺失**: 首次构建时，Buildozer 会自动下载所需的 SDK 和 NDK，但可能需要较长时间，请耐心等待。

2. **构建速度慢**: 构建过程可能需要 30 分钟或更长时间，取决于您的网络速度和计算机性能。

3. **图标不显示**: 确保 buildozer.spec 文件中正确配置了图标路径: `icon.filename = IMG_20250811_212447.jpg`

4. **Windows 特定问题**: 如果遇到与 Windows 相关的构建问题，考虑使用 Windows Subsystem for Linux (WSL) 进行构建。

## 构建成功后
构建成功后，APK 文件将位于项目目录的 `bin` 文件夹中，文件名为 `X-chat-Android-0.1-armeabi-v7a.debug.apk` (具体名称可能略有不同)。

您可以将此 APK 文件传输到您的安卓设备上进行安装和测试。