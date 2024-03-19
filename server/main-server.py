from flask import Flask, jsonify
import socket, threading, sys, pymysql, requests
import signal, json

app = Flask(__name__)

host = '127.0.0.1'
port = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

class_list = []
class_joiner = []

class Lecture:
    def __init__(self, id, name, user_id, password, file_id):
        self.lecture_name = name
        self.lecture_id = id
        self.user_id = user_id
        self.password = password
        self.file_id = file_id

    def open_lecture(self):
        print("open_lecture")
        
        with open("/home/jeongeunseong/python-project/server/ipaddress.json", "r") as f:
            print("debug")
            db_info = json.load(f)
            ip = db_info['ip']
            name = db_info['user_name']
            pw = db_info['password']
            db_name = db_info['db_name']
        print("debug0")
        conn = pymysql.connect(host=ip, user=name, password=pw, db=db_name, charset='utf8')
        # conn = pymysql.connect(host=ip, user=name, password=pw, db=db_name, charset='utf8')
        
        print("debug1")
        sql = "INSERT INTO Lecture (lecture_id, lecture_name, user_id, lecture_password, file_id) VALUES (%s, %s, %s, %s, %s)"
        cur = conn.cursor()
        print("debug2")
        cur.execute(sql, (self.lecture_id, self.lecture_name, self.user_id, self.password, self.file_id))
        print("debug3")
        conn.commit()  # 데이터베이스에 쿼리를 커밋합니다.
        print("debug4")
        conn.close()
        cur.close()
        print("debug5")
        return jsonify({"status": "success", "message": "Lecture opened"})


class Server:
    def __init__(self):
        self.broadcast = self.broadcast
        self.handle = self.handle
        self.receive = self.receive
        
        
    def get_lecture_info(self, client, questions):
        answers = []
        for question in questions:
            client.send(question.encode('ascii'))
            answer = client.recv(1024).decode('ascii')
            answers.append(answer)
        return answers
    
    def broadcast(self, message):
        for client in clients:
            client.send(message)
            
            
    def handle(self, client):
        while True:
            try:
                message = client.recv(1024)
                if b"join" in message:  # 바이트에서 문자열로 변환하여 "join"을 찾습니다.
                    print("check join1")
                    answer = self.get_lecture_info(client)
                    
                    for (index, value) in enumerate(answer):
                        print(f"Answer {index + 1}: {value}")
                    
                    
                    lecture = Lecture(id, name, user_id, password, file_id)
                    json_result = lecture.open_lecture()
                    self.broadcast(json_result.encode('ascii'))
                
                elif b"login" in message:
                    print("check login")
                    url = "http://localhost:5100/login"
                    name, password = message.decode('ascii').split(' ')[2], message.decode('ascii').split(' ')[3]
                    data = {
                        "name": name,
                        "password": password
                    }
                    try:
                        response = requests.get(url, params=data)
                        response.raise_for_status()
                        print(response.json())
                    except requests.exceptions.RequestException as e:
                        print(f"Error: {e}")
                
                
                # partially implement complete
                elif b"signup" in message:
                    user_id = 0
                    
                    # user_id 생성
                    url = "http://localhost:5100/generate_user_id"
                    try:
                        response = requests.get(url)
                        response.raise_for_status()
                        user_id = response.json()['user_id']
                        print(user_id)
                        print(response.json())
                    except requests.exceptions.RequestException as e:
                        print(f"Error: {e}")    
                    
                    
                    name = message.decode('ascii').split(' ')[2]
                    password = message.decode('ascii').split(' ')[3]
                    print(name, password, user_id)
                    url = "http://localhost:5100/signup"
                    data = {
                        "id": user_id,
                        "name": name,
                        "password": password,
                        "identity": 1
                    }
                    try:
                        response = requests.get(url, params=data)
                        response.raise_for_status()
                        print(response.json())
                    except requests.exceptions.RequestException as e:
                        print(f"Error: {e}")
                
                else:
                    self.broadcast(message)
                    
            except:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                self.broadcast("{} left!\n".format(nickname).encode('ascii'))
                self.broadcast("{} people in this room!\n".format(len(nicknames)).encode('ascii'))
                nicknames.remove(nickname)
                break

    def receive(self):
        while True:
            # 클라이언트 연결 수락
            client, address = server.accept()
            print("Connected with {}".format(str(address)))
            
            
            client.send('NICKNAME'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')
            nicknames.append(nickname)
            clients.append(client)
            
            
            print("Nickname is {}".format(nickname))
            self.broadcast("{} joined!\n".format(nickname).encode('ascii'))
            self.broadcast("{} people in this room!\n".format(len(nicknames)).encode('ascii'))
            client.send('Connected to server!'.encode('ascii'))
            
            
            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()

# Ctrl+C 시그널 핸들러
def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    server.close()  # 서버 소켓 닫기
    sys.exit(0)

# 시그널 핸들러 등록
signal.signal(signal.SIGINT, signal_handler)

# Flask 서버 시작
if __name__ == '__main__':
    sv = Server()
    thread = threading.Thread(target=sv.receive)
    thread.start()
    app.run(debug=True, threaded=True, port=5000)