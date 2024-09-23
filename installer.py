# !/usr/bin/env python
# 使用源码请标注出处
# 此代码由zuo-qirun/B站undefined_左提供
# V9版本 大版本更新！！新增禁用高德、打开高德头枕播放等多种功能！！

import os, sys, easygui, re, argparse
import modechooser
import OutputColoredText as oct

print("---------------初始化---------------")

modes = ["退出程序", "安装模式", "卸载模式(需要你知道卸载软件的包名)",
         "解决安装后高德与原车机高德HUD闪的问题(禁用原车机高德地图)", 
         "解禁原车机高德地图(恢复原车机高德地图)", "头枕播放解决方案", 
         "adb输入指令模式", "激活shizuku", "激活权限狗"]
ModeChooser = modechooser.Mode(modes)


def isLegalString(string):
    return re.match("^[a-zA-Z0-9_\-\.\(\)]*$", string)

def chooseMode():
    global ModeChooser
    print("欢迎使用Chery-Tiggo9-Install-software")
    print("本程序由Github zuo-qirun提供 使用请标明出处")
    print("本程序仅供学习和交流使用 遇到问题概不负责")
    print("若本程序出现问题，欢迎提交issues! 项目地址: https://github.com/zuo-qirun/Chery-Tiggo9-Install-software/\n\n\n")
    os.system("adb devices")
    print(oct.ColoredText( [ ("请检查上方输出在", "normal"), ("\"List of devices attached\"", "red"), 
                            ("下方是否有", "normal"), 
                            ("\"******* device\"", "red"), 
                            ("字样", "normal") ] ))
    print(oct.ColoredText([ ("若无", "normal"), 
                           ("\"device\"", "red"), 
                            ("字样，请检查是否连接车机或打开车机adb", "normal") ]))


    print("************************选择模式******************************")
    return ModeChooser.getmode()
    
def Installation():
    loop = True

    while loop:
        print("选择要上传的文件")
        path = easygui.fileopenbox("选择安装包", "选择安装包", '*')
        if path == None:
            easygui.msgbox("请重新选择文件，若再次不选择文件将会退出安装")
            path = easygui.fileopenbox("选择安装包", "选择安装包", '*.apk')
            if path == None:
                break
        print(f"您的文件路径: {path}")
        
        # 检测并生成新文件名
        filename = os.path.basename(path)
        if filename[-4:] != ".apk":
            print(oct.ColoredText([("警告：您选择的文件后缀名不为.apk，请检查文件是否正确", "red")]))
            print(oct.ColoredText([("已自动将文件后缀名改为apk", "normal")]))
            filename = filename + ".apk"
        print(f"您的文件名：{filename}")

        if not isLegalString(filename):
            print(oct.ColoredText([("检测到您的文件名不合法，文件名仅能包含", "normal"), 
                                   ("英文字符 数字 () .", "red")]))
            filename = input(oct.ColoredText([("请输入新文件名: ", "normal")]))
            if filename == "":
                print(oct.ColoredText([("由于您未输入任何文件名，已将文件名改为The_apk_to_be_installed.apk", "normal")]))
                filename = "The_apk_to_be_installed.apk"
            elif len(filename) <= 4 or filename[-4:] != ".apk":
                filename = filename + ".apk"
                print(oct.ColoredText([(f"您新输入的文件名：{filename}", "normal")]))
        else:
            print(oct.ColoredText([("您的文件名合法", "normal")]))

        if os.system(f"adb push \"{path}\" \"/data/local/tmp/{filename}\""):
            print(oct.ColoredText([("上传失败，请截图并联系作者", "red")]))
        
        print("---------------正在安装---------------")
        if input("请确认安装方式 1: 自动安装 2: 手动安装 (defule: 2)") != '1':
            print(oct.ColoredText([("请", "normal"), 
                                   ("右键这条信息", "red"), 
                                   (f"，或复制:  pm install -g /data/local/tmp/{filename}, 并", "normal"), 
                                   ("点击回车", "red")]))
            print("输入后，请手动输入exit并回车")
            os.system(f"echo pm install -g /data/local/tmp/{filename} | clip")
            if os.system("adb shell"):
                print(oct.ColoredText([("启动命令行失败，请截图并联系作者", "red")]))
        else:
            if os.system(f"adb shell pm install -g /data/local/tmp/{filename}"):
                print(oct.ColoredText([("自动安装失败，请尝试使用手动安装", "red")]))
            
        ans = input("是否清除缓存(Y/N, defult: N):")
        if ans.upper() == 'Y':
            if os.system("adb shell rm -rf /data/local/tmp/*"): #应该没写错吧......
                print(oct.ColoredText([("清除失败，请截图并联系作者", "red")]))
            print("清除成功")
            
        loopans = input("是否继续安装软件? (Y/N, defult: N):")
        loop = True if loopans == 'Y' or loopans == 'N' else False

