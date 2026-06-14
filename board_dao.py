import pymysql

class BoardDAO:

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

    def select_all(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        sql= """SELECT * FROM board ORDER BY id DESC"""

        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        return result
    
    def register(self, login_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        title = input("제목을 입력하시오: ")
        content = input("내용을 입력하시오: ")
        # name = input("사용자 이름을 입력하시오: ")

        sql = """INSERT INTO board (title, content, user_id) 
        VALUES ('{}', '{}', '{}');""".format(title, content, login_id)

        # print(sql)
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

    def show_content(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            id = int(input("내용을 조회 할 ID를 입력 하세요: "))
            # sql = """SELECT * FROM board WHERE ID = %d""" % (id)
            sql = """
            SELECT b.ID, b.user_id, b.title, b.content, b.created_at, u.user_id 
            FROM board b
            JOIN user u ON b.user_id = u.id
            WHERE b.ID = %s
            """ % (id) 
            # print(sql)
            cursor.execute(sql)
            result = cursor.fetchall()
            board_id = result[0][0]
            writer_no = result[0][1] # 기존의 작성자 번호 (예: 4)
            title = result[0][2]
            content = result[0][3]
            reg_time = result[0][4]
            user_id = result[0][5]

            print("\n" + "=" * 40)
            print(f"📄 게시글 상세조회 (ID: {board_id})")
            print("=" * 40)
            print(f"🔹 제  목 : {title}")
            print(f"🔹 작성자 : {user_id}") 
            print(f"🔹 작성일 : {reg_time}")
            print("-" * 40)
            print(f"📝 내  용 :\n\n{content}")
            print("=" * 40 + "\n")
            
        except ValueError:
            print("숫자만 입력하세요.")
            return
        
        except IndexError:
            print("해당 ID의 게시물이 존재하지 않습니다.")
            return
        
        finally:
            cursor.close()
            conn.close()

    def delete_content(self, login_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            id = int(input("삭제할 ID를 입력 하세요: "))
            sql = """DELETE FROM BOARD WHERE ID = %d AND USER_ID = '%s'""" % (id, login_id)
            cursor.execute(sql)
            conn.commit()

        except ValueError:
            print("숫자만 입력하세요.")
            return
        
        except IndexError:
            print("해당 ID의 게시물이 존재하지 않습니다.")
            return
        
        finally:
            cursor.close()
            conn.close()

    def update_content(self, login_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            id = int(input("수정 ID를 입력 하세요: "))
            new_title = input("새로운 제목을 입력하세요: ")
            new_content = input("새로운 내용을 입력하세요: ")
            sql = """UPDATE BOARD SET TITLE = '%s', CONTENT = '%s' WHERE ID = %d AND USER_ID = '%s'""" % (new_title, new_content, id, login_id)
            # print(sql)
            cursor.execute(sql)
            conn.commit()

        except ValueError:
            print("숫자만 입력하세요.")
            return
        
        except IndexError:
            print("해당 ID의 게시물이 존재하지 않습니다.")
            return
        
        finally:
            cursor.close()
            conn.close()