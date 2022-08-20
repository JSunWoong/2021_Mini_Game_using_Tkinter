from tkinter import Button, Label, Menu, Entry
from tkinter import messagebox
from PIL import Image, ImageTk
import tkinter as tk
import turtle as t
import winsound
import random
import timeit
import time
import ast
import sys
import os

## global variable in game ##
coin = 1000
user = ""

## Set the image file path to use the pyinstaller module. ##
# 실행하는 경로에 있는 위치로부터 상대경로를 불러옴.
# base_path : 현재 위치 , relative_path : 현재 위치로부터 상대경로를 불러옴.
# pyinstaller --onefile --add-data='src경로 및 데이터;dst경로(저장공간)' pyfile  ( 예시 )
# 터미널 보이기 (관리자용): pyinstaller --onefile --add-data="./datasheet.txt;." --add-data="./wordlist.txt;." --add-data="./img/*.png;./img" --add-data="./img/*.ico;./img" main_frame.py
# 터미널 숨기기 (사용자용): pyinstaller --noconsole --onefile --add-data="./datasheet.txt;." --add-data="./wordlist.txt;." --add-data="./img/*.png;./img" --add-data="./img/*.ico;./img" main_frame.py
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

## game related function ##
def game_over():
    global coin
    global check_start

    if coin <= 0:
        check_end = timeit.default_timer()
        messagebox.showinfo("Game Over", "게임 오버.\n플레이 시간: %d초"%(check_end - check_start))
        window.destroy()


def game_penalty():
    global coin
    coin -= 50
    screen_main()

def game_lose():
    Label(window, text=" LOSE ! ", bg="#DEE2FF", font=("Comic Sans MS", 40)).place(x=380,y=420) # lose
    Button(window, text="Back to Menu",  bg="#DEE2FF", activebackground="#DEE2FF", bd=0, fg="#00669F",
           font=("Comic Sans MS", 40),width=15, height=2, command=lambda: screen_main()).place(x=0, y=500)
    Button(window, text="Game Off",  bg="#DEE2FF", activebackground="#DEE2FF", bd=0, fg="#00669F",
           font=("Comic Sans MS", 40),width=15, height=2, command=window.quit).place(x=430, y=500)

def game_win():
    Label(window, text=" WIN ! ", bg="#DEE2FF", font=("Comic Sans MS", 40)).place(x=390,y=420)  # win
    Button(window, text="Back to Menu",  bg="#DEE2FF", activebackground="#DEE2FF", bd=0, fg="#00669F",
           font=("Comic Sans MS", 40),width=15, height=2, command=lambda: screen_main()).place(x=0, y=500)
    Button(window, text="Game Off",  bg="#DEE2FF", activebackground="#DEE2FF", bd=0, fg="#00669F",
           font=("Comic Sans MS", 40),width=15, height=2, command=window.quit).place(x=430, y=500)

# hangman image load
def hngman_image_load():
    # image route
    path_dir = './img/'

    # image list road  (hangman)
    img_list = os.listdir(resource_path(path_dir))

    # hangman images load : h_img
    h_img = []
    for img_name in img_list:
        if int(len(img_name)) == 6:
            img_path = path_dir + img_name
            h_img.append(ImageTk.PhotoImage(Image.open(resource_path(img_path)).resize((350, 350))))

    return h_img

# turtle coin game random pos function
def rand_pos():
    x_cor = random.randint(-420, 420)
    y_cor = random.randint(-180, 180)
    return x_cor, y_cor

## root terminal printing option ##
# first root terminal print
def printing_root():
    print("##################################")
    print("###### 관리자 터미널 입니다 ######")
    print("##################################\n")

# enter game (terminal printing)
def printing_mv_title(title_name):
    global user, coin
    print(f"\n========== {title_name} ==========")
    print(f"user: {user}")
    print(f"coin: {coin}")


## screen option ##
# clear frame
def clear_frame():
    for widget in window.winfo_children():
        widget.destroy()

# screen design
def line_design():
    text = " "
    for void_word in range(300): text += "     "
    design_line = Label(window, text=text, bg="#FEEAFA", font=('', 1))
    design_line.place(x=0,y=650)

# menu bar
def func_msg():
    messagebox.showinfo("Making","17th 장 선 웅\n18th 강 영 원\n21th 이 병 주")

def menu_bar():
    menubar = Menu(window)
    infomenu = Menu(menubar, tearoff=0)
    window.iconbitmap(resource_path('img/4.ico'))

    infomenu.add_command(label="Producer",command=func_msg)
    infomenu.add_command(label="Exit", command=window.quit)
    menubar.add_cascade(label="MENU", menu=infomenu)
    window.config(menu=menubar)

