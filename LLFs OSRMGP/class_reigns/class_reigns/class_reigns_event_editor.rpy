## 该项目来源于LLFs-OSRMGP（https://github.com/llfseik/LLFs-OSRMGP）,遵循MIT协议。
## 严禁售卖该项目代码！你可以随意将其用修改并于任何非商业用途，但请注明出处！

init python:
    import os
    import json
    import re
    import math
    import copy
    from builtins import dict as real_dict
    from builtins import list as real_list

    class class_reigns_event_editor_class():
        def __init__(self):
            ## 界面所显示的内容
            self.cree_dict = {}
            ## update_init_value_Screen界面中对_init_value的临时变量
            self.temporary_init_value_attr={}
            ## update_event_editor_screen界面中的临时变量
            self.temporary_event_tag=""
            self.temporary_event_attr={}
            ## copy列表
            self.copy_list=[]
        
        ## 读取json后，转化dict格式
        def trans_dict(self, old):
            new_dict = renpy.revertable.RevertableDict()
            for key, value in old.items():
                if type(value) == real_dict:
                    new_dict[key] = self.trans_dict(value)
                elif type(value) == real_list:
                    new_dict[key] = self.trans_list(value)
                else:
                    new_dict[key] = value
            return new_dict
        
        ## 读取json后，转化list格式
        def trans_list(self, old):
            new_list = renpy.revertable.RevertableList()
            for item in old:
                new_list.append(item)
            return new_list

        ## 读取目录下的class_reigns_event.json文件
        def read_json(self):
            with open(os.path.join(config.gamedir, 'class_reigns_event.json'), 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.cree_dict.clear()
            self.cree_dict.update(self.trans_dict(data))

        ## 读取dict
        def read_dict(self):
            self.cree_dict.clear()
            self.cree_dict.update(class_reigns_event_dict)

        ## 保存目录下的calss_reigns_event.json文件
        def save_json(self):
            with open(os.path.join(config.gamedir, 'class_reigns_event.json'), 'w', encoding='utf-8') as f:
                json.dump(self.cree_dict, f, ensure_ascii=False, indent=4)

        ## 判断是否保存了json（比较内容）
        def is_json_saved(self):
            with open(os.path.join(config.gamedir, 'class_reigns_event.json'), 'r', encoding='utf-8') as f:
                data = json.load(f)
            if data == self.cree_dict:
                return True
            else:
                return False

        ## 删除事件
        def remove_event(self, event_tag):
            del self.cree_dict[event_tag]

        ## 置顶事件
        def move_to_top_event(self, event_tag):
            temporary_event_1 = {}
            temporary_event_2 = {}
            temporary_event_3 = {}
            for key, value in self.cree_dict.items():
                if key == "_init_value":
                    temporary_event_1[key] = value
                elif key == event_tag:
                    temporary_event_2[key] = value
                else:
                    temporary_event_3[key] = value
            self.cree_dict.clear()
            self.cree_dict.update(temporary_event_1)
            self.cree_dict.update(temporary_event_2)
            self.cree_dict.update(temporary_event_3)

        ## 复制事件
        def copy_event(self, event_tag):
            self.cree_dict[event_tag + "_copy"] = copy.deepcopy(self.cree_dict[event_tag])
            self.copy_list.append(event_tag + "_copy")
        
        ## 删除复制的事件
        def del_copy_event(self, event_tag, action):
            if event_tag in self.cree_dict and event_tag in self.copy_list:
                if action == "delete":
                    del self.cree_dict[event_tag]
                self.copy_list.remove(event_tag)
        
        ## 删除旧事件
        def del_old_event(self, event_tag, action):
            if event_tag in self.cree_dict:
                if action == "delete":
                    del self.cree_dict[event_tag]

        ## 快速排序
        def sort_event_by_tag(self):
            temporary_event_dict = {}
            temporary_event_list = []
            for key, value in self.cree_dict.items():
                if key == "_init_value":
                    temporary_event_dict[key] = value
                else:
                    temporary_event_list.append(key)
            temporary_event_list.sort()
            for key in temporary_event_list:
                temporary_event_dict[key] = self.cree_dict[key]
            self.cree_dict.clear()
            self.cree_dict.update(temporary_event_dict)

        ## 新建初始变量
        def add_init_value(self):
            ## 添加初始化变量
            self.cree_dict["_init_value"] = {
                "Health_Value":50,
                "Force_Value":50,
                "Wisdom_Value":50,
                "Money_Value":50,
                "Network_Value":50,
                "Round_Value":0,
                "Round_Max_Value":10,
                "Loop_Value":0,
                "Loop_Max_Value":10
            }
            ## 将变量位置重新排列，将_init_value放在第一位
            temp_dict_1 = {}
            temp_dict_2 = {}
            for key, value in self.cree_dict.items():
                if key == "_init_value":
                    temp_dict_1[key] = value
                else:
                    temp_dict_2[key] = value
            self.cree_dict.clear()
            self.cree_dict.update(temp_dict_1)
            self.cree_dict.update(temp_dict_2)

        ## 新建事件
        def update_temporary(self, event_tag, event_attr):
            self.temporary_event_tag=""
            self.temporary_event_attr={}
            if event_tag == "" and event_attr == {}:
                self.temporary_event_tag = "new_event"
                self.temporary_event_attr = {
                        "event_text":"",
                        "event_image":"",
                        "event_note":"",
                        "yes":{},
                        "yes_text":"",
                        "no":{},
                        "no_text":"",
                        "other":{},
                        "other_text":"",
                        "round":[],
                        "loop":[],
                        "probability":0,
                        "condition":{},
                        "condition_loop":{},
                        "condition_value":{}
                        }
            elif event_tag in self.cree_dict:
                self.temporary_event_tag = event_tag
                self.temporary_event_attr = event_attr
        
        ## 切换类型
        def yes_no_other_type_toggle(self, the_action, action_attr):
            ## 分别为：yes/no/other、NONE/INT/STR
            if action_attr not in self.temporary_event_attr[the_action]:
                self.temporary_event_attr[the_action][action_attr] = 0
            elif isinstance(self.temporary_event_attr[the_action][action_attr], int):
                self.temporary_event_attr[the_action][action_attr] = str(self.temporary_event_attr[the_action][action_attr])
            elif isinstance(self.temporary_event_attr[the_action][action_attr], str):
                del self.temporary_event_attr[the_action][action_attr]
        
        ## 添加特殊事件
        def update_special_event(self, the_action, special_event_name):
            ## 分别为：yes/no/other、特殊事件名
            if "special_event" not in self.temporary_event_attr[the_action]:
                self.temporary_event_attr[the_action]["special_event"] = []
            if special_event_name not in self.temporary_event_attr[the_action]["special_event"]:
                self.temporary_event_attr[the_action]["special_event"].append(special_event_name)
            else:
                self.temporary_event_attr[the_action]["special_event"].remove(special_event_name)
            if len(self.temporary_event_attr[the_action]["special_event"]) == 0:
                del self.temporary_event_attr[the_action]["special_event"]
        
        ## 更新round和loop限制（list）
        def update_round_loop_limit_list(self, limit_type="", limit_value=None):
            ## 分别为：round/loop、数值
            if limit_value == None:
                self.temporary_event_attr[limit_type] = []
                return
            
            if isinstance(self.temporary_event_attr[limit_type], dict):
                self.temporary_event_attr[limit_type] = []

            if isinstance(self.temporary_event_attr[limit_type], list) and limit_value != None:
                if limit_value not in self.temporary_event_attr[limit_type]:
                    self.temporary_event_attr[limit_type].append(limit_value)
                else:
                    self.temporary_event_attr[limit_type].remove(limit_value)
        
        ## 更新round和loop限制（dict）
        def update_round_loop_limit_dict(self, limit_type="", min_or_max=""):
            ## 分别为：round/loop、min/max
            if limit_type != "" and isinstance(self.temporary_event_attr[limit_type], list):
                self.temporary_event_attr[limit_type] = {}
            
            if limit_type != "" and min_or_max != "":
                if min_or_max not in self.temporary_event_attr[limit_type]:
                    self.temporary_event_attr[limit_type][min_or_max] = 0
                else:
                    del self.temporary_event_attr[limit_type][min_or_max]

        ## 更新事件触发条件
        def update_event_condition(self, condition="", choice=""):
            if choice == "":
                if condition in self.temporary_event_attr["condition"]:
                    del self.temporary_event_attr["condition"][condition]
                else:
                    self.temporary_event_attr["condition"][condition] = []
            else:
                if choice in self.temporary_event_attr["condition"][condition]:
                    self.temporary_event_attr["condition"][condition].remove(choice)
                else:
                    self.temporary_event_attr["condition"][condition].append(choice)

        ## 更新事件触发条件（循环）
        def update_event_condition_loop(self, condition="", choice=""):
            if choice == "":
                if condition in self.temporary_event_attr["condition_loop"]:
                    del self.temporary_event_attr["condition_loop"][condition]
                else:
                    self.temporary_event_attr["condition_loop"][condition] = []
            else:
                if choice in self.temporary_event_attr["condition_loop"][condition]:
                    self.temporary_event_attr["condition_loop"][condition].remove(choice)
                else:
                    self.temporary_event_attr["condition_loop"][condition].append(choice)
        
        ## 更新事件触发条件（数值）
        def update_event_condition_value(self, condition=""):
            if condition in self.temporary_event_attr["condition_value"]:
                del self.temporary_event_attr["condition_value"][condition]
            else:
                self.temporary_event_attr["condition_value"][condition] = 0

        ## 检查待保存内容
        def check_save_content(self):
            ## 检查是否存在错误配置
            ## event_tag相关
            if self.temporary_event_tag == "":
                return "事件tag不能为空！ -> 事件tag"
            elif self.temporary_event_tag == "new_event":
                return "事件tag不能为默认！ -> 事件tag"
            elif self.temporary_event_tag == "_init_value":
                return "事件tag不能为_init_value！ -> 事件tag"
            ## yes/no/other相关
            if len(self.temporary_event_attr['yes'])+len(self.temporary_event_attr['no'])+len(self.temporary_event_attr['other']) == 0:
                return "事件行为不能为空！ -> yes/no/other行为"
            ## round/loop限制相关
            if "min" in self.temporary_event_attr['round'] and "max" in self.temporary_event_attr['round']:
                if self.temporary_event_attr['round']['min'] > self.temporary_event_attr['round']['max']:
                    return "回合数限制区间最小值不能大于最大值！ -> round限制"
                elif self.temporary_event_attr['round']['min'] == self.temporary_event_attr['round']['max']:
                    return "回合数限制区间最小值不能等于最大值！ -> round限制"
            if "min" in self.temporary_event_attr['loop'] and "max" in self.temporary_event_attr['loop']:
                if self.temporary_event_attr['loop']['min'] > self.temporary_event_attr['loop']['max']:
                    return "循环数限制区间最小值不能大于最大值！ -> loop限制"
                elif self.temporary_event_attr['loop']['min'] == self.temporary_event_attr['loop']['max']:
                    return "循环数限制区间最小值不能等于最大值！ -> loop限制"

            return True

        ## 保存已编辑的事件
        def save_temporary_event_to_dict(self):
            self.cree_dict[self.temporary_event_tag] = self.temporary_event_attr

        ## 判断是否保存了具体内容
        def is_event_saved(self):
            if self.temporary_event_tag in self.cree_dict and self.cree_dict[self.temporary_event_tag] == self.temporary_event_attr:
                return True
            else:
                return False
            

    CREEC = class_reigns_event_editor_class()

## 编辑器视口位置
default crees_viewport_yadjustment = ui.adjustment()
## 快捷操作
default event_quick_action = False

## 事件编辑器
screen class_reigns_event_editor_screen():

    modal True

    ## 选择显示哪个事件的备注
    default hover_event_note = ""

    frame:
        xysize(1600,900)
        xycenter(0.5,0.5)
        hbox:
            spacing 10
            textbutton "关闭界面(ESC)":
                text_size 24
                action Confirm("确认关闭界面？这会导致已修改的内容丢失！", Hide('class_reigns_event_editor_screen'))
                keysym "K_ESCAPE"
            textbutton "读取Dict(D)":
                text_size 24
                action Confirm("确认读取Dict？这会导致目前已有事件被覆盖！", Function(CREEC.read_dict))
                keysym "K_d"
            textbutton "读取Json(J)":
                text_size 24
                action Confirm("确认读取Json？这会导致目前已有事件被覆盖！", Function(CREEC.read_json))
                keysym "K_j"
            hbox:
                textbutton "保存Json(S)":
                    text_size 24
                    action Confirm("确认保存Json？", Function(CREEC.save_json))
                    keysym "K_s"
                if CREEC.is_json_saved():
                    text "(已保存)" size 21 xycenter(0.5,0.5) color "#9de0b7"
                else:
                    text "(未保存)" size 21 xycenter(0.5,0.5) color "#e09d9d"
            textbutton "快速操作(Q)":
                text_size 24
                if event_quick_action == False:
                    action Confirm("开启此选项？这可能会导致误操作！", SetVariable("event_quick_action", True))
                else:
                    text_color "#9de0b7"
                    action SetVariable("event_quick_action", False)
                keysym "K_q"
            textbutton "快速排序(W)":
                text_size 24
                if event_quick_action == False:
                    action Confirm("确认快速排序？", Function(CREEC.sort_event_by_tag))
                else:
                    action Function(CREEC.sort_event_by_tag)
                keysym "K_w"
            textbutton "新建事件(E)":
                text_size 24
                action [Show("update_event_editor_screen"),Hide()]
                keysym "K_e"

        ## 主要内容部分
        viewport:
            yadjustment crees_viewport_yadjustment
            xysize(1600,840)
            yalign 1.0
            xalign 0.5
            id "crees_viewport"
            mousewheel True
            draggable True
            vbox:
                align(0.5,0.0)
                spacing 15

                ## 新建初始变量按钮
                if "_init_value" not in CREEC.cree_dict:
                    button:
                        xysize(1600,100)
                        action Function(CREEC.add_init_value)
                        frame:
                            xycenter(0.5,0.5)
                            xysize(1500,100)
                            text "+ 新建初始变量 +" xycenter(0.5,0.5)

                ## 事件列表
                for event_tag, event_attr in CREEC.cree_dict.items():
                    ## 初始化变量
                    if event_tag == "_init_value":
                        fixed:
                            xysize(1600,100)
                            frame:
                                xycenter(0.5,0.5)
                                xysize(1500,100)
                                vbox:
                                    spacing 2
                                    anchor(0.0,0.5)
                                    pos(0.0,0.5)
                                    text "初始变量：" size 28
                                    grid 5 2:
                                        align(0.0,0.5)
                                        xspacing 20
                                        for attr_name, attr_value in event_attr.items():
                                            if attr_name == "Health_Value":
                                                text "初始健康值：" + str(attr_value) size 22
                                            elif attr_name == "Force_Value":
                                                text "初始武力值：" + str(attr_value) size 22
                                            elif attr_name == "Wisdom_Value":
                                                text "初始智力值：" + str(attr_value) size 22
                                            elif attr_name == "Money_Value":
                                                text "初始金钱值：" + str(attr_value) size 22
                                            elif attr_name == "Network_Value":
                                                text "初始联络值：" + str(attr_value) size 22
                                            elif attr_name == "Round_Value":
                                                text "初始回合数：" + str(attr_value) size 22
                                            elif attr_name == "Round_Max_Value":
                                                text "最大回合数：" + str(attr_value) size 22
                                            elif attr_name == "Loop_Value":
                                                text "初始循环数：" + str(attr_value) size 22
                                            elif attr_name == "Loop_Max_Value":
                                                text "最大循环数：" + str(attr_value) size 22
                                
                                ## 编辑按钮
                                button:
                                    anchor(1.0,0.5)
                                    pos(1.0,0.5)
                                    action [Show("update_init_value_Screen"),Hide()]
                                    frame:
                                        xycenter(0.5,0.5)
                                        xysize(60,80)
                                        text "编辑" size 24 xycenter(0.5,0.5) color "#ffffff" vertical True
                    
                    ## 其他事件列表
                    else:
                        fixed:
                            xysize(1600,100)
                            frame:
                                xycenter(0.5,0.5)
                                xysize(1500,100)
                                hbox:
                                    spacing 2
                                    anchor(0.0,0.5)
                                    pos(0.0,0.5)
                                    if event_attr['event_image'] == "":
                                        add "#ffffff" xysize(65, 100) xoffset 2
                                    else:
                                        add event_attr['event_image'] xysize(65, 100) xoffset 2
                                    button:
                                        frame:
                                            xysize(700,100)
                                            align(0.0,0.5)
                                            if hover_event_note == event_tag and event_attr['event_note'] != "":
                                                text event_attr['event_note'] size 26 xycenter(0.5,0.5)
                                            else:
                                                text "事件标签：" + event_tag align(0,0.1) size 30
                                                text "事件名：" + event_attr['event_text'] align(0,1.0) size 22 line_spacing -5
                                        action SetScreenVariable("hover_event_note", event_tag)
                                        hovered SetScreenVariable("hover_event_note", event_tag)
                                        unhovered SetScreenVariable("hover_event_note", "")
                                    
                                    add Null(10,0)

                                    ## yes/no/other行为数
                                    vbox:
                                        align(0.0,0.5)
                                        if "yes" in event_attr and len(event_attr['yes']) > 0:
                                            text "yes行为数：" + str(len(event_attr['yes'])) size 22 color "#fdfffd"
                                        else:
                                            text "yes行为未设置" size 22 color "#606060"
                                        
                                        if "no" in event_attr and len(event_attr['no']) > 0:
                                            text "no行为数：" + str(len(event_attr['no'])) size 22 color "#ffffff"
                                        else:
                                            text "no行为未设置" size 22 color "#606060"
                                        
                                        if "other" in event_attr and len(event_attr['other']) > 0:
                                            text "other行为数：" + str(len(event_attr['other'])) size 22 color "#ffffff"
                                        else:
                                            text "other行为未设置" size 22 color "#606060"
                                    
                                    add Null(10,0)

                                    ## 回合和循环限制数
                                    vbox:
                                        align(0.0,0.5)
                                        if "round" in event_attr and len(event_attr['round']) > 0:
                                            if isinstance(event_attr['round'], list):
                                                text "回合限制数：" + str(len(event_attr['round'])) size 22 color "#ffffff"
                                            elif isinstance(event_attr['round'], dict):
                                                if "min" in event_attr['round'] and "max" in event_attr['round']:
                                                    text "回合限制区：" + str(event_attr['round']['min']) + "至" + str(event_attr['round']['max']) size 22 color "#ffffff"

                                                elif "max" in event_attr['round']:
                                                    text "回合限制区：" + "0至" + str(event_attr['round']['max']) size 22 color "#ffffff"
                                                
                                                elif "min" in event_attr['round']:
                                                    text "回合限制区：" +  str(event_attr['round']['min']) + "至" + str(CREEC.cree_dict["_init_value"]["Round_Max_Value"]) size 22 color "#ffffff"
                                        else:
                                            text "回合无限制" size 22 color "#606060"

                                        if "loop" in event_attr and len(event_attr['loop']) > 0:
                                            if isinstance(event_attr['loop'], list):
                                                text "循环限制数：" + str(len(event_attr['loop'])) size 22 color "#ffffff"
                                            elif isinstance(event_attr['loop'], dict):
                                                if "min" in event_attr['loop'] and "max" in event_attr['loop']:
                                                    text "循环限制区：" + str(event_attr['loop']['min']) + "至" + str(event_attr['loop']['max']) size 22 color "#ffffff"

                                                elif "max" in event_attr['loop']:
                                                    text "循环限制区：" + "0至" + str(event_attr['loop']['max']) size 22 color "#ffffff"
                                                
                                                elif "min" in event_attr['loop']:
                                                    text "循环限制区：" +  str(event_attr['loop']['min']) + "至" + str(CREEC.cree_dict["_init_value"]["Loop_Max_Value"]) size 22 color "#ffffff"
                                        else:
                                            text "循环无限制" size 22 color "#606060"
                                            
                                        if "probability" in event_attr and event_attr['probability'] > 0:
                                            text "触发权重：" + str(event_attr['probability']) size 22 color "#ffffff"
                                        else:
                                            text "无法触发该事件！" size 22 color "#ff8f8f"
                                
                                ## 事件编辑与删除按钮
                                hbox:
                                    spacing 5
                                    anchor(1.0,0.5)
                                    pos(1.0,0.5)
                                    button:
                                        if event_quick_action == True:
                                            action Function(CREEC.remove_event, event_tag)
                                        else:
                                            action Confirm("确认删除事件？", Function(CREEC.remove_event, event_tag))
                                        frame:
                                            xycenter(0.5,0.5)
                                            xysize(60,80)
                                            text "删除" size 24 xycenter(0.5,0.5) color "#ff8f8f" vertical True
                                    
                                    button:
                                        if event_quick_action == True:
                                            action Function(CREEC.move_to_top_event, event_tag)
                                        else:
                                            action Confirm("确认置顶事件？", Function(CREEC.move_to_top_event, event_tag))
                                        frame:
                                            xycenter(0.5,0.5)
                                            xysize(60,80)
                                            text "置顶" size 24 xycenter(0.5,0.5) color "#ffffff" vertical True

                                    button:
                                        if event_quick_action == True:
                                            action Function(CREEC.copy_event, event_tag)
                                        else:
                                            action Confirm("确认复制事件？", Function(CREEC.copy_event, event_tag))
                                        frame:
                                            xycenter(0.5,0.5)
                                            xysize(60,80)
                                            text "复制" size 24 xycenter(0.5,0.5) color "#ffffff" vertical True

                                    button:
                                        action [Show("update_event_editor_screen", update_event_tag=event_tag, update_event_attr=event_attr),Hide()]
                                        frame:
                                            xycenter(0.5,0.5)
                                            xysize(60,80)
                                            text "编辑" size 24 xycenter(0.5,0.5) color "#ffffff" vertical True
                                    
                ## 新建按钮
                button:
                    xysize(1600,100)
                    action [Show("update_event_editor_screen"),Hide()]
                    frame:
                        xycenter(0.5,0.5)
                        xysize(1500,100)
                        text "+ 新建事件 +" xycenter(0.5,0.5)

    ## viewport的滚动条
    vbar:
        xysize(20,840)
        xycenter(0.93,0.53)
        unscrollable "hide"
        value YScrollValue("crees_viewport")

## 事件编辑器的具体事件编辑
screen update_event_editor_screen(update_event_tag="", update_event_attr={}):

    modal True

    ## 当前焦点所在的组件
    default focus_toggle = ""

    ## 回车取消焦点
    key "K_KP_ENTER" action SetLocalVariable("focus_toggle", "")

    ## 当界面显示时将临时变量清除或更新
    on "show" action Function(CREEC.update_temporary, update_event_tag, update_event_attr)

    frame:
        xysize(1600,900)
        xycenter(0.5,0.5)
        hbox:
            spacing 10
            textbutton "关闭界面(ESC)":
                text_size 26
                xycenter(0.5,0.5)
                action Confirm("确认关闭界面？这会导致已修改内容丢失！", [Hide("update_event_editor_screen"),Show("class_reigns_event_editor_screen")])
                keysym "K_ESCAPE"
            
            if CREEC.check_save_content() == True and CREEC.is_event_saved() == False:
                if update_event_tag in CREEC.copy_list:
                    textbutton "覆盖事件(删除复制S)":
                        text_size 26
                        xycenter(0.5,0.5)
                        action Confirm("确认保存事件？这会覆盖原先的内容！", [Function(CREEC.save_temporary_event_to_dict),Function(CREEC.del_copy_event, update_event_tag, 'delete')])
                        keysym "K_s"
                    textbutton "新建事件(保留复制D)":
                        text_size 26
                        xycenter(0.5,0.5)
                        action [Function(CREEC.save_temporary_event_to_dict),Function(CREEC.del_copy_event, update_event_tag, 'save')]
                        keysym "K_d"
                elif update_event_tag in CREEC.cree_dict and update_event_tag != CREEC.temporary_event_tag and CREEC.temporary_event_tag not in CREEC.cree_dict:
                    textbutton "覆盖事件(删除原名S)":
                        text_size 26
                        xycenter(0.5,0.5)
                        action Confirm("确认保存事件？这会覆盖原先的内容！", [Function(CREEC.save_temporary_event_to_dict),Function(CREEC.del_old_event, update_event_tag, 'delete')])
                        keysym "K_s"
                    textbutton "新建事件(保留原名D)":
                        text_size 26
                        xycenter(0.5,0.5)
                        action [Function(CREEC.save_temporary_event_to_dict),Function(CREEC.del_old_event, update_event_tag, 'save')]
                        keysym "K_d"
                elif CREEC.temporary_event_tag in CREEC.cree_dict:
                    textbutton "覆盖事件(S)":
                        text_size 26
                        xycenter(0.5,0.5)
                        action Confirm("确认保存事件？这会覆盖原先的内容！", Function(CREEC.save_temporary_event_to_dict))
                        keysym "K_s"
                else:
                    textbutton "新建事件(S)":
                        text_size 26
                        xycenter(0.5,0.5)
                        action Function(CREEC.save_temporary_event_to_dict)
                        keysym "K_s"
            elif CREEC.is_event_saved() == True:
                text "已保存" color "#9de0b7" size 26 xycenter(0.5,0.5)
            else:
                text CREEC.check_save_content() color "#e09d9d" size 26 xycenter(0.5,0.5)

        if CREEC.temporary_event_attr != {} and update_event_tag != "_init_value":
            ## 主要内容部分
            viewport:
                xoffset 10
                xysize(1600,840)
                yalign 1.0
                xalign 0.5
                id "uees_viewport"
                mousewheel True
                draggable True
                vbox:
                    align(0.5,0.0)
                    spacing 5

                    ## 使用已有事件tag
                    button:
                        text "选择已有事件tag"
                        if focus_toggle == "has_event_tag":
                            background "#333333"
                            action SetLocalVariable("focus_toggle", "")
                        else:
                            action SetLocalVariable("focus_toggle", "has_event_tag")
                    if focus_toggle == "has_event_tag":
                        for event_tag in CREEC.cree_dict.keys():
                            if CREEC.temporary_event_tag != event_tag and event_tag != "_init_value":
                                button:
                                    text event_tag:
                                        size 30
                                        color "#9dbbe0"
                                    action SetVariable("CREEC.temporary_event_tag", event_tag)

                    ## 事件tag
                    button:
                        hbox:
                            text "事件tag:"
                            input:
                                copypaste True
                                value VariableInputValue("CREEC.temporary_event_tag", default=(True if focus_toggle == "event_tag" else False))
                                action SetLocalVariable("focus_toggle", "")
                        if focus_toggle == "event_tag":
                            background "#333333"
                            action SetLocalVariable("focus_toggle", "")
                        else:
                            action SetLocalVariable("focus_toggle", "event_tag")

                    ## 继承原有事件文本
                    if CREEC.temporary_event_tag in CREEC.cree_dict and "event_text" in CREEC.cree_dict[CREEC.temporary_event_tag]:
                        textbutton "继承原有事件文本":
                            action SetDict(CREEC.temporary_event_attr, "event_text", CREEC.cree_dict[CREEC.temporary_event_tag]["event_text"])

                    ## 事件文本
                    button:
                        hbox:
                            text "事件文本:"
                            input:
                                copypaste True
                                value DictInputValue(CREEC.temporary_event_attr, "event_text", default=(True if focus_toggle == "event_text" else False))
                                action SetLocalVariable("focus_toggle", "")
                        if focus_toggle == "event_text":
                            background "#333333"
                            action SetLocalVariable("focus_toggle", "")
                        else:
                            action SetLocalVariable("focus_toggle", "event_text")

                    ## 事件图片
                    button:
                        hbox:
                            text "事件图片:"
                            input:
                                copypaste True
                                value DictInputValue(CREEC.temporary_event_attr, "event_image", default=(True if focus_toggle == "event_image" else False))
                                action SetLocalVariable("focus_toggle", "")
                        if focus_toggle == "event_image":
                            background "#333333"
                            action SetLocalVariable("focus_toggle", "")
                        else:
                            action SetLocalVariable("focus_toggle", "event_image")
                    
                    ## 事件备注
                    button:
                        hbox:
                            text "事件备注:"
                            input:
                                copypaste True
                                value DictInputValue(CREEC.temporary_event_attr, "event_note", default=(True if focus_toggle == "event_note" else False))
                                action SetLocalVariable("focus_toggle", "")
                        if focus_toggle == "event_note":
                            background "#333333"
                            action SetLocalVariable("focus_toggle", "")
                        else:
                            action SetLocalVariable("focus_toggle", "event_note")

                    ## yes/no/other行为
                    for the_action in ["yes", "no", "other"]:
                        
                        ## 文本输入框
                        button:
                            hbox:
                                text the_action + "文本:"
                                input:
                                    copypaste True
                                    value DictInputValue(CREEC.temporary_event_attr, the_action+"_text", default=(True if focus_toggle == the_action+"_text" else False))
                                    action SetLocalVariable("focus_toggle", "")
                            if focus_toggle == the_action+"_text":
                                background "#333333"
                                action SetLocalVariable("focus_toggle", "")
                            else:
                                action SetLocalVariable("focus_toggle", the_action+"_text")

                        ## 行为选择
                        hbox:
                            text the_action + "行为:"
                            for action_tag, action_name in {"Health_Value":"健康值", "Force_Value":"武力值", "Wisdom_Value":"智力值", "Money_Value":"金钱值", "Network_Value":"联络值", "Round_Value":"回合数", "Round_Max_Value":"最大回合","Loop_Value":"循环数", "Loop_Max_Value":"最大循环", "special_event":"特殊事件"}.items():
                                button:
                                    if focus_toggle == the_action+"_"+action_tag:
                                        background "#333333"
                                    text action_name:
                                        size 30
                                        xycenter(0.5,0.5)
                                        if action_tag in CREEC.temporary_event_attr[the_action]:
                                            color "#9de0b7"
                                        else:
                                            color "#e09d9d"
                                    if focus_toggle == the_action+"_"+action_tag:
                                        background "#333333"
                                        action SetLocalVariable("focus_toggle", "")
                                    else:
                                        action SetLocalVariable("focus_toggle", the_action+"_"+action_tag)
                        if focus_toggle == the_action+"_special_event":
                            ## 特殊事件
                            vbox:
                                if focus_toggle == the_action+"_"+action_tag:
                                    for special_event_tag, special_event_name in {"pass":"无", 
                                    "break_loop":"跳出当前循环，并开始下一个循环", 
                                    "game_start":"游戏开始", 
                                    "game_over":"使游戏立刻结束", 
                                    "restart_round":"使回合数不增加", 
                                    "trigger_again":"选择过后再次触发该事件", 
                                    "RRTA":"回合数不增加且选择过后再次触发该事件", 
                                    "not_add_to_selected_event":"选择过后不再增加到已选择事件列表中", 
                                    "loop_ignore":"在当前循环内不再出现该事件", 
                                    "keep_ignore":"在本次游戏中不再出现该事件"
                                    }.items():
                                        button:
                                            xsize 1000
                                            xycenter(0.5,0.5)
                                            text special_event_tag+":"+special_event_name:
                                                size 30
                                                if "special_event" in CREEC.temporary_event_attr[the_action] and special_event_tag in CREEC.temporary_event_attr[the_action]["special_event"]:
                                                    color "#9de0b7"
                                                else:
                                                    color "#e09d9d"
                                            action Function(CREEC.update_special_event, the_action, special_event_tag)
                        else:
                            ## 非特殊事件
                            hbox:
                                for action_tag, action_name in {"Health_Value":"健康值", "Force_Value":"武力值", "Wisdom_Value":"智力值", "Money_Value":"金钱值", "Network_Value":"联络值", "Round_Value":"回合数", "Round_Max_Value":"最大回合","Loop_Value":"循环数", "Loop_Max_Value":"最大循环","special_event":"特殊事件"}.items():
                                    if focus_toggle == the_action+"_"+action_tag:
                                        button:
                                            xycenter(0.5,0.5)
                                            if action_tag not in CREEC.temporary_event_attr[the_action]:
                                                text "NONE" color "#9dbbe0"
                                            elif action_tag in CREEC.temporary_event_attr[the_action] and isinstance(CREEC.temporary_event_attr[the_action][action_tag], int):
                                                text "INT" color "#9de0b7"
                                            elif action_tag in CREEC.temporary_event_attr[the_action] and isinstance(CREEC.temporary_event_attr[the_action][action_tag], str):
                                                text "STR" color "#9de0b7"
                                            action Function(CREEC.yes_no_other_type_toggle, the_action, action_tag)
                                    if focus_toggle == the_action+"_"+action_tag and action_tag in CREEC.temporary_event_attr[the_action] and isinstance(CREEC.temporary_event_attr[the_action][action_tag], int):
                                        bar:
                                            xysize(1000,30)
                                            xycenter(0.5,0.5)
                                            value DictValue(CREEC.temporary_event_attr[the_action], action_tag, range=200, offset=-100)
                                        text str(CREEC.temporary_event_attr[the_action][action_tag]) xycenter(0.5,0.5)

                                    elif focus_toggle == the_action+"_"+action_tag and action_tag in CREEC.temporary_event_attr[the_action] and isinstance(CREEC.temporary_event_attr[the_action][action_tag], str):
                                        button:
                                            input:
                                                copypaste True
                                                value DictInputValue(CREEC.temporary_event_attr[the_action], action_tag, default=(True if focus_toggle == the_action+"_"+action_tag else False))
                                                action SetLocalVariable("focus_toggle", "")
                                            if focus_toggle == the_action+"_"+action_tag:
                                                background "#333333"
                                                action SetLocalVariable("focus_toggle", "")
                                            else:
                                                action SetLocalVariable("focus_toggle", the_action+"_"+action_tag)

                    ## round和loop限制
                    for limit_type, limit_type_max in {"round":"Round_Max_Value", "loop":"Loop_Max_Value"}.items():
                        hbox:
                            text limit_type + "限制:"
                            for limit_value_type in ["LIST", "DICT"]:
                                button:
                                    text limit_value_type:
                                        size 30
                                        if len(CREEC.temporary_event_attr[limit_type]) > 0 and isinstance(CREEC.temporary_event_attr[limit_type], list) and limit_value_type == "LIST":
                                            color "#9de0b7"
                                        elif len(CREEC.temporary_event_attr[limit_type]) > 0 and isinstance(CREEC.temporary_event_attr[limit_type], dict) and limit_value_type == "DICT":
                                            color "#9de0b7"
                                        else:
                                            color "#e09d9d"
                                    if focus_toggle == limit_type+"_"+limit_value_type:
                                        background "#333333"
                                        action SetLocalVariable("focus_toggle", "")
                                    else:
                                        action SetLocalVariable("focus_toggle", limit_type+"_"+limit_value_type)

                            button:
                                text "清除限制"
                                action [Function(CREEC.update_round_loop_limit_list, limit_type),Function(CREEC.update_round_loop_limit_dict)]

                        ## 列表限制
                        if focus_toggle == limit_type+"_LIST":
                            grid 9 math.ceil(CREEC.cree_dict["_init_value"][limit_type_max]/9):
                                spacing 5
                                for i in range(CREEC.cree_dict["_init_value"][limit_type_max]):
                                    button:
                                        xysize(50,50)
                                        background "#1e1e1e" xycenter(0.5,0.5)
                                        text str(i):
                                            xycenter(0.5,0.5)
                                            size 30
                                            if i in CREEC.temporary_event_attr[limit_type]:
                                                color "#9de0b7"
                                            else:
                                                color "#e09d9d"
                                        action Function(CREEC.update_round_loop_limit_list, limit_type, i)

                        ## 字典限制
                        elif focus_toggle == limit_type+"_DICT":
                            if isinstance(CREEC.temporary_event_attr[limit_type], list):
                                button:
                                    text "更改为dict" color "#9dbbe0"
                                    action Function(CREEC.update_round_loop_limit_dict, limit_type)
                            if isinstance(CREEC.temporary_event_attr[limit_type], dict):
                                for min_or_max, min_or_max_name in {"min":"最小值", "max":"最大值"}.items():
                                    hbox:
                                        if min_or_max not in CREEC.temporary_event_attr[limit_type]:
                                            button:
                                                text "添加" + min_or_max_name + "限制" color "#9dbbe0"
                                                action Function(CREEC.update_round_loop_limit_dict, limit_type, min_or_max)
                                        if min_or_max in CREEC.temporary_event_attr[limit_type]:
                                            text min_or_max_name + "限制:" xycenter(0.5,0.5) color "#9de0b7"
                                            bar:
                                                xysize(1000,30)
                                                xycenter(0.5,0.5)
                                                value DictValue(CREEC.temporary_event_attr[limit_type], min_or_max, range=CREEC.cree_dict["_init_value"][limit_type_max])
                                            text str(CREEC.temporary_event_attr[limit_type][min_or_max]) xycenter(0.5,0.5)
                                            button:
                                                xycenter(0.5,0.5)
                                                text "清除" + min_or_max_name color "#e09d9d" 
                                                action Function(CREEC.update_round_loop_limit_dict, limit_type, min_or_max)

                            if "min" in CREEC.temporary_event_attr[limit_type] and "max" in CREEC.temporary_event_attr[limit_type]:
                                if CREEC.temporary_event_attr[limit_type]["min"] < CREEC.temporary_event_attr[limit_type]["max"]:
                                    text "限制区间" + str(CREEC.temporary_event_attr[limit_type]["min"]) + "至" + str(CREEC.temporary_event_attr[limit_type]["max"]) color "#9de0b7"
                                else:
                                    text "限制区间错误！请重新配置！" color "#e09d9d"
                            elif "min" in CREEC.temporary_event_attr[limit_type] and limit_type == limit_type:
                                text "限制区间" + str(CREEC.temporary_event_attr[limit_type]["min"]) + "至" + str(CREEC.cree_dict["_init_value"][limit_type_max]) color "#9de0b7"
                            elif "max" in CREEC.temporary_event_attr[limit_type] and limit_type == limit_type:
                                text "限制区间" + str(0) + "至" + str(CREEC.temporary_event_attr[limit_type]["max"]) color "#9de0b7"

                    ## 事件触发概率（权重）
                    hbox:
                        text "事件触发概率（权重）:"
                        bar:
                            xysize(1000,30)
                            xycenter(0.5,0.5)
                            value DictValue(CREEC.temporary_event_attr, "probability", range=100)
                        text str(CREEC.temporary_event_attr["probability"]) xycenter(0.5,0.5)
                    
                    ## 事件触发条件
                    ## 可能出现的报错 -> 事件触发条件不存在或已被清除
                    button:
                        text "前置条件:":
                            if len(CREEC.temporary_event_attr["condition"]) > 0:
                                color "#9de0b7"
                            else:
                                color "#e09d9d"
                        if focus_toggle == "condition":
                            background "#333333"
                            action SetLocalVariable("focus_toggle", "")
                        else:
                            action SetLocalVariable("focus_toggle", "condition")
                    if focus_toggle == "condition":
                        for event_tag in CREEC.cree_dict.keys():
                            if event_tag != "_init_value":
                                button:
                                    text event_tag:
                                        size 30
                                        if event_tag in CREEC.temporary_event_attr["condition"] and len(CREEC.temporary_event_attr["condition"][event_tag]) > 0:
                                            color "#9dbbe0"
                                        elif event_tag in CREEC.temporary_event_attr["condition"]:
                                            color "#9de0b7"
                                        else:
                                            color "#e09d9d"
                                    action Function(CREEC.update_event_condition, event_tag)

                                if event_tag in CREEC.temporary_event_attr["condition"]:
                                    hbox:
                                        xoffset 60
                                        for choice in ["yes", "no", "other"]:
                                            button:
                                                text choice:
                                                    size 30
                                                    if choice in CREEC.temporary_event_attr["condition"][event_tag]:
                                                        color "#9de0b7"
                                                    else:
                                                        color "#e09d9d"
                                                action Function(CREEC.update_event_condition, event_tag, choice)

                    ## 事件触发条件（在任何循环内）
                    ## 可能出现的报错 -> 事件触发条件不存在或已被清除
                    button:
                        text "前置条件（在任何循环内）:":
                            if len(CREEC.temporary_event_attr["condition_loop"]) > 0:
                                color "#9de0b7"
                            else:
                                color "#e09d9d"
                        if focus_toggle == "condition_loop":
                            background "#333333"
                            action SetLocalVariable("focus_toggle", "")
                        else:
                            action SetLocalVariable("focus_toggle", "condition_loop")
                    if focus_toggle == "condition_loop":
                        for event_tag in CREEC.cree_dict.keys():
                            if event_tag != "_init_value":
                                button:
                                    text event_tag:
                                        size 30
                                        if event_tag in CREEC.temporary_event_attr["condition_loop"] and len(CREEC.temporary_event_attr["condition_loop"][event_tag]) > 0:
                                            color "#9dbbe0"
                                        elif event_tag in CREEC.temporary_event_attr["condition_loop"]:
                                            color "#9de0b7"
                                        else:
                                            color "#e09d9d"
                                    action Function(CREEC.update_event_condition_loop, event_tag)

                                if event_tag in CREEC.temporary_event_attr["condition_loop"]:
                                    hbox:
                                        xoffset 60
                                        for choice in ["yes", "no", "other"]:
                                            button:
                                                text choice:
                                                    size 30
                                                    if choice in CREEC.temporary_event_attr["condition_loop"][event_tag]:
                                                        color "#9de0b7"
                                                    else:
                                                        color "#e09d9d"
                                                action Function(CREEC.update_event_condition_loop, event_tag, choice)

                    ## 事件触发条件（数值类型）
                    button:
                        text "前置条件（数值类型）:":
                            if len(CREEC.temporary_event_attr["condition_value"]) > 0:
                                color "#9de0b7"
                            else:
                                color "#e09d9d"
                        if focus_toggle == "condition_value":
                            background "#333333"
                            action SetLocalVariable("focus_toggle", "")
                        else:
                            action SetLocalVariable("focus_toggle", "condition_value")
                    if focus_toggle == "condition_value":
                        vbox:
                            for init_value_name, init_value_info in CREEC.cree_dict["_init_value"].items():
                                hbox:
                                    if init_value_name == "Health_Value":
                                        text "健康值:" xycenter(0.5,0.5)
                                    elif init_value_name == "Force_Value":
                                        text "武力值:" xycenter(0.5,0.5)
                                    elif init_value_name == "Wisdom_Value":
                                        text "智力值:" xycenter(0.5,0.5)
                                    elif init_value_name == "Money_Value":
                                        text "金钱值:" xycenter(0.5,0.5)
                                    elif init_value_name == "Network_Value":
                                        text "联络值:" xycenter(0.5,0.5)
                                    elif init_value_name == "Round_Value":
                                        text "回合数:" xycenter(0.5,0.5)
                                    elif init_value_name == "Round_Max_Value":
                                        text "最大回合数:" xycenter(0.5,0.5)
                                    elif init_value_name == "Loop_Value":
                                        text "循环数:" xycenter(0.5,0.5)
                                    elif init_value_name == "Loop_Max_Value":
                                        text "最大循环数:" xycenter(0.5,0.5)
                                    if init_value_name not in CREEC.temporary_event_attr["condition_value"]:
                                        button:
                                            text "添加"+init_value_name+"条件" color "#9dbbe0" xycenter(0.5,0.5)
                                            action Function(CREEC.update_event_condition_value, init_value_name)
                                    else:
                                        bar:
                                            xysize(1000,30)
                                            xycenter(0.5,0.5)
                                            if init_value_name in ["Round_Value", "Round_Max_Value"]:
                                                value DictValue(CREEC.temporary_event_attr["condition_value"], init_value_name, range=CREEC.cree_dict["_init_value"]["Round_Max_Value"])
                                            elif init_value_name in ["Loop_Value", "Loop_Max_Value"]:
                                                value DictValue(CREEC.temporary_event_attr["condition_value"], init_value_name, range=CREEC.cree_dict["_init_value"]["Loop_Max_Value"])
                                            else:
                                                value DictValue(CREEC.temporary_event_attr["condition_value"], init_value_name, range=100)
                                        text str(CREEC.temporary_event_attr["condition_value"][init_value_name]) xycenter(0.5,0.5)
                                        textbutton "清除条件":
                                            xycenter(0.5,0.5)
                                            text_color "#e09d9d"
                                            action Function(CREEC.update_event_condition_value, init_value_name)

    if CREEC.temporary_event_attr != {} and update_event_tag != "_init_value":
        ## viewport的滚动条
        vbar:
            xysize(20,840)
            xycenter(0.93,0.53)
            unscrollable "hide"
            value YScrollValue("uees_viewport")

## 初始值编辑器
screen update_init_value_Screen():
    button:
        xysize(1920,1080)
        action NullAction()

    frame:
        xysize(1600,900)
        xycenter(0.5,0.5)
        vbox:
            hbox:
                textbutton "恢复默认":
                    text_size 26
                    action Confirm("确认恢复默认？", Function(CREEC.add_init_value))
                textbutton "关闭界面":
                    text_size 26
                    action Confirm("确认关闭界面？", [Hide("update_init_value_Screen"),Show("class_reigns_event_editor_screen")])
            
            vbox:
                spacing 10
                for init_value_name, init_value_info in CREEC.cree_dict["_init_value"].items():
                    hbox:
                        spacing 10
                        
                        button:
                            xysize(30,30)
                            xycenter(0.5, 0.5)
                            background "#1e1e1e"
                            if CREEC.cree_dict["_init_value"][init_value_name] < 100:
                                text "+" xycenter(0.5,0.5) size 26 color "#9de0b7"
                                action IncrementDict(CREEC.cree_dict["_init_value"], init_value_name, 1)
                            else:
                                text "+" xycenter(0.5,0.5) size 26 color "#e09d9d"
                                action NullAction()
                        
                        button:
                            xysize(30,30)
                            xycenter(0.5, 0.5)
                            background "#1e1e1e"
                            if CREEC.cree_dict["_init_value"][init_value_name] > 0:
                                text "-" xycenter(0.5,0.5) size 26 color "#9de0b7"
                                action IncrementDict(CREEC.cree_dict["_init_value"], init_value_name, -1)
                            else:
                                text "-" xycenter(0.5,0.5) size 26 color "#e09d9d"
                                action NullAction()

                        if init_value_name == "Health_Value":
                            text "初始健康值:"
                        elif init_value_name == "Force_Value":
                            text "初始武力值:"
                        elif init_value_name == "Wisdom_Value":
                            text "初始智力值:"
                        elif init_value_name == "Money_Value":
                            text "初始金钱值:"
                        elif init_value_name == "Network_Value":
                            text "初始联络值:"
                        elif init_value_name == "Round_Value":
                            text "初始回合数:"
                        elif init_value_name == "Round_Max_Value":
                            text "最大回合数:"
                        elif init_value_name == "Loop_Value":
                            text "初始循环数:"
                        elif init_value_name == "Loop_Max_Value":
                            text "最大循环数:"
                        bar:
                            xysize(1000,30)
                            xycenter(0.5,0.5)
                            value DictValue(CREEC.cree_dict["_init_value"], init_value_name, range=100)
                        text str(init_value_info) xycenter(0.5,0.5)
