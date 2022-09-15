## remoteapp applets 集合

### 使用方法
python 版本 3.10.6

remoteapp 需要的 JSON 数据通过 base64 处理成参数字符串
```shell
export args=`base64 << EOF 
{
  "username": "root",
  "password": "password",
  "host": "127.0.0.1",
  "port": "3306",
  "db_name": "mysql"
}
EOF`
```

执行 python 脚本
```shell
python main.py $args
```
