# -*- coding: utf-8 -*-
from logging import basicConfig, DEBUG, info
from os import getcwd, path
from time import time, sleep, ctime

# from matplotlib import pyplot as plt
from Algorithm.data_splitting_integration import optical_data_splitting, optical_data_to_wheel
from Algorithm.algorithm_main import al_main_weight
from Config import ConfigInfo
from Database.data_storage import car_json_integration, write_json
from Database.data_collection import format_conversion
from Database.scanning_interface import database_creation

basicConfig(filename='logging_file.log', level=DEBUG)


def main_exe():
    x_wheel_data = []
    all_wheel_data = []
    try:
        # 主程序路径读取
        main_path = getcwd()
        # main_path = path.realpath(getcwd())
        # main_path = path.dirname(path.realpath(argv[0]))

        # 配置文件确认
        config_dir = main_path + '\\Config\\config.ini'
        cfp = path.exists(config_dir)

        if cfp:
            # 配置文件的信息读取
            conf = ConfigInfo()
            o_f_frequency = int(conf.get_optical_fiber_frequency())
            print('当前采样频率:%sHz' % o_f_frequency)

            # 数据预处理
            format_conversion(main_path)  # 进行数据预处理，并保存在Original_DB文件夹下

            info('---------------------------------------')
            info(ctime())
            print('数据正在处理，请稍等……')
            a = time()

            # 检测数据库中txt和AEI文件并读取，folders中为12个传感器的数据
            json_file_name, folders, all_car_aei = database_creation(main_path)

            # 数据库中有txt文件后，对folders读取，并做车轮数据提取整合，然后保存成json文件
            # optical_fiber_data的输出格式：三维列表[12个传感器×32个车轮车×600个数据][12×32×600]的矩阵
            optical_fiber_data = optical_data_splitting(folders, o_f_frequency)
            # all_wheel_data的输出格式:三维列表[32个车轮×2个车轮×3600个数据][32×2×3600]的矩阵
            x_wheel_data, all_wheel_data = optical_data_to_wheel(optical_fiber_data, o_f_frequency)

            # 计算车辆相关参数的重量
            all_weight = al_main_weight(all_wheel_data)

            # 将车轮数据保存成json文件
            if len(json_file_name) != 0:
                all_car_set_json = car_json_integration(json_file_name, x_wheel_data, all_wheel_data,
                                                        all_weight, all_car_aei)
                write_json(json_file_name, all_car_set_json)

            b = time()
            print('数据处理耗时:%.4fs，程序结束！' % (b - a))
            sleep(1)
            info('本次数据处理已完成，共耗时%.4fs:' % (b - a))
            info('---------------------------------------')
        else:
            print('配置文件缺失，请再次确认！')
            info('配置文件缺失，请再次确认！')
            sleep(1)
    except Exception as e:
        info('main_error:', e)

    # info('---------------------------------------')
    # info(ctime())
    # print('数据正在处理，请稍等……')
    # a = time()
    # main_path = getcwd()
    # folders = database_creation(main_path)
    # b = time()
    # print('数据处理耗时:%.4fs，程序结束！' % (b - a))
    # sleep(3)
    # info('本次数据处理已完成，共耗时%.4fs:' % (b - a))
    # info('---------------------------------------')
    return x_wheel_data, all_wheel_data


if __name__ == '__main__':
    x, y = main_exe()

    # plt.figure()
    # plt.plot(x, y[0][0])
    # # plt.plot(folders[0][0], folders[0][1])
    # plt.grid()
    # plt.show()
