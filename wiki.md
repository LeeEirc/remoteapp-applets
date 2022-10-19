## 离线安装包制作

下载 python 3.10 [官方地址](https://www.python.org/ftp/python/3.10.8/python-3.10.8-amd64.exe)

使用 pip 下载依赖包
```shell
mkdir pip_packages
pip download -d  pip_packages -r requirements.txt
```


安装离线的 python 包
```shell
pip install --no-index --find-links=./pip_packages -r requirements.txt
```
