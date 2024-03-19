# CREATE TABLE `User` (
#     `user_id` BIGINT NOT NULL PRIMARY KEY,
#     `user_name` VARCHAR(45) NOT NULL,
#     `user_password` VARCHAR(45) NOT NULL,
#     `user_mode` ENUM('prof', 'stud', 'manager') NOT NULL DEFAULT 'stud'
# );

# CREATE TABLE `File` (
#     `file_id` BIGINT NOT NULL PRIMARY KEY,
#     `lecutre_id` BIGINT NOT NULL,
#     `file_location` VARCHAR(256) NOT NULL,
#     `user_id` BIGINT NOT NULL,
#     FOREIGN KEY (`user_id`) REFERENCES `User`(`user_id`)
# );

# CREATE TABLE `lecutre_id` (
#     `lecutre_id` BIGINT NOT NULL PRIMARY KEY,
#     `user_id` BIGINT NOT NULL,
#     `lecutre_password` INT NOT NULL,
#     `file_id` BIGINT,
#     FOREIGN KEY (`user_id`) REFERENCES `User`(`user_id`),
#     FOREIGN KEY (`file_id`) REFERENCES `File`(`file_id`)
# );






from flask import Flask, jsonify, request
import pymysql
import json

class User:
    
    def login(self):
        user_id = request.args.get('id')
        user_password = request.args.get('password')
        
        with open("/home/jeongeunseong/python-project/server/ipaddress.json", "r") as f:
            db_info = json.load(f)
            ip = db_info['ip']
            name = db_info['user_name']
            pw = db_info['password']
            db_name = db_info['db_name']
        conn = pymysql.connect(host=ip, user=name, password=pw, db=db_name, charset='utf8')
        
        sql = "SELECT * FROM User WHERE user_id = %s AND user_password = %s"
        cur = conn.cursor()
        cur.execute(sql, (user_id, user_password))
        result = cur.fetchall()
        conn.close()
        cur.close()
        if len(result) == 0:
            return jsonify({"status": "fail", "message": "User not found"})
        else:
            return jsonify({"status": "success", "message": "User logged in"})
    
    def signup(self):
        user_id = request.args.get('id')
        user_name = request.args.get('name')
        user_password = request.args.get('password')
        user_identity = request.args.get('identity')
        
        with open("/home/jeongeunseong/python-project/server/ipaddress.json", "r") as f:
            db_info = json.load(f)
            ip = db_info['ip']
            name = db_info['user_name']
            pw = db_info['password']
            db_name = db_info['db_name']
        print(ip, name, pw, db_name)
        conn = pymysql.connect(host=ip, user=name, password=pw, db=db_name, charset='utf8')
        sql = "INSERT INTO User (user_id, user_name, user_password, user_mode) VALUES (%s, %s, %s, %s)"
        cur = conn.cursor()
        cur.execute(sql, (user_id, user_name, user_password, user_identity))
        conn.commit()
        conn.close()
        cur.close()
        return jsonify({"status": "success", "message": "User signed up"})
    
    def generate_user_id(self):
        with open("/home/jeongeunseong/python-project/server/ipaddress.json", "r") as f:
            db_info = json.load(f)
            ip = db_info['ip']
            name = db_info['user_name']
            pw = db_info['password']
            db_name = db_info['db_name']
        
        conn = pymysql.connect(host=ip, user=name, password=pw, db=db_name, charset='utf8')
        sql = "SELECT MAX(user_id) FROM User"
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        conn.close()
        cur.close()
        return jsonify({"status": "success", "message": "User id", "user_id": result[0][0] + 1})

class lecutre:
    def __init__(self):
        self.lecutre_id = 0
        self.user_id = 0
        self.lecutre_password = 0
        self.file_id = 0
    
    def lecutre_open(self):
        lecutre_id = request.args.get('lecutre_id')
        lecutre_password = request.args.get('lecutre_password')
        
        with open("/home/jeongeunseong/python-project/server/ipaddress.json", "r") as f:
            db_info = json.load(f)
            ip = db_info['ip']
            name = db_info['user_name']
            pw = db_info['password']
            db_name = db_info['db_name']
        conn = pymysql.connect(host=ip, user=name, password=pw, db=db_name, charset='utf8')
        
        sql = "SELECT * FROM lecutre WHERE lecutre_id = %s AND lecutre_password = %s"
        cur = conn.cursor()
        cur.execute(sql, (lecutre_id, lecutre_password))
        result = cur.fetchall()
        conn.close()
        cur.close()
        if len(result) == 0:
            return jsonify({"status": "fail", "message": "lecutre not found"})
        else:
            return jsonify({"status": "success", "message": "lecutre opened"})
        
class Server:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/check_connection', methods=['GET'])
        def check_connection():
            return jsonify({"status": "success", "message": "User logged in"})

        @self.app.route('/signup', methods=['GET', 'POST'])
        def signup():
            user = User()
            user.signup()
            return jsonify({"status": "success", "message": "User signed up"})
        
        @self.app.route('/login', methods=['GET', 'POST'])
        def login():
            user = User()
            user.login()
            return jsonify({"status": "success", "message": "User logged in"})
        
        
        @self.app.route('/generate_user_id', methods=['GET'])
        def generate_user_id():
            user = User()
            return user.generate_user_id()

    def run(self):
        self.app.run(port=5100, debug=False, threaded=True) 




if __name__ == '__main__':
    server = Server()
    server.run()