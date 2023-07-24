# SWYAutoScript
ShiWuYuAutoScript（SAS）食物语自动脚本

# 计划接入[MaaFramework](https://github.com/MaaAssistantArknights/MaaFramework)
如果您有编程经验，欢迎提交pr来帮助本项目接入[MaaFramework](https://github.com/MaaAssistantArknights/MaaFramework)

# Features
- 自动战斗（拒绝手刷绀珠）:支持选择技能释放目标
- 技能表生成
- 自动探索
- 自动客潮

# 注意事项
- 模拟器：腾讯手游助手（其他模拟器需要配置adb） 分辨率`2560x1440`
- 请确定已安装```Python```，```adb```等依赖文件
- 首次运行前请先在打开模拟器的情况下运行```setup.py```来为模拟器安装```minicap```和```minitouch```
- 自动战斗（```autoFight.py```）使用时需要进入战斗场景再开启脚本
- 自动战斗的运作基于```skill_click.json```（技能选择目标）和```skill_number_sequences.json```（技能释放顺序），在```skillTables/```目录下有几份内置的作业，使用时需要将作业覆盖到主目录，再启动```autoFight.py```
- 自动探索（```autoExplore.py```）需要在主界面使用
- 自动客潮（```autoKeChao.py```）需要在客潮界面使用（在客潮结束后可能需要手动关闭程序来停止，且停止后可能需要等待剩余的触控事件完成）

---

# To do
- ~~模板识别（cv2）~~
- ~~更换模拟点击方案（minitouch/maatouch?）~~
- 奖励识别（存疑，没有昨夜圆车的企鹅物流那种数据站的话奖励识别真的有用吗，感觉在这游戏剩余的寿命也不会有人做）
- 自动探索
- 自动寻踪
- 自动送礼+点好感度
- 自动任务（感觉很难，识别没满级的卡和膳具什么的）
- 刷在线时长自动领奖励
- 自动连战
- 优化自动客潮（目前是遍历所有需求点，优化为只点击出现的需求点）