# back to menu & show user information
def penalty_back_button():
    back_bt = Button(window, text="BACK", bg="#DEE2FF", activebackground="#DEE2FF", font=("Comic Sans MS", 30),
                     fg="#00669F", bd=0, command=game_penalty)
    back_bt.place(x=700, y=10)

def show_user_info():
    get_coin = 'COIN : ' + str(coin)
    coin_label = Label(window, text=get_coin, bg="#DEE2FF", font=("Comic Sans MS", 20))
    coin_label.place(x=10, y=10)

    get_user_name = 'USER : ' + user
    user_name_label = Label(window, text=get_user_name, bg="#DEE2FF", font=("Comic Sans MS", 20))
    user_name_label.place(x=10, y=50)

def back_button():
    back_bt = Button(window, text="BACK", bg="#DEE2FF", activebackground="#DEE2FF", font=("Comic Sans MS", 30),
                     fg="#00669F", bd=0, command=lambda: screen_main())
    back_bt.place(x=700, y=10)


## show screen ##
# signin, signup page
def login_page():
    clear_frame()
    menu_bar()

    # title
    line_design()
    login_title = Label(window, text="LOGIN", bg='#DEE2FF', font=("Comic Sans MS", 40, "bold"))
    login_title.place(x=365, y=140)


    # user id, password variable
    user_id, password = tk.StringVar(), tk.StringVar()

    # compare user id, password
    def check_data():
        global user
        global coin
        with open(resource_path('datasheet.txt'), 'r') as f:
            get_user_list = f.read()

            # 딕셔너리로 변환
            user_list = ast.literal_eval(get_user_list)

        id = user_id.get()
        pw = password.get()

        # 로그인 체크 알고리즘
        if id in user_list.keys() and pw == user_list[id]:
            messagebox.showinfo("로그인 성공", "로그인에 성공하였습니다.")
            user = id

            print(f"===== {user} 님이 입장하였습니다. =====")

            if user == "root": coin = 1000000
            screen_main()
        else:
            messagebox.showwarning('로그인 실패', '아이디 또는 패스워드가 옳바르지 않습니다.')


    # id, password, Graphic UI
    name_label = Label(window, text="Username", bg='#DEE2FF', font=("Comic Sans MS", 20))
    pwd_label = Label(window, text="Password", bg='#DEE2FF', font=("Comic Sans MS", 20))

    name_entry = Entry(window, textvariable=user_id, font=("Comic Sans MS", 15))
    pwd_entry = Entry(window, textvariable=password, show="*", font=("Comic Sans MS", 15))

    signin_button = Button(window, text="Sign in", command=check_data, font=("Comic Sans MS", 25, "bold"),
                           bg='#DEE2FF', fg="#00669F", activebackground="#DEE2FF", bd=0)
    signup_button = Button(window, text="Sign up", command=lambda: signup_page(), font=("Comic Sans MS", 25, "bold"),
                           bg='#DEE2FF', fg="#00669F", activebackground="#DEE2FF", bd=0)

    # placement
    name_label.place(x=250, y=260)
    name_entry.place(x=400, y=270)
    pwd_label.place(x=250, y=330)
    pwd_entry.place(x=400, y=340)
    signin_button.place(x=265, y=400)
    signup_button.place(x=475, y=400)

