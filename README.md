# Lie Ling Feng's Open Source Renpy Mini-Games Project
- 项目名称：LLFs-OSRMGP
- 项目简介：这是属于烈林凤的的开源renpy迷你游戏项目！
- 项目作者：烈林凤

在这里，我会将我所开发的renpy迷你游戏项目分享给大家，这一部分均为开源项目，均为原创，*不使用pygame以及任何第三方库*，仅使用renpy原生功能实现，注释详细，代码易懂，就算是仅知道renpy语法的人也能看懂。

> 包含了所有小游戏中最基础的核心内容（基础内容），遵循MIT协议，**严禁售卖该项目代码**！你可以随意将其修改并用于任何非商业用途，但请注明出处！→[GitHub项目地址](https://github.com/llfseik/LLFs-OSRMGP)

> 若需要内嵌到**付费项目**当中，请与我联系，得到授权后才可使用！

> 还有部分非开源内容（高级内容），是在原本游戏基础内容上的扩展，你可以前往我的*爱发电*主页上购买使用！购买后你可以获得完整代码源文件和游戏素材，每月都会更新，**严禁进行二次售卖**！你可以随意将其用于任何类型的项目中，可以注明出处！→[b站主页](https://space.bilibili.com/378904108?spm_id_from=333.1007.0.0)
> 
> 我的b站账号：[烈林凤](https://space.bilibili.com/378904108?spm_id_from=333.1007.0.0)
> 
> 我的爱发电账号：[烈林凤](https://afdian.com/a/lielinfeng)

## 目前的计划
> 开源迷你游戏（随缘更新）
- [x] 扫雷游戏
- [x] 五子棋游戏
- [x] 类王权游戏
- [x] 猜盅游戏
- [ ] 围棋游戏
- [ ] 俄罗斯方块游戏
- [ ] 贪吃蛇游戏
- [ ] 塔防游戏
- [ ] 种田/模拟经营类游戏
- [ ] 吃豆人
- [ ] “flappy bird”类游戏
> 开源迷你游戏扩展模块（同步进行中）
- [ ] 成就系统
- [ ] 排行榜系统
> 仅部分开源迷你游戏扩展模块（遥遥无期）
- [ ] 局域网联机功能


## 项目介绍

### [扫雷游戏](https://github.com/llfseik/LLFs-OSRMGP/blob/main/LLFs%20OSRMGP/minesweeper.rpy)

> 该项目基础内容
  - 点击方格后显示数字，数字越大，雷越多，若没有雷则不显示，且打开所有相邻没有雷的方格。
  - 按q键并左击方格，标记为旗帜，再次q键并左击方格，取消标记。
  - 若点击到雷，游戏结束，并在屏幕中央显示重新开游戏
  - 棋盘最下方显示emoji表情，表示游戏状态，如游戏开始、游戏结束、游戏胜利等。

> 该项目高级内容
  - 可以使用滚轮缩放棋盘大小，鼠标拖动边缘移动棋盘视角。
  - 可以分别使用q键和w键分别标注旗帜和问号两种标志。
  - 屏幕左侧显示快捷菜单，可以点击后快速标记或清除标记、重新开始游戏、重置缩放
  - 屏幕左侧显示计分板，显示剩余格子数、雷数、分数、游戏时间等信息。
  - 在代码中添加了部分成就彩蛋，之后大概率会加入自制的成就系统。
> 该项目教程链接
  - [renpy中文论坛-扫雷迷你游戏代码讲解/教程【LLFs-OSRMGP内容扩展-1】](https://www.renpy.cn/forum.php?mod=viewthread&tid=1593)
> 项目预览（上：基础内容，下：高级内容）
<center>

![扫雷_基础](https://github.com/llfseik/LLFs-OSRMGP/blob/main/legend/minesweeper_1.jpg "扫雷_基础")
![扫雷_高级](https://github.com/llfseik/LLFs-OSRMGP/blob/main/legend/minesweeper_2.jpg "扫雷_高级")
</center>

### [五子棋游戏](https://github.com/llfseik/LLFs-OSRMGP/blob/main/LLFs%20OSRMGP/gobang.rpy)
> 注意：本项目为双人游戏，且暂未开发联机功能，仅能本地游玩

> 该项目基础内容
  - 白棋先手，点击方格放下棋子，随后更改为黑棋，以此往复。
  - 若有5颗相同颜色的棋子在上下左右以及斜向方向连成5个，则那一方获胜。
  - 游戏结束在屏幕中央显示获胜者与重新开始按钮。

> 该项目高级内容
  - 暂无

> 该项目教程链接
  - [renpy中文论坛-五子棋迷你游戏代码讲解/教程【LLFs-OSRMGP内容扩展-2】](https://www.renpy.cn/forum.php?mod=viewthread&tid=1612&page=1&extra=#pid6006)

> 项目预览
<center>

![五子棋_基础](https://github.com/llfseik/LLFs-OSRMGP/blob/main/legend/gobang_1.png "五子棋_基础")
</center>

### [类王权游戏](https://github.com/llfseik/LLFs-OSRMGP/tree/main/LLFs%20OSRMGP/class_reigns)
> 注意：本迷你游戏已经部分超出了所谓“迷你游戏”的范畴，且代码更加复杂和庞大，某种程度上来说，它更像是一个完整的游戏项目，若要修改使用，请保证能完整理解本项目，以防出现一些无法解决的BUG。

> 该项目基础内容
  - 中间卡牌可左右下滑动，最多可提供三种选项，选项将改变数值和结局走向
  - 游戏结束在屏幕中央显示游戏结果，并提供重新开始和退出按钮
  - 为开发者提供了事件编辑器，可以方便地制作事件

> 该项目高级内容
  - 暂无

> 该项目教程链接
  - 暂无

> 项目预览
<center>
</center>