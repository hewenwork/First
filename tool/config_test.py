import configparser
'''
配置文件的格式如下：中括号“[ ]”内包含的为section。section 下面为类似于key-value 的配置内容。
使用ConfigParser 首选需要初始化实例，并读取配置文件
获取所用的section节点config.read("ini", encoding="utf-8")
获取指定section 的options      r = config.options("db")
获取指定section下指点option的值    r = config.get("db", "db_host")
获取指定section的所用配置信息       r = config.items("db")
修改某个option的值，如果不存在则会出创建  config.set("db", "db_port", "69") 
检查section或option是否存在   config.has_section("default")   config.has_option("default", "db_host")
删除section 和 option      config.remove_section("default")
写入文件 config.write(open("ini", "w")) 
'''


class Config:

    def __init__(self):
        self.config_file = r"C:\Users\hewen\Desktop\main.ini"
        self.parser = configparser.ConfigParser()
        self.parser.read(self.config_file)

    def read_all(self):
        b = self.parser.options("main")
        c = self.parser.get("main", "mode1")
        print(c)


if __name__ == "__main__":
    Config().read_all()