def signup_page():
    clear_frame()
    menu_bar()

    # title
    line_design()
    login_title = Label(window, text="Sign Up", bg='#DEE2FF', font=("Comic Sans MS", 40, "bold"))
    login_title.place(x=355, y=140)

    # user id, password variable
    user_id, password, password2 = tk.StringVar(), tk.StringVar(), tk.StringVar()

    # compare user id, password
    def check_data():
        id = user_id.get()
        pw1 = password.get()
        pw2 = password2.get()

        # 로그인 체크 알고리즘
        # confirm same user id
        with open(resource_path('datasheet.txt'), 'r') as f:
            get_user_list = f.read()

            # 딕셔너리로 변환
            user_list = ast.literal_eval(get_user_list)

        if id in user_list.keys():
            messagebox.showwarning('아이디 만들기 실패', '같은 아이디가 존재합니다.\n다른 아이디를 사용해주세요.')

        # confirm password and excution signup
        elif pw1 == pw2:
            with open(resource_path('datasheet.txt'), 'r+') as f:
                get_user_list = f.read()

                # 딕셔너리로 변환
                user_list = ast.literal_eval(get_user_list)

                add_user_dict = {id:pw1}
                user_list.update(add_user_dict) # 리스트값 여러개 추가
                f.truncate(0)  # 파일 용량 0으로 변경

            with open(resource_path('datasheet.txt'), 'w') as f2:
                f2.write(str(user_list))

            print("계정이 생성되었습니다.")
            print("ID: ", id)
            print("PW: ", pw1)

            messagebox.showinfo("아이디 만들기 성공", "Welcome! 어서 로그인을 해보세요!!")
            login_page()
        else:
            messagebox.showwarning('아이디 만들기 실패', '패스워드가 같은지 확인해주세요.')

    # print account list in terminal
    def printing_account_list():
        with open(resource_path('datasheet.txt'), 'r') as f:
            get_user_list = f.read()

        # 딕셔너리로 변환
        user_list = ast.literal_eval(get_user_list)

        num = 0
        for tmp_id in user_list.keys():
            print(f"[{num+1}]번째 계정")
            print(f"ID: {tmp_id}")
            print(f"PW: {user_list[tmp_id]}")
            num+=1

    # id, password, Graphic UI
    name_label = Label(window, text="New Username", bg='#DEE2FF', font=("Comic Sans MS", 20))
    pwd_label = Label(window, text="New Password", bg='#DEE2FF', font=("Comic Sans MS", 20))
    pwd_label2 = Label(window, text="Confirm Password", bg='#DEE2FF', font=("Comic Sans MS", 20))

    name_entry = Entry(window, textvariable=user_id, font=("Comic Sans MS", 15))
    pwd_entry = Entry(window, textvariable=password, font=("Comic Sans MS", 15))
    pwd_entry2 = Entry(window, textvariable=password2, font=("Comic Sans MS", 15))

    back_login_button = Button(window, text="Back", command=lambda: login_page(), font=("Comic Sans MS", 25, "bold"),
                           bg='#DEE2FF', fg="#00669F", activebackground="#DEE2FF", bd=0)
    signup_button = Button(window, text="Sign up", command=check_data, font=("Comic Sans MS", 25, "bold"),
                           bg='#DEE2FF', fg="#00669F", activebackground="#DEE2FF", bd=0)
    root_account_label = Button(window, text="🔑", command=printing_account_list, font=("Comic Sans MS", 25, "bold"),
                           bg='#DEE2FF', fg="#FEEAFA", activebackground="#DEE2FF", bd=0)

    # placement
    root_account_label.place(x=820,y=0)
    name_label.place(x=200, y=260)
    name_entry.place(x=400, y=270)
    pwd_label.place(x=205, y=330)
    pwd_entry.place(x=400, y=340)
    pwd_label2.place(x=160, y=400)
    pwd_entry2.place(x=400, y=410)
    back_login_button.place(x=265, y=470)
    signup_button.place(x=475, y=470)


# main page
def screen_main():
    clear_frame()
    menu_bar()
    line_design()
    game_over()

    # root terminal printing
    title_name = "Game Menu"
    printing_mv_title(title_name)

    # get user info
    get_coin = 'COIN : ' + str(coin)
    coin_label = Label(window, text=get_coin, bg="#DEE2FF", font=("Comic Sans MS", 20))
    coin_label.place(x=10, y=10)

    get_user_name = 'USER : ' + user
    user_name_label = Label(window, text=get_user_name, bg="#DEE2FF", font=("Comic Sans MS", 20))
    user_name_label.place(x=10, y=50)

    # menu label
    l1 = Label(window, text=title_name, fg='black', bg='#DEE2FF', font=('Comic Sans MS', 40, 'bold'))
    l2 = Label(window, text="GAME", fg='black', bg='#DEE2FF', font=('Comic Sans MS', 28, 'bold'))
    l3 = Label(window, text="ETC", fg='black', bg='#DEE2FF', font=('Comic Sans MS', 28, 'bold'))

    # label place
    l1.place(x=310, y=80)
    l2.place(x=165, y=180)
    l3.place(x=630, y=180)

    # show divisive line
    # PhotoImage함수에서 지역 변수에 대입되는 잘 알려진 문제가 있다.
    # 이로인해 이미지 출력이 안되는 오류가 존재.
    # 따라서 전역변수 global 처리를 해야 보인다.
    global divline_img

    pre_img = Image.open(resource_path('./img/divline.png')).transpose(Image.ROTATE_90)   # 90도 회전
    pre_img = pre_img.resize((40, 280))
    divline_img = ImageTk.PhotoImage(pre_img)
    div_label = Label(window, bg='#DEE2FF', image=divline_img)
    div_label.place(x=430, y=230)

    # menu button
    hngman_bt = Button(window, text="Hangman", bg="#DEE2FF", activebackground="#DEE2FF", fg="#00669F",
                       font=("Comic Sans MS", 30), bd=0, command=lambda: screen_game_1())
    ttl_race_bt = Button(window, text="Turtle Race", bg="#DEE2FF", activebackground="#DEE2FF", fg="#00669F",
                         font=("Comic Sans MS", 30), bd=0, command=lambda: screen_game_2())
    ttl_coin_bt = Button(window, text="Trutle Coin", bg="#DEE2FF", activebackground="#DEE2FF", fg="#00669F",
                         font=("Comic Sans MS", 30), bd=0, command=lambda: screen_game_3())

    produce_bt = Button(window, text="Project Details", bg="#DEE2FF", activebackground="#DEE2FF", fg="#00669F",
                        font=("Comic Sans MS", 30), bd=0, command=lambda: screen_details_1())
    explain_bt = Button(window, text="Game Rules", bg="#DEE2FF", activebackground="#DEE2FF", fg="#00669F",
                        font=("Comic Sans MS", 30), bd=0, command=lambda: screen_rule_1())
    exit_bt = Button(window, text="Exit", bg="#DEE2FF", activebackground="#DEE2FF", fg="#00669F",
                     font=("Comic Sans MS", 30), bd=0, command=window.quit)

    # button place
    hngman_bt.place(x=125, y=240)
    ttl_race_bt.place(x=95, y=320)
    ttl_coin_bt.place(x=100, y=400)

    produce_bt.place(x=520, y=240)
    explain_bt.place(x=545, y=320)
    exit_bt.place(x=616, y=400)

