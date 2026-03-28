#!/usr/bin/env python
"""Entry point for Chery-Tiggo9 installer.

Refactored to keep business logic in `installer_core.py` and provide
both CLI and GUI frontends.
"""

from __future__ import annotations

import argparse
import sys

import installer_core as core


def cli_menu() -> None:
    actions = {
        "1": "安装软件",
        "2": "批量安装软件",
        "3": "卸载软件",
        "4": "快捷指令",
        "5": "清除缓存",
        "0": "退出",
    }

    while True:
        print("\n=== Chery-Tiggo9-Install-software CLI ===")
        for key, label in actions.items():
            print(f"{key}. {label}")

        choice = input("请选择模式: ").strip()

        if choice == "0":
            return
        if choice == "1":
            path = input("请输入 APK 文件路径: ").strip('" ')
            filename, ok = core.upload_and_install(path, logger=print)
            print(f"完成: {filename}" if ok else f"失败: {filename}")
        elif choice == "2":
            folder = input("请输入 APK 文件夹路径: ").strip('" ')
            names, cmd = core.batch_install(folder, logger=print)
            print(f"已上传 {len(names)} 个 APK")
            if cmd:
                print("安装命令已复制到剪贴板，正在打开 adb shell...")
                core.run("adb shell", logger=print)
        elif choice == "3":
            package = input("请输入包名: ").strip()
            manual = input("手动卸载模式？(Y/n): ").strip().lower() != "n"
            result = core.uninstall(package, manual=manual, logger=print)
            print("卸载成功" if result.ok else "卸载失败")
        elif choice == "4":
            all_actions = list(core.quick_actions().keys())
            for i, name in enumerate(all_actions, 1):
                print(f"{i}. {name}")
            try:
                index = int(input("请选择快捷指令编号: ")) - 1
                if not (0 <= index < len(all_actions)):
                    raise ValueError
            except ValueError:
                print("输入错误")
                continue

            result = core.run_quick_action(all_actions[index], logger=print)
            print("执行成功" if result.ok else "执行失败")
        elif choice == "5":
            steps = core.clear_cache(logger=print)
            print("清理成功" if all(step.ok for step in steps) else "清理过程中出现错误")
        else:
            print("输入错误，请重试")


def main() -> int:
    parser = argparse.ArgumentParser(description="A Installer for Chery Tiggo9")
    parser.add_argument("apk", nargs="?", help="直接传入 APK 文件路径后立即处理")
    parser.add_argument("--cli", action="store_true", help="使用命令行模式")
    parser.add_argument("--gui", action="store_true", help="使用图形界面模式（默认）")
    parser.add_argument("-v", "--version", action="version", version=core.VERSION)
    args = parser.parse_args()

    if args.apk:
        _, ok = core.upload_and_install(args.apk, logger=print)
        return 0 if ok else 1

    use_gui = args.gui or not args.cli
    if use_gui:
        from gui_installer import run

        run()
        return 0

    cli_menu()
    return 0


if __name__ == "__main__":
    sys.exit(main())
