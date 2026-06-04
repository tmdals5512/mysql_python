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
    
    def register(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        title = input("제목을 입력하시오: ")
        content = input("내용을 입력하시오: ")
        name = input("사용자 이름을 입력하시오: ")

        sql = """INSERT INTO board (title, content, writer)
        VALUES ('{}', '{}', '{}');""".format(title, content, name)

        #print(sql)
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

    def show_content(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            id = int(input("내용을 조회 할 ID를 입력 하세요: "))
            sql = """SELECT * FROM board WHERE ID = %d""" % (id)
            # print(sql)
            cursor.execute(sql)
            result = cursor.fetchall()
            # print(result)
            print("ID:", result[0][0])
            print("제목:", result[0][1])
            print("작성자:", result[0][3])
            print("작성시각:", result[0][4])
            print("내용:", result[0][2])
        
        except ValueError:
            print("숫자만 입력하세요.")
            return
        
        except IndexError:
            print("해당 ID의 게시물이 존재하지 않습니다.")
            return
        
        finally:
            cursor.close()
            conn.close()

    def delete_content(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            id = int(input("삭제할 ID를 입력 하세요: "))
            sql = """DELETE FROM BOARD WHERE ID = %d""" % (id)
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