#! python3
# 替换代码和文件
import os

appNames = ["联营达", "易企订", "佐邻订货", "优厨帮", "蓉城易购", "创康良品", "淘广材", "烁客", "成铁生活", "新东日建材"]
appIds = ["LYD", "YQD", "ZL", "YCB", "RCYG", "CKLP", "TGC", "SK", "CTSH", "XDRJC"]
apkNames = ["lianyingda.cn", "yidianlife.com", "zoli.vip", "168ycb.com", "028rcyg.com", "cdck168.com", "zm-am.com",
            "svlok.com", "ctshgs168.com", "newdongri.com"]
targetDir = "H:\\WORK_DHB_STUDIO\\Android\\Code\\DHB\\dHB\\src\\main\\res"
sourceDir = "H:\\custom_app_img\\"


# 拷贝文件
def copyFiles(sourceDir, targetDir):
    for file in os.listdir(sourceDir):
        sourceFile = os.path.join(sourceDir, file)
        targetFile = os.path.join(targetDir, file)
        if os.path.isfile(sourceFile):
            if not os.path.exists(targetDir):
                os.makedirs(targetDir)
            open(targetFile, "wb").write(open(sourceFile, "rb").read())
        if os.path.isdir(sourceFile):
            copyFiles(sourceFile, targetFile)


def replaceText(f_path, text1, text2):
    with open(f_path, 'r', encoding='utf-8') as r:
        s = r.read()
        replace = s.replace(text1, text2)
    with open(f_path, 'w', encoding='utf-8') as w:
        w.write(replace)
    r.close()
    w.close()


print("begin")
# 循环执行打包操作
for i in range(len(appNames)):
    if i != 0:
        # 替换C配置companyId
        replaceText(r'H:\WORK_DHB_STUDIO\Android\Code\DHB\dHB\src\main\java\com\rs\dhb\config\C.java',
                    "return COMPANYID_" + appIds[i - 1], "return COMPANYID_" + appIds[i])
        # 替换资源图片
        replaceText(r'H:\WORK_DHB_STUDIO\Android\Code\DHB\dHB\src\main\res\values\strings.xml', appNames[i - 1],
                    appNames[i])
        replaceText(r'H:\WORK_DHB_STUDIO\Android\Code\DHB\dHB\build.gradle',apkNames[i-1],apkNames[i])
        #替換输出路径和文件名
        copyFiles(sourceDir + appIds[i], targetDir)
    # 打包
    os.system("gradlew assembleRelease")

    #重命名并放到单独的文件夹下
    path = r'C:\Users\zhengshuai\Desktop'
    # os.rename(os.path.join(path, 'dHB-release.apk'), os.path.join(path, apkNames[i]+'.apk'))
    # copyFiles(path + apkNames[i]+'.apk', 'C:\\Users\\zhengshuai\\Desktop\\'+apkNames[i]+'\\'+apkNames[i]+'.apk')
    # Tinker打包patch文件,还需要修改build。gradle文件中依赖apk名
    # os.system("gradlew tinkerPatchRelease")

# 回归原位
replaceText(r'H:\WORK_DHB_STUDIO\Android\Code\DHB\dHB\src\main\java\com\rs\dhb\config\C.java',
            "return COMPANYID_" + appIds[len(appNames) - 1], "return COMPANYID_" + appIds[0])
replaceText(r'H:\WORK_DHB_STUDIO\Android\Code\DHB\dHB\src\main\res\values\strings.xml', appNames[len(appNames) - 1],
            appNames[0])
replaceText(r'H:\WORK_DHB_STUDIO\Android\Code\DHB\dHB\build.gradle',apkNames[len(appNames) - 1],apkNames[0])
copyFiles(sourceDir + appIds[0], targetDir)
print("success")
