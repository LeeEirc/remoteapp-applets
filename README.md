## remoteapp applets 集合

### 环境

python 版本: 3.10.6
OS 版本: Windows Server 2019 Standard

### 使用方法

remoteapp 需要的 JSON 数据 `test_data.json` 通过 base64 处理成参数字符串
```shell
export args=`cat test_data.json| base64`
```

执行 python 脚本
```shell
python main.py $args
```
