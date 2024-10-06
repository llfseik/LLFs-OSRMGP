## 该项目来源于LLFs-OSRMGP（https://github.com/llfseik/LLFs-OSRMGP），遵循MIT协议。
## 严禁进行售卖！若需嵌入付费项目请与我联系！

label minesweeper_label:
    $ quick_menu = False
    ## 四个参数分别为：行数、列数、雷数
    call screen minesweeper_screen(10,10,10)

## 图标样式
style box_style:
    color "#ffffff"
    size 30
    xalign 0.5
    yalign 0.5

init python:
    import random

    ## 格子大小
    box_xysize = 50
    ## 行数、列数、所有格子的坐标、雷数、雷的坐标、每个坐标对应周围雷的数量
    box_rows = 10
    box_cols = 10
    all_box_list = []
    num_mines = 10
    mine_tag_list = []
    box_around_mines = {}
    ## 判断按键是否按下、格子是否被标记
    K_q = False
    marked_box_list = []
    ## 输赢、游戏状态
    win_or_lose = False
    game_over = None

    ## 初始化游戏参数
    def init_game(cols=10,rows=10,mines=10):

        ## 清空已经打开格子和标记
        box_around_mines.clear()
        marked_box_list.clear()
        
        if rows < 1 or cols < 1 or mines < 1 or mines > rows*cols:
            ## 检测参数是否合法，如果不合法则初始化为默认参数
            box_rows = 10
            box_cols = 10
            num_mines = 10
            renpy.notify("参数错误，已将游戏初始化为默认参数！")
        else:
            ## 初始化棋盘参数
            box_rows = rows
            box_cols = cols
            num_mines = mines
            ## 初始化棋盘参数
            renpy.run(SetVariable("box_rows",rows))
            renpy.run(SetVariable("box_cols",cols))
            renpy.run(SetVariable("num_mines",mines))
            renpy.notify("开始游戏！")

        ## 随机生成所有格子坐标
        all_box_list.clear()
        for i in range(1,box_rows+1):
            for j in range(1,box_cols+1):
                all_box_list.append((i,j))
        ## 随机生成雷的坐标
        mine_tag_list.clear()
        for i in range(num_mines):
            tag = random.choice(all_box_list)
            ## 如果随机生成的雷的坐标已经在雷的标记列表中，则重新生成
            while tag in mine_tag_list:
                tag = random.choice(all_box_list)
            mine_tag_list.append(tag)
        
        ## 开始游戏
        renpy.run(SetVariable("game_over",False))

    ## 打开格子
    def show_box(box_tag):
        ## 清除掉遗留下来的标记
        if box_tag in marked_box_list:
            marked_box_list.remove(box_tag)

        ## 范围内的雷的数量
        num_mines_around = 0
        ## 格子的具体坐标
        box_x = box_tag[0]
        box_y = box_tag[1]
        for i in mine_tag_list:
            if -1 <= box_x-i[0] <= 1:
                if -1 <= box_y-i[1] <= 1:
                    num_mines_around += 1
        box_around_mines[box_tag] = num_mines_around
        ## 如果周围没有雷，则再次调用函数，打开周围的格子
        if box_around_mines[box_tag] == 0:
            for i in range(box_x-1,box_x+2):
                for j in range(box_y-1,box_y+2):
                    if ((i,j) in all_box_list) and ((i,j) not in box_around_mines.keys()):
                        show_box((i,j))

    ## 标记格子
    def mark_box(box_tag=None,key=None):
        ## 如果按下的是q，则将格子标记为旗子
        if key == "q":
            if box_tag not in marked_box_list:
                marked_box_list.append(box_tag)
            else:
                marked_box_list.remove(box_tag)
    
    ## 结算游戏
    def check_win_or_lose(box_tag=None):

        ## 判断游戏是否结束
        if ((len(all_box_list)-len(mine_tag_list)) == len(box_around_mines.keys())) and (box_tag not in mine_tag_list):
            ## 打开所有格子，没有雷，游戏结束，胜利
            renpy.run(SetVariable("win_or_lose",True))
            renpy.run(SetVariable("game_over",True))
            renpy.notify("你赢了！")

        elif box_tag in mine_tag_list:
            ## 打开的格子有雷，游戏结束，输了
            renpy.run(SetVariable("win_or_lose",False))
            renpy.run(SetVariable("game_over",True))
            renpy.notify("踩雷了，你输了！")

        else:
            ## 游戏继续
            pass

## 游戏界面
screen minesweeper_screen(cols=10,rows=10,mines=10):

    ## 初始化游戏参数
    on "show" action [Function(init_game,rows=rows,cols=cols,mines=mines),SetVariable("game_over",False)]

    ## 判断按键是否按下
    key "keydown_K_q" action SetVariable("K_q",True)
    key "keyup_K_q" action SetVariable("K_q",False)

    ## 棋盘
    fixed:
        xycenter (0.5,0.5)
        vbox:
            xycenter (0.5,0.5)
            add "#b3b3b3" xysize (int(box_cols*box_xysize*1.2+box_xysize*0.6),int(box_rows*box_xysize*1.2+box_xysize*0.6)) xycenter (0.5,0.5) yoffset int(box_xysize*0.6)
            ## 不同游戏状态时切换不同的表情
            if game_over == None or game_over == False:
                add Text("😀",style="box_style",size=int(box_xysize)) xycenter (0.5,1.2)
            elif game_over == True and win_or_lose == True:
                add Text("😎",style="box_style",size=int(box_xysize)) xycenter (0.5,1.2)
            elif game_over == True and win_or_lose == False:
                add Text("💀",style="box_style",size=int(box_xysize)) xycenter (0.5,1.2)
        add "#000000" xysize (int(box_cols*box_xysize*1.2+box_xysize*0.2),int(box_rows*box_xysize*1.2+box_xysize*0.2)) xycenter (0.5,0.5)

        if game_over == None or game_over == False:
            grid box_cols box_rows:
                xycenter (0.5,0.5)
                xsize int(box_rows*box_xysize*1.2)
                ysize int(box_cols*box_xysize*1.2)
                spacing int(box_xysize*0.2)

                for i in all_box_list:
                    ## 判断格子的状态
                    if i in box_around_mines.keys():
                        ## 如果被打开，则变为图片，显示数字
                        if box_around_mines[i] == 0:
                            add Fixed("#363636",xysize=(int(box_xysize),int(box_xysize)))
                        else:
                            add Fixed("#363636",Text(str(box_around_mines[i]),style="box_style",size=int(box_xysize*0.6)),xysize=(int(box_xysize),int(box_xysize)))
                    else:
                        ## 如果没有被打开，则变为按钮
                        imagebutton:
                            ## 判断格子是否被标记
                            if i in marked_box_list:
                                idle Fixed("#7593d4",Text(("🚩"),style="box_style",size=int(box_xysize*0.6)),xysize=(int(box_xysize),int(box_xysize)))
                            else:
                                idle Fixed("#7593d4",xysize=(int(box_xysize),int(box_xysize)))

                            ## 判断按下的按键，并将已经打开的格子排除在外
                            if (K_q == True) and (i not in box_around_mines.keys()):
                                action Function(mark_box,i,"q") 
                            else:
                                action [Function(show_box,i),Function(check_win_or_lose,i)]
        
        ## 游戏结束后重开
        else:
            textbutton "重新开始":
                style "box_style"
                xalign 0.5
                yalign 0.5
                text_color "#7593d4"
                text_hover_color "#ffffff"
                text_size int(box_xysize*0.6)
                action [Function(init_game,rows=rows,cols=cols,mines=mines),SetVariable("game_over",False)]