from utils import *
from com.dtmilano.android.viewclient import ViewClient
import time


def startTest(pkgName, activity):
    device, serialno = ViewClient.connectToDeviceOrExit()
    vc = ViewClient(device=device, serialno=serialno)

    print("----------------------------------------------------------------")
    print("Device:", serialno)
    width, height = getPixel(serialno)
    print("Pixel:", f"{width}x{height}")
    startPkg(device, pkgName, activity)
    print("APP start!")
    print("------------------------------------------------------------------------------------------------")
    while True:
        mem = getMemory(serialno, pkgName)
        pid = getPid(serialno, pkgName)
        print("Package Name:", pkgName)
        print("Process Pid:", pid)
        print("Memory Occupied:", mem)
        print("Enter A Number To Start Monkey Test")
        print("1: Adb Random Test\t\t2: Adb Touch Test\t\t3: Adb Motion Test")
        print("4: Adb Trackball Test\t\t5: Adb Nav Test\t\t\t6: Adb MajorNav Test")
        print("7: Adb Syskeys Test\t\t8: Adb Appswitch Test\t\t9: Adb Anyevent Test")
        print("10: Smart Random Test\t\t11: Smart Touch Test\t\t12: Smart Swipe Test")
        print("13: Smart Nav Test\t\t14: Smart HomePage Test\t\t15: Smart GamePage Test")
        print("0: Exit")
        print("------------------------------------------------------------------------------------------------")

        op_dict = {2: "touch", 3: "motion", 4: "trackball", 5: "nav",
                   6: "majornav", 7: "syskeys", 8: "appswitch", 9: "anyevent"}
        op = int(input("Please Enter a Num: "))
        startPkg(device, pkgName, activity)
        before = time.time()
        if op == 1:
            adbRandomTest(serialno, pkgName)
        elif op >= 2 and op <= 9:
            startGame(vc)
            adbPctTest(serialno, pkgName, "--pct-"+op_dict[op])
        elif op == 10:
            randomTest(vc, serialno, device, pkgName, activity,)
        elif op == 11:
            startGame(vc)
            touch(vc)
        elif op == 12:
            swipe(vc)
        elif op == 13:
            nav(serialno, device, pkgName, activity)
        elif op == 14:
            homePageTest(vc, serialno, device, pkgName, activity)
        elif op == 15:
            gamePageTest(vc, serialno, device, pkgName, activity)
        elif op == 0:
            print("Bye!")
            break
        after = time.time()
        print("Used Time:", after-before, "seconds")
        input("Press Any Key To Continue")


if __name__ == '__main__':
    pkgName = "com.androbaby.game2048"
    activity = "MainActivity"
    startTest(pkgName, activity)
