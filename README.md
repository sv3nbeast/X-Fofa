# X-Fofa
基于Fofa会员前提，获得任意页数的目标数量URL

![](./cmd.png)

```
PS:为解决部分漏洞在搜索引擎内包含较少，Fofa的API为固定数量获取相同的目标URL，使用API获取会有大量冗余，其实只需要搜索引擎靠后位置的目标URL的问题，加工自某位师傅(忘记在哪找到的了! 0.0)的小工具~
```

### 用法
* Usage: python3 X-Fofa.py 'app="Solr"' Solr  94bbbb177c4a564feddb8c7d413d5d61
* Usage: python3 X-Fofa.py  Fofa搜索语法   搜索结果文件名   Fofa的Cookie的_fofapro_ars_session值
* 然后按照需求输入 从哪页开始 和 获取多少页数 即可
### 获取_fofapro_ars_session值

CTRL+C,CTRL+V
目标一定要是https://classic.fofa.so/ 而不是新版的地址哦


![](./getCookie.png)

