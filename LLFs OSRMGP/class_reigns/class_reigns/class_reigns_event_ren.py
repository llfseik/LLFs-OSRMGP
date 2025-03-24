## 该项目来源于LLFs-OSRMGP（https://github.com/llfseik/LLFs-OSRMGP）,遵循MIT协议。
## 严禁售卖该项目代码！你可以随意将其用修改并于任何非商业用途，但请注明出处！

"""renpy
init -2 python:
"""

## 保存着各类事件的字典
'''
class_reigns_event_dict : dict = {
    ## 该事件名不可变动，用于初始化游戏时的初始值
    "_init_value":{
        ## 健康值
        "Health_Value":50,
        ## 力量值
        "Force_Value":50,
        ## 智力值
        "Wisdom_Value":50,
        ## 金钱值
        "Money_Value":50,
        ## 联络值
        "Network_Value":50,
        ## 回合数
        "Round_Value":0,
        ## 回合最大值
        "Round_Max_Value":20,
        ## 循环次数
        "Loop_Value":0,
        ## 循环最大值
        "Loop_Max_Value":10,
    },
    
    ## 事件tag（该tag需要是唯一的）
    "event_tag":{
        
        ## 事件文本/名称
        ## 若为空则不显示文本
        "event_text":"",
        
        ## 事件图片
        ## 若为空则为纯白色的矩形占位图
        ## 例如你有一张图片名为“床”，可以直接将其写在这里
        ## 例如：“床”
        ## 若需要用路径的方式填写到此处，请自行在class_reigns_logic_ren.py中添加判断
        "event_image":"",
        
        ## 事件备注
        ## 若为空则不显示备注
        "event_note":"",
        
        ## 选项1会触发的事件，若为空则不显示，yes和no至少需要有一个不为空
        ## 例如：{"Health_Value":-10, "Force_Value":10, "Loop_Value_Max":10 }
        ## 如果其后方的值为str类型，则表示直接更改为对应的值，否则代表+=该值
        ## 特殊事件"special_event"/"SE"：
        ## pass/PASS 代表什么都不做，可以用于占位
        ## break_loop/BL 表示跳出当前循环，并开始下一个循环
        ## game_start/GS 代表游戏开始
        ## game_over/GO 使游戏立刻结束
        ## restart_round/RR 使回合数不增加（用于一些需要循环的事件）
        ## trigger_again/TA 选择过后再次触发该事件（最好与restart_round配合使用）
        ## RRTA "restart_round"与"trigger_again"的组合，表示回合数不增加且选择过后再次触发该事件
        ## not_add_to_selected_event/NATSE 选择过后不再增加到已选择事件列表中
        ## loop_ignore/LI 在当前循环内不再出现该事件
        ## keep_ignore/KI 在本次游戏中不再出现该事件
        ## 例如：{"special_event":["break_loop", "pass"]}
        ## 又或者可以使用简写：
        ## 例如：{"SE":["BL", "pass"]}
        ## 行为的执行顺序是从上至下，从左往右的，这点需要注意
        ## yes/no/other均可套用此逻辑
        "yes":{},
        
        ## 选项1文本
        ## 若为空，则默认为“点头”，常为屏幕左侧文字
        "yes_text":"",
        
        ## 选项2会触发的事件，若为空则不显示，yes和no至少需要有一个不为空
        ## 例如：{"Health_Value":10, "Force_Value":-10}
        "no":{},
        
        ## 选项2文本
        ## 若为空，则默认为“摇头”，常为屏幕右侧文字
        "no_text":"",
        
        ## 选项3会触发的事件，若为空则不显示
        ## 例如：{"Health_Value":0, "Force_Value":0}
        "other":{},
        
        ## 选项3文本
        ## 若为空，则默认为“沉默”，常为屏幕下方文字
        "other_text":"",
        
        ## 会出现的回合内
        ## 若为空，则代表任何回合都可能出现
        ## 例如：[1,3,10]
        ## 若需要显示为某个范围，则可以用字典（min、max）表示
        ## min代表大于等于该值的才会触发，max代表小于该值的才会触发，min和max都存在表示为一个区间
        ## 例如：{"min":1, "max":10}
        "round":[],
        
        ## 会出现的循环内
        ## 若为空，则代表任何循环都可能出现
        ## 例如：[1,3,10]
        ## 若需要显示为某个范围，则可以用字典（min、max）表示
        ## min代表大于等于该值的才会触发，max代表小于该值的才会触发，min和max都存在表示为一个区间
        ## 例如：{"min":1, "max":10}
        "loop":[],
        
        ## 在轮次内出现的概率
        ## 若为0（任何小于1的值），则表示不会出现
        ## 若为100及以上，则表示必然出现
        ## 若为0-100之间的数值，则表示出现的概率
        ## 若该值为0，则probability的优先级比round、loop和condition高，且round、loop、condition均不起作用
        "probability":0,
        
        ## 事件触发条件
        ## 前置条件，不满足条件则不会出现该事件，若为空则所有时候都会出现
        ## 该属性只会读取本次循环内已经被选择过的事件，例如在循环1中事件A为yes，到循环2中则不会被视为触发条件
        ## 例如：{"event_tag_1":["yes","no"], "event_tag_2":[]}
        ## 若事件后的列表为空，则代表只要存在该事件，就不会触发本事件
        "condition":{},
        
        ## 事件触发条件（在任何循环内）
        ## 与condition类似，但会读取所有循环内已经被选择过的事件，例如在循环1中事件A为yes，到循环2中也会被视为触发条件
        "condition_loop":{},
        
        ## 事件触发条件（数值类型）
        ## 与condition类似，但是仅能为数值类型，例如Health_Value、Force_Value等
        ## 例如：{"Health_Value":10, "Force_Value":10}
        ## 若需要显示为某个范围，则可以用字典（min、max）表示
        ## min代表大于等于该值的才会触发，max代表小于该值的才会触发，min和max都存在表示为一个区间
        ## 例如：{"Health_Value":{"min":10, "max":20}, "Force_Value":{"min":10, "max":20}}
        "condition_value":{}
    },
    ## 额外再强调一下事件的出现的优先级：
    ## 1. probability > condition > round > loop
    ## 2. 若probability为0，则round、loop、condition均不起作用
    ## 3. 若round、loop、condition均为空，则任何回合、循环、条件均可能出现
    ## 4. 若round、loop、condition均不为空，则只要满足其中一个条件，则该事件就会出现
    ## 5. 若round、loop、condition均存在，则优先级为round、loop、condition，若round、loop、condition均不为空，则优先级为probability
}

# ## 保存着各类事件的字典
# class_reigns_event_dict: dict = {
#     ## 该事件名不可变动，用于初始化游戏时的初始值
#     "_init_value": {
#         "Health_Value": 50,
#         "Force_Value": 50,
#         "Wisdom_Value": 50,
#         "Money_Value": 50,
#         "Network_Value": 50,
#         "Round_Value": 0,
#         "Round_Max_Value": 20,
#         "Loop_Value": 0,
#         "Loop_Max_Value": 10,
#     },

#     ## 当后续没有可以显示的事件时，便会默认再次显示当前事件
#     ## 这个命名代表所有循环中第一个会出现的事件，可以用来作为游戏最开始的事件
#     ## 所有事件tag最好都遵照这种方式命名，方便使用查找搜索同类型事件
#     ## 这些样例均是由事件编辑器所生成的，在实际使用中可以移除一些不需要的属性
#     "event_any_1_A": {
#         "event_text": "新的一天，从起床开始？",
#         "event_image": "床",
#         "yes": {
#             "Health_Value": 2,
#             "special_event": ["loop_ignore"]  # 在当前循环内不再出现该事件
#         },
#         "yes_text": "",
#         "no": {
#             "Health_Value": -2,
#             "special_event": [
#                 "restart_round",
#                 "loop_ignore"
#             ],
#         },
#                 "no_text":"",
#         "other": {},
#         "other_text": "",
#         "round": [1],
#         "loop": [],
#         "probability": 1,
#         "condition": {},
#         "condition_loop": {},
#         "condition_value": {}
#     },
#     "event_any_1_B": {
#         "event_text": "嗯……今天还有很多事情要做，确定不起床吗？",
#         "event_image": "床",
#         "yes": {
#             "Health_Value": 2
#         },
#         "yes_text": "",
#         "no": {
#             "Health_Value": -2,
#             "special_event": ["RRTA"]  # 使回合数不增加，并再次触发该事件
#         },
#         "no_text":"",
#         "other": {},
#         "other_text": "",
#         "round": [1],
#         "loop": [],
#         "probability": 1,
#         "condition": {"event_any_1_A": ["no"]},
#         "condition_loop": {},
#         "condition_value": {}
#     },
#     "event_any_2_A": {
#         "event_text": "非常好！让我们下床去做点其他事情吧！",
#         "event_image": "床",
#         "yes": {
#             "special_event": ["PASS"]  # 什么都不做
#         },
#         "yes_text": "",
#         "no": {},
#         "no_text":"",
#         "other": {},
#         "other_text": "",
#         "round": [2],
#         "loop": [],
#         "probability": 1,
#         "condition": {},
#         "condition_loop": {},
#         "condition_value": {}
#     },
#     "event_any_3_A": {
#         "event_text": "今天的早饭是……烈烈的秘制炒饭！",
#         "event_image": "米饭",
#         "yes": {
#             "Health_Value": 3
#         },
#         "yes_text": "",
#         "no": {
#             "Health_Value": -2
#         },
#         "no_text":"",
#         "other": {},
#         "other_text": "",
#         "round": [3],
#         "loop": [],
#         "probability": 1,
#         "condition": {},
#         "condition_loop": {},
#         "condition_value": {}
#     },
#     ## event_any_3_A的特殊分支，这次选择yes还是会扣健康值
#     "event_any_3_B": {
#         "event_text": "今天的早饭是……烈烈的秘制炒饭！",
#         "event_image": "米饭",
#         "yes": {
#             "Health_Value": -1
#         },
#         "yes_text": "",
#         "no": {
#             "Health_Value": -2
#         },
#         "no_text":"",
#         "other": {},
#         "other_text": "",
#         "round": [3],
#         "loop": [],
#         "probability": 1,
#         "condition": {},
#         "condition_loop": {},
#         "condition_value": {}
#     },
#     "event_any_3_C": {
#         "event_text": "今天的早饭是……龙叔昨晚的剩饭！",
#         "event_image": "米饭",
#         "yes": {
#             "Health_Value": 2
#         },
#         "yes_text": "",
#         "no": {
#             "Health_Value": -2
#         },
#         "no_text":"",
#         "other": {},
#         "other_text": "",
#         "round": [3],
#         "loop": [],
#         "probability": 1,
#         "condition": {},
#         "condition_loop": {},
#         "condition_value": {}
#     },
#     "event_any_3_D": {
#         "event_text": "今天的早饭是……菖蒲亲手制作的丰盛早饭！",
#         "event_image": "米饭",
#         "yes": {
#             "Health_Value": 4
#         },
#         "yes_text": "",
#         "no": {
#             "Health_Value": -2
#         },
#         "no_text":"",
#         "other": {},
#         "other_text": "",
#         "round": [3],
#         "loop": [],
#         "probability": 1,
#         "condition": {},
#         "condition_loop": {},
#         "condition_value": {}
#     },
# }
'''