# hangman game page
def screen_game_1():
    clear_frame()
    menu_bar()
    show_user_info()
    penalty_back_button()

    # root terminal printing
    title_name = "HANG MAN"
    printing_mv_title(title_name)

    # game head title
    word = Label(window, text=title_name, width=10, height=2, fg="black", bg='#DEE2FF', font=("Comic Sans MS", 40))
    word.pack(side='top', padx=0)

    global hangman_img_list
    global words_label_list
    global win_count
    global life

    life = 0  # life
    win_count = 0
    fin = False  # loop end key


    # main loop
    while not fin:
        life = 0  # life
        win_count = 0

        # word choice
        with open(resource_path('wordlist.txt'), 'r') as f:
            x = f.readlines()
            words = random.choice(x)[:-1].upper()
            # test용 답안
            print(f"Answer : {words}")


        # display underbar
        words_label_list = []
        blnk = 370

        for i in range(len(words)):
            blnk += 60
            words_label = Label(window, text="_", bg='#DEE2FF', font=("Comic Sans MS", 40), bd=1)
            words_label.place(x=blnk, y=300)
            words_label_list.append(words_label)


        # alphabet position set imformation (button)
        button_place = [['bt1', 'A', 0, 480], ['bt2', 'B', 70, 480], ['bt3', 'C', 140, 480], ['bt4', 'D', 210, 480],
                        ['bt5', 'E', 280, 480], ['bt6', 'F', 350, 480], ['bt7', 'G', 420, 480], ['bt8', 'H', 490, 480],
                        ['bt9', 'I', 560, 480], ['bt10', 'J', 630, 480], ['bt11', 'K', 700, 480], ['bt12', 'L', 770, 480],
                        ['bt13', 'M', 830, 480], ['bt14', 'N', 0, 570], ['bt15', 'O', 70, 570], ['bt16', 'P', 140, 570],
                        ['bt17', 'Q', 210, 570], ['bt18', 'R', 280, 570], ['bt19', 'S', 350, 570], ['bt20', 'T', 420, 570],
                        ['bt21', 'U', 490, 570], ['bt22', 'V', 560, 570], ['bt23', 'W', 630, 570], ['bt24', 'X', 700, 570],
                        ['bt25', 'Y', 770, 570], ['bt26', 'Z', 830, 570]]

        button_list = []

        # alphabet position set
        for btn in button_place:
            btn[0] = Button(window, text=btn[1], command=lambda arg1=btn[1], arg2=btn[0]: guess(arg1, arg2), bg="#DEE2FF"
                            , activebackground="#DEE2FF",fg="#00669F" ,font=("Comic Sans MS", 33, "bold"), bd=0)
            btn[0].place(x=btn[2], y=btn[3])
            button_list.append(btn[0])

        # hangman position set information (label)
        hangman = [['c1', 'h1'], ['c2', 'h2'], ['c3', 'h3'], ['c4', 'h4'],
                   ['c5', 'h5'], ['c6', 'h6'], ['c7', 'h7'], ['c8', 'h8']]

        # hangman image load
        h_img = hngman_image_load()

        # hangman image labeling
        hangman_img_list = []
        j = 0
        for hm in hangman:
            hm[0] = Label(window, bg="#DEE2FF", image=h_img[j])
            hm[0].image = h_img[j]
            hangman_img_list.append(hm[0])
            j += 1

        # first image set
        hangman_img_list[0].place(x=30, y=130)

        fin = True

    # button event function
    def guess(guess_word, button):
        global hangman_img_list
        global words_label_list
        global win_count
        global life
        global coin

        num = 0  # words_label_list number

        button_list[int(button[2:]) - 1].destroy()
        winsound.Beep(323, 200)

        if guess_word.upper() in words:
            for word in words:
                if word == guess_word.upper():
                    win_count += 1
                    words_label_list[num].config(text=word)
                num += 1
        else:
            life += 1
            hangman_img_list[life].place(x=30, y=130)
            if life == 6:
                coin -= 100
                game_lose()

        if win_count == len(words):
            coin += 100
            hangman_img_list[7].place(x=30, y=130)
            game_win()

