import os
import re
import subprocess
import numpy as np
import time


def run(cmd):
    """
    在终端运行命令
    Parameters:
        cmd:str     要执行的命令

    Returns:
        output:str  输出结果
    """
    output = subprocess.check_output(cmd.split()).decode()
    return output


def startPkg(device, pkgName, activity):
    """
    启动应用

    Args:
        device (str): 设备
        pkgName (str): 包名
        activity (str): 进程名
    """
    device.startActivity(component=f"{pkgName}/.{activity}")


def getMemory(serialno, pkgName):
    """
    获取应用占用的内存

    Args:
        serialno (str): 设备名称
        pkgName (str): 应用名称

    Returns:
        str: 占用内存大小
    """
    cmd = f"adb -s {serialno} shell dumpsys  meminfo {pkgName}"
    output = run(cmd)
    mem = re.findall(r"(?<=Native Heap)[0-9\s]+", output)[0].split()[0]
    return mem


def getPixel(serialno):
    """
    得到手机像素

    Args:
        serialno (str): 序列号

    Returns:
        width, height: 手机的像素
    """
    cmd = f"adb -s {serialno} shell wm size"
    width, height = run(cmd).split()[-1].split('x')
    return width, height


def getPid(serialno, pkgName):
    """
    获取应用的进城ID

    Args:
        serialno (str): 序列号
        pkgName (str): 包名

    Returns:
        pid: 进程号
    """
    cmd = f"adb -s {serialno} shell ps | grep {pkgName}"
    pid = run(cmd).split()[1]
    return pid


def adbRandomTest(serialno, pkgName):
    """
    进行随机测试

    Args:
        serialno (str): 序列号
        pkgName (str): 包名
    """
    cmd = f"adb -s {serialno} shell monkey -p {pkgName} -v 500"
    run(cmd)


def adbPctTest(serialno, pkgName, option):
    """
    对某一种特定的操作进行测试

    Args:
        serialno (str): 序列号
        pkgName (str): 包名
        option (str): 操作名称
    """
    cmd = f"adb -s {serialno} shell monkey -p {pkgName} -v {option} 100 500"
    run(cmd)


def adbNav(serialno, keyevent):
    """
    通过adb实现返回，home等操作

    Args:
        serialno (str): 序列号
        keyevent (str): 执行的操作
    """
    cmd = f"adb -s {serialno} shell input keyevent {keyevent}"
    run(cmd)


def startGame(vc):
    """
    点击开始游戏按钮开始游戏
    """
    if vc.findViewWithText("Start Game") != None:
        vc.findViewWithText("Start Game").touch()


def touch(vc, times=50):
    """
    在地图范围内模拟点击

    Args:
        vc (viewclient): viewclient 实例.
        times (int, optional): 测试次数. 默认为50. 
    """
    for _ in range(times):
        x = np.random.randint(low=85, high=995, size=1)
        y = np.random.randint(low=660, high=1560, size=1)
        vc.swipe(x[0], y[0])


def swipe(vc, times=50):
    """
    在地图范围内模拟滑动

    Args:
        vc (viewclient): viewclient 实例.
        times (int, optional): 测试次数. 默认为50. 
    """
    for _ in range(times):
        x = np.random.randint(low=85, high=995, size=2)
        y = np.random.randint(low=660, high=1560, size=2)
        vc.swipe(x[0], y[0], x[1], y[1])


def nav(serialno, device, pkgName, activity, times=50):
    """
    模拟导航按键操作

    Args:
        serialno (str): 序列号
        device (str): 设备
        pkgName (str): 包名
        activity (str): 进程名
        times (int, optional): 测试次数. 默认为50.
    """
    x = np.random.randint(low=0, high=6, size=times)
    op_dict = {0: "KEYCODE_MENU", 1: "KEYCODE_HOME", 2: "KEYCODE_BACK",
               3: "KEYCODE_DPAD_LEFT", 4: "KEYCODE_DPAD_RIGHT", 5: "KEYCODE_KEYCODE_DEL"}
    for i in range(times):
        startPkg(device, pkgName, activity)
        adbNav(serialno, op_dict[x[i]])


def goHomePage(vc, serialno, device, pkgName, activity):
    """
    定位到 home page

    Args:
        vc (viewclient): viewclient 实例
        serialno (str): 序列号
        device (str): 设备
        pkgName (str): 包名
        activity (str): 进程名

    Returns:
        changeSize: 地图大小改变按钮
        startButton: 开始游戏按钮
    """
    changeSize = []
    startButton = None
    startPkg(device, pkgName, activity)
    for i in range(10):
        adbNav(serialno, "KEYCODE_BACK")
    startPkg(device, pkgName, activity)
    time.sleep(2)
    for view in vc.views:
        if view.getClass() == "android.widget.ImageView":
            changeSize.append(vc.findViewById(view.uniqueId()))
        elif view.getText() == "Start Game":
            startButton = vc.findViewById(view.uniqueId())
    return changeSize, startButton


def homePageTest(vc, serialno, device, pkgName, activity, times=50):
    """
    对 home page 进行测试

    Args:
        vc (viewclient): viewclient 实例
        serialno (str): 序列号
        device (str): 设备
        pkgName (str): 包名
        activity (str): 进程名
        times (int, optional): 测试次数. 默认为50. 
    """
    x = np.random.randint(low=0, high=3, size=times)
    changeSize, startButton = goHomePage(
        vc, serialno, device, pkgName, activity)
    time.sleep(2)
    for i in range(times):
        if x[i] == 0:
            changeSize[0].touch()
        elif x[i] == 1:
            changeSize[1].touch()
        elif x[i] == 2:
            startButton.touch()
            adbNav(serialno, "KEYCODE_BACK")


def gamePageTest(vc, serialno, device, pkgName, activity, times=50):
    """
    对 game page 进行测试

    Args:
        vc (viewclient): viewclient 实例
        serialno (str): 序列号
        device (str): 设备
        pkgName (str): 包名
        activity (str): 进程名
        times (int, optional): 测试次数. 默认为50. 
    """
    x = np.random.randint(low=0, high=5, size=times)
    changeSize, startButton = goHomePage(
        vc, serialno, device, pkgName, activity)
    time.sleep(2)
    startButton.touch()
    for i in range(times):
        if x[i] == 0:
            swipe(vc, times=10)
        elif x[i] == 1:
            touch(vc, times=10)
        elif x[i] == 2:
            vc.touch(790, 535)
        elif x[i] == 3:
            vc.touch(970, 535)
            vc.touch(350, 1295)
        elif x[i] == 4:
            vc.touch(970, 535)
            vc.touch(725, 1295)


def randomTest(vc, serialno, device, pkgName, activity, times=10):
    """
    进行随机智能测试， 随机执行上述智能测试函数

    Args:
        vc (viewclient): viewclient 实例
        serialno (str): 序列号
        device (str): 设备
        pkgName (str): 包名
        activity (str): 进程名
        times (int, optional): 测试次数. 默认为10. 
    """
    x = np.random.randint(low=0, high=6, size=times)
    for i in range(times):
        if x[i] == 0:
            swipe(vc, times=10)
        elif x[i] == 1:
            touch(vc, times=10)
        elif x[i] == 2:
            nav(serialno, device, pkgName, activity, times=10)
        elif x[i] == 3:
            homePageTest(vc, serialno, device, pkgName, activity, times=10)
        elif x[i] == 4:
            gamePageTest(vc, serialno, device, pkgName, activity, times=10)
        cancelButton=vc.findViewWithText("Cancel")
        if cancelButton!=None:
            cancelButton.touch()
