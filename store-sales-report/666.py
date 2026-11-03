import csv
import json
import os

# 1. 定义文件路径 (注意：检查你的 csv 文件名到底是 sales.csv 还是 sales_data.csv)
csv_file = "../sales.csv"
report_file = "report.txt"
json_file = "summary.json"

# 检查文件是否存在
if not os.path.exists(csv_file):
    print(f"错误：找不到 {csv_file} 文件，请检查文件名！")
    exit()  # 这里改成了 exit()，因为没在函数里不能用 return

# 2. 读取 CSV 并计算
store_sales = {}
total_sales = 0.0

with open(csv_file, mode="r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        store = row["门店名称"]
        amount = float(row["销售金额"])

        # 累加每家门店的销售额
        store_sales[store] = store_sales.get(store, 0.0) + amount
        # 累加总销售额
        total_sales += amount

# 3. 生成 summary.json (核心：必须先写入，才能读取)
summary_data = {
    "stores": store_sales,
    "total": total_sales
}
with open(json_file, mode="w", encoding="utf-8") as f:
    json.dump(summary_data, f, ensure_ascii=False, indent=4)

# 4. 用 json.load() 重新读取并核对
with open(json_file, mode="r", encoding="utf-8") as f:  # 注意这里必须是 "r" 读取模式
    reloaded_data = json.load(f)

reloaded_stores = reloaded_data["stores"]
reloaded_total = reloaded_data["total"]

# 重新计算门店小计之和
calculated_sum = sum(reloaded_stores.values())

print("\n--- 数据核对 ---")
print(f"JSON中门店小计之和: ￥{calculated_sum:.2f}")
print(f"JSON中记录的总额: ￥{reloaded_total:.2f}")

if abs(calculated_sum - reloaded_total) < 0.001:
    print("✅ 校验通过：门店小计之和等于总额。")
else:
    print("❌ 校验失败：数据存在差异！")

# 5. 生成 report.txt
with open(report_file, mode="w", encoding="utf-8") as f:
    f.write("====== 门店销售日报 ======\n")
    for store, sales in store_sales.items():
        f.write(f"门店：{store} | 小计：￥{sales:.2f}\n")
    f.write("------------------------\n")
    f.write(f"总计销售额：￥{total_sales:.2f}\n")

print(f"\n✅ 已生成 {report_file} 和 {json_file}")

# Python 编译缓存
__pycache__/
*.py[cod]
*$py.class

# 虚拟环境
venv/
env/
.env

# 编辑器配置
.vscode/
.idea/
.DS_Store

# 注意：这里没有忽略 .csv / .txt / .json，因为它们是需要提交的项目产物
# 但如果你有真实的顾客隐私数据，请在这里把真实数据文件屏蔽掉！