## remoteapp applets 集合

### 环境

python 版本: 3.10.6
OS 版本: Windows Server 2019 Standard

### 使用方法

remoteapp 需要的 JSON 数据 `test_data.json` 通过 base64 处理成参数字符串

或者使用 PowerShell
```PowerShell
$base64Args = (Get-Content 'data.json' -Raw | ForEach-Object { [System.Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($_)) })
```

执行 python 脚本
```shell
python main.py $base64Args
```
