# !/usr/bin/env python
# 使用源码请标注出处
# 此代码由zuoqirun/B站山本大佐在北京提供
# V8版本 修复error： closed

import os, easygui
print("本程序由Github zuoqirun提供 使用请标明出处")
print("---------------初始化---------------")
loop = True
os.system("adb devices")

while loop:
    print("选择要上传的文件")
    path = easygui.fileopenbox("选择安装包", "选择安装包", '*.apk')
    print(path)
    
    
    filename = input("是否更改文件名? 文件名\033[1;31m不能含有中文或空格!! 若含有中文或空格请在此处输入新文件名!!!!\033[0m 若无请点击回车键跳过此流程")
    if filename == "":
        filename = os.path.basename(path)
    elif len(filename) <= 4 or filename[-4:] != ".apk":
        filename = filename + ".apk"
    print(filename)
    if os.system(f"adb push \"{path}\" \"/data/local/tmp/{filename}\""):
        print("\033[1;31m上传失败，请截图并联系作者\033[0m")
    #os.system("adb shell ls -a /data/local/tmp/")   
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
    if ans == 'Y' or ans == 'y':
        if os.system("adb shell rm -rf /data/local/tmp/*"): #应该没写错吧......
            print("\033[1;31m清除失败，请截图并联系作者\033[0m")
        print("清除成功")
        
        
    loopans = input("是否继续安装软件? (Y/N, defult: N):")
    loop = True if loopans == 'Y' or loopans == 'N' else False
os.system("pause")