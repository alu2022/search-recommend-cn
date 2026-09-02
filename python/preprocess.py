import sys
import repo.jieba.jieba as jieba

def main():
    # 检查参数是否正确
    if len(sys.argv) != 3:
        print("用法：python3 jieba_cut.py 输入语料路径 输出分词路径")
        print("示例：python3 jieba_cut.py input.txt output.txt")
        return

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        result = []
        for line in lines:
            line = line.strip()
            if not line:
                result.append("")
                continue

            # jieba 分词（默认精确模式，最常用）
            words = jieba.cut(line)
            result.append(" ".join(words))

        # 写入分词结果
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(result))

        print(f"✅ 分词完成！已保存到：{output_path}")

    except Exception as e:
        print(f"❌ 出错：{e}")

if __name__ == "__main__":
    main()