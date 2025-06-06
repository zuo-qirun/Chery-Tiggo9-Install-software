# !/usr/bin/env python
# 使用源码请标注出处
# 此代码由zuo-qirun/B站undefined_左提供
# V9版本 大版本更新！！新增禁用高德、打开高德头枕播放等多种功能！！

import os, sys, easygui, re, subprocess, argparse
import modechooser
import OutputColoredText as oct
from pyperclip import copy

########################################## 常量 ##########################################

VERSION = '9.9.2'

# 模式选择
modes = [oct.ColoredText([("退出程序", "red")]), 
            oct.ColoredText([("安装软件", "yellow")]), 
            oct.ColoredText([("批量安装软件", "yellow")]), 
            oct.ColoredText([("卸载软件(需要你知道卸载软件的包名)", "yellow")]),
            oct.ColoredText([("快捷指令", "magenta")]), 
            oct.ColoredText([("adb输入指令模式", "cyan")]), 
            oct.ColoredText([("清除缓存", "blue")]),  
            oct.ColoredText([("获取帮助", "green")]), 
            oct.ColoredText([("更新程序", "green")])] # ,
            # oct.ColoredText([("更新更新程序", "green")])]


submodes = [oct.ColoredText([("返回上一级", "red")]),  # 0
            oct.ColoredText([("头枕播放解决方案", "normal")]), # 1
            oct.ColoredText([("解决安装后高德与原车机高德HUD闪的问题(禁用原车机高德地图)", "magenta")]),  # 2
            oct.ColoredText([("解禁原车机高德地图(恢复原车机高德地图)", "magenta")]), # 3
            oct.ColoredText([("激活shizuku", "blue")]), # 4
            oct.ColoredText([("激活权限狗(仅一次 下次重启后无效)", "blue")]), # 5
            oct.ColoredText([("激活tasker相关", "blue")]), # 6
            oct.ColoredText([("激活无障碍管理器", "blue")]), # 7
            oct.ColoredText([("激活小黑屋", "blue")]), # 8
            oct.ColoredText([("开启无线调试(port: 5555)", "yellow")]), # 9
            oct.ColoredText([("重启adb守护进程", "yellow")])] # 10

            
ModeChooser = modechooser.Mode(modes)
SubModeChooser = modechooser.Mode(submodes)

########################################## 字符串处理相关 ##########################################
def isLegalString(string):
    return re.match("^[a-zA-Z0-9()._-]*$", string)


########################################## 模式选择 ##########################################
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

def submenu():
    global SubModeChooser
    while True:
        submode = SubModeChooser.getmode()
        os.system('cls')
        if submode == 0:
            return
        elif submode == 1:
            ShowSolution()
        elif submode == 2:
            DisableAutonavi()
        elif submode == 3:
            EnableAutonavi()
        elif submode == 4:
            # 激活shizuku
            ExecCommand('adb shell sh /storage/emulated/0/Android/data/moe.shizuku.privileged.api/start.sh')
        elif submode == 5:
            # 激活权限狗(仅一次 下次重启后无效)
            ExecCommand("adb shell sh /storage/emulated/0/Android/data/com.web1n.permissiondog/files/starter.sh")
        elif submode == 6:
            # 激活tasker相关
            ExecCommand('adb shell pm grant net.dinglisch.android.taskerm android.permission.READ_LOGS')
            ExecCommand('adb shell pm grant net.dinglisch.android.taskerm android.permission.WRITE_SECURE_SETTINGS')
        elif submode == 7:
            # 激活无障碍管理器
            ExecCommand('adb shell pm grant com.accessibilitymanager android.permission.WRITE_SECURE_SETTINGS')
        elif submode == 8:
            # 激活小黑屋
            ExecCommand('adb shell dpm set-device-owner web1n.stopapp/.receiver.AdminReceiver', fail_msg=oct.ColoredText([("激活失败，请检查是否已退出所有账号", "red")]))
        elif submode == 9:
            # 开启无线调试(port: 5555)
            ExecCommand('adb tcpip 5555')
        elif submode == 10:
            # 重启adb守护进程
            ExecCommand('adb kill-server')
            ExecCommand('adb start-server')
        os.system('pause & cls')

########################################## 安装相关 ############################################
def UploadAndInstall(path: str, install = True, default_text = "") -> str:
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
            print(oct.ColoredText([(f"由于您未输入任何文件名，已将文件名改为The_apk_to_be_installed{default_text}.apk", "normal")]))
            filename = f"The_apk_to_be_installed{default_text}.apk"
        elif len(filename) <= 4 or filename[-4:] != ".apk":
            filename = filename + ".apk"
            print(oct.ColoredText([(f"您新输入的文件名：{filename}", "normal")]))
    else:
        print(oct.ColoredText([("您的文件名合法", "normal")]))

    UploadFile(path, filename)
    if install:
        InstallByAdb(filename)
    return filename

def UploadFile(path: str, filename: str):
    if os.system(f"adb push \"{path}\" \"/data/local/tmp/{filename}\""):
        print(oct.ColoredText([("上传失败，请截图并联系作者", "red")]))

