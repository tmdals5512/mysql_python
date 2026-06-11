from board_dao import * 
from user_dao import UserDAO

board_dao =BoardDAO()
user_dao = UserDAO()

#커넥션 테스트

board_dao.get_connection()

login_user = None

while True:
    print("=" * 40)
    print("               로그인               ")
    print("=" * 40)
    
    login_user = user_dao.login() 
    
    if login_user is not None:
        break
    else:
        print("로그인 실패! 다시 시도하시겠습니까?")
        retry = input("종료하려면 '0'을 입력하고, 다시 시도하려면 아무 키나 누르세요: ")
        if retry == "0":
            print("프로그램을 종료합니다.")
            exit() # 프로그램 강제 종료

while True:
    print("=" * 40)
    print("1.목록 2.등록 3.내용 4.삭제 5.수정 0.종료")
    print("=" * 40)

    menu = input("선택 > ")

    if menu == "0":
        break
    elif menu == "1":
        boards = board_dao.select_all()
        # print(boards)

        for board in boards:
            print(board[0],board[1],board[2],board[3])

    elif menu == "2":
        board_dao.register(login_user[0])

    elif menu == "3":
        board_dao.show_content() 
    
    elif menu == "4":
        board_dao.delete_content(login_user[0])
    
    elif menu == "5":
        board_dao.update_content(login_user[0]) 


print("게시판 종료")