# turtle race page
def screen_game_2():
    clear_frame()
    menu_bar()
    show_user_info()
    penalty_back_button()

    global coin



    # root terminal printing
    title_name = "Turtle Race"
    printing_mv_title(title_name)

    # game head title
    word = Label(window, text=title_name, width=10, height=2, fg="black", bg='#DEE2FF', font=("Comic Sans MS", 40))
    word.pack(side='top', padx=0)

    canvas = tk.Canvas(window, width=900, height=400)
    canvas.place(x=0, y=200)


    try:
        # 경기장 그리기
        draw = t.RawTurtle(canvas)
        draw.up()
        draw.ht()
        draw.goto(-400,85)  #경기장 크기
        draw.down()
        draw.color("#f5802c")  #경기장 색
        draw.speed(0)

        draw.begin_fill()
        for i in range(2):  #운동장 색채우기
            draw.forward(800)
            draw.right(90)
            draw.forward(170)
            draw.right(90)
        draw.end_fill()

        #결승선 그리기
        draw.color("black")
        draw.up()
        draw.pensize(5)
        draw.goto(330,150)
        draw.write("결승선",False,"center",font=('휴먼편지체',20))
        draw.goto(330,130)
        draw.down()
        draw.goto(330,-130)

        #터틀 선수 생성
        start_ycor = [60,0,-60]
        color_list = ["red","blue","yellow"]

        #레이스 라인 생성
        for i in range(2):
            draw.up()
            draw.goto(-400,start_ycor[i]-30)
            draw.color("white")
            draw.down()
            draw.goto(400,start_ycor[i]-30)

        turtle_list = []
        for i in range(3):
            new_turtle = t.RawTurtle(canvas)
            new_turtle.up()
            new_turtle.shape("turtle")
            new_turtle.color(color_list[i])
            new_turtle.goto(-370,start_ycor[i])
            new_turtle.write(i+1)
            new_turtle.goto(-350,start_ycor[i]) #출발선
            turtle_list.append(new_turtle)


        # 베팅하기 turtle_ch : 몇번에 배팅했는지 확인 변수
        guess_turtle = tk.StringVar()
        guess_turtle_place = Entry(window, textvariable=guess_turtle, font=("Comic Sans MS", 15), width=7)


        guess_button = Button(window, text="베팅", command=lambda: guess_turtle_func(), font=("휴먼편지체", 23,"bold"),
                               bg='#DEE2FF', fg="#00669F", activebackground="#DEE2FF", bd=0)

        guess_turtle_place.place(x=380,y=150)
        guess_button.place(x=460,y=135)

    except:
        pass

    def guess_turtle_func():
        global coin
        turtle_ch = int(guess_turtle.get())
        hide_label = "        "+str(turtle_ch)+"번 거북이에 베팅하였습니다.     "
        hide_guess_tt_place = Label(window, text=hide_label, font=("휴먼편지체", 26,"bold"),
                                    bg='#DEE2FF', bd=0)
        hide_guess_tt_place.place(x=120, y=150)

        # 경기 시작 알림
        for _ in range(3):
            winsound.Beep(523, 300)
            time.sleep(0.3)

        #경기 시작
        try:
            game_over = False
            while not game_over:
                for i in range(len(turtle_list)):
                    rand_speed = random.randint(3,15)
                    player = turtle_list[i]
                    player.forward(rand_speed)

                    if player.xcor()>330:
                        winner = i+1
                        game_over = True

            hide_label2 = "          "+str(winner)+"번 거북이 1등 !!       "
            hide_guess_tt_place2 = Label(window, text=hide_label2, font=("휴먼편지체", 26, "bold"),
                                            bg='white', bd=0)
            hide_guess_tt_place2.place(x=150, y=220)


            # 베팅 결과 발표하기
            if turtle_ch == int(winner):
                coin +=200
                game_win()
            else:
                coin-=100
                game_lose()
        except:
            pass


