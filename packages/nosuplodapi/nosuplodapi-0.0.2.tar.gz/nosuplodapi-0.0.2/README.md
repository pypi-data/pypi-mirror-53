
`python`封装`nos`上传文件逻辑，支持大文件(>100M)分片上传


### 安装

```
pip install nosuplodapi
```

<br>

### 初始化实例

<br>

```
from uploadapi import UploadClient

# 初始化nos上传实例
uploadClient = UploadClient(access_key="******",
                            secret_key="******",
                            bucket="******",
                            end_point="******")
```

注: 所需对象存储请到网易云开发者平台申请


### 上传文件

```
result = uploadClient.upload(path="******")
```


### 返回数据

```
{
  'url': 'nos下载地址',
  'fileByteSize': 文件大小,
  'md5': '文件md5值',
  'fileName': '源文件名'
}
```


### 参考文档

<br>

[nos python sdk 手册](https://www.163yun.com/help/documents/15677647572680704)

<br><br>