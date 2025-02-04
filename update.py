import requests
import json
import os
import subprocess

def update_software():
    # 备份当前版本
    print("正在备份当前版本...")
    try:
        with open("installer.exe", "rb") as original_file:
            original_data = original_file.read()
        with open("installer.exe.bak", "wb") as backup_file:
            backup_file.write(original_data)
    except PermissionError:
        print("没有足够的权限访问该文件。请检查文件权限或尝试以管理员身份运行。")
    except:
        print("备份失败")
    # 获取升级信息
    url = "https://api.zuoqirun.top/software/Chery-Tiggo9-Install-software/latest.json"
    try:
        response = requests.get(url)
        data = json.loads(response.text)
        update_url, version = data["update_url"], data["version"]
        print("最新版本：", version)
        print("更新日志：\n", data["update_log"])

    except:
        print("获取升级信息失败")

    # 解析链接
    try:
        result = subprocess.run(["installer.exe", "-v"], capture_output=True, text=True)
        print("当前版本：", result.stdout)
        if version in result.stdout:
            print("当前已是最新版本")
        else:
            ans = input("发现新版本，是否升级？(Y/N, defult: Y)")
            if ans.lower() == "n":
                print("取消升级")
            else:
                print("开始升级")
                print("正在下载升级包...")
                update_result = requests.get(update_url)
                print("下载完成，正在安装...")
                with open("installer.exe", "wb") as f:
                    f.write(update_result.content)
                print("升级成功")
    except OSError:
        print("未找到安装程序或安装程序已损坏")
        print("开始重新安装")
        print("正在下载安装包...")
        update_result = requests.get(update_url)
        print("下载完成，正在安装...")
        with open("installer.exe", "wb") as f:
            f.write(update_result.content)
        print("升级成功")
    except:
        print("升级失败，已为您回退到当前版本")
        with open("installer.exe.bak", "rb") as backup_file:
            backup_data = backup_file.read()
        with open("installer.exe", "wb") as f:
            f.write(backup_data)
if __name__ == "__main__":
    update_software()
    os.system("pause")