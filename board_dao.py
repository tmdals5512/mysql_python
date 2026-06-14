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

    def show_content(self, login_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            id = int(input("내용을 조회 할 ID를 입력 하세요: "))
            # sql = """SELECT * FROM board WHERE ID = %d""" % (id)
            sql = """
            SELECT b.ID, b.user_id, b.title, b.content, b.created_at, u.user_id, b.updated_at
            FROM board b
            JOIN user u ON b.user_id = u.id
            WHERE b.ID = %s
            """ % (id) 
            # print(sql)
            cursor.execute(sql)
            result = cursor.fetchall()
            board_id = result[0][0]
            writer_no = result[0][1] 
            title = result[0][2]
            content = result[0][3]
            reg_time = result[0][4]
            user_id = result[0][5]
            updated_time = result[0][6]

            edited_tag = " (수정됨)" if reg_time != updated_time else ""

            print("\n" + "=" * 40)
            print(f"📄 게시글 상세조회 (ID: {board_id}){edited_tag}")
            print("=" * 40)
            print(f"🔹 제  목 : {title}")
            print(f"🔹 작성자 : {user_id}") 
            print(f"🔹 작성일 : {reg_time}")
            print("-" * 40)
            print(f"📝 내  용 :\n\n{content}")
            print("=" * 40 + "\n")
            
            reply_sql = """
            SELECT r.content, u.user_id, r.created_at, r.id, r.updated_at
            FROM reply r
            JOIN user u ON r.user_id = u.id
            WHERE r.board_id = %s
            ORDER BY r.created_at ASC
            """ % board_id
            cursor.execute(reply_sql)
            replies = cursor.fetchall()
            print(f"💬 댓글 ({len(replies)})")
            print("-" * 40)
            
            if replies:
                for reply in replies:
                    if reply[2] != reply[4]:
                        print(f"{reply[3]} {reply[1]} ({reply[2]}) (수정됨)")
                        print(reply[0])
                    else:
                        print(f"{reply[3]} {reply[1]} ({reply[2]})")
                        print(reply[0])
            else:
                print("아직 등록된 댓글이 없습니다.")
                
            print("=" * 40 + "\n")

            while True:
                print(" 1. 댓글 등록   2. 댓글 삭제  3. 댓글 수정  0. 메인으로")
                print("=" * 40)
                sub_menu = input("선택 > ")

                if sub_menu == '1': # 댓글 등록
                    
                    reply = input("댓글을 입력하세요 > ").strip()
                    if not reply:
                        print("댓글내용을 입력해야 합니다.")
                        continue
                    
                    insert_reply_sql = """
                    INSERT INTO reply (board_id, user_id, content) VALUES ('%s', '%s', '%s')
                    """ % (board_id, login_id, reply)
                    # print(insert_reply_sql)
                    cursor.execute(insert_reply_sql)
                    conn.commit()
                    print("댓글이 등록되었습니다.")
                    break

                elif sub_menu == '2': # 댓글 삭제
                    try:
                        reply_id = int(input("삭제할 댓글 번호를 입력하세요 > "))
                        delete_sql = """DELETE FROM reply WHERE id = '%s' AND user_id = '%s' AND board_id = '%s'""" % (reply_id, login_id, board_id)
                        # print(delete_sql)
                        affected_rows = cursor.execute(delete_sql)
                        conn.commit()

                        if affected_rows > 0 :
                            print("댓글이 성공적으로 삭제 되었습니다.")
                        else : 
                            print("댓글 삭제 실패")
                        break;
                    except ValueError:
                        print("숫자로 된 댓글 번호를 입력하세요.")
                
                elif sub_menu == '3': # 댓글 수정
                    try:
                        reply_id = int(input("수정 할 댓글 번호를 입력하세요 > "))
                        update_reply = input("댓글을 입력하세요 > ")
                        update_sql = """UPDATE reply 
                        SET content = '%s' 
                        WHERE id = '%s' AND user_id = '%s' AND board_id = '%s'""" % (update_reply, reply_id, login_id, board_id)
                        # print(update_sql)
                        affected_rows = cursor.execute(update_sql)
                        conn.commit()
                        
                        if affected_rows > 0 :
                            print("댓글이 성공적으로 수정 되었습니다.")
                        else : 
                            print("댓글 수정 실패")
                        break;

                    except ValueError:
                        print("숫자로 된 댓글 번호를 입력하세요.")

                elif sub_menu == '0':
                    break

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