def Uninstallation():
    print(oct.ColoredText([("此功能需有一定android开发基础，若不理解什么是包名，请安装", "normal"), 
                           ("ES文件管理器", "red"), 
                           ("或", "normal"), 
                           ("MT管理器", "red"), 
                           ("进行卸载操作", "normal")]))
    if input("是否退出该模式？(Y/N, defult: N)").upper() == 'Y':
        return
    if input("是否需要列出所有包名？(Y/N, defult: N): ").upper() == "Y":
        os.system("adb shell pm list packages")
    uninstallpackage = input("请输入要卸载的包名：")
    print(f"即将卸载: {uninstallpackage}, 请确认包名是否正确")
    os.system("pause")
    if input("请确认卸载方式 1: 自动卸载 2: 手动卸载 (defule: 2)") != '1':
        print(oct.ColoredText([("请", "normal"), 
                               ("右键这条信息", "red"), 
                               (f"，或复制:  pm uninstall {uninstallpackage}, 并", "normal"), 
                               ("点击回车", "red")]))
        print("输入后，请手动输入exit并回车")
        os.system(f"echo pm uninstall {uninstallpackage} | clip")
        if os.system("adb shell") != 0:
            print(oct.ColoredText([("启动命令行失败，请截图并联系作者", "red")]))
    else:
        if os.system(f"adb shell pm uninstall {uninstallpackage}"):
            print(oct.ColoredText([("自动卸载失败，请尝试使用手动卸载", "red")]))
        
def DisableAutonavi():
    print("此功能的原理是禁用原车机导航，仪表盘上的地图显示和车道显示可能会失效")
    if input("是否禁用？(Y/N, defult: Y)").upper() != "N":
        if os.system("adb shell pm disable-user com.autonavi.amapauto") == 0:
            print("禁用成功")
        else:
            print(oct.ColoredText([("禁用失败，请截图并联系作者", "red")]))

def EnableAutonavi():
    print("此功能是启用原车机导航，若与新版本高德冲突，HUD抬头显示功能可能会闪来闪去")
    if input("是否启用？(Y/N, defult: Y)").upper() != "N":
        if os.system("adb shell pm enable com.autonavi.amapauto") == 0:
            print("启用成功")
        else:
            print(oct.ColoredText([("启用失败，请截图并联系作者", "red")]))

def ShowSolution():
    print("先进入驾享模式")
    print("打开新装的高德的设置->播报")
    print("一直点击播报 进入高级设置")
    print("音频通道选择一个能从头枕播出来的通道 (我这里是0号通道)")
    print("返回高级设置 将使用高版本api改为1")

def ADBMode():
    print("此模式对于非专业人员来说具有一定风险，请务必确保安全！！！")
    print("请正常输入adb指令，输入exit退出")
    while True:
        command = input("ADB> ")
        if command == "exit":
            break
        if os.system(command) != 0:
            print(oct.ColoredText([("该条指令报错，请检查输入是否正确", "red")]))
            
def ActiveShizuku():
    print("激活中...")
    if os.system("adb shell sh /storage/emulated/0/Android/data/moe.shizuku.privileged.api/start.sh") == 0:
        print("激活成功！")
    else:
        print(oct.ColoredText([("激活失败，请截图并联系作者", "red")]))

def ActivePermissiondog():
    print("激活中...")
    if os.system("adb shell sh /storage/emulated/0/Android/data/com.web1n.permissiondog/files/starter.sh") == 0:
        print("激活成功！")
    else:
        print(oct.ColoredText([("激活失败，请截图并联系作者", "red")]))


while True:
    mode = chooseMode()
    if mode != ModeChooser.wrong_code:
        os.system("cls")
        if mode == 0:
            sys.exit(0)
        elif mode == 1:
            Installation()
        elif mode == 2:
            Uninstallation()
        elif mode == 3:
            DisableAutonavi()
        elif mode == 4:
            EnableAutonavi()
        elif mode == 5:
            ShowSolution()
        elif mode == 6:
            ADBMode()
        elif mode == 7:
            ActiveShizuku()
        elif mode == 8:
            ActivePermissiondog()
    os.system("pause")
    os.system("cls")
