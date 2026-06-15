import pymysql
import getpass

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

        conn = self.get_connection()
        cursor = conn.cursor()
        
        print("\n--- 로그인 ---")
        user_id = input("ID: ")
        # password = input("Password: ")
        password = getpass.getpass("Password: ")
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
        
    def register_user(self):
        """회원 가입을 처리하는 함수"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        print("\n--- 회원 가입 ---")
        user_id = input("사용할 ID를 입력하세요: ")
        password = input("비밀번호를 입력하세요: ")
        name = input("이름(닉네임)을 입력하세요: ")
        email = input("이메일을 입력하세요 (선택): ")

        try:
            # user_id는 UNIQUE 제약 조건이 있으므로 중복 가입을 방지합니다.
            sql = """INSERT INTO user (user_id, password, name, email) 
                     VALUES ('%s', '%s', '%s', '%s')""" % (user_id, password, name, email)
            
            cursor.execute(sql)
            conn.commit()
            print("\n회원가입이 완료되었습니다! 로그인을 진행해 주세요.\n")
            
        except pymysql.serializers.err.IntegrityError:
            # 똑같은 ID로 가입을 시도할 때 발생하는 에러 처리
            print("\n오류: 이미 존재하는 아이디입니다. 다른 아이디를 사용하세요.\n")
        except Exception as e:
            print(f"\n오류 발생: {e}\n")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()