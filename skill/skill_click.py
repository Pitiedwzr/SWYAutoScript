import json
skill_click = []
round_click = []
round_count = 1
char_count = 1
    
while True:
    print(f"Round: {round_count} | Character: {char_count}")
    user_input = input("请输入额外点击点的 x 坐标和 y 坐标（以空格分隔），或输入 'END' 结束输入：")
        
    if user_input == "END":
        break
        
    try:
        x, y = map(int, user_input.split())
        round_click.append((x, y))
    except ValueError:
        print("Invalid input. Please try again.")
        continue
        
    if len(round_click) == 4:
        skill_click.append(round_click)
        round_click = []

    char_count += 1
    if char_count > 4:
        char_count = 1
        round_count += 1
    
# 保存到 JSON 文件
with open('skill_click.json', 'w') as f:
    json.dump(skill_click, f)
