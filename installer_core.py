"""Core install utilities for Chery-Tiggo9-Install-software.

This module keeps the original installation/uninstallation ADB logic,
while exposing reusable functions for CLI and GUI frontends.
"""

from __future__ import annotations

import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from pyperclip import copy


VERSION = "10.0.0"


def is_legal_filename(name: str) -> bool:
    return bool(re.match(r"^[a-zA-Z0-9()._-]*$", name))


def ensure_apk_name(filename: str, default_suffix: str = "") -> str:
    if not filename.lower().endswith(".apk"):
        filename = f"{filename}.apk"

    if is_legal_filename(filename):
        return filename

    # Keep the old fallback strategy when users provide unsupported file names.
    return f"The_apk_to_be_installed{default_suffix}.apk"


@dataclass
class CommandResult:
    ok: bool
    code: int
    command: str


Logger = Callable[[str], None]


def run(command: str, logger: Logger | None = None) -> CommandResult:
    if logger:
        logger(f"$ {command}")
    code = os.system(command)
    return CommandResult(ok=code == 0, code=code, command=command)


def upload_file(local_path: str | Path, remote_filename: str, logger: Logger | None = None) -> CommandResult:
    local = Path(local_path)
    return run(f'adb push "{local}" "/data/local/tmp/{remote_filename}"', logger)


def install_by_adb(remote_filename: str, logger: Logger | None = None) -> CommandResult:
    cmd = f"pm install -g /data/local/tmp/{remote_filename}"
    copy(cmd)
    if logger:
        logger("安装命令已复制到剪贴板，正在打开 adb shell。")
    return run("adb shell", logger)


def upload_and_install(
    local_path: str | Path,
    install: bool = True,
    default_suffix: str = "",
    logger: Logger | None = None,
) -> tuple[str, bool]:
    filename = ensure_apk_name(Path(local_path).name, default_suffix)
    uploaded = upload_file(local_path, filename, logger)
    if not uploaded.ok:
        return filename, False

    if install:
        installed = install_by_adb(filename, logger)
        return filename, installed.ok
    return filename, True


def batch_install(folder: str | Path, logger: Logger | None = None) -> tuple[list[str], str]:
    folder_path = Path(folder)
    apk_files = sorted([p for p in folder_path.iterdir() if p.suffix.lower() == ".apk"])

    installed_names: list[str] = []
    cmds: list[str] = []

    for index, apk in enumerate(apk_files, 1):
        remote_name, ok = upload_and_install(apk, install=False, default_suffix=str(index), logger=logger)
        if ok:
            installed_names.append(remote_name)
            cmds.append(f"pm install -g /data/local/tmp/{remote_name}")

    command_chain = " & ".join(cmds)
    if command_chain:
        copy(command_chain)

    return installed_names, command_chain


def uninstall(package_name: str, manual: bool = True, logger: Logger | None = None) -> CommandResult:
    cmd = f"pm uninstall {package_name}" if manual else f"adb shell pm uninstall {package_name}"
    if manual:
        copy(cmd)
        return run("adb shell", logger)
    return run(cmd, logger)


def clear_cache(logger: Logger | None = None) -> list[CommandResult]:
    steps = [
        run('adb shell "cd /data/local/tmp/ && du -sh"', logger),
        run('adb shell "cd /data/local/tmp/ && ls -lh"', logger),
        run("adb shell rm -rf /data/local/tmp/*", logger),
    ]
    return steps


def enable_autonavi(logger: Logger | None = None) -> CommandResult:
    return run("adb shell pm enable com.autonavi.amapauto", logger)


def disable_autonavi(logger: Logger | None = None) -> CommandResult:
    return run("adb shell pm disable-user com.autonavi.amapauto", logger)


def quick_actions() -> dict[str, str]:
    return {
        "激活 shizuku": "adb shell sh /storage/emulated/0/Android/data/moe.shizuku.privileged.api/start.sh",
        "激活权限狗": "adb shell sh /storage/emulated/0/Android/data/com.web1n.permissiondog/files/starter.sh",
        "激活 tasker 读取日志": "adb shell pm grant net.dinglisch.android.taskerm android.permission.READ_LOGS",
        "激活 tasker 写安全设置": "adb shell pm grant net.dinglisch.android.taskerm android.permission.WRITE_SECURE_SETTINGS",
        "激活无障碍管理器": "adb shell pm grant com.accessibilitymanager android.permission.WRITE_SECURE_SETTINGS",
        "激活导航投屏 com.navi.tool": "adb shell pm grant com.navi.tool android.permission.READ_LOGS",
        "激活悬浮窗 com.dayang": "adb shell appops set com.dayang SYSTEM_ALERT_WINDOW allow",
        "激活小黑屋": "adb shell dpm set-device-owner web1n.stopapp/.receiver.AdminReceiver",
        "开启无线调试 5555": "adb tcpip 5555",
        "重启 adb 服务": "adb kill-server && adb start-server",
    }


def run_quick_action(name: str, logger: Logger | None = None) -> CommandResult:
    actions = quick_actions()
    return run(actions[name], logger)


def list_packages(logger: Logger | None = None) -> CommandResult:
    return run("adb shell pm list packages", logger)


def open_help() -> CommandResult:
    return run("start https://github.com/zuo-qirun/Chery-Tiggo9-Install-software/wiki")


def launch_update() -> CommandResult:
    subprocess.Popen("./update.exe")
    return CommandResult(ok=True, code=0, command="./update.exe")
