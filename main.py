from board_dao import * 

board_dao =BoardDAO()

#커넥션 테스트

board_dao.get_connection()
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
        board_dao.register()

    elif menu == "3":
        board_dao.show_content() 
    
    elif menu == "4":
        board_dao.delete_content()
    
    elif menu == "5":
        board_dao.update_content() 


print("게시판 종료")