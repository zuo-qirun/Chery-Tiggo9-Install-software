## Chery-Tiggo9-Install-software

一个用于奇瑞 Tiggo9 车机 ADB 安装/卸载的工具，现已重构为：

- **核心逻辑层**：`installer_core.py`（保留原有基本安装逻辑）
- **图形界面**：`gui_installer.py`（Tkinter，开箱即用）
- **命令行入口**：`installer.py`

## 运行方式

```bash
python installer.py           # 默认启动 GUI
python installer.py --cli     # 启动命令行模式
python installer.py <apk路径>  # 直接安装指定 APK
python installer.py -v        # 查看版本
```

## 说明

- 批量安装会上传 APK 到 `/data/local/tmp/`，并生成 `pm install -g ...` 命令链。
- 为兼容原有工作流，手动安装/卸载命令仍会复制到剪贴板并打开 `adb shell`。
- 快捷指令（Shizuku、权限狗、Tasker 授权等）已保留并集中管理。

## 依赖

```bash
pip install -r requirements.txt
```

## 项目地址

- GitHub: https://github.com/zuo-qirun/Chery-Tiggo9-Install-software
- Wiki: https://github.com/zuo-qirun/Chery-Tiggo9-Install-software/wiki