class_reigns_event_dict : dict = {
    "_init_value": {
        "Health_Value": 50,
        "Force_Value": 50,
        "Wisdom_Value": 50,
        "Money_Value": 50,
        "Network_Value": 50,
        "Round_Value": 0,
        "Round_Max_Value": 24,
        "Loop_Value": 0,
        "Loop_Max_Value": 7
    },
    "event_any_00_A": {
        "event_text": "新的一天到来了！",
        "event_image": "床",
        "event_note": "",
        "yes": {},
        "yes_text": "",
        "no": {},
        "no_text": "",
        "other": {
            "special_event": [
                "pass"
            ]
        },
        "other_text": "",
        "round": [
            0
        ],
        "loop": [],
        "probability": 1,
        "condition": {},
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_01_A": {
        "event_text": "新的一天，从起床开始？",
        "event_image": "床",
        "event_note": "",
        "yes": {
            "Health_Value": 2,
            "special_event": [
                "loop_ignore"
            ]
        },
        "yes_text": "",
        "no": {
            "Health_Value": -2,
            "special_event": [
                "restart_round",
                "loop_ignore"
            ]
        },
        "no_text": "",
        "other": {},
        "other_text": "",
        "round": [
            1
        ],
        "loop": [],
        "probability": 1,
        "condition": {},
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_01_B": {
        "event_text": "嗯……今天还有很多事情要做，确定不起床吗？",
        "event_image": "床",
        "event_note": "",
        "yes": {
            "Health_Value": 2
        },
        "yes_text": "",
        "no": {
            "Health_Value": -2,
            "special_event": [
                "RRTA"
            ]
        },
        "no_text": "",
        "other": {},
        "other_text": "",
        "round": [
            1
        ],
        "loop": [],
        "probability": 1,
        "condition": {
            "event_any_01_A": [
                "no"
            ]
        },
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_02_A": {
        "event_text": "非常好！让我们下床去做点其他事情吧！",
        "event_image": "床",
        "event_note": "",
        "yes": {},
        "yes_text": "",
        "no": {},
        "no_text": "",
        "other": {
            "special_event": [
                "pass"
            ]
        },
        "other_text": "下床",
        "round": [
            2
        ],
        "loop": [],
        "probability": 100,
        "condition": {},
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_03_A#1": {
        "event_text": "今天的早饭是……烈烈的秘制炒饭！",
        "event_image": "米饭",
        "event_note": "yes会增加5点健康",
        "yes": {
            "Health_Value": 5
        },
        "yes_text": "",
        "no": {
            "Health_Value": -5
        },
        "no_text": "",
        "other": {},
        "other_text": "",
        "round": [
            3
        ],
        "loop": [],
        "probability": 1,
        "condition": {},
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_03_A#2": {
        "event_text": "今天的早饭是……烈烈的秘制炒饭！",
        "event_image": "米饭",
        "event_note": "会减少6点健康值",
        "yes": {
            "Health_Value": -6
        },
        "yes_text": "",
        "no": {
            "Health_Value": -5
        },
        "no_text": "",
        "other": {},
        "other_text": "",
        "round": [
            3
        ],
        "loop": [],
        "probability": 1,
        "condition": {},
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_03_B#1": {
        "event_text": "今天的早饭是……龙叔昨晚的剩饭！",
        "event_image": "米饭",
        "event_note": "选择yes会增加8点健康值",
        "yes": {
            "Health_Value": 6
        },
        "yes_text": "",
        "no": {
            "Health_Value": -5
        },
        "no_text": "",
        "other": {},
        "other_text": "",
        "round": [
            3
        ],
        "loop": [],
        "probability": 1,
        "condition": {},
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_03_B#2": {
        "event_text": "今天的早饭是……龙叔昨晚的剩饭！",
        "event_image": "米饭",
        "event_note": "选择yes会减少6点健康值",
        "yes": {
            "Health_Value": -6
        },
        "yes_text": "",
        "no": {
            "Health_Value": -5
        },
        "no_text": "",
        "other": {},
        "other_text": "",
        "round": [
            3
        ],
        "loop": [],
        "probability": 1,
        "condition": {},
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_03_C": {
        "event_text": "今天的早饭是……菖蒲亲手制作的丰盛早饭！",
        "event_image": "米饭",
        "event_note": "",
        "yes": {
            "Health_Value": 10
        },
        "yes_text": "",
        "no": {
            "Health_Value": -5
        },
        "no_text": "",
        "other": {},
        "other_text": "",
        "round": [
            3
        ],
        "loop": [],
        "probability": 1,
        "condition": {},
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_04_A": {
        "event_text": "作为renpy制作人的你对新的一天充满了决心！",
        "event_image": "肌肉",
        "event_note": "",
        "yes": {
            "Wisdom_Value": 10
        },
        "yes_text": "我一定要把游戏做出来！",
        "no": {
            "Wisdom_Value": 6
        },
        "no_text": "做六十分足够了~",
        "other": {
            "special_event": [
                "restart_round",
                "game_over"
            ]
        },
        "other_text": "还是放弃吧……",
        "round": [
            4
        ],
        "loop": [],
        "probability": 1,
        "condition": {},
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_04_se": {
        "event_text": "好像吃坏肚子了……",
        "event_image": "米饭",
        "event_note": "",
        "yes": {},
        "yes_text": "",
        "no": {},
        "no_text": "",
        "other": {
            "special_event": [
                "pass",
                "restart_round",
                "loop_ignore"
            ]
        },
        "other_text": "",
        "round": [
            4
        ],
        "loop": [],
        "probability": 100,
        "condition": {
            "event_any_03_A#2": [
                "yes"
            ],
            "event_any_03_B#2": [
                "yes"
            ]
        },
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_05_A": {
        "event_text": "今天打算出门玩吗？",
        "event_image": " 门",
        "event_note": "选择yes会额外度过3回合，增加7点健康减少3点金钱",
        "yes": {
            "Health_Value": 7,
            "Money_Value": -3,
            "Round_Value": 2
        },
        "yes_text": "",
        "no": {
            "Wisdom_Value": 6
        },
        "no_text": "",
        "other": {},
        "other_text": "",
        "round": [
            5
        ],
        "loop": [],
        "probability": 1,
        "condition": {},
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_05_B": {
        "event_text": "出门打工吗？",
        "event_image": " 门",
        "event_note": "选择yes额外度过3回合，增加5点金钱减少5点健康",
        "yes": {
            "Health_Value": -5,
            "Money_Value": 5,
            "Round_Value": 3
        },
        "yes_text": "",
        "no": {
            "Wisdom_Value": 6
        },
        "no_text": "",
        "other": {},
        "other_text": "",
        "round": [
            5
        ],
        "loop": [],
        "probability": 1,
        "condition": {},
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_05_C": {
        "event_text": "出门锻炼吗？",
        "event_image": " 门",
        "event_note": "选择yes会额外度过3回合，增加10点健康",
        "yes": {
            "Health_Value": 10,
            "Round_Value": 3
        },
        "yes_text": "",
        "no": {
            "Wisdom_Value": 6
        },
        "no_text": "",
        "other": {},
        "other_text": "",
        "round": [
            5
        ],
        "loop": [],
        "probability": 1,
        "condition": {},
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_06_A#1": {
        "event_text": "打开电脑， 准备面对自己的史山代码",
        "event_image": " 电脑",
        "event_note": "",
        "yes": {
            "Health_Value": -5,
            "Wisdom_Value": 5,
            "special_event": [
                "loop_ignore"
            ]
        },
        "yes_text": "",
        "no": {
            "Wisdom_Value": -5,
            "Health_Value": 5,
            "special_event": [
                "loop_ignore"
            ]
        },
        "no_text": "",
        "other": {},
        "other_text": "",
        "round": {
            "min": 6,
            "max": 11
        },
        "loop": [],
        "probability": 15,
        "condition": {
            "event_any_05_A": [
                "no"
            ],
            "event_any_05_B": [
                "no"
            ],
            "event_any_05_C": [
                "no"
            ]
        },
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_06_A#2": {
        "event_text": "回到家，打开电脑， 准备面对自己的史山代码",
        "event_image": " 电脑",
        "event_note": "",
        "yes": {
            "Health_Value": -5,
            "Wisdom_Value": 5,
            "special_event": [
                "loop_ignore"
            ]
        },
        "yes_text": "",
        "no": {
            "Wisdom_Value": -5,
            "Health_Value": 5,
            "special_event": [
                "loop_ignore"
            ]
        },
        "no_text": "",
        "other": {},
        "other_text": "",
        "round": {
            "min": 6,
            "max": 11
        },
        "loop": [],
        "probability": 100,
        "condition": {
            "event_any_05_B": [
                "yes"
            ],
            "event_any_05_A": [
                "yes"
            ],
            "event_any_05_C": [
                "yes"
            ]
        },
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_06_B": {
        "event_text": "打会游戏",
        "event_image": " 游戏",
        "event_note": "",
        "yes": {
            "Wisdom_Value": 3,
            "Health_Value": -5,
            "Network_Value": 2
        },
        "yes_text": "",
        "no": {
            "Health_Value": 5
        },
        "no_text": "",
        "other": {},
        "other_text": "",
        "round": {
            "min": 6,
            "max": 11
        },
        "loop": [],
        "probability": 5,
        "condition": {},
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_06_D": {
        "event_text": "听会音乐",
        "event_image": "音乐",
        "event_note": "",
        "yes": {
            "Health_Value": 5
        },
        "yes_text": "",
        "no": {
            "special_event": [
                "pass"
            ]
        },
        "no_text": "",
        "other": {},
        "other_text": "",
        "round": {
            "min": 6,
            "max": 11
        },
        "loop": [],
        "probability": 5,
        "condition": {},
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_06_E": {
        "event_text": "和群友们聊天",
        "event_image": " 聊天",
        "event_note": "",
        "yes": {
            "Network_Value": 6
        },
        "yes_text": "",
        "no": {
            "special_event": [
                "pass"
            ],
            "Network_Value": -3
        },
        "no_text": "",
        "other": {},
        "other_text": "",
        "round": {
            "min": 6,
            "max": 11
        },
        "loop": [],
        "probability": 5,
        "condition": {},
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_06_F": {
        "event_text": "在游戏平台上买新游戏",
        "event_image": " 电脑",
        "event_note": "",
        "yes": {
            "Money_Value": -8,
            "Health_Value": 5,
            "special_event": [
                "loop_ignore"
            ]
        },
        "yes_text": "",
        "no": {
            "special_event": [
                "loop_ignore"
            ]
        },
        "no_text": "",
        "other": {},
        "other_text": "",
        "round": {
            "min": 6,
            "max": 11
        },
        "loop": [],
        "probability": 5,
        "condition": {},
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_06_G": {
        "event_text": "吃点零食",
        "event_image": " 零食",
        "event_note": "",
        "yes": {
            "Health_Value": 5
        },
        "yes_text": "",
        "no": {
            "Health_Value": -2
        },
        "no_text": "",
        "other": {},
        "other_text": "",
        "round": {
            "min": 6,
            "max": 11
        },
        "loop": [],
        "probability": 5,
        "condition": {},
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_06_H": {
        "event_text": "写会代码",
        "event_image": " 电脑",
        "event_note": "",
        "yes": {
            "Wisdom_Value": 5,
            "Health_Value": -5
        },
        "yes_text": "",
        "no": {
            "Health_Value": 2
        },
        "no_text": "",
        "other": {},
        "other_text": "",
        "round": {
            "min": 6,
            "max": 11
        },
        "loop": [],
        "probability": 15,
        "condition": {
            "event_any_06_A#1": [
                "yes"
            ],
            "event_any_06_A#2": [
                "yes"
            ]
        },
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_07_A": {
        "event_text": "今天的午饭是……肯德基？",
        "event_image": " 米饭",
        "event_note": "",
        "yes": {
            "Health_Value": 15,
            "Money_Value": -10
        },
        "yes_text": "",
        "no": {
            "Health_Value": -8
        },
        "no_text": "",
        "other": {},
        "other_text": "",
        "round": [
            12
        ],
        "loop": [],
        "probability": 1,
        "condition": {},
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_07_B#1": {
        "event_text": "今天的午饭是……拼好饭？",
        "event_image": " 米饭",
        "event_note": "增加5健康",
        "yes": {
            "Health_Value": 5,
            "Money_Value": -5
        },
        "yes_text": "",
        "no": {
            "Health_Value": -8
        },
        "no_text": "",
        "other": {},
        "other_text": "",
        "round": [
            12
        ],
        "loop": [],
        "probability": 1,
        "condition": {},
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_07_B#2": {
        "event_text": "今天的午饭是……拼好饭？",
        "event_image": " 米饭",
        "event_note": "减少10健康",
        "yes": {
            "Health_Value": -10,
            "Money_Value": -5
        },
        "yes_text": "",
        "no": {
            "Health_Value": -8
        },
        "no_text": "",
        "other": {},
        "other_text": "",
        "round": [
            12
        ],
        "loop": [],
        "probability": 1,
        "condition": {},
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_07_C": {
        "event_text": "今天的午饭是……阳光青提？",
        "event_image": " 米饭",
        "event_note": "",
        "yes": {
            "Health_Value": -2
        },
        "yes_text": "",
        "no": {
            "Health_Value": -8
        },
        "no_text": "",
        "other": {
            "special_event": [
                "loop_ignore",
                "restart_round"
            ]
        },
        "other_text": "还是吃点别的吧……",
        "round": [
            12
        ],
        "loop": [],
        "probability": 1,
        "condition": {},
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_08_A": {
        "event_text": "今天打算出门玩吗？",
        "event_image": " 门",
        "event_note": "选择yes会额外度过3回合，增加7点健康减少3点金钱",
        "yes": {
            "Health_Value": 7,
            "Money_Value": -3,
            "Round_Value": 2
        },
        "yes_text": "",
        "no": {
            "Wisdom_Value": 6
        },
        "no_text": "",
        "other": {},
        "other_text": "",
        "round": [
            13
        ],
        "loop": [],
        "probability": 1,
        "condition": {},
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_08_B": {
        "event_text": "出门打工吗？",
        "event_image": " 门",
        "event_note": "选择yes额外度过3回合，增加5点金钱减少5点健康",
        "yes": {
            "Health_Value": -5,
            "Money_Value": 5,
            "Round_Value": 3
        },
        "yes_text": "",
        "no": {
            "Wisdom_Value": 6
        },
        "no_text": "",
        "other": {},
        "other_text": "",
        "round": [
            13
        ],
        "loop": [],
        "probability": 1,
        "condition": {},
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_08_C": {
        "event_text": "出门锻炼吗？",
        "event_image": " 门",
        "event_note": "选择yes会额外度过3回合，增加10点健康",
        "yes": {
            "Health_Value": 10,
            "Round_Value": 3
        },
        "yes_text": "",
        "no": {
            "Wisdom_Value": 6
        },
        "no_text": "",
        "other": {},
        "other_text": "",
        "round": [
            13
        ],
        "loop": [],
        "probability": 1,
        "condition": {},
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_08_se": {
        "event_text": "好像吃坏肚子了……",
        "event_image": "米饭",
        "event_note": "",
        "yes": {},
        "yes_text": "",
        "no": {},
        "no_text": "",
        "other": {
            "special_event": [
                "pass",
                "restart_round",
                "loop_ignore"
            ]
        },
        "other_text": "",
        "round": [
            13
        ],
        "loop": [],
        "probability": 100,
        "condition": {
            "event_any_07_B#2": [
                "yes"
            ],
            "event_any_07_C": [
                "yes"
            ]
        },
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_09_A#1": {
        "event_text": "打开电脑， 准备面对自己的史山代码",
        "event_image": " 电脑",
        "event_note": "",
        "yes": {
            "Health_Value": -5,
            "Wisdom_Value": 5,
            "special_event": [
                "loop_ignore"
            ]
        },
        "yes_text": "",
        "no": {
            "Wisdom_Value": -5,
            "Health_Value": 5,
            "special_event": [
                "loop_ignore"
            ]
        },
        "no_text": "",
        "other": {},
        "other_text": "",
        "round": {
            "min": 14,
            "max": 21
        },
        "loop": [],
        "probability": 15,
        "condition": {
            "event_any_08_A": [
                "no"
            ],
            "event_any_08_B": [
                "no"
            ],
            "event_any_08_C": [
                "no"
            ]
        },
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_09_A#2": {
        "event_text": "回到家，打开电脑， 准备面对自己的史山代码",
        "event_image": " 电脑",
        "event_note": "",
        "yes": {
            "Health_Value": -5,
            "Wisdom_Value": 5,
            "special_event": [
                "loop_ignore"
            ]
        },
        "yes_text": "",
        "no": {
            "Wisdom_Value": -5,
            "Health_Value": 5,
            "special_event": [
                "loop_ignore"
            ]
        },
        "no_text": "",
        "other": {},
        "other_text": "",
        "round": {
            "min": 14,
            "max": 21
        },
        "loop": [],
        "probability": 100,
        "condition": {
            "event_any_05_B": [
                "yes"
            ],
            "event_any_05_A": [
                "yes"
            ],
            "event_any_05_C": [
                "yes"
            ]
        },
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_09_B": {
        "event_text": "打会游戏",
        "event_image": " 游戏",
        "event_note": "",
        "yes": {
            "Wisdom_Value": 3,
            "Health_Value": -5,
            "Network_Value": 2
        },
        "yes_text": "",
        "no": {
            "Health_Value": 5
        },
        "no_text": "",
        "other": {},
        "other_text": "",
        "round": {
            "min": 14,
            "max": 21
        },
        "loop": [],
        "probability": 5,
        "condition": {},
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_09_D": {
        "event_text": "听会音乐",
        "event_image": "音乐",
        "event_note": "",
        "yes": {
            "Health_Value": 5
        },
        "yes_text": "",
        "no": {
            "special_event": [
                "pass"
            ]
        },
        "no_text": "",
        "other": {},
        "other_text": "",
        "round": {
            "min": 14,
            "max": 21
        },
        "loop": [],
        "probability": 5,
        "condition": {},
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_09_E": {
        "event_text": "和群友们聊天",
        "event_image": " 聊天",
        "event_note": "",
        "yes": {
            "Network_Value": 6
        },
        "yes_text": "",
        "no": {
            "special_event": [
                "pass"
            ],
            "Network_Value": -3
        },
        "no_text": "",
        "other": {},
        "other_text": "",
        "round": {
            "min": 14,
            "max": 21
        },
        "loop": [],
        "probability": 5,
        "condition": {},
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_09_F": {
        "event_text": "在游戏平台上买新游戏",
        "event_image": " 电脑",
        "event_note": "",
        "yes": {
            "Money_Value": -8,
            "Health_Value": 5,
            "special_event": [
                "loop_ignore"
            ]
        },
        "yes_text": "",
        "no": {
            "special_event": [
                "loop_ignore"
            ]
        },
        "no_text": "",
        "other": {},
        "other_text": "",
        "round": {
            "min": 14,
            "max": 21
        },
        "loop": [],
        "probability": 5,
        "condition": {},
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_09_G": {
        "event_text": "吃点零食",
        "event_image": " 零食",
        "event_note": "",
        "yes": {
            "Health_Value": 5
        },
        "yes_text": "",
        "no": {
            "Health_Value": -2
        },
        "no_text": "",
        "other": {},
        "other_text": "",
        "round": {
            "min": 14,
            "max": 21
        },
        "loop": [],
        "probability": 5,
        "condition": {},
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_09_H": {
        "event_text": "写会代码",
        "event_image": " 电脑",
        "event_note": "",
        "yes": {
            "Health_Value": -5,
            "Wisdom_Value": 5
        },
        "yes_text": "",
        "no": {
            "Health_Value": 5
        },
        "no_text": "",
        "other": {},
        "other_text": "",
        "round": {
            "min": 14,
            "max": 21
        },
        "loop": [],
        "probability": 15,
        "condition": {},
        "condition_loop": {
            "event_any_09_A#1": [
                "yes"
            ],
            "event_any_09_A#2": [
                "yes"
            ]
        },
        "condition_value": {}
    },
    "event_any_10_A": {
        "event_text": "今天的晚饭是……肯德基？",
        "event_image": " 米饭",
        "event_note": "",
        "yes": {
            "Health_Value": 15,
            "Money_Value": -10
        },
        "yes_text": "",
        "no": {
            "Health_Value": -5
        },
        "no_text": "",
        "other": {},
        "other_text": "",
        "round": [
            21
        ],
        "loop": [],
        "probability": 1,
        "condition": {},
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_10_B#1": {
        "event_text": "今天的晚饭是……拼好饭？",
        "event_image": " 米饭",
        "event_note": "增加5健康",
        "yes": {
            "Health_Value": 5,
            "Money_Value": -5
        },
        "yes_text": "",
        "no": {
            "Health_Value": -5
        },
        "no_text": "",
        "other": {},
        "other_text": "",
        "round": [
            21
        ],
        "loop": [],
        "probability": 1,
        "condition": {},
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_10_B#2": {
        "event_text": "今天的晚饭是……拼好饭？",
        "event_image": " 米饭",
        "event_note": "减少10健康",
        "yes": {
            "Health_Value": -10,
            "Money_Value": -5
        },
        "yes_text": "",
        "no": {
            "Health_Value": -5
        },
        "no_text": "",
        "other": {},
        "other_text": "",
        "round": [
            21
        ],
        "loop": [],
        "probability": 1,
        "condition": {},
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_10_C": {
        "event_text": "今天的晚饭是……阳光青提？",
        "event_image": " 米饭",
        "event_note": "",
        "yes": {
            "Health_Value": -2
        },
        "yes_text": "",
        "no": {
            "Health_Value": -5
        },
        "no_text": "",
        "other": {
            "special_event": [
                "loop_ignore",
                "restart_round"
            ]
        },
        "other_text": "还是吃点别的吧……",
        "round": [
            21
        ],
        "loop": [],
        "probability": 1,
        "condition": {},
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_11_A": {
        "event_text": "洗漱一下",
        "event_image": " 洗澡",
        "event_note": "",
        "yes": {
            "Health_Value": 5
        },
        "yes_text": "",
        "no": {
            "Health_Value": -5
        },
        "no_text": "",
        "other": {},
        "other_text": "",
        "round": [
            22
        ],
        "loop": [],
        "probability": 1,
        "condition": {},
        "condition_loop": {},
        "condition_value": {}
    },
    "event_any_12_A": {
        "event_text": "上床睡觉……等待明天的到来……",
        "event_image": " 床",
        "event_note": "",
        "yes": {},
        "yes_text": "",
        "no": {},
        "no_text": "",
        "other": {
            "special_event": [
                "pass"
            ]
        },
        "other_text": "",
        "round": [
            23
        ],
        "loop": [],
        "probability": 1,
        "condition": {},
        "condition_loop": {},
        "condition_value": {}
    }
}