# turtle get coin page
def screen_game_3():
    back_button()

    # root terminal printing
    title_name = "Turtle Coin"
    printing_mv_title(title_name)

    # game head title
    word = Label(window, text=title_name, width=10, height=2, fg="black", bg='#DEE2FF', font=("Comic Sans MS", 40))
    word.pack(side='top', padx=0)

    canvas = tk.Canvas(window, width=900, height=400)
    canvas.place(x=0, y=170)

    player = t.RawTurtle(canvas)
    player.shape("turtle")
    player.shapesize(1.5)
    player.up()
    player.color("green")
    player.speed(0)

    # 변수
    turtle_speed = 5
    game_over = False

    # coin
    food = t.RawTurtle(canvas)
    food.ht()
    food.shape("circle")
    food.up()
    food.color("yellow")
    food.speed(0)
    food.goto(rand_pos())
    food.st()

    # 독초
    pos_poison_x = []  # 새로운 poison의 x좌표값
    pos_poison_y = []  # 새로운 poison의 y좌표값
    plus_poison = 1

    def pos_poison():
        for i in range(3):
            rand_color = ["#" + ''.join([random.choice('ABCDEF0123456789') for _ in range(6)])]
            poison = t.RawTurtle(canvas)
            poison.ht()
            poison.shape("triangle")
            poison.shapesize(0.8)
            poison.up()
            poison.color(rand_color)
            poison.speed(0.2)
            poison.goto(rand_pos())
            poison.st()

            x, y = poison.pos()

            pos_poison_x.append(x)
            pos_poison_y.append(y)

    pos_poison()
    screen = player.getscreen()

    def turn_left():
        player.left(30)

    def turn_right():
        player.right(30)

    def back_strate():
        player.right(180)

    def go_strate():
        player.right(180)

    screen.onkeypress(turn_left, "Left")
    screen.onkeypress(turn_right, "Right")
    screen.onkeypress(back_strate, "Down")
    screen.onkeypress(go_strate, "Up")

    screen.listen()

    try: # 예외처리
        while not game_over:
            global coin
            show_user_info()

            player.forward(turtle_speed)

            # 벽을 만날 때 180도 회전
            if player.xcor() > 420 or player.xcor() < -420 or player.ycor() > 180 or player.ycor() < -180:
                player.right(180)

            # 먹이를 먹었을 때 get coin
            if player.distance(food) < 20:
                plus_poison += 1
                food.goto(rand_pos())
                pos_poison()
                turtle_speed += 1
                coin += 50
    
            # 독초를 먹었을 때 게임 종료
            for i in range(3 * plus_poison):
                if player.distance(pos_poison_x[i], pos_poison_y[i]) < 10:
                    game_over = True
                    game_lose()
    except:
        pass


# part of the project 1 : 장선웅
def screen_details_1():
    clear_frame()
    menu_bar()
    show_user_info()
    back_button()
    line_design()

    title = Label(window, text="프로젝트 각 담당부분", fg="black", bg='#DEE2FF', font=("휴먼편지체", 40, "bold"))
    title_name = Label(window, text="< 장선웅 >", fg="black", bg='#DEE2FF', font=("휴먼편지체", 30, "bold"))

    title.place(x=260, y=100)
    title_name.place(x=370, y=32)

    # show divisive line
    global divline_img

    pre_img = Image.open(resource_path('./img/divline.png')).transpose(Image.ROTATE_90)   # 90도 회전
    pre_img = pre_img.resize((30, 350))
    divline_img = ImageTk.PhotoImage(pre_img)
    div_label = Label(window, bg='#DEE2FF', image=divline_img)
    div_label.place(x=430, y=180)

    text_contents1 = """- 로그인 구현 -
datasheet.txt 파일 로그인정보 저장
로그인 정보는 딕셔너리 형태로 저장
ID, PW 체크 후 옳바르면 로그인

- 회원가입 구현 -
ID 중복 불가, PW 2중 체크
요건 충족시 txt파일에 딕셔너리 형태로 저장

- 메뉴 구현 -
6가지 메인메뉴 GUI 및 메뉴 바 제작"""

    text_contents2 = """- 행맨 게임 구현 -
터미널상에서 구현 후 GUI 구현
tkinter 모듈을 이용하여 행맨게임 구현
(관련내용 게임 룰 이용)

- 전체 코드 통합 -
코인, 유저 정보 통합 및 게임 화면 연동
관리자 터미널 추가 제작

- PPT 제작 및 발표 -
본인 코드 부분 PPT 제작 후 인계
PPT 최종 발표"""

    contents1 = Label(window, text=text_contents1, justify="center", fg="black", bg='#DEE2FF', font=("휴먼편지체", 17))
    contents2 = Label(window, text=text_contents2, justify="center", fg="black", bg='#DEE2FF', font=("휴먼편지체", 17))

    contents1.place(x=30, y=190)
    contents2.place(x=470, y=190)

    button_1 = Button(window, text="← 강XX", bg="#DEE2FF", activebackground="#DEE2FF", fg="#00669F",
                       font=("휴먼편지체", 30, "bold"), bd=0, command=lambda: screen_details_2())
    button_1.place(x=70, y=570)
    button_2 = Button(window, text="이XX →", bg="#DEE2FF", activebackground="#DEE2FF", fg="#00669F",
                       font=("휴먼편지체", 30, "bold"), bd=0, command=lambda: screen_details_3())
    button_2.place(x=620,y=570)

