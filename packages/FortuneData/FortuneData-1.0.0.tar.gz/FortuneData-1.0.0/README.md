#FortuneData
### database模块
  数据库模块
  - Company数据库模型类
    - en_name 英文名
    - cn_name 中文名
    - rank 排名
    - revenues 收入
    - profits 利润
    - assets 市值
    - employees 雇员人数
  - create_database()方法
    创建包含Company表的数据库

### datasource模块
  - load_fortune_data( appid, secretKey ) 
    从fortune网站获取数据入库
    - appid 百度翻译开发平台APP ID
    - secretKey 百度翻译开放平台秘钥
  - get_company_cn_name( en_name, appid, secretKey )
    根据英文en_name获取中文译文
    - appid 百度翻译开发平台APP ID
    - secretKey 百度翻译开放平台秘钥
