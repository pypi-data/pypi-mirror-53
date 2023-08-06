zlparse_time 包 ：是用来时间数据挖掘的。
后期所需要的变更的操作可以通过以下api完成。



note = """
time : 2019年8月22日10:39:01
一切都是可配置的，
可以进行对 parse_time 方法 进行增删改差操作：
    1. 对数据库 quyu_time_func 各个地区的时间操作函数 进行配置
        from zlparse.zlparse_time.conf import update,delete
        更新：
            update(quyu, time_func, conp)
        删除：
            delete(quyu, conp)

    2. 对 common.py 和 exec_func_f.py 函数地区解析时间的方法， 进行操作
        from zlparse.zlparse_time.conf import add_func,delete_func

        用法:
            funcxxx = '''def extime_v2xxxxxx(ggstart_time,page):
                if ggstart_time is not None:
                    res = ggstart_time
                else:
                    res = extime(ggstart_time,page)
                return res'''
            delete_func(funcxxx)
            add_func(funcxxx)

    3. 对本地 quyu_time_func.json 文件进行增加或删除操作。
        from zlparse.zlparse_time.conf import add_quyu_time_func_json,del_quyu_time_func_json
        增加用法：
            add_quyu_time_func_json(quyu_name, time_func)
        删除：
            del_quyu_time_func_json(quyu_name, time_func)

    4. 将本地 quyu_time_func.json 文件同步到指定数据库中。
        用法：

            file_to_db(conp)

"""

conf.py文件用法：
    '''
1. 增加时间解析函数用法：

定义所要增加的函数：func=''   # 完整的函数
add_func(func)

2. 删除某个时间解析函数：
del_funct = 'extime_guangx33333i_baise_gcjs'
delete_func(func)
func可以是完整函数或者函数名。

3。 将本地json文件，复制到db中：
file_to_db(conp)   # conp为目标数据库位置
conp = ["postgres", "since2015", "192.168.3.171", "anbang", "test"]

4. 对数据库进行操作：
    1.插入某个quyu新的时间解析对应的方法：insert(quyu, time_func, conp)
    2.更新某个quyu对应的时间解析方法：update(quyu, time_func, conp)
    3.删除某个quyu对应的时间解析方法：delete(quyu, conp)

'''