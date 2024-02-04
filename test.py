import datetime
import random
import time
import schedule


def my_task():
    print("任务执行：", datetime.datetime.now())


def generate_random_times(start, end, num):
    random_times = []
    for _ in range(num):
        random_time = start + (end - start) * random.uniform(0.1, 0.9)
        random_times.append(random_time)
    return random_times


def schedule_tasks(random_times):
    for rt in random_times:
        # schedule库不直接支持datetime时间，所以我们需要转换成特定的格式
        schedule_time = rt.strftime("%H:%M")
        print(f"任务将在 {schedule_time} 执行")
        schedule.every().day.at(schedule_time).do(my_task)


# 设置开始和结束时间
start_time = datetime.datetime.now()
end_time = start_time + datetime.timedelta(minutes=10)  # 设置1小时后为结束时间

# 生成5个随机时间点
random_times = generate_random_times(start_time, end_time, 20)

# 安排任务
schedule_tasks(random_times)

# 循环运行，直到所有任务完成
while True:
    schedule.run_pending()
    print(schedule.jobs)
    time.sleep(1)
