# MiraiCP-debug-docs
MiraiCP的debug模板以及文档。

模板用于一键生成Visual Studio项目或Clion项目，支持Windows与Linux使用。

文档可能能为您debug MiraiCP提供一些帮助。

## 如何使用

* clone该仓库。

* 安装python（python3或以上），JDK（>=11）。

* Linux：设置环境变量`JAVA_HOME`到JDK目录。

* 在仓库目录下执行（尖角括号部分可以忽略）：

  * Windows：
  
    ```powershell
    python .\scripts\init.py <%versiontag%> <compile>
    ```
  
  * Linux：
  
    ```shell
    python3 ./scripts/init.py <$versiontag> <compile>
    ```
  
  其中`versiontag`是需要debug的MiraiCP版本，不指明时，默认值为`init.py`的`DEFAULT_VERSION_TAG`，可能随版本更新；`versiontag`可以以v开头或不以v开头。第二个可选参数为字符串`compile`，代表在生成项目后立刻编译，默认没有该参数，即不编译。

* 将全部的插件代码放入`./src/plugin/`目录下，记得删除里面原有的`test.cpp`。

## 如何使用IDE调试

> 调试开始时会发生多次内存访问异常。这是因为jvm在进行垃圾回收，如果Visual Studio显示“帧不在模块中”，Clion显示disassembly代码，即可继续运行，忽略掉这个异常。不建议取消勾选“引发此异常类型时中断”，这可能会导致MiraiCP本体出现异常时不中断。直接点击“继续”即可。
>
> 使用gdb调试时的一个（不太聪明，但好用的）解决方案：在家目录下创建`.gdbinit`文件，写入一行
>
> ```
> handle SIGSEGV noprint nostop pass
> ```
>
> 即可阻止所有的SIGSEGV。但这可能导致MiraiCP或插件造成的SIGSEGV被忽略。当出现这种情况时，用`#`注释掉上述内容即可。注意，这样做的话其他程序被调试时SIGSEGV也会被忽略，最好调试结束之后注释掉它。

### Visual Studio

此处以Visual Studio 2019为例说明如何调试。

* 双击`build/MiraiCP-debug.sln`打开visual studio项目。
* 解决方案资源管理器->Loader右键->属性->配置属性->常规->输出目录，这个目录将是编译出的libLoader.dll存放的目录，您可以自行修改该目录位置。如果想省去麻烦，建议直接将输出目录修改到您当前启动MiraiCP时libLoader所在的目录下。如果还需要修改插件生成的路径，修改 解决方案资源管理器->MiraiCP_plugin右键->属性->配置属性->常规->输出目录。
* 将mcl或`MiraiCP-loader-<version>.jar`放入运行目录。[MiraiCP Release页面](https://github.com/Nambers/MiraiCP/releases)
* 打开：解决方案资源管理器->Loader右键->属性->配置属性->调试，命令一行写`java.exe`的完整路径（不要带双引号），参数写`-jar MiraiCP-loader-<version>.jar `，此处jar文件要修改为你的启动器文件名（可以是mcl的jar文件），工作目录修改为与上述jar所在的目录相同。
* 按照启动MiraiCP同样的方法，填好配置文件、`device.json`等信息。注意，默认生成的插件dll文件名为`libMyMiraiCPPlugin.dll`，`config.json`中请确认路径正确。如果需要修改生成的文件名，请在 解决方案资源管理器->MiraiCP_plugin右键->属性->配置属性->常规->目标文件名修改。

* 解决方案资源管理器->Loader右键->设为启动项目，按F5即可开始调试。

### CLion

CLion读取CMakeLists.txt较为方便，可以在Linux和Windows平台下使用，不需要上一个步骤中的build文件夹。

> 推荐Windows系统下工具链切换至MSVC，CLion + MSVC（LLDB）调试时，jvm的内存访问异常将被压制。

* 以文件夹形式打开`MiraiCP-debug-docs`。
* 运行->编辑配置->Loader，可执行文件输入java的可执行文件完整路径，实参输入`-jar MiraiCP-loader-<version>.jar`，工作目录修改为与上述jar所在的目录相同。该步骤与Visual Studio中步骤类似。
* 按照启动MiraiCP同样的方法，填好配置文件、`device.json`等信息。注意，默认生成的插件dll文件名为`libMyMiraiCPPlugin.dll`，`config.json`中请确认路径正确。如果需要修改生成的文件名，请在 解决方案资源管理器->MiraiCP_plugin右键->属性->配置属性->常规->目标文件名修改。该步骤与Visual Studio中步骤完全相同。

* 调试Loader。
