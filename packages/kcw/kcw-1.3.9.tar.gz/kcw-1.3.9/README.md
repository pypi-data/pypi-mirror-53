# kcw

#### 介绍
快速创建cli和你web应用框架

### 安装扩展
1. pip install pyinstaller

###打包exe
pyinstaller -F kcw.py



setup.py打包命令各参数详解：
>>python setup.py --help-commands
  --python setup.py build     # 仅编译不安装
  --python setup.py install    #安装到python安装目录的lib下
  --python setup.py sdist      #生成压缩包(zip/tar.gz)
  --python setup.py bdist_wininst  #生成NT平台安装包(.exe)
  --python setup.py bdist_rpm #生成rpm包 