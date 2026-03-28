"""Tkinter GUI frontend for Chery-Tiggo9 installer."""

from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

import installer_core as core


class InstallerGUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(f"Chery Tiggo9 Installer v{core.VERSION}")
        self.geometry("900x640")
        self._build_ui()

    def _build_ui(self) -> None:
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        notebook.add(self._build_install_tab(notebook), text="安装")
        notebook.add(self._build_uninstall_tab(notebook), text="卸载")
        notebook.add(self._build_quick_tab(notebook), text="快捷操作")

        self.log = scrolledtext.ScrolledText(self, height=12)
        self.log.pack(fill=tk.BOTH, expand=False, padx=10, pady=(0, 10))
        self._write("欢迎使用图形版安装器。")

    def _build_install_tab(self, parent: ttk.Notebook) -> ttk.Frame:
        frame = ttk.Frame(parent)

        ttk.Button(frame, text="选择 APK 并安装", command=self.install_one).pack(fill=tk.X, padx=8, pady=8)
        ttk.Button(frame, text="选择文件夹批量安装", command=self.install_batch).pack(fill=tk.X, padx=8, pady=8)
        ttk.Button(frame, text="清理 /data/local/tmp 缓存", command=self.clear_cache).pack(fill=tk.X, padx=8, pady=8)
        ttk.Button(frame, text="禁用原车机高德", command=lambda: self._run_simple(core.disable_autonavi, "禁用成功", "禁用失败")).pack(fill=tk.X, padx=8, pady=8)
        ttk.Button(frame, text="启用原车机高德", command=lambda: self._run_simple(core.enable_autonavi, "启用成功", "启用失败")).pack(fill=tk.X, padx=8, pady=8)

        return frame

    def _build_uninstall_tab(self, parent: ttk.Notebook) -> ttk.Frame:
        frame = ttk.Frame(parent)

        input_row = ttk.Frame(frame)
        input_row.pack(fill=tk.X, padx=8, pady=8)

        ttk.Label(input_row, text="包名：").pack(side=tk.LEFT)
        self.pkg_name = tk.StringVar()
        ttk.Entry(input_row, textvariable=self.pkg_name).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=6)

        ttk.Button(frame, text="列出全部包名", command=lambda: core.list_packages(logger=self._write)).pack(fill=tk.X, padx=8, pady=8)
        ttk.Button(frame, text="手动卸载（复制命令并打开 shell）", command=lambda: self.uninstall(manual=True)).pack(fill=tk.X, padx=8, pady=8)
        ttk.Button(frame, text="自动卸载", command=lambda: self.uninstall(manual=False)).pack(fill=tk.X, padx=8, pady=8)

        return frame

    def _build_quick_tab(self, parent: ttk.Notebook) -> ttk.Frame:
        frame = ttk.Frame(parent)

        for name in core.quick_actions().keys():
            ttk.Button(frame, text=name, command=lambda action=name: self.quick_action(action)).pack(fill=tk.X, padx=8, pady=4)

        return frame

    def _write(self, text: str) -> None:
        self.log.insert(tk.END, f"{text}\n")
        self.log.see(tk.END)

    def _run_simple(self, fn, ok_msg: str, fail_msg: str) -> None:
        result = fn(logger=self._write)
        if result.ok:
            messagebox.showinfo("完成", ok_msg)
        else:
            messagebox.showerror("失败", fail_msg)

    def install_one(self) -> None:
        path = filedialog.askopenfilename(title="选择 APK 文件")
        if not path:
            return
        filename, ok = core.upload_and_install(path, logger=self._write)
        if ok:
            messagebox.showinfo("完成", f"已处理：{filename}")
        else:
            messagebox.showerror("失败", f"处理失败：{filename}")

    def install_batch(self) -> None:
        folder = filedialog.askdirectory(title="选择 APK 文件夹")
        if not folder:
            return
        names, cmd = core.batch_install(folder, logger=self._write)
        if not names:
            messagebox.showwarning("提示", "未在文件夹中找到 APK 文件")
            return

        if cmd:
            self._write("批量安装命令已复制到剪贴板。")
            self._write(cmd)
            core.run("adb shell", logger=self._write)

        messagebox.showinfo("完成", f"已上传 {len(names)} 个 APK")

    def uninstall(self, manual: bool) -> None:
        package = self.pkg_name.get().strip()
        if not package:
            messagebox.showwarning("提示", "请先输入包名")
            return

        result = core.uninstall(package, manual=manual, logger=self._write)
        if result.ok:
            messagebox.showinfo("完成", "卸载命令已执行")
        else:
            messagebox.showerror("失败", "卸载失败，请检查包名或 ADB 连接")

    def quick_action(self, name: str) -> None:
        result = core.run_quick_action(name, logger=self._write)
        if result.ok:
            messagebox.showinfo("完成", f"{name} 执行成功")
        else:
            messagebox.showerror("失败", f"{name} 执行失败")

    def clear_cache(self) -> None:
        if not messagebox.askyesno("确认", "确认清理 /data/local/tmp 缓存？"):
            return
        steps = core.clear_cache(logger=self._write)
        if all(step.ok for step in steps):
            messagebox.showinfo("完成", "缓存清理成功")
        else:
            messagebox.showerror("失败", "缓存清理中有步骤失败")


def run() -> None:
    app = InstallerGUI()
    app.mainloop()


if __name__ == "__main__":
    run()
