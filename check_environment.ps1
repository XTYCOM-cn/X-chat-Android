# 检查Python安装
Write-Host "检查Python安装..."
Try {
    python --version
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Python未安装或未添加到PATH"
    }
} Catch {
    Write-Host "Python未安装或未添加到PATH: $_"
}

# 检查pip安装
Write-Host "\n检查pip安装..."
Try {
    pip --version
    if ($LASTEXITCODE -ne 0) {
        Write-Host "pip未安装或未添加到PATH"
    } else {
        # 检查Buildozer安装
        Write-Host "\n检查Buildozer安装..."
        pip list | Select-String -Pattern "buildozer"
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Buildozer未安装"
        } else {
            Write-Host "Buildozer已安装"
        }
    }
} Catch {
    Write-Host "pip未安装或未添加到PATH: $_"
}

# 检查环境变量
Write-Host "\n检查环境变量..."
Write-Host "ANDROID_HOME: $env:ANDROID_HOME"
Write-Host "ANDROID_NDK_HOME: $env:ANDROID_NDK_HOME"

# 检查Buildozer.spec文件
Write-Host "\n检查buildozer.spec文件..."
if (Test-Path -Path "buildozer.spec") {
    Write-Host "buildozer.spec文件存在"
    Get-Content -Path "buildozer.spec" | Select-Object -First 10
} else {
    Write-Host "buildozer.spec文件不存在"
}