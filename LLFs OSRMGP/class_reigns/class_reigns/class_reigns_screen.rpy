## 该项目来源于LLFs-OSRMGP（https://github.com/llfseik/LLFs-OSRMGP）,遵循MIT协议。
## 严禁售卖该项目代码！你可以随意将其用修改并于任何非商业用途，但请注明出处！

label class_reigns_label:
    $ quick_menu = False
    call screen class_reigns_screen(the_CRED=class_reigns_event_dict)

transform class_reigns_card_trans(rotate_value=0,xoffset_value=0,yoffset_value=0):
    rotate_pad False
    transform_anchor True
    parallel:
        ease 0.3 rotate rotate_value
    parallel:
        ease 0.2 offset (xoffset_value,yoffset_value)

init python:
    def init_calss_reigns_screen(the_CRED):
        global CRL
        CRL = ClassReignsLogic(the_CRED)
        CRL.the_start_event()

screen class_reigns_screen(the_CRED=class_reigns_event_dict):
    default mouse_pos = ""
    default the_display_event = dict(*CRL.display_event.values())

    ## 初始化游戏数据，判断应用哪个字典
    ## 此处为默认的class_reigns_event_dict字典（详情查看class_reigns_event_ren.py）
    on "show" action Function(init_calss_reigns_screen, the_CRED)

    ## 重置按钮
    button:
        xysize(1920,1080)
        add "#00000000"
        hovered SetScreenVariable("mouse_pos","")
        action NullAction()

    ## 各类数值显示
    hbox:
        anchor (0.5,0.0)
        pos(0.5,0.07)
        spacing 30
        for value_name, value_title in {"Health_Value":"健康值", "Force_Value":"武力值", "Wisdom_Value":"智力值", "Money_Value":"金钱值", "Network_Value":"联络值"}.items():
            hbox:
                xycenter(0.5,0.5)
                spacing 5
                text "[value_title]" vertical True xycenter(0.5,0.5)
                vbar:
                    # value int(eval("CRL." + value_name))
                    value AnimatedValue(value=int(eval("CRL." + value_name)), range=100, delay=0.5)
                    # range 100
                    xysize(20,120)
                    xycenter(0.5,0.5)
    
    ## 回合数和循环次数
    vbox:
        anchor (0.5,0.0)
        pos(0.5,0.16)
        spacing 5
        text "第[ CRL.Loop_Value ]天" size 26 xalign 0.0
        # text "第[ CRL.Round_Value ]回合" size 26 xalign 0.0
        bar:
            value AnimatedValue(value=CRL.Round_Value, range=CRL.Round_Max_Value, delay=0.5)
            xysize(860,10)
            xycenter(0.5,0.5)
    
    ## 事件显示
    frame:
        anchor (0.5,0.0)
        pos(0.5,0.22)
        xysize(860,140)
        fixed:
            xycenter(0.5,0.5)
            xysize(780,120)
            text the_display_event["event_text"] size 26 xycenter(0.5,0.5)
    frame:
        xysize(280,420)
        anchor (0.5,1.0)
        pos(0.5,0.79)

    ## 事件卡牌
    fixed:
        xysize(260,400)
        anchor (0.5,1.0)
        pos(0.5,0.78)
        if the_display_event["event_image"] == "":
            add "#ffffff"
        else:
            add the_display_event["event_image"]

        if mouse_pos == "left":
            at class_reigns_card_trans(-5,-80,-10)
        elif mouse_pos == "right":
            at class_reigns_card_trans(5,80,-10)
        elif mouse_pos == "below":
            at class_reigns_card_trans(0,0,30)
        else:
            at class_reigns_card_trans(0,0,0)

    ## 左侧按钮
    if "yes" in the_display_event and len(the_display_event["yes"]) > 0:
        button:
            xysize(810,1080)
            align(0.0,0.5)
            hovered SetScreenVariable("mouse_pos","left")
            unhovered SetScreenVariable("mouse_pos","")
            action Function(CRL.what_happens_after_choice, "yes")
            if "yes_text"  not in the_display_event or the_display_event["yes_text"] == "":
                text "点头":
                    style "button_vertical_left_text_style"
            else:
                text the_display_event["yes_text"]:
                    style "button_vertical_left_text_style"

    ## 右侧按钮
    if "no" in the_display_event and len(the_display_event["no"]) > 0:
        button:
            xysize(810,1080)
            align(1.0,0.5)
            hovered SetScreenVariable("mouse_pos","right")
            unhovered SetScreenVariable("mouse_pos","")
            action Function(CRL.what_happens_after_choice, "no")
            if "no_text" not in the_display_event or the_display_event["no_text"] == "":
                text "摇头":
                    style "button_vertical_right_text_style"
            else:
                text the_display_event["no_text"]:
                    style "button_vertical_right_text_style"

    ## 下方按钮
    if "other" in the_display_event and len(the_display_event["other"]) > 0:
        button:
            xysize(1000,240)
            align(0.5,1.0)
            hovered SetScreenVariable("mouse_pos","below")
            unhovered SetScreenVariable("mouse_pos","")
            action Function(CRL.what_happens_after_choice, "other")
            if "other_text" not in the_display_event or the_display_event["other_text"] == "":
                text "沉默":
                    style "button_vertical_below_text_style"
            else:
                text the_display_event["other_text"]:
                    style "button_vertical_below_text_style"

    textbutton "事件编辑器":
        action [Show("class_reigns_event_editor_screen"),Function(CREEC.read_dict)]

