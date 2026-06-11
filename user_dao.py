import pymysql

class UserDAO:
    def __init__(self):
        self.host = "localhost"
        self.user = "board_user"
        self.password = "board1234"
        self.database = "board_db"

    def get_connection(self):
        return pymysql.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database,
            charset = "utf8mb4" 
        )

    def login(self):
        """
        main.py에서 직접 호출하는 로그인 함수
        성공 시 유저 정보(튜플) 반환, 실패 시 None 반환
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        print("\n--- 로그인 ---")
        user_id = input("ID: ")
        password = input("Password: ")

        # 기존 board_dao의 스타일대로 %s 문자열 포매팅 방식을 사용합니다.
        sql = """SELECT id, user_id, name FROM user WHERE user_id = '%s' AND password = '%s'""" % (user_id, password)
        
        cursor.execute(sql)
        result = cursor.fetchone() # 조건에 맞는 유저 1명 가져오기 (결과는 튜플 형태)
        
        cursor.close()
        conn.close()

        if result:
            print(f"\n로그인 성공! {result[2]}님 환영합니다.")
            return result # (id, user_id, name) 형태의 데이터 반환
        else:
            print("\n로그인 실패: 아이디 또는 비밀번호가 일치하지 않습니다.")
            return None