# part of the project 2 : 강XX
def screen_details_2():
    clear_frame()
    menu_bar()
    show_user_info()
    back_button()
    line_design()

    title = Label(window, text="프로젝트 각 담당부분", fg="black", bg='#DEE2FF', font=("휴먼편지체", 40, "bold"))
    title_name = Label(window, text="< 강XX >", fg="black", bg='#DEE2FF', font=("휴먼편지체", 30, "bold"))

    title.place(x=260, y=100)
    title_name.place(x=370, y=32)

    text_contents = """- 거북이 경주 구현 -
거북이 경주 게임 구현 (관련내용 게임 룰 이용)

- PPT 제작 -
본인 코드 부분 PPT를 제작하고
팀원들의 PPT 내용을 통합하여 정리 및 제작

- PPT 발표 -
본인 코드 질의응답

- 디자인 -
전체적인 색, 디자인 의견 제시"""

    contents = Label(window, text=text_contents, justify="center", fg="black", bg='#DEE2FF',
                     font=("휴먼편지체", 20))
    contents.place(x=210, y=180)

    button_1 = Button(window, text="← 이XX", bg="#DEE2FF", activebackground="#DEE2FF", fg="#00669F",
                      font=("휴먼편지체", 30, "bold"), bd=0, command=lambda: screen_details_3())
    button_1.place(x=70, y=570)
    button_2 = Button(window, text="장선웅 →", bg="#DEE2FF", activebackground="#DEE2FF", fg="#00669F",
                      font=("휴먼편지체", 30, "bold"), bd=0, command=lambda: screen_details_1())
    button_2.place(x=620, y=570)

# part of the project 3 : 이XX
def screen_details_3():
    clear_frame()
    menu_bar()
    show_user_info()
    back_button()
    line_design()

    title = Label(window, text="프로젝트 각 담당부분", fg="black", bg='#DEE2FF', font=("휴먼편지체", 40, "bold"))
    title_name = Label(window, text="< 이XX >", fg="black", bg='#DEE2FF', font=("휴먼편지체", 30, "bold"))

    title.place(x=260, y=100)
    title_name.place(x=370, y=32)

    text_contents = """- 거북이 잡기 게임 구현 -
Turtle 모듈을 이용하여 거북이로 COIN 먹기 게임 구현
(관련내용 게임 룰 이용)

- PPT 제작 -
본인 코드 부분 PPT 제작 후 인계

- PPT 발표 -
본인 코드 질의응답

- 회의 주최 -
회의 날짜를 정하고 회의 내용을 정리"""

    contents = Label(window, text=text_contents, justify="center", fg="black", bg='#DEE2FF',
                     font=("휴먼편지체", 20))
    contents.place(x=180, y=180)

    button_1 = Button(window, text="← 장선웅", bg="#DEE2FF", activebackground="#DEE2FF", fg="#00669F",
                      font=("휴먼편지체", 30, "bold"), bd=0, command=lambda: screen_details_1())
    button_1.place(x=70, y=570)
    button_2 = Button(window, text="강XX →", bg="#DEE2FF", activebackground="#DEE2FF", fg="#00669F",
                      font=("휴먼편지체", 30, "bold"), bd=0, command=lambda: screen_details_2())
    button_2.place(x=620, y=570)


# game rules 1 : HANG MAN
def screen_rule_1():
    clear_frame()
    menu_bar()
    show_user_info()
    back_button()
    line_design()

    title = Label(window, text="HANG MAN", fg="black", bg='#DEE2FF', font=("Comic Sans MS", 40, "bold"))
    title_name = Label(window, text="Rule 1", fg="black", bg='#DEE2FF', font=("Comic Sans MS", 30, "bold"))

    title.place(x=280, y=50)
    title_name.place(x=370, y=10)

    text_contents = """문제 단어는 1개 주어지며 1~8글자입니다.
( 단어에 대한 힌트는 주어지지 않습니다. )
문제 단어의 글자 수만큼 밑줄이 존재합니다.

하단에 알파벳을 클릭하여 단어를 추측하세요.
기회는 5번이며 6번의 기회 안에 맞출 경우 당신의 승리입니다.
6번째 턴까지 맞추지 못할 경우 당신의 패배입니다.

승리시 100 COIN을 획득합니다.
패배시 100 COIN이 차감됩니다.

오른쪽 상단 BACK 버튼을 눌러 게임 도중 나갈경우
패널티로 50 COIN이 차감됩니다."""

    contents = Label(window, text=text_contents, justify="center", fg="black", bg='#DEE2FF',
                     font=("휴먼편지체", 20))
    contents.place(x=100, y=150)

    button_1 = Button(window, text="← Turtle Race", bg="#DEE2FF", activebackground="#DEE2FF", fg="#00669F",
                      font=("Comic Sans MS", 30, "bold"), bd=0, command=lambda: screen_rule_2())
    button_1.place(x=25, y=560)
    button_2 = Button(window, text="Turtle Coin →", bg="#DEE2FF", activebackground="#DEE2FF", fg="#00669F",
                      font=("Comic Sans MS", 30, "bold"), bd=0, command=lambda: screen_rule_3())
    button_2.place(x=550, y=560)

