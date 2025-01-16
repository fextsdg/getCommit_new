# 这是一个用于从 'Github' 或者 'Gitlab' 中获取指定项目的版本commit信息的项目
# ReadMe



------

## 1.修改配置文件 commit.json

{
"repo_owner": "php", #仓库所有者
"repo_name": "php-src", #仓库名称
"file_path": "ext/standard/http_fopen_wrapper.c",   #下载的文件
"commit_sha": "523f230c831d7b33353203fa34aee4e92ac12bba"   #commit起始号
}

## 2.下载commit号

getCommit.py



## 3.下载commit文件（所有文件）

getPatch.py



## 4.提取单个文件的Patch

getOnePatch.py

