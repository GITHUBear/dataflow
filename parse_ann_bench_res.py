import re

# 设置文件路径
input_file = 'data.txt'  # 输入文件名
output_file = 'hnsw_faiss.txt'  # 输出文件名

# 使用正则表达式提取 x 和 y 的值
pattern = r'\{ x:\s*(-?\d+\.?\d*)\s*,\s*y:\s*(-?\d+\.?\d*)'

# 用于存储结果
results = []

# 读取数据文件
with open(input_file, 'r') as f:
    for line in f:
        match = re.search(pattern, line)
        if match:
            x_value = match.group(1)
            y_value = match.group(2)
            results.append((x_value, y_value))

# # 输出结果到控制台或保存到文件
with open(output_file, 'w') as f:
    for x, y in results:
        f.write(f'{x} {y}\n')
