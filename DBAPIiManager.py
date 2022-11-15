import requests
import json
import os

class DBAPIManager:

    session = None
    token = None
    headers = {}
    addapiHeaders = {}
    username = "admin"
    password = "admin"

    rootPath = "http://10.77.110.222:8520"
    loginPath = "/user/login" # login to get Token

    addDataSourcePath = "/datasource/add"
    testDataSourcePath = "/datasource/connect"
    getAllDataSourcePath = "/datasource/getAll"

    getAllGroupPath = "/group/getAll/"
    addGroupPath = "/group/create/"

    addApiPath = "/apiConfig/add"
    getAllApiPath = "/apiConfig/getAll"
    onlineApiPath = "/apiConfig/online/apiId"


    def __init__(self):
        self.session = requests.Session()
        self.addapiHeaders["Content-Type"] = "application/json"
        if os.path.exists(".\\token"):
            with open(".\\token", "r") as f:
                self.token = f.readline().strip()
                self.headers["Authorization"] = self.token
                self.addapiHeaders["Authorization"] = self.token
                if self.checkTokenExpired() == True:
                    self.login()
                else:
                    print("Token is: " + self.token)
        else:
            self.login()
        return

    def login(self):
        url = self.rootPath + self.loginPath
        formData = {"username": self.username, "password": self.password}
        r = self.session.post(url, data=formData)
        response = json.loads(r.text)
        try:
            if response["success"] == True:
                self.token = response["msg"]
                self.headers["Authorization"] = self.token
                self.addapiHeaders["Authorization"] = self.token
                print("Token is: " + self.token)
                with open(".\\token", "w") as f:
                    f.write(self.token)
            else:
                print("Login Failed")
                print("Error info: ")
                print(r.text)
                exit(0)
        except:
            print("Error when login")
            print(r.text)
            exit(0)

    def readDataSourceConfig(self, dataSourceName):
        configPath = ".\\dataSource\\" + dataSourceName + ".json"
        if not os.path.exists(configPath):
            print("DataSource config file does not exist at " + configPath)
            return None
        configFile = open(configPath, "r")
        config = json.load(configFile)
        formData = {
        "name": config["dataSourceName"], "note":config["dataSourceNote"], "driver": "com.mysql.cj.jdbc.Driver",
        "url": "jdbc:mysql://" + config["dataSourceUrl"] + "/" + config["dbName"] + "?useSSL=false","characterEncoding":"UTF-8","serverTimezone":"GMT%252B8","type":"mysql",
        "username": config["dbUsername"], "password": config["dbPassword"], "tableSql": "tableSql=show tables"
        }
        configFile.close()
        return formData

    def addDataSource(self, dataSourceName):
        url = self.rootPath + self.addDataSourcePath
        formData = self.readDataSourceConfig(dataSourceName)
        if formData == None:
            print("Check your dataSource config file. \nThis program exit when creating dataSource.")
            exit(0)
        r = self.session.post(url, headers=self.headers, data=formData)
        if r.text == "":
            print("Create DataSource Success")
        else:
            print(r.text)

        # this is the response format in version1.0.0, which changes in 3.1.2
        # response = json.loads(r.text)
        # try:
        #     if response["success"] == True:
        #         print("Create DataSource Success")
        #     else:
        #         print("Create DataSource Failed")
        #         print("Error info: ")
        #         print(r.text)
        #         exit(0)
        # except:
        #     print("Error when CreateDataSource")
        #     print(r.text)
        #     exit(0)

    # abandoned in version 3.1.2, check the connection of DataSource in WebUI
    # def testDataSource(self, dataSourceName):
    #     url = self.rootPath + self.testDataSourcePath
    #     configPath = ".\\dataSource\\" + dataSourceName + ".json"
    #     if not os.path.exists(configPath):
    #         print("DataSource config file does not exist at " + configPath)
    #         print("Check your dataSource config file. \nThis program exit when testing dataSource.")
    #         exit(0)
    #     configFile = open(configPath, "r")
    #     config = json.load(configFile)
    #     configFile.close()
    #     formData = {
    #     "driver": "com.mysql.cj.jdbc.Driver","url": "jdbc:mysql://" + config["dataSourceUrl"] + "/" + config["dbName"] + "?useSSL=false","characterEncoding":"UTF-8","serverTimezone":"GMT%252B8","type":"mysql",
    #     "username": config["dbUsername"], "password": config["dbPassword"], "tableSql": "tableSql=show tables", "edit_password": "true"
    #     }
    #     r = self.session.post(url, headers=self.headers, data=formData)
    #     response = json.loads(r.text)
    #     try:
    #         if response["success"] == True:
    #             print("Test DataSource Success")
    #             print(response)
    #         else:
    #             print("Test DataSource Failed")
    #             print("Error info: ")
    #             print(r.text)
    #             exit(0)
    #     except:
    #         print("Error when TestDataSource")
    #         print(r.text)
    #         exit(0)

    def getAllDataSource(self):
        url = self.rootPath + self.getAllDataSourcePath
        r = self.session.get(url, headers=self.headers)
        return json.loads(r.text)

    def getDataSourceIdByName(self, dataSourceName):
        allDataSourceDesc = self.getAllDataSource()
        for dataSourceDesc in allDataSourceDesc:
            if dataSourceDesc["name"] == dataSourceName:
                print("Find dataSource: " + str(dataSourceDesc))
                return dataSourceDesc["id"]
        return None

    def addGroup(self, name):
        url = self.rootPath + self.addGroupPath
        r = self.session.post(url, headers=self.headers, data={"name": name})
        if r.text == "":
            print("Create Group Success")
        else:
            print(r.text)

    def getAllGroup(self):
        url = self.rootPath + self.getAllGroupPath
        r = self.session.get(url, headers=self.headers)
        return json.loads(r.text)

    def getGroupIdByName(self, groupName):
        allGroupDesc = self.getAllGroup()
        for groupDesc in allGroupDesc:
            if groupDesc["name"] == groupName:
                print("Find group: " + str(groupDesc))
                return groupDesc["id"]
        return None

    def readApiConfig(self, apiName):
        configPath = ".\\api\\" + apiName + ".json"
        if not os.path.exists(configPath):
            print("ApiConfig file does not exist at " + configPath)
            return None
        configFile = open(configPath, "r")
        config = json.load(configFile)
        configFile.close()
        params = json.dumps(config["paramList"])
        sqlList = config["sqlList"]
        formatSqlList = []
        dataSoucreId = self.getDataSourceIdByName(config["dataSourceName"])
        if dataSoucreId == None:
            print("dataSource failed to find.")
            return None
        groupId = self.getGroupIdByName(config["groupName"])
        if groupId == None:
            print("group failed to find.")
            return None
        for sql in sqlList:
            formatSqlList.append({"transformPlugin":None,"transformPluginParams":None,"sqlText":sql})
        formData = {"name":config["apiName"],"path":config["apiPath"],"note":config["apiNote"],"groupId": groupId,"previlege":1,"cachePlugin":None,"cachePluginParams":None,"datasourceId": dataSoucreId,"params": params, "sqlList":formatSqlList, "contentType": "application/x-www-form-urlencoded","jsonParam":None,"openTrans":0,"alarmPlugin":None,"alarmPluginParam":None}
        return formData

    def addApi(self, apiName):
        url = self.rootPath + self.addApiPath
        formData = self.readApiConfig(apiName)
        if formData == None:
            print("Check your api config file. \nThis program exit when creating api.")
            exit(0)
        r = self.session.post(url, headers=self.addapiHeaders, data=json.dumps(formData))
        response = json.loads(r.text)
        try:
            if response["success"] == True:
                print("Api Create Success")
            else:
                print("Create Api Failed")
                print("Error info: ")
                print(r.text)
                exit(0)
        except:
            print("Error when CreateApi")
            print(r.text)
            exit(0)

    def getAllApi(self):
        url = self.rootPath + self.getAllApiPath
        r = self.session.post(url, headers=self.headers)
        return json.loads(r.text)

    def getApiIdByName(self, apiName):
        allApiDesc = self.getAllApi()
        for apiDesc in allApiDesc:
            if apiDesc["name"] == apiName:
                print("Find api: " + str(apiDesc))
                return apiDesc["id"]
        return None

    def onlineApi(self, apiName):
        apiId = self.getApiIdByName(apiName)
        if apiId == None:
            print("api failed to find.")
            print("Check if your api has created. \nThis program exit when onlining api.")
            exit(0)
        url = self.rootPath + self.onlineApiPath.replace("apiId", apiId)
        r = self.session.post(url, headers=self.headers)
        print(r.text)
        print("Online Api success")

    def testApi(self, url):
        # Only use for http GET test
        # 如果有乱码，请注意编码问题
        print(self.session.get(url).text)

    def testApiWithParam(self, url, params):
        print(self.session.post(url, data=params).text)

    def checkTokenExpired(self):
        url = url = self.rootPath + self.getAllApiPath
        r = self.session.post(url, headers=self.headers)
        if "token无效，请重新登录" in r.text:
            return True
        else:
            return False