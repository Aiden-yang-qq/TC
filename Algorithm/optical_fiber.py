from Function.func_collection import read_txt
from datetime import datetime, timedelta
from logging import warning, info


def read_fiber_data(rfd_data):
    """
    分析Data_***.txt文件
    :param rfd_data:
    :return:
    """
    data_all = []
    for d in rfd_data:
        wave_list = []
        d = d.replace('\t', ' ').split('|')
        for wave in d:
            if wave != ' \n':
                wave = wave.split()
                wave_list.append(wave)
        data_all.append(wave_list)
    return data_all


def read_fiber_data_simple(rfds_data):
    data_all = []
    for d in rfds_data:
        fiber_data_list = []
        d = d.replace('\t', ' ').split('|')
        date_time_temp = d[0].split()
        date_time = datetime.fromisoformat(date_time_temp[0].replace(',', ' '))
        temperature = float(date_time_temp[1])
        fiber_data = d[3].split()[:6]
        for i in fiber_data:
            # fiber_data_list.append(float(i))
            fiber_data_list.append(float(i))

        data_all.append([date_time, temperature, fiber_data_list])
    return data_all


def time_temp_wave(ttw_data):
    datetime_list = []
    temp_list = []
    wave_list = []
    for d in ttw_data:
        datetime_list.append(d[0])
        temp_list.append(d[1])
        wave_list.append(d[2])

    # 时间重置到100000microsecond
    counter = 0
    datetime_new_list = []
    time_microsecond = timedelta(microseconds=100000)
    for i in range(11):  # 采样频率为10Hz，1s10个数据点，取11为了能全部包含
        if datetime_list[i + 1] - datetime_list[i] == timedelta(seconds=1):
            counter = i + 1
            break
    original_datetime = datetime_list[counter]
    for j in range(-1 * counter, len(datetime_list) - counter):
        new_datetime = original_datetime + j * time_microsecond
        datetime_new_list.append(new_datetime)
    return datetime_new_list, temp_list, wave_list


def wave_collection(wave_list):
    wave_1 = []
    wave_2 = []
    wave_3 = []
    wave_4 = []
    wave_5 = []
    wave_6 = []
    for w in wave_list:
        wave_1.append(w[0])
        wave_2.append(w[1])
        wave_3.append(w[2])
        wave_4.append(w[3])
        wave_5.append(w[4])
        wave_6.append(w[5])
    return [wave_1, wave_2, wave_3, wave_4, wave_5, wave_6]


def time_wave(tw_time, tw_wave):
    try:
        tw_all_list = []
        for wave in tw_wave:
            if len(tw_time) == len(wave):
                tw_list = []
                for i in range(len(tw_time)):
                    tw_time_str = str(tw_time[i])
                    if len(tw_time_str) == 26:
                        tw_list.append(tw_time_str + ' ' + str(wave[i]))
                    else:
                        tw_list.append(tw_time_str + '.000000 ' + str(wave[i]))
                tw_all_list.append(tw_list)
        return tw_all_list
    except Exception as e:
        info(e)


if __name__ == '__main__':
    p = 'D:\\jaysk\\Desktop\\TP\\optical_fiber_data\\2020-07-01\\Available\\Data_20200701_160241.txt'
    data = read_txt(p)
    d_a = read_fiber_data_simple(data)
    ttw_date_list, ttw_temp_list, ttw_wave_list = time_temp_wave(d_a)
    wave_all = wave_collection(ttw_wave_list)

    # tw_txt = []
    # for each_wave in wave_all:
    #     tw_txt.append(time_wave(ttw_date_list,each_wave))
    tw_txt = time_wave(ttw_date_list, wave_all)