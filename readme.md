# 安装

- 安装anaconda

- 创建虚拟环境：

- 安装三方包
  `pip install re` （好像是自带的，也许不用安装...）

- 添加本地包

    - 在虚拟环境根目录（例如D:\ProgramFiles\anaconda3\envs\GrowingDict）下添加
      mypath.pth文件。文件内写入`E:\ProgramCode\dbsql`。
    - 为了用户方便，我已经把dbsql包直接放在工作路径下了，所以你其实什么都不用做...

- 清空输出路径：我们的输出放在`/dict/`、`/static/oxford9/`和`/raw/`中。请在运行程序前确保这些文件夹是空的（至少第一个路径是空的，这是最终输出结果；后两个路径中的内容涉及手动操作，我就留着了，用户可以不删除。）。

# 流程
## 字典抽取
- 下载[GetDict](https://pan.baidu.com/share/link?uk=305151372&shareid=2565690867)
- 下载[牛津高阶英汉双解词典(第9版)的mdx文件和mdd文件](https://download.csdn.net/download/qq_36682526/12304563?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522159336452619195265959514%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=159336452619195265959514&biz_id=1&utm_medium=distribute.pc_search_result.none-task-download-2~all~top_click~default-3-12304563.ecpm_v1_rank_ctr_v4&utm_term=%E7%89%9B%E6%B4%A5%E9%AB%98%E9%98%B6%E8%8B%B1%E6%B1%89%E5%8F%8C%E8%A7%A3%E8%AF%8D%E5%85%B8)。
- 用[GetDict](E:\resource\document\1科目：COMPUTER\4科目：人工智能\1：数据\语料\牛津词典\GetDict.exe)
  把mdx抽取为txt，再更改后缀为html;用getDict把mdd抽取得到css。具体参见[教程](http://www.ducidian.com/forum.php?mod=viewthread&tid=178)。
- [得到的内容](E:\resource\document\1科目：COMPUTER\4科目：人工智能\1：数据\语料\牛津词典\牛津高阶英汉双解词典(第9版)_V2.0\牛津高阶英汉双解词典(第9版)_V2.0(抽取))
  放入本项目中作为资源，其中：
  
    - 图片（*.png, *.svg）放到/static/oxford9/pic目录下。
    - `oalecd9.css`重命名后放在/static/oxford9/oxford9.css目录下。
        - 同时手动把其中的url定位改成local定位，并指向static/oxford9/font。例如`src: url('/font/Optima_LT_Medium_Italic.ttf')`改成`src: local('../static/oxford9/font/Optima_LT_Medium_Italic.ttf')`。如果不改，也不影响使用，但浏览器控制台上会报一堆错。（当前版本中的/static/oxford9/oxford9.css是改过的）
    - `oalecd9.js`重命名后放在/static/oxford9/oxford9.js目录下。
    - html重命名为`原版.html`,放到./raw目录下。

## 字典debug
- `raw/原版.html` 有如下bug，修改后得到`raw/原版debug.html` ：
  - lint词项内容有重复。
  - 好像还有别的重复，我记不清了。
  
## 分割entry
- 运行`从html中提取原始词条.py`即可。功能如下：
    - 切分出html中的一个个entry(有些词对应多个entry，会合并到一起，并在控制台输出信息)
    - 删除<head>标签
    - 修改图片路径到/static/oxford9/pic下边
    - 存储到sqlite数据库（/dict/entry.sqlite）

# 原理
* 使用自己写的dbsql库来实现对不同数据库类型的封装。
  这样只需在使用时（本项目中是storage_sqlite.py）把
  `from dbsql_sqlite import DbSql`
  改成`from dbsql_mysql import DbSql`
  就可以方便的切换各种数据库了。 
  相关文件由.pth方式作为三方包导入，参见“安装”。
* 使用storage_api.py实现对字典不同存储方式的封装。
  这样只需在使用时`from storage_sqlite import StorageSqlite as Storage`
  改成`from storage_mysql import StorageSqlite as Storage`
  就可以方便的切换各种存储方式了。 
  和上边的dbsql不同，这里的存储方式是针对entry的，设计了字段等定制化信息，
  所以是项目内，而不是三方包。
  storage_api.py中是接口类。storage_sqlite.py使用sqlite数据库实现了这个接口类。
