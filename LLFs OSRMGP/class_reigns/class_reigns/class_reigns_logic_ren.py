## 该项目来源于LLFs-OSRMGP（https://github.com/llfseik/LLFs-OSRMGP）,遵循MIT协议。
## 严禁售卖该项目代码！你可以随意将其用修改并于任何非商业用途，但请注明出处！

"""renpy
init -1 python:
"""
import random

class ClassReignsLogic:
    def __init__(self, the_CRED=class_reigns_event_dict):
        ## 健康值、武力值、智力值、金钱值、联络值、回合数、循环次数、每次循环最大回合数
        try:
            self.Health_Value = the_CRED['_init_value']["Health_Value"]
            self.Force_Value = the_CRED['_init_value']["Force_Value"]
            self.Wisdom_Value = the_CRED['_init_value']["Wisdom_Value"]
            self.Money_Value = the_CRED['_init_value']["Money_Value"]
            self.Network_Value = the_CRED['_init_value']["Network_Value"]
            self.Round_Value = the_CRED['_init_value']["Round_Value"]
            self.Round_Max_Value = the_CRED['_init_value']["Round_Max_Value"]
            self.Loop_Value = the_CRED['_init_value']["Loop_Value"]
            self.Loop_Max_Value = the_CRED['_init_value']["Loop_Max_Value"]
        except:
            print("Error: 初始值设置错误 -> class_reigns_logic_ren.py -> __init__()")
            self.Health_Value = 50
            self.Force_Value = 50
            self.Wisdom_Value = 50
            self.Money_Value = 50
            self.Network_Value = 50
            self.Round_Value = 0
            self.Round_Max_Value = 20
            self.Loop_Value = 0
            self.Loop_Max_Value = 10
        
        ## 所有事件的字典
        self.CRED = the_CRED
        ## 已选择的事件
        ## self.selected_event = {1:{1:{"event_1":"yes"}, 2:{"event_1":"no"}}, 2:{1:{"event_2":"yes"}, 2:{"event_2":"no"}}}
        self.selected_event = {}
        ## 正在显示的事件
        self.display_event = {}
        ## 在当前循环需要忽略的事件
        self.loop_ignore_event_list = []
        ## 需要一直忽略的事件
        self.keep_ignore_event_list = []
        ## 下次必定出现的事件
        self.next_event_list = ""
        
        self.the_start_event()
    
    ## 设置特殊事件，不放入事件字典中方便单独管理
    def the_start_event(self):
        ## 最开始的事件
        self.display_event = {
            "start_event":{
                "event_text":"最上方将显示你会看到的事件，如果你准备好了，就将卡牌划到左边开始游戏",
                "event_image":"",
                "event_note":"",
                "yes":{
                    "special_event":["pass"]
                    },
                "yes_text":"开始游戏",
                "no":{
                    "special_event":["game_over"]
                    },
                "no_text":"游戏结束",
                "other":{"special_event":"pass"},
                "other_text":"",
                "round":[0],
                "loop":[0],
                "probability":1,
                "condition":{},
                "condition_loop":{},
                "condition_value":{}
            }
        }
        ## 将当前界面的临时变量也改变
        renpy.run(SetScreenVariable("the_display_event", dict(*self.display_event.values()))) # type: ignore
    
    ## 选择当前给玩家展示的事件
    def the_event(self):
        ## 所有可能会出现的事件
        all_event = []
        
        ## 获取可能出现的事件
        def get_event(event_tag, event_attr):
            ## 待返回的事件列表
            event_list = []
            ## 出现概率
            if event_attr["probability"] < 1:
                return []
            else:
                ## 前置条件（所有循环内）如果存在
                if "condition_loop" in event_attr.keys() and event_attr["condition_loop"] != {}:
                    if len(self.selected_event) < 1:
                        return []
                    ## 先将所有事件的选项合并到一个list中
                    all_event_condition_loop = {}
                    for loop_num in range(self.Loop_Value+1):
                        if loop_num in self.selected_event.keys():
                            for selected_event in self.selected_event[loop_num].values():
                                for event_key, event_value in selected_event.items():
                                    if event_key not in all_event_condition_loop.keys():
                                        all_event_condition_loop[event_key] = []
                                    all_event_condition_loop[event_key].append(event_value)
                    can_event = []
                    if len(all_event_condition_loop) > 0:
                        for event_key_condition, event_value_condition in event_attr["condition_loop"].items():
                            for event_key, event_value in all_event_condition_loop.items():
                                if event_key_condition == event_key:
                                    if event_value in event_value_condition:
                                        can_event.append(event_key)
                                        break
                    if len(can_event) == 0:
                        return []
                
                ## 前置条件如果存在
                if "condition" in event_attr.keys() and event_attr["condition"] != {}:
                    if len(self.selected_event) < 1:
                        return []
                    ## 只判断当前循环内的事件
                    can_event = []
                    if len(self.selected_event) > 0:
                        for event_key_condition, event_value_condition in event_attr["condition"].items():
                            if self.Loop_Value in self.selected_event.keys():
                                for selected_event in self.selected_event[self.Loop_Value].values():
                                    for event_key, event_value in selected_event.items():
                                        if event_key_condition == event_key:
                                            if event_value in event_value_condition:
                                                can_event.append(event_key)
                                                break
                    if len(can_event) == 0:
                        return []
                            
                ## 前置条件（数值类型）如果存在
                if "condition_value" in event_attr.keys() and event_attr["condition_value"] != {}:
                    for condition_key, condition_value in event_attr["condition_value"].items():
                        if condition_key in ["Health_Value", "Force_Value", "Wisdom_Value", "Money_Value", "Network_Value"]:
                            if isinstance(condition_value, int):
                                ## 将获取到的字符串转化为函数内的变量
                                if eval("self."+condition_key) != condition_value:
                                    return []
                            elif isinstance(condition_value, list):
                                if "max" in condition_value and eval("self."+condition_key) > condition_value["max"]:
                                    return []
                                if "min" in condition_value and eval("self."+condition_key) < condition_value["min"]:
                                    return []
                            else:
                                print("Error: 前置条件（数值类型）值类型错误 -> the_event() -> get_event()")
                                return []
                
                ## 如果存在回合
                if "round" in event_attr.keys() and len(event_attr["round"]) > 0:
                    if isinstance(event_attr["round"], list) and self.Round_Value not in event_attr["round"]:
                        return []
                    elif isinstance(event_attr["round"], dict) and "min" in event_attr["round"] and "max" in event_attr["round"]:
                        if self.Round_Value < event_attr["round"]["min"]:
                            return []
                        if self.Round_Value > event_attr["round"]["max"]:
                            return []
                ## 如果存在循环
                if  "loop" in event_attr.keys() and len(event_attr["loop"]) > 0:
                    if isinstance(event_attr["loop"], list) and self.Loop_Value not in event_attr["loop"]:
                        return []
                    elif isinstance(event_attr["loop"], dict) and "min" in event_attr["loop"] and "max" in event_attr["loop"]:
                        if self.Loop_Value < event_attr["loop"]["min"]:
                            return []
                        if self.Loop_Value > event_attr["loop"]["max"]:
                            return []
                
                ## 如果完全符合全部条件，则判断需返回多少个参数
                for i in range(event_attr["probability"]):
                    event_list.append(event_tag)
                
                return event_list
        
        ## 遍历所有事件，将符合条件的事件加入列表
        if self.next_event_list != "":
            for event_tag, event_attr in self.CRED.items():
                if event_tag not in self.keep_ignore_event_list and event_tag not in self.loop_ignore_event_list and event_tag != "_init_value":
                    all_event.extend(get_event(event_tag, event_attr))
            ## 如果可以触发的事件内存在概率为100的事件，则启用特殊可用事件列表(下个事件必定为这个事件)
            if len(all_event) > 0:
                for event_tag in all_event:
                    if event_tag in self.CRED.keys() and self.CRED[event_tag]["probability"] == 100 and event_tag not in self.loop_ignore_event_list and event_tag not in self.keep_ignore_event_list:
                        all_event.clear()
                        all_event.append(event_tag)
                        break
        else:
            for event_tag, event_attr in self.CRED.items():
                if event_tag == self.next_event_list:
                    all_event.append(event_tag)
                    self.next_event_list = ""
                    break
        
        ## 随机选择一个事件，最终显示给玩家
        if len(all_event) > 0:
            random_event = random.choice(all_event)
            self.display_event = {random_event : self.CRED[random_event]}
        else:
            self.what_happens_after_judgment("no_event")
        
        ## 将当前界面的临时变量也改变
        renpy.run(SetScreenVariable("the_display_event", dict(*self.display_event.values()))) # type: ignore

    ## 玩家选择选项后发生的事件
    def what_happens_after_choice(self,choice):
        # self.game_over_special_event()

        ## 获取choice所对应的事件
        the_display_event = dict(*self.display_event.values())
        ## 事件行为字典
        choice_event = the_display_event[choice]
        ## 是否要增加回合数
        change_round = True
        ## 是否要增加循环次数
        change_loop = False
        ## 是否再次触发事件
        trigger_again = False
        ## 是否要将此事件结果加入selected_event字典
        add_to_selected_event = True
        
        for event_key, event_value in choice_event.items():
            ## 直接修改参数的事件
            if event_key in ["Health_Value", "Force_Value", "Wisdom_Value", "Money_Value", "Network_Value", "Round_Value", "Loop_Value", "Round_Max_Value", "Loop_Max_Value"]:
                if isinstance(event_value, int):
                    exec("self." + event_key + " += " + str(event_value))
                elif isinstance(event_value, str):
                    exec("self." + event_key + " = " + str(event_value))
            
            ## 特殊事件
            elif event_key == "special_event" or event_key == "SE":
                ## 代表什么都不做，可以用于占位
                for se_action in event_value:
                    if se_action == "pass" or se_action == "PASS":
                        pass
                    ## 表示跳出当前循环，并开始下一个循环
                    elif se_action == "break_loop" or se_action == "BL":
                        self.Round_Value = 1
                        self.Loop_Value += 1
                    ## 表示游戏开始
                    elif se_action == "game_start" or se_action == "GS":
                        self.Round_Value = 1
                        self.Loop_Value = 0
                        change_round = False
                        change_loop = False
                        add_to_selected_event = False
                    ## 表示游戏结束
                    elif se_action == "game_over" or se_action == "GO":
                        change_round = False
                        change_loop = False
                        add_to_selected_event = False
                        self.game_over_special_event()
                        return
                    ## 表示回合数不增加（用于一些需要循环的事件）
                    elif se_action == "restart_round" or se_action == "RR":
                        change_round = False
                    ## 选择过后下一个事件必定为该事件（最好与restart_round配合使用）
                    elif se_action == "trigger_again" or se_action == "TA":
                        trigger_again = True
                    ## "restart_round"与"trigger_again"的组合，表示回合数不增加且选择过后下一个事件必定为该事件
                    elif se_action == "RRTA":
                        change_round = False
                        trigger_again = True
                    ## 表示不再将此事件结果加入selected_event字典
                    elif se_action == "not_add_to_selected_event" or se_action == "NTASE":
                        add_to_selected_event = False
                    ## 在当前循环内不再出现该事件
                    elif se_action == "loop_ignore" or se_action == "LI":
                        self.loop_ignore_event_list.append(str(*self.display_event.keys()))
                    ## 在所有循环内不再出现该事件
                    elif se_action == "keep_ignore" or se_action == "KI":
                        self.keep_ignore_event_list.append(str(*self.display_event.keys()))
                    else:
                        print("Error: 事件行为字典值类型错误 -> what_happens_after_choice()")
        
        ## 将事件选择的结果加入selected_event字典
        if add_to_selected_event == True:
            if self.Loop_Value not in self.selected_event.keys():
                self.selected_event[self.Loop_Value] = {}
            if self.Round_Value not in self.selected_event[self.Loop_Value].keys():
                self.selected_event[self.Loop_Value][self.Round_Value] = {}
            self.selected_event[self.Loop_Value][self.Round_Value][str(*self.display_event.keys())] = choice
        
        ## 判断是否要增加回合数、循环次数
        if change_round == True:
            self.Round_Value += 1
        if change_loop == True:
            self.Loop_Value += 1
        if trigger_again == False:
            self.next_event_list = str(*self.display_event.keys())
        
        self.what_happens_after_judgment()

    ## 判断完事件后，判断是否要更新循环或达成结局
    def what_happens_after_judgment(self, action=None):
        ## 结局显示的话
        the_message = ""
        
        ## 如果触发了这结局，说明游戏中可能存在bug（如果不是有意为之的）
        ## 你需要保证玩家有足够多的事件可以选择
        if action == "no_event":
            renpy.notify('游戏通关！')
            renpy.run(Show("class_reigns_game_over_screen", message='你走到了事件的尽头！'))
            return
        
        if self.Health_Value <= 0:
            the_message = "你虚死了！"
        elif self.Force_Value <= 0:
            the_message = "你弱死了！"
        elif self.Wisdom_Value <= 0:
            the_message = "你笨死了！"
        elif self.Money_Value <= 0:
            the_message = "你穷死了！"
        elif self.Network_Value <= 0:
            the_message = "你孤独死了！"
        
        if self.Health_Value >= 100:
            the_message = "你在追求健康上迷失了方向……"
        elif self.Force_Value >= 100:
            the_message = "你在追求力量上迷失了方向……"
        elif self.Wisdom_Value >= 100:
            the_message = "你在追求智力上迷失了方向……"
        elif self.Money_Value >= 100:
            the_message = "你在追求金钱上迷失了方向……"
        elif self.Network_Value >= 100:
            the_message = "你在追求人际关系上迷失了方向……"
        
        if the_message != "":
            renpy.notify('游戏结束！')
            renpy.run(Show("class_reigns_game_over_screen", message=the_message))
            return
        
        if self.Round_Value >= self.Round_Max_Value:
            self.Round_Value = 0
            self.Loop_Value += 1
            ## 清空当前循环需要忽略的事件列表
            self.loop_ignore_event_list = []
        if self.Loop_Value >= self.Loop_Max_Value:
            the_message = "恭喜你通关了游戏！"
        
        if the_message != "":
            renpy.notify('游戏通关！')
            renpy.run(Show("class_reigns_game_over_screen", message=the_message))
            return
        
        ## 如果没有达成任何结局则继续游戏
        self.the_event()
    
    ## 特殊事件：游戏结束
    def game_over_special_event(self):
        renpy.notify('游戏结束！')
        renpy.run(Show("class_reigns_game_over_screen", message='游戏结束！'))
        

CRL = ClassReignsLogic()