def InstallByAdb(filename: str):
    print("---------------正在安装---------------")
    print(oct.ColoredText([("请", "normal"), 
                            ("右键这条信息", "red"), 
                            (f"，或复制:  pm install -g /data/local/tmp/{filename}, 并", "normal"), 
                            ("点击回车", "red")]))
    print("输入后，请手动输入exit并回车")
    os.system(f"echo pm install -g /data/local/tmp/{filename} | clip")
    if os.system("adb shell"):
        print(oct.ColoredText([("启动命令行失败或命令行命令出错，请截图并联系作者", "red")]))
    
def Installation():
    loop = True

    while loop:
        print("选择要上传的文件")
        path = easygui.fileopenbox("选择安装包", "选择安装包", '*')
        if path == None:
            easygui.msgbox("请重新选择文件，若再次不选择文件将会退出安装")
            path = easygui.fileopenbox("选择安装包", "选择安装包", '*')
            if path == None:
                break
        print(f"您的文件路径: {path}")
        UploadAndInstall(path)
        
        loopans = input("是否继续安装软件? (Y/N, defult: N):")
        loop = True if loopans == 'Y' or loopans == 'N' else False

def LoopInstall():
    # 选择文件夹
    print("选择要上传的文件夹")
    path = easygui.diropenbox("选择文件夹", "选择文件夹")
    if path == None:
        easygui.msgbox("请重新选择文件夹，若再次不选择文件夹将会退出安装")
        path = easygui.diropenbox("选择文件夹", "选择文件夹")
        if path == None:
            return
        print(f"您的文件夹路径: {path}")

    # 列出文件夹下所有文件
    files = os.listdir(path)
    cmdstr = ""
    num = 0
    for file in files:
        if file[-4:] == ".apk":
            num += 1
            print(f"正在处理: {num}. {file}")
            cmdstr += 'pm install -g /data/local/tmp/' + UploadAndInstall(os.path.join(path, file), install=False, default_text=str(num)) + ' & '
    print(oct.ColoredText([("请", "normal"), 
                            ("右键这条信息", "red"), 
                            (f"，或复制:  {cmdstr[:-2]}, 并", "normal"), 
                            ("点击回车", "red")]))
    print(oct.ColoredText([(f"请等待出现{len(files)}个success后，再输入exit!!!!", "green")]))
    print("输入后，请手动输入exit并回车")
    copy(cmdstr[:-2])
    os.system("adb shell")

############################### 卸载相关 ################################################

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
        
########################################## 激活/禁用相关 #####################################################

def ExecCommand(cmd: str, before_msg: str = "激活中...", after_msg: str = "激活成功！", 
                fail_msg: str = oct.ColoredText([("激活失败，请截图并联系作者", "red")])):
    print(before_msg)
    if os.system(cmd) == 0:
        print(after_msg)
    else:
        print(fail_msg)

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


########################################## 快捷指令相关 ################################################
def ShowSolution():
    print("先进入驾享模式")
    print("打开新装的高德的设置->播报")
    print("一直点击播报 进入高级设置")
    print("音频通道选择一个能从头枕播出来的通道 (我这里是0号通道)")
    print("返回高级设置 将使用高版本api改为1")

def ADBMode():
    print("此模式对于非专业人员来说具有一定风险，请务必确保安全！！！")
    print("请正常输入shell指令，输入exit退出")
    while True:
        command = input("ADB> ")
        if command == "exit":
            break
        if os.system(command) != 0:
            print(oct.ColoredText([("该条指令报错，请检查输入是否正确", "red")]))



def DelCache():
    print("当前/data/local/tmp目录下已用大小: ")
    os.system("adb shell \"cd /data/local/tmp/ && du -sh\"")
    ans = input("是否列出该目录下文件？(Y, N) (defult: Y)")
    if not ans.upper() == "N":
        os.system("adb shell \"cd /data/local/tmp/ && ls -lh\"")
    ans = input(oct.ColoredText([("二次确认：是否清除缓存？(Y, N) (defult: Y)", "red")]))
    if not ans.upper() == "N":
        if os.system("adb shell rm -rf /data/local/tmp/*"):
            print(oct.ColoredText([("清除失败，请截图并联系作者", "red")]))
        print("清除成功")


if __name__ == '__main__':
    ########################################## 文件拖动相关 #################################################
    parser = argparse.ArgumentParser(description='A Installer for Chery-Tiggo9')
    parser.add_argument('-v', '--version', action='version', version=VERSION)
    parser.add_argument('directory', nargs='?', default=None, help='an optional directory to process')
    args = parser.parse_args()

    if args.directory is not None:
        print(f"Processing directory: {args.directory}")
        UploadAndInstall(args.directory)
        sys.exit(0)

    print("---------------初始化---------------")

    ########################################## 主程序 #####################################################
    while True:
        mode = chooseMode()
        if mode != ModeChooser.wrong_code:
            os.system("cls")
            if mode == 0:
                sys.exit(0)
            elif mode == 1:
                Installation()
            elif mode == 2:
                LoopInstall()
            elif mode == 3:
                Uninstallation()
            elif mode == 4:
                # choosemode2
                submenu()
            elif mode == 5:
                ADBMode()
            elif mode == 6:
                DelCache()
            elif mode == 7:
                os.system("start https://github.com/zuo-qirun/Chery-Tiggo9-Install-software/wiki")
            elif mode == 8:
                # subprocess.run(['runas', '/user:Administrator', '"pythonw ' + script_path + '"'])
                subprocess.Popen("./update.exe")
                sys.exit(0)
            # elif mode == 9:

        if mode != 4:
            os.system("pause")
            os.system("cls")
