import os
import re

import pymongo
import xlrd

from .lk_logger import lk


def main(db_name, read_dir):
    """

    功能:
        将指定目录下的所有 excel 文件按照文件名作为表名, 录入到指定的数据库中

    注意事项:
        只读取 "xls" 和 "xlsx" 后缀的文件
        只读取每个 excel 文件的第一个 sheet
        请确保在处理的过程中 (和处理前), 目标目录下的 excel 文件没有被打开
        请预先确保第一行 (标题行字段) 是自己想要的格式

    :param db_name:
    :param read_dir:
    :return: db
    """
    return create_database(db_name, read_dir)


def create_database(db_name, read_dir):
    """
    
    使用须知

    功能说明:
        1. 支持批量文件处理
        2. 脚本启动后会弹出控制台, 会询问你要导入到哪个数据库 (输入数据库名称即可)
        3. 脚本会默认查找目录下的表格文件, 或者你也可以自定义某个绝对路径的目录作为参数传入

    注意事项:
        1. 在启动文件前, 请确保 MongoDB 服务已启动 (提示: 命令行输入 "mongod --dbpath
        $your_db_path$" 启动)
        2. 默认会把文件名作为表名录入
        3. 暂不支持判断数据库或表是否已存在, 为了您的安全, 请自行确保该数据库或表没有被覆盖的
        风险
        4. 该脚本默认会检查当前所在目录是否有名为 "data" 的文件夹, 如果有的话, 会将里面的文
        件作为要入库的 excel; 没有的话会将当前目录的所有表格类型的文件 (xlsx 以及 xls 后缀)
        作为待入库的表格对象. 如有其他需求 (例如你的表格文件位于其他盘下的某个目录里), 请在脚
        本启动后根据控制台提示填写你的自定义目录的绝对路径
        5. 暂不支持处理 ".csv" 后缀的表格文件
        6. 脚本处理完成后, 会提示你按任意键退出脚本控制台

    :param db_name: str.
    :param read_dir: str.
    :return: db
    """
    
    # 连接/创建数据库
    client = pymongo.MongoClient(host='localhost', port=27017)  # 首先启动客户端
    db = client[db_name]  # 然后连接/创建数据库
    
    # 这里脚本默认会查找脚本所在的文件夹有没有名为 "data" 的文件夹, 如果有的话, 则将 data 里
    # 面的文件认为是要处理的表格
    # 如果找不到 "data" 文件夹, 则脚本会认为用户把表格放在了与脚本同级的文件夹中, 则脚本会在
    # 同级搜集所有的文件 (后面会自动排除掉类型非表格的文件, 所以不要担心脚本把自己当成一个表格)
    if os.path.exists(read_dir):
        if read_dir[-1] != '/':
            read_dir += '/'
            # '../my_custom_data_folder' --> '../my_custom_data_folder/'
            # 这里做一个小处理, 如果传入的路径参数末尾不含斜杠, 则加上一个斜杠
            # 之所以这样做, 是为了在后面打开 workbook 的时候不会出错
    else:
        # noinspection PyProtectedMember
        read_dir = os.path._getfullpathname(os.path.abspath(__file__))
        # --> r'E:\workspace\smart_tools\excel_2_mongodb_tool\main_app.py'
        read_dir = read_dir.replace('\\', '/')
        # --> 'E:/workspace/smart_tools/excel_2_mongodb_tool/main_app.py'
        read_dir = re.sub(r'(/)(?!.*\1).+$', '', read_dir) + '/'
        # --> 'E:/workspace/smart_tools/excel_2_mongodb_tool/'
        lk.smart_prt('current directory', read_dir)
    
    files = os.listdir(read_dir)  # --> ['a.xlsx', 'b.xls', 'c.xlsx', ...]
    if not files:
        lk.smart_prt('[W2329] no excel found in your directory!')
        raise AttributeError
    
    for file in files:
        if '.xls' in file:
            lk.divider_line(file)  # 打印一条分割线
            lk.total_count += 1
            
            table_name = '_'.join(file.split('.')[:-1])
            # 'a.xlsx' --> ['a', 'xlsx'] --> 'a'
            # 'a.1.xlsx' --> ['a', '1', 'xlsx'] --> 'a_1'
            current_table = db[table_name]  # 以文件名为表名, 创建一张表
            
            workbook = xlrd.open_workbook(read_dir + file)
            # --> open_workbook('data/a.xlsx')
            sheet = workbook.sheet_by_index(0)  # 获得 sheet1 的数据
            
            # 获得第一行的表格数据, 一般来说这就是标题头, 可以作为字典的键名使用
            rows_tag = sheet.row_values(0)
            lk.smart_prt(rows_tag)
            
            # 开始遍历表格的每一行, 将每一行的数据作为一个对象录入到这张表中
            for j in range(1, sheet.nrows):
                row_data = dict(zip(rows_tag, sheet.row_values(j)))
                """example

                举个例子说明一下 zip(list, list) 的作用:
                    a = zip(['iii', 'jjj'],
                            ['uuu', 'vvv', 'www', 'xxx', 'yyy', 'zzz'])
                    print(a)  # --> <zip object at 0x0000019F876A8C48>
                    print(dict(a))  # --> {'iii': 'uuu', 'jjj': 'vvv'}
                    print(list(a))  # --> [('iii', 'uuu'), ('jjj', 'vvv')]

                所以经过此步骤我们得到的 row_data 为：
                    {
                        'name'  : 'Mark',
                        'gender': 'male',
                        'age'   : '23',
                        ...
                    }

                pymongo 可以接受 dict 类型的数据, 所以接下来直接将 row_data 插入到表
                中即可
                """
                current_table.insert_one(row_data)
    
    return db


if __name__ == '__main__':
    my_db = input('please input the db name which would be created or connected'
                  ' to: ')
    my_data_path = input("please input the data path "
                         "(press enter to use default path: 'data/'): ")
    main(my_db, my_data_path)
    
    lk.over()
    input('script executed over, press anykey to leave...')
