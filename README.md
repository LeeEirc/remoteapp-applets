## remoteapp applets 集合

### 使用方法

remoteapp 需要的 JSON 数据通过 base64 处理成参数字符串
```shell
base64 << EOF 
{
  "username": "root",
  "password": "password",
  "host": "127.0.0.1",
  "port": "3306",
  "db": "mysql"
}
EOF

ewogICJ1c2VybmFtZSI6ICJyb290IiwKICAicGFzc3dvcmQiOiAicGFzc3dvcmQiLAogICJob3N0IjogIjEyNy4wLjAuMSIsCiAgInBvcnQiOiAiMzMwNiIsCiAgImRiIjogIm15c3FsIgp9Cg==
```

执行 python 脚本
```shell
python main.py ewogICJ1c2VybmFtZSI6ICJyb290IiwKICAicGFzc3dvcmQiOiAicGFzc3dvcmQiLAogICJob3N0IjogIjEyNy4wLjAuMSIsCiAgInBvcnQiOiAiMzMwNiIsCiAgImRiIjogIm15c3FsIgp9Cg==
```
