import requests
import json
from requests import structures
from requests.cookies import RequestsCookieJar


class API(object):

    def __init__(self, url, session_id, login_id, course_id, timeout):
        session = requests.Session()
        session.headers = structures.CaseInsensitiveDict({
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6,th;q=0.5',
            'Accept': 'application/json, text/plain, */*',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'dataType': 'json',
            'Host': 'sdjj.ct-edu.com.cn',
            'Origin': 'https://sdjj.ct-edu.com.cn',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
        })
        jar = RequestsCookieJar()
        jar['homeUrl'] = 'http://www.ad.shu.edu.cn/IndexPage.html'
        jar['CLARITY_INDEX'] = '0'
        jar['SESSION'] = session_id
        session.cookies = jar
        self.session = session
        self.url = url
        self.login_id = login_id
        self.course_id = course_id
        self.timeout = timeout

    def execute(self, code, data):
        """执行接口请求"""

        params = {
            'functionCode': code,
        }
        resp = self.session.post(self.url, params=params, data=data, timeout=self.timeout)
        if resp.status_code == 200:
            json = resp.json()
            print(f'code: {json["returnCode"]}, message: {json["returnMessage"]}')
            return json

        print(f'status_code: {resp.status_code}, code: {code}, data: {data}')
        return None

    def get_homework_list(self):
        """获取家庭作业列表"""

        payload = {
            'courseId': self.course_id
        }
        data = self.execute('queryHomeworkList', payload)
        if data:
            return data['homeworkDataList']
        return []

    def get_homework(self, homework_id):
        """获取指定家庭作业信息"""

        payload = {
            'courseId': self.course_id,
            'homeworkId': homework_id,
        }
        data = self.execute('doHomework', payload)
        if not data:
            return [], [], 0

        title = data['homeworkObj']['title']
        status = data['homeworkObj']['status']
        print(f'title: {title}, status: {status}')

        question = data['questionObj']
        return question.get('danxuanList', []), question.get('duoxuanList', []), \
               question.get('panduanList', []), question['showTimestamp']

    def submit_homework(self, paper_id, timestamp, user_answer):
        """提交家庭作业"""

        answer_str = json.dumps(user_answer)
        payload = {
            'courseId': self.course_id,
            'paperId': paper_id,
            'showTimestamp': timestamp,
            'userAnswerJSONString': answer_str
        }
        self.execute('submitHomework', payload)

    def send_learn_time(self):
        """发送学习时间"""

        payload = {
            'courseId': self.course_id,
            'loginId': self.login_id,
            'learnTime': '300'
        }
        self.execute('sendLearnTime', payload)







