import time
import random
import os

from api import API

session_id = os.getenv('SESSION_ID')    # 用户会话编号
login_id = os.getenv('LOGIN_ID')        # 登录编号
course_id = os.getenv('COURSE_ID')      # 课程编号

api = API(
    'https://sdjj.ct-edu.com.cn/learning/student/studentDataAPI.action',
    session_id,
    login_id,
    course_id,
    30,
)


def parse_answer(radio_questions, multiple_questions, judge_questions):
    """转换课程答案"""

    def __gen_answer_list(questions):
        return [{
            'id': q['id'],
            'uanswer': q['sanswer']
        } for q in questions]

    return {
        'danxuanUserAnswerList': __gen_answer_list(radio_questions),
        'duoxuanUserAnswerList': __gen_answer_list(multiple_questions),
        'panduanUserAnswerList': __gen_answer_list(judge_questions),
        'wendaUserAnswerList': []
    }


def await_time(min_time, max_time):
    """等待时间"""

    await_value = random.randint(min_time, max_time)
    time.sleep(await_value)


if __name__ == '__main__':
    data = api.get_homework_list()
    for item in data:
        if item['homeworkStatus'] == 3 and item['score'] > 60 or item['homeworkType'] == '2':
            continue

        id = item['id']
        radio_list, multiple_list, judge_list, timestamp = api.get_homework(id)
        answer = parse_answer(radio_list, multiple_list, judge_list)
        api.send_learn_time()

        # 延时等待
        await_time(120, 240)

        print(f'开始提交答案：{item["chapterTitle"]}')
        api.submit_homework(id, timestamp, answer)
        print(f'id: {id}, title: {item["chapterTitle"]}, 答案已成功提交!')
