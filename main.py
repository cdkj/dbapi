from DBAPIiManager import DBAPIManager

# 使用者应对python List, Dict等基本数据类型有基本了解，基本了解json消息格式
if __name__ == "__main__":
    dbapiManager = DBAPIManager()

    # 数据源信息使用配置文件声明
    dataSourceName = "test-heyAhhhhh"

    # 增加数据源
    # dbapiManager.addDataSource(dataSourceName)

    groupName = "test-heyAhhhhh" # 创建的分组名字
    # 创建分组
    # dbapiManager.addGroup(groupName)

    apiName = "test-arrayParams"
    # 创建api
    # dbapiManager.addApi(apiName)

    # Api上线
    # dbapiManager.onlineApi(apiName)


    # 测试Api, 不带参数
    # dbapiManager.testApi("your URL")



    """
    测试Api，带参数版本
    不带参数时生成的api接口使用http GET类型请求访问，带参数时生成的api接口使用http POST类型请求访问
    代码中的测试方法仅为样例，当参数为数组类型时并不确定是否可以成功调用，更多调用测试方法建议使用可视化界面调用，或者抓包开发自己的测试方法
    参数使用python字典类型声，格式为 "参数名": "参数值"
    """
    testParams = {
        "requestNum": 2
    }
    testParamsUrl = "http://10.77.110.222:8520/api/test-params"
    # dbapiManager.testApiWithParam(testParamsUrl, testParams)


    testArrayParams = {
        "requestNum": 2,
        "hosts": ["peer0.fabric-ruc-com", "peer1.fabric-dbiir-com", "peer2.fabric-deke-com"]
    }
    testArrayParamsUrl = "http://10.77.110.222:8520/api/test-arrayParams"
    # dbapiManager.testApiWithParam(testArrayParamsUrl, testArrayParams)

    # 使用api名字获取详细信息
    # print(dbapiManager.getApiDetail("test-params"))

    # 获取所有api详细信息
    # allApi = dbapiManager.getAllApi()
    # for api in allApi:
    #     print(dbapiManager.getApiDetail(api["name"]))