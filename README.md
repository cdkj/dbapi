# DB-Api使用接口说明

**Note:: **

- **使用者应对python List, Dict等基本数据类型有基本了解，基本了解json消息格式。**
- **代码中对数据源的定义是一个数据库服务中的一个数据库**

## 1. 增加数据源

 `dbapiManager.addDataSource(dataSourceName)`

- 使用配置文件增加数据源，数据源配置文件位于`.\dataSource\{dataSourceName}.json`
- 配置文件的格式请阅读dataSource目录下的README文件

## 2. 测试数据源连接

**Note:: 当前3.1.2版本弃用该功能，可以在webUI界面测试连接**

`dbapiManager.testDataSource(dataSourceName)`，使用方式同**增加数据源**

## 3. 创建分组

`dbapiManager.addGroup(groupName)`

- `groupName`是要创建的分组名字

## 4. 创建Api

`dbapiManager.addApi(apiName)`

- 使用配置文件创建Api，Api配置文件位于`.\api\{apiName}.json`

- 配置文件的格式请阅读api目录下的README文件

- 关于Api参数：

  -   每个api可以定义一个或多个参数，这些参数在代码中以列表的形式定义，并可以在sql语句中被引用。
  - 每个参数的定义需要提供{name, type, note}, 其中name是参数名字，type是参数的类型，note是对该参数的描述信息。
  - 参数类型(type)虽然以字符串的形式给出，但只支持八种格式：`string, bigint, double, date, Array<string>, Array<bigint>, Array<double>, Array<date>`
  - 参数类型(type)不属于以上任意一种的情况，会导致sql执行遇到参数使用时报错。

- 关于Sql语句：

  - 每个api可以包含一个或多个sql语句，这些sql语句在代码中以列表的形式定义。 在访问api时，会顺序执行api包含的sql语句并将结果以json格式返回。

  - 在定义时，若sql不包含参数,那么将sql语句以字符串的形式在列表中给出即可，比如下方定义

    ```python
    sqlList = [
    	"Select ID,Name,Tel from live_table where live_table.Nei_addr =\"浙江省杭州市江干区闸弄口街道110号\" and live_table.Building_info =\"5栋6单元203\" and live_table.Enter_time between '2021-04-28 12:00:00.000' and '2021-05-04 16:25:00.000'",
        "Select ID,Name,Tel from live_table where live_table.Nei_addr =\"浙江省杭州市江干区下沙街道33号\" and live_table.Building_info =\"4栋5单元610\" and live_table.Enter_time between '2021-04-28 12:00:00.000' and '2021-05-04 16:25:00.000'"
    ]
    ```

  - 若sql语句包含参数，那么参数以 #{param} 的形式给出，比如下方定义, 其中requestNum是设定的参数的名称

    ```python
    sqlList = [
    	"select * from monitor where monitor.nums = #{requestNum}"
    ]
    ```
    
  - sql还可以为动态sql，具体使用方法参考https://www.w3cschool.cn/mybatis/l5cx1ilz.html，下面给出一个例子
  
    ```python
    sqlList = [
        "select monitor.nums, monitor.host from monitor where monitor.nums = #{requestNum} and host in <foreach item=\"host\" collection=\"hosts\" open=\"(\" separator=\",\" close=\")\" nullable=\"true\"> #{host} </foreach>"
    ]
    ```
  
    

## 5. 上线Api

`dbapiManager.onlineApi(apiName)`

- `apiName`是要创建的Api名字

## 6. 测试Api

**Notice::**

- **对Api的测试有不带参数和带参数的版本**
- **对接口的测试本质上是发送Http请求，其中不带参数时生成的api接口使用http GET类型请求访问，带参数时生成的api接口使用http POST类型请求访问**
- **测试方式很灵活，代码中只是样例**

### 6.1 不带参数

`dbapiManager.testApi(apiUrl)`

- `apiUrl`是要测试的接口路径

### 6.2 带参数

`dbapiManager.testApiWithParam(apiUrl, testParams)`

- `apiUrl`是要测试的接口路径
- `testParams`是要上传的参数，该样例中使用json格式发送参数，也可以通过改变http头部来使用其他格式发送参数

## 7.各种查询

```python
print(dbapiManager.getAllApi) # 以json形式返回所有api信息
print(dbapiManager.getAllGroup) # 以json形式返回所有分组信息
print(dbapiManager.getAllDataSource) # 以json形式返回所有数据源信息
```