# game rules 2 : Turtle Race
def screen_rule_2():
    clear_frame()
    menu_bar()
    show_user_info()
    back_button()
    line_design()

    title = Label(window, text="Turtle Race", fg="black", bg='#DEE2FF', font=("Comic Sans MS", 40, "bold"))
    title_name = Label(window, text="Rule 2", fg="black", bg='#DEE2FF', font=("Comic Sans MS", 30, "bold"))

    title.place(x=280, y=50)
    title_name.place(x=370, y=10)

    text_contents = """게임을 시작하면 레이스를 하는 거북이 3마리가 나옵니다. 
거북이중 마음에 드는 거북이에게 베팅합니다.
OK 버튼을 누르면 경기가 시작됩니다.

베팅한 거북이가 승리할경우 200 COIN을 획득합니다.
베팅한 거북이가 패배할경우 100 COIN이 차감됩니다.

오른쪽 상단 BACK 버튼을 눌러 게임 도중 나갈경우
패널티로 50 COIN이 차감됩니다."""

    contents = Label(window, text=text_contents, justify="center", fg="black", bg='#DEE2FF',
                     font=("휴먼편지체", 20))
    contents.place(x=140, y=180)

    button_1 = Button(window, text="← Turtle Coin", bg="#DEE2FF", activebackground="#DEE2FF", fg="#00669F",
                      font=("Comic Sans MS", 30, "bold"), bd=0, command=lambda: screen_rule_3())
    button_1.place(x=25, y=560)
    button_2 = Button(window, text="HANG MAN →", bg="#DEE2FF", activebackground="#DEE2FF", fg="#00669F",
                      font=("Comic Sans MS", 30, "bold"), bd=0, command=lambda: screen_rule_1())
    button_2.place(x=550, y=560)

# game rules 3 : Turtle Coin
def screen_rule_3():
    clear_frame()
    menu_bar()
    show_user_info()
    back_button()
    line_design()

    title = Label(window, text="Trutle Coin", fg="black", bg='#DEE2FF', font=("Comic Sans MS", 40, "bold"))
    title_name = Label(window, text="Rule 3", fg="black", bg='#DEE2FF', font=("Comic Sans MS", 30, "bold"))

    title.place(x=280, y=50)
    title_name.place(x=370, y=10)

    text_contents = """↑ : 거북이 180도 회전   
↓ : 거북이 180도 회전   
← : 거북이 좌측 30도 회전
→ : 거북이 우측 30도 회전

방향키를 이용하여 거북이를 움직일 수 있습니다.
코인을 먹을 시 50 COIN을 획득합니다.
코인을 먹게되면 거북이의 속도가 점점 빨라집니다.
코인을 먹게되면 장애물이 3개씩 늘어납니다.
장애물을 밟게되면 게임이 종료됩니다.

해당 게임은 코인을 무료로 얻기 위한 게임이므로
패널티는 존재하지 않습니다.
장애물을 밟더라도 COIN이 깎이지 않습니다."""


    contents = Label(window, text=text_contents, justify="center", fg="black", bg='#DEE2FF',
                     font=("휴먼편지체", 19))
    contents.place(x=190, y=150)

    button_1 = Button(window, text="← HANG MAN", bg="#DEE2FF", activebackground="#DEE2FF", fg="#00669F",
                      font=("Comic Sans MS", 30, "bold"), bd=0, command=lambda: screen_rule_1())
    button_1.place(x=25, y=560)
    button_2 = Button(window, text="Turtle Race →", bg="#DEE2FF", activebackground="#DEE2FF", fg="#00669F",
                      font=("Comic Sans MS", 30, "bold"), bd=0, command=lambda: screen_rule_2())
    button_2.place(x=550, y=560)


window = tk.Tk()
window.resizable(0, 0)
window.geometry('900x700')
window.title('TEAM 4 Game Project')
window.config(bg='#DEE2FF')

check_start = timeit.default_timer()

printing_root()
login_page()

window.mainloop()