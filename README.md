# [M8Test](https://dev-docs.m8test.com) Python Gradle 模板

> 如有疑问，请加入我们的官方 QQ 群：[749248182](https://qm.qq.com/q/jVVADJCAI8) 或 QQ
> 频道：[m8testofficial](https://pd.qq.com/s/8pidhywcy)

---

## 📦 Gradle 任务说明

### 任务分组

1. **`m8test-build`**  
   M8Test构建相关任务组，包含`buildPython`（构建Python项目）、`runPython`（运行项目）等任务。

2. **`m8test-code-completion`**  
   M8Test代码补全相关任务组，包含`generatePythonAllCodeCompletionFiles` （生成所有需要的代码补全文件）,
   `generatePythonGlobalVariables`（生成全局变量代码补全文件）等任务。

3. **`m8test-developmenet-environment`**  
   M8Test开发环境相关任务组，包含`installDevelopmentEnvironment`（安装开发环境）、`installPythonPlugin`（安装语言插件）等任务。

4. **`m8test-download`**  
   M8Test资源下载相关任务组，包含`downloadPythonCodeTemplate`（下载示例代码模板）、`downloadPythonDocs`（下载文档）等任务。

> 实际开发中主要关注构建任务和代码补全任务即可。

### 常用任务

| 任务名称                                                    | 任务分组                             | 功能描述                                                                                           |
|---------------------------------------------------------|----------------------------------|------------------------------------------------------------------------------------------------|
| `generatePythonAllCodeCompletionFiles`                  | `m8test-code-completion`         | 生成所有Python代码补全文件，会执行所有的 `generatePythonCodeXXXCodeCompletionFiles` 任务, 编写脚本之前执行一次此任务即可有代码提示功能。 |
| `generatePythonGlobalVariables`                         | `m8test-code-completion`         | 生成Python全局变量代码补全文件，提供IDE代码提示功能。需连接安卓设备，建议编写代码前执行一次，依赖更新后需重新执行。                                 |
| `generatePythonNormalAndroidCodeCompletionFiles`        | `m8test-code-completion`         | 生成 Android API 的 Python 代码提示文件。成功后，Python 代码中将有 Android API 的代码提示。                             |
| `generatePythonNormalDevelopmentKitCodeCompletionFiles` | `m8test-code-completion`         | 生成 M8Test API 的 Python 代码提示文件。成功后，Python 代码中将有 M8Test API 的代码提示。                               |
| `generatePythonComponentXXXCodeCompletionFiles`         | `m8test-code-completion`         | 生成 XXX 组件 API 的 Python 代码提示文件。成功后，Python 代码中将有 XXX 组件 API 的代码提示。                               |
| `buildPython`                                           | `m8test-build`                   | 构建M8Test Python脚本项目源码（不执行），构建结果位于`build/project`目录。                                            |
| `runPython`                                             | `m8test-build`                   | 构建并将项目推送到已连接的安卓设备上运行。                                                                          |
| `buildPythonApk`                                        | `m8test-build`                   | 将M8Test Python脚本项目打包成APK文件。                                                                    |
| `installPythonInterceptor`                              | `m8test-development-environment` | 安装 Python 解析器。执行此任务会从网络下载 Python 并安装到 `~/.m8test/bin/python` 目录。若已安装 Python 解析器，执行此任务不会重新安装。   |

---

## 🚀 执行任务的方法

### 方法一：使用快捷搜索

1. 双击 `Ctrl` 键，打开搜索框。
2. 输入 `gradle 任务名`，例如 `gradle runPython`，然后按回车执行。

   ![方法一示例](images/1.png)

### 方法二：通过 Gradle 面板

1. 点击 Gradle 图标。
2. 依次展开 `python` > `Tasks` > `m8test`。
3. 双击需要执行的任务。

   ![方法二示例](images/2.png)

### 方法三：使用终端命令

1. 按下快捷键 `Alt + F12` 打开终端。
2. 输入命令 `./gradlew 任务名`，例如 `./gradlew runPython`，然后按回车执行。

   ![方法三示例](images/3.png)

---

## ⚙️ 配置脚本项目

脚本项目的配置位于 `python/build.gradle.kts` 文件中。您可以根据需要修改设备的 IP、ADB 端口等参数。该文件中包含详细的代码注释，供参考。

---

## 🛠️ 项目开发流程

1. **生成代码提示文件**  
   执行 `generatePythonAllCodeCompletionFiles` 任务，生成 Python 代码补全文件，提供代码提示功能。

2. **安装 Python 解析器**  
   执行 `installPythonInterceptor` 任务，安装 Python 解析器, 如果使用M8Test集成开发环境的话已经自带python解析器, 此步骤可以跳过。

3. **配置 Python 解析器**

   如果项目没有配置python解析器就会出现下面的提示, 这时候可以点击 `configure python interceptor` <br>

   ![](images/4.png)

   点击 `Modules` > `python` > `添加按钮图标`

   ![](images/5.png)

   选择 `python`

   ![](images/6.png)

   点击三个点图标

   ![](images/7.png)

   点击添加按钮

   ![](images/8.png)

   选择 `Add Python Sdk`

   ![](images/9.png)

   选择 `System Interceptor` 后点击三个点按钮

   ![](images/10.png)

   选择python解析器(python.exe)的路径后点击 `Ok`,
   如果是集成开发环境则选择 `C:\Users\Your username\.m8test\bin\python\python.exe`

   ![](images/11.png)

   添加解析器成功后点击 `Ok`

   ![](images/12.png)

   可以看到python解析器添加成功, 继续点击 `Ok`

   ![](images/13.png)

   点击 `Python Interceptor` 右边的输入框选择我们刚添加的python sdk

   ![](images/14.png)

   点击 `apply` 再点击 `Ok`

   ![](images/15.png)

   我们再看一下python源码, 可以看到已经没有 `configure python interceptor` 的提示了

   ![](images/16.png)

4. **连接日志服务**

   按下快捷键 `Alt + T`，依次选择 `M8Test` > `连接日志服务`。

5. **编写并运行脚本**

   编写代码并保存后，执行 `runPython` 任务，即可在安卓设备上运行脚本项目。确保安卓设备已开启 ADB 调试。运行日志可在
   M8Test 日志面板中查看。

6. **打包Apk**  
   所有的脚本开发工作都完整后, 如果你需要打包成独立的apk可以执行 `buildPythonApk` 任务。

## APK 启动策略

应用身份在 `projectConfig` 中设置：`name` 是显示名称，`packageName` 是唯一包名，`versionName` 与 `versionCode` 控制版本，`logo` 指向 `res` 下的图标。构建生成的脚本配置会将这些值应用到 APK。`appName`、`appVersionName` 和 `appVersionCode` Gradle 属性可覆盖名称和版本。默认安装后自动运行脚本。需要由用户点击运行时，在语言配置块中选择手动启动：

```kotlin
m8testPython {
    apkBuild {
        launchMode = "manual"
    }
}
```

`launchMode` 只接受 `"automatic"` 或 `"manual"`。手动模式显示启动页，由用户决定何时运行。
## 发布签名

APK 默认使用开发签名。发布时在 `m8testPython { apkBuild { ... } }` 中设置 `signingMode = "release"`、密钥库路径和别名，并通过 `providers.environmentVariable("M8TEST_RELEASE_STORE_PASSWORD")` 与 `providers.environmentVariable("M8TEST_RELEASE_KEY_PASSWORD")` 提供密码。发布 APK 在本机签名并验证，输出到 `build/apk/`。密钥库和密码不会进入生成源码或设备项目；缺少发布签名配置时构建会失败。请把密钥库保存在受控位置并排除在版本控制之外，JDK `keytool` 可用于生成、导入和导出密钥材料。