## 展示游戏结束的画面
## 这里直接改写了“确认屏幕”部分的代码，并拓展了参数
screen class_reigns_game_over_screen(message, yes_action=MainMenu(confirm=False, save=False), no_action=[Hide(),Jump('class_reigns_label')], yes_text="退出", no_text="重开"):

    ## 显示此屏幕时，确保其他屏幕无法输入。
    modal True

    zorder 200

    style_prefix "confirm"

    add "#00000040"

    draggroup:
        xysize(1920,1080)

        drag:
            xycenter(0.5,0.5)

            frame:

                vbox:
                    xalign .5
                    yalign .5
                    spacing 30

                    label _(message):
                        style "confirm_prompt"
                        xalign 0.5
                    
                    vbox:
                        yoffset -5
                        xycenter(0.5,0.5)
                        text "已经历[ CRL.Loop_Value ]天" size 30 xycenter(0.5,0.5)

                        text "健康值：[ CRL.Health_Value ]":
                            size 26
                            xycenter(0.5,0.5)
                            if CRL.Health_Value <= 0 or CRL.Health_Value >= 100:
                                color "#e09d9d"
                        text "武力值：[ CRL.Force_Value ]":
                            size 26
                            xycenter(0.5,0.5)
                            if CRL.Force_Value <= 0 or CRL.Force_Value >= 100:
                                color "#e09d9d"
                        text "智力值：[ CRL.Wisdom_Value ]":
                            size 26
                            xycenter(0.5,0.5)
                            if CRL.Wisdom_Value <= 0 or CRL.Wisdom_Value >= 100:
                                color "#e09d9d"
                        text "金钱值：[ CRL.Money_Value ]":
                            size 26
                            xycenter(0.5,0.5)
                            if CRL.Money_Value <= 0 or CRL.Money_Value >= 100:
                                color "#e09d9d"
                        text "联络值：[ CRL.Network_Value ]":
                            size 26
                            xycenter(0.5,0.5)
                            if CRL.Network_Value <= 0 or CRL.Network_Value >= 100:
                                color "#e09d9d"

                    hbox:
                        xalign 0.5
                        spacing 150

                        textbutton yes_text action yes_action
                        textbutton no_text action no_action

    ## 右键点击退出并答复 no（取消）。
    key "game_menu" action no_action



style button_vertical_left_text_style:
    color "#ffffff"
    size 30
    anchor (0.5,0.0)
    pos(0.7,0.5)
    vertical True

style button_vertical_right_text_style:
    color "#ffffff"
    size 30
    anchor (0.5,0.0)
    pos(0.3,0.5)
    vertical True

style button_vertical_below_text_style:
    color "#ffffff"
    size 30
    anchor (0.5,0.5)
    pos(0.5,0.5)