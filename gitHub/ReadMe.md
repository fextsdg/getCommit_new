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



## 5.下载bf文件

downlaod.py



## 6.反向应用补丁
*修改补丁中的文件名* 

patch -R < patch.diff



