import json

skill_number_sequences = []
round_count = 1

while True:
    print(f"Round: {round_count}")
    user_input = input("输入本轮的技能顺序（例如：3112），或输入 'END' 结束输入: ")
    if user_input == "END":
        break

    numbers = [int(num) for num in user_input]
    skill_number_sequences.append(numbers)
    
    round_count += 1
# 保存为 JSON 文件
with open('skill_number_sequences.json', 'w') as f:
    json.dump(skill_number_sequences, f)

print("skill_number_sequences =", skill_number_sequences)
#3111 2133 1111 1111 1311 3113 2131 1111 1111 1313 3111 2131 1111 1113 1311 3111 2131 1113 1111 1311 3111 2133 1111 1111