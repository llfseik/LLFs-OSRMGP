## 该项目来源于LLFs-OSRMGP（https://github.com/llfseik/LLFs-OSRMGP），遵循MIT协议。
## 严禁进行售卖！若需嵌入付费项目请与我联系！

label gobang_label:
    $ quick_menu = False
    call screen gobang_screen()

## 绘制无棋子时的格子
image gobang_normal_box:
    xysize(int(box_xysize),int(box_xysize))
    "#000000"

init 1 python:
    import random

    ## 格子大小
    box_xysize = 50
    ## 行数、列数、所有格子的坐标、棋盘的坐标、白棋的坐标、黑棋的坐标
    box_rows = 10
    box_cols = 10
    all_box_list = []
    gobang_whilte_box_list = []
    gobang_black_box_list = []
    ## 先手
    first_turn = "white"
    ## 输赢、游玩次数、胜场、分数
    win_or_lose = ""
    count = 0
    win_count = 0
    score = 0
    game_over = None

    ## 绘制圆形棋子
    class Chess(renpy.Displayable):
        def __init__(self,x,y,color,radius,**kwargs):
            super(Chess, self).__init__(**kwargs)
            self.x = x
            self.y = y
            self.color = color
            self.radius = radius

        ## 绘制圆形棋子
        def render(self,width,height,st,at):
            render = renpy.Render(width,height)
            canvas = render.canvas()
            canvas.circle(self.color,(self.x,self.y),self.radius)
            return render
    
    ## 绘制棋子
    renpy.image("gobang_white", Fixed(Chess(box_xysize/2,box_xysize/2,"#FFFFFF",box_xysize/2-1), xysize=(box_xysize,box_xysize)))
    renpy.image("gobang_black", Fixed(Chess(box_xysize/2,box_xysize/2,"#000000",box_xysize/2-1), xysize=(box_xysize,box_xysize)))

    ## 初始化游戏
    def gobang_init_game():
        global box_rows, box_cols, all_box_list, gobang_tag_list, gobang_gobang_whilte_box_list, first_turn, win_or_lose, count, win_count, score, game_over

        ## 清空棋盘
        gobang_whilte_box_list.clear()
        gobang_black_box_list.clear()
        all_box_list.clear()

        ## 重置游戏状态
        box_rows = 15
        box_cols = 15

        
        ## 生成所有格子的坐标
        all_box_list = []
        for i in range(0,box_rows):
            for j in range(0,box_cols):
                all_box_list.append((i,j))
        
        ## 开始游戏
        game_over = False
        win_or_lose = ""
    
    ## 落子并判断胜负（游戏的核心算法）
    def gobang_falling(chess_color=None,box_pos=None):
        global win_or_lose,game_over
        x_num = 0
        y_num = 0
        x_left_num = 0
        x_right_num = 0
        box_x = box_pos[0]
        box_y = box_pos[1]
        ## 如果棋子是白色则将坐标加进白棋的列表，否则将坐标加进黑棋的列表，并判断是否获胜
        if chess_color == "white":
            gobang_whilte_box_list.append(box_pos)
            ## 这一部分还有优化空间，但是目前先这样吧，优化算法什么的就交给后人吧）
            ## 搜索当前棋子上下左右以及四个斜向方向的4格棋子状态，如果是白色则将变量+1
            for i in range(1,5):
                if (box_x+i,box_y) in gobang_whilte_box_list:
                    x_num += 1
                elif (box_x-i,box_y) in gobang_whilte_box_list:
                    x_num += 1
                if (box_x,box_y+i) in gobang_whilte_box_list:
                    y_num += 1
                elif (box_x,box_y-i) in gobang_whilte_box_list:
                    y_num += 1
                if (box_x+i,box_y+i) in gobang_whilte_box_list:
                    x_left_num += 1
                elif (box_x-i,box_y-i) in gobang_whilte_box_list:
                    x_left_num += 1
                if (box_x+i,box_y-i) in gobang_whilte_box_list:
                    x_right_num += 1
                elif (box_x-i,box_y+i) in gobang_whilte_box_list:
                    x_right_num += 1
            ## 如果四个方向的棋子有一条加起来等于5个，则获胜（排除自身的这颗棋子，避免重复判断）
            if x_num >= 4 or y_num >= 4 or x_left_num >= 4 or x_right_num >= 4:
                win_or_lose = "white"
                game_over = True

        ## 算法同上，只是将白棋的列表换成黑棋的列表
        elif chess_color == "black":
            gobang_black_box_list.append(box_pos)
            for i in range(1,5):
                if (box_x+i,box_y) in gobang_black_box_list:
                    x_num += 1
                elif (box_x-i,box_y) in gobang_black_box_list:
                    x_num += 1
                if (box_x,box_y+i) in gobang_black_box_list:
                    y_num += 1
                elif (box_x,box_y-i) in gobang_black_box_list:
                    y_num += 1
                if (box_x+i,box_y+i) in gobang_black_box_list:
                    x_left_num += 1
                elif (box_x-i,box_y-i) in gobang_black_box_list:
                    x_left_num += 1
                if (box_x+i,box_y-i) in gobang_black_box_list:
                    x_right_num += 1
                elif (box_x-i,box_y+i) in gobang_black_box_list:
                    x_right_num += 1
            if x_num >= 4 or y_num >= 4 or x_left_num >= 4 or x_right_num >= 4:
                win_or_lose = "black"
                game_over = True

screen gobang_screen():

    ## 初始化游戏
    on "show" action [Function(gobang_init_game,),SetVariable("game_over",False)]

    ## 当前下的棋子颜色
    default now_turn = first_turn

    ## 绘制棋盘
    fixed:
        xycenter (0.5,0.5)
        ## 棋盘底图
        add "#b6a4ff" xysize (int(box_cols*box_xysize*1.1+box_xysize*0.1),int(box_rows*box_xysize*1.1+box_xysize*0.1)) xycenter (0.5,0.5)

        if game_over == None or game_over == False:
            grid box_cols box_rows:
                xycenter (0.5,0.5)
                xsize int(box_rows*box_xysize*1.1)
                ysize int(box_cols*box_xysize*1.1)
                spacing int(box_xysize*0.1)

                for i in all_box_list:
                    ## 判断格子的状态
                    if i in gobang_whilte_box_list:
                        add "gobang_white" xysize(int(box_xysize),int(box_xysize))
                    elif i in gobang_black_box_list:
                        add "gobang_black" xysize(int(box_xysize),int(box_xysize))
                    else:
                        ## 因为没有hover效果，所以说不使用imagebutton以节省性能
                        button:
                            image "gobang_normal_box":
                                xycenter (0.5,0.5)
                                xysize(int(box_xysize),int(box_xysize))
                            xysize(int(box_xysize),int(box_xysize))
                            ## 调用落子函数并将当前棋子的颜色改变
                            action [Function(gobang_falling,now_turn,i),
                                    SetScreenVariable("now_turn","black" if now_turn == "white" else "white")]
        else:
            fixed:
                xycenter (0.5,0.5)
                xsize int(box_rows*box_xysize*1.1)
                ysize int(box_cols*box_xysize*1.1)
                add "#000000"
                vbox:
                    xycenter (0.5,0.5)
                    text "胜者：[win_or_lose]" xycenter (0.5,0.5) size box_xysize*0.6
                    textbutton "再来一局":
                        xycenter (0.5,0.5)
                        text_size box_xysize*0.6
                        action  [Function(gobang_init_game),SetVariable("game_over",False)]