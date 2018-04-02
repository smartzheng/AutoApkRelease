# AutoApkRelease
>工作中有一个定制需求：根据不同的用户需求，需要替换APP内的图片，以及部分代码里面的配置信息，打出不同的apk交给客户使用。如果只用生成少量的apk，那么可以将所有图片放入资源文件夹然后根据服务端的信息来进行指定显示，但是随着客户量增加，需要打出数十个apk，并且启动图片不能根据配置来进行替换。所以必须手动更换图片和代码进行打包。这样容易出错，也比较低效，一旦出错必须全部重新返工。所有就写了一个简单的Python脚本来进行一次性批量打包。


###安装Python环境内容不再赘述，可参见网上教程。我使用的是Python3。  
  
###以下是详细代码，可参见注释进行配置。

```
#! python3
# 替换代码和文件，所替换的文本内容必须是当前文件的唯一字符串（可以加长需要替换扥字符串实现唯一性）
#如需增加要替换的代码内容或者资源，只需要增加数组并且调用替换方法即可
import os
#app启动名
appNames = ["app1","app2","app3"]
#gradle中的applicationId
replaceText = ["text1","text2","text3"]
#gradle中的applicationId
appIds = ["applicationId1","applicationId2","applicationId3"]
#输出apk的文件名
apkNames = ["apk1","apk2","apk3"]
#项目的资源文件夹路径
targetDir = "/Users/smartzheng/AndroidStudioProjects/MyApplication/app/src/main/res"
#配置自己存放不同apk资源图片的路径,分别命名为apk1，apk2，apk3...（apkNames的每个元素）需要替换的图片必须名字对应一致
sourceDir = "/Users/smartzheng/custom_app_imgs/"

# 拷贝替换文件，传入图片路径和项目资源目录
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

#替换文本内容，传入文件路径，原字符串，目标字符串
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
        # 替换Config配置文件下的代码内容
        replaceText(r'/Users/smartzheng/AndroidStudioProjects/MyApplication/app/src/main/java/com/smartzheng/Config.java',replaceText[i - 1],replaceText[i])
        #替换app名字
        replaceText(r'/Users/smartzheng/AndroidStudioProjects/MyApplication/app/src/main/res/values/strings.xml', appNames[i - 1],appNames[i])
        #替換applicationId,即替换包名
        replaceText(r'/Users/smartzheng/AndroidStudioProjects/MyApplication/app/build.gradle',appIds[i-1],appIds[i])
        #替换输出的路径
        replaceText(r'/Users/smartzheng/AndroidStudioProjects/MyApplication/app/build.gradle',apkNames[i-1],apkNames[i])
        # 替换资源图片
        copyFiles(sourceDir + apkNames[i], targetDir)
        # 打包(windows为gradlew assembleRelease)
        os.system("gradle assembleRelease")

# 将代码及资源文件回归到原位
replaceText(r'/Users/smartzheng/AndroidStudioProjects/MyApplication/app/src/main/java/com/smartzheng/Config.java',replaceText[len(appNames) - 1],replaceText[0])
replaceText(r'/Users/smartzheng/AndroidStudioProjects/MyApplication/app/src/main/res/values/strings.xml', appNames[len(appNames) - 1],appNames[0])
replaceText(r'/Users/smartzheng/AndroidStudioProjects/MyApplication/app/build.gradle',apkNames[len(appNames) - 1],apkNames[0])
replaceText(r'/Users/smartzheng/AndroidStudioProjects/MyApplication/app/build.gradle',appIds[len(appIds) - 1],appIds[0])
copyFiles(sourceDir + replaceText[0], targetDir)
print("success")

```
###代码保存为autoRelease.py

###默认情况下，.gradle文件需要加入以下内容：  
###android节点下：
```  
applicationVariants.all { variant -> 
        variant.outputs.each { output ->  
            //开始输出
            output.outputFile = new File(outputPathName)
        }
    }  
```

###输出路径修改
```
def apkName = "apk1"//apkNames[0]，每次输出不一样名字的apk
//前面加上自己的本地输出路径
def outputPathName = /Users/smartzheng/AndroidStudioProjects/apks + apkName
```
###默认的applicationId
```
applicationId "com.smartzheng." + applicationId1 //默认为前缀加appIds[0]
```
只需在命令行中键入python autoRelease，即可运行打包，原来需要大半天搞定的工作，现在只需静待电脑自动完成即可。



另外，项目中需要替换的内容不多，如果多的话还可以利用字典进行优化。


###以上。
