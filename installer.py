# !/usr/bin/env python
# 使用源码请标注出处
# 此代码由zuo-qirun/B站山本大佐在北京提供
# V9版本 大版本更新！！新增禁用高德、打开高德头枕播放等多种功能！！

import os, sys, easygui, re
print("本程序由Github zuo-qirun提供 使用请标明出处")
print("本程序仅供学习和交流使用 遇到问题概不负责")
print("若本程序出现问题，欢迎提交issues! 项目地址: https://github.com/zuo-qirun/Chery-Tiggo9-Install-software/\n\n\n")

print("---------------初始化---------------")
os.system("adb devices")
print("请检查上方输出在\033[1;31m\"List of devices attached\"下方\033[0m是否有\033[1;31m******* device\033[0m字样")
print("若无\033[1;31m\"device\"\033[0m字样，请检查是否\033[1;31m连接车机或打开车机adb\033[0m")

def isLegalString(string):
    return re.match("^[a-zA-Z0-9_\-\.\(\)]*$", string)

def chooseMode():
    print("************************选择模式******************************")
    print("0. 退出程序")
    print("1. 安装模式")
    print("2. 卸载模式(需要你知道卸载软件的包名)")
    print("3. 解决安装后高德与原车机高德HUD闪的问题(禁用高德地图)")
    print("4. 解禁原车机高德地图(恢复高德地图)")
    print("5. 头枕播放解决方案")
    print("6. adb输入指令模式")
    print("7. 激活shizuku")
    mode = input("请输入模式(0, 1, 2, 3, 4, 5, 6, 7): ")
    try:
        return int(mode)
    except:
        print("输入异常，请重新输入")
    
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
        
        '''
        # 准备上传 检测是否更改文件名
        filename = input("\033[1;31m注意阅读此处通知！！！\033[0m 是否更改文件名? 文件名\033[1;31m不能含有中文或空格!! 若含有中文或空格请在此处输入新文件名!!!!\033[0m 若无请点击回车键跳过此流程: ")
        if filename == "":
            filename = os.path.basename(path)
        elif len(filename) <= 4 or filename[-4:] != ".apk":
            filename = filename + ".apk"
        print(filename)
        # 已弃用
        '''
        # 检测并生成新文件名
        filename = os.path.basename(path)
        if filename[-4:] != ".apk":
            print("\033[1;31m警告：您选择的文件后缀名不为.apk，请检查文件是否正确\033[0m")
            print("已自动将文件后缀名改为apk")
            filename = filename + ".apk"
        print(f"您的文件名：{filename}")
        if not isLegalString(filename):
            print("检测到您的文件名不合法，文件名仅能包含\033[1;31m英文字符 数字 () .\033[0m")
            filename = input("请输入新文件名: ")
            if filename == "":
                print("由于您未输入任何文件名，已将文件名改为The_apk_to_be_installed.apk")
                filename = "The_apk_to_be_installed.apk"
            elif len(filename) <= 4 or filename[-4:] != ".apk":
                filename = filename + ".apk"
                print(f"您新输入的文件名：{filename}")
        else:
            print("您的文件名合法")
        if os.system(f"adb push \"{path}\" \"/data/local/tmp/{filename}\""):
            print("\033[1;31m上传失败，请截图并联系作者\033[0m")
        # os.system("adb shell ls -a /data/local/tmp/")   
        
        print("---------------正在安装---------------")
        if input("请确认安装方式 1: 自动安装 2: 手动安装 (defule: 2)") != '1':
            print(f"请\033[1;31m右键这条信息\033[0m，或复制:  pm install -g /data/local/tmp/{filename}，并\033[1;31m点击回车!\033[0m")
            print("输入后，请手动输入exit并回车")
            os.system(f"echo pm install -g /data/local/tmp/{filename} | clip")
            if os.system("adb shell"):
                print("\033[1;31m启动命令行失败，请截图并联系作者\033[0m")
        else:
            if os.system(f"adb shell pm install -g /data/local/tmp/{filename}"):
                print("\033[1;31m自动安装失败，请尝试使用手动安装截图并联系作者\033[0m")
            
        ans = input("是否清除缓存(Y/N, defult: N):")
        if ans.upper() == 'Y':
            if os.system("adb shell rm -rf /data/local/tmp/*"): #应该没写错吧......
                print("\033[1;31m清除失败，请截图并联系作者\033[0m")
            print("清除成功")
            
        loopans = input("是否继续安装软件? (Y/N, defult: N):")
        loop = True if loopans == 'Y' or loopans == 'N' else False

def Uninstallation():
    print("此功能需有一定android开发基础，若不理解什么是包名，请安装\033[1;31mES文件管理器\033[0m或\033[1;31mMT管理器\033[0m进行卸载操作")
    if input("是否退出该模式？(Y/N, defult: N)").upper() == 'Y':
        return
    if input("是否需要列出所有包名？(Y/N, defult: N): ").upper() == "Y":
        os.system("adb shell pm list packages")
    uninstallpackage = input("请输入要卸载的包名：")
    print(f"即将卸载: {uninstallpackage}, 请确认包名是否正确")
    os.system("pause")
    if input("请确认卸载方式 1: 自动卸载 2: 手动卸载 (defule: 2)") != '1':
        print(f"请\033[1;31m右键这条信息\033[0m，或复制:  pm uninstall {uninstallpackage}，并\033[1;31m点击回车!\033[0m")
        print("输入后，请手动输入exit并回车")
        os.system(f"echo pm uninstall {uninstallpackage} | clip")
        if os.system("adb shell") != 0:
            print("\033[1;31m启动命令行失败，请截图并联系作者\033[0m")
    else:
        if os.system(f"adb shell pm uninstall {uninstallpackage}"):
            print("\033[1;31m自动卸载失败，请尝试使用手动安装截图并联系作者\033[0m")
        
def DisableAutonavi():
    print("此功能的原理是禁用原车机导航，仪表盘上的地图显示和车道显示可能会失效")
    if input("是否禁用？(Y/N, defult: Y)").upper() != "N":
        if os.system("adb shell pm disable-user com.autonavi.amapauto") == 0:
            print("禁用成功")
        else:
            print("\033[1;31m禁用失败，请截图并联系作者\033[0m")

def EnableAutonavi():
    print("此功能是启用原车机导航，若与新版本高德冲突，HUD抬头显示功能可能会闪来闪去")
    if input("是否启用？(Y/N, defult: Y)").upper() != "N":
        if os.system("adb shell pm enable com.autonavi.amapauto") == 0:
            print("启用成功")
        else:
            print("\033[1;31m启用失败，请截图并联系作者\033[0m")

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
            print("\033[1;31m该条指令报错\033[0m")
def ActiveShizuku():
    print("激活中...")
    if os.system("adb shell sh /storage/emulated/0/Android/data/moe.shizuku.privileged.api/start.sh") == 0:
        print("激活成功！")
    else:
        print("\033[1;31m激活失败，请截图并联系作者\033[0m")


while True:
    mode = chooseMode()
    if mode != None:
        if mode < 0 or mode > 7:
            print("输入异常，请重新输入")
        else:
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
    os.system("pause")
    os.system("cls")