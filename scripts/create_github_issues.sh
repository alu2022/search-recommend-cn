#!/usr/bin/env bash
# Create the 8 tutorial GitHub issues. Requires: gh auth login
set -euo pipefail

if ! command -v gh >/dev/null 2>&1; then
  echo "需要 GitHub CLI (gh)。安装: https://cli.github.com/" >&2
  exit 1
fi

create_issue() {
  local title="$1"
  local body="$2"
  gh issue create --title "$title" --label enhancement --body "$body"
}

create_issue "步骤 0: 仓库脚手架与环境准备" "$(cat <<'EOF'
## 目标
把仓库初始化成可编译、可运行脚本的骨架。

## 验收
- [ ] `requirements.txt`、`.gitignore`、`cpp/CMakeLists.txt` 就位
- [ ] `python scripts/check_env.py` 通过
- [ ] README 写清目录结构和常用命令

## 参考
仓库 README「步骤 0 — 准备仓库与目录」
EOF
)"

create_issue "步骤 1: 中文语料准备与预处理" "$(cat <<'EOF'
## 目标
准备中文语料，完成分词和去停用词，输出空格分隔的清洗文本。

## 验收
- [ ] `data/corpus.txt` 每行一篇文档
- [ ] `python scripts/preprocess.py --input data/corpus.txt --output data/corpus_cleaned.txt`
- [ ] 支持停用词表和 jieba 自定义词典
- [ ] `python -m unittest tests.test_preprocess` 通过

## 参考
jieba README；仓库 README「步骤 1 — 语料准备与预处理」
EOF
)"

create_issue "步骤 2: C++ 倒排索引" "$(cat <<'EOF'
## 目标
实现 term → postings 的内存倒排，并支持存盘 / 加载。

## 验收
- [ ] 读取 `data/corpus_cleaned.txt`
- [ ] 记录 df、tf、文档长度、总文档数
- [ ] 文本格式序列化（后续可换二进制）
- [ ] 小样本单元测试

## 建议命令
```
cmake -S cpp -B build && cmake --build build
./build/indexer data/corpus_cleaned.txt data/index.txt
```
EOF
)"

create_issue "步骤 3: TF-IDF 检索基线" "$(cat <<'EOF'
## 目标
先用 TF-IDF 打出 top-k，作为后续 BM25 的对照基线。

## 验收
- [ ] 加载倒排索引
- [ ] 查询分词后计算 TF-IDF 分数
- [ ] 返回 docID、score、snippet
- [ ] 小查询集可复现排序结果
EOF
)"

create_issue "步骤 4: BM25 排序与布尔查询" "$(cat <<'EOF'
## 目标
用 BM25 替换 TF-IDF，并支持简单 AND/OR。

## 验收
- [ ] 实现 BM25（可调 k1、b）
- [ ] 支持布尔过滤 + BM25 排序
- [ ] 与 TF-IDF 对比同一 query 的 top-k
- [ ] README 写清公式和参数含义（面试要点）
EOF
)"

create_issue "步骤 5: Python 与 C++ 集成 + 评测" "$(cat <<'EOF'
## 目标
用 subprocess（或 pybind11）调用 C++ searcher，计算 Precision@K、NDCG@K。

## 验收
- [ ] CLI 或 Python API 能批量查询
- [ ] `scripts/eval.py` 读取 results / qrels
- [ ] 输出 Precision@K、NDCG@K
EOF
)"

create_issue "步骤 6: Streamlit 交互 Demo" "$(cat <<'EOF'
## 目标
提供一个可演示的搜索页面。

## 验收
- [ ] 输入 query、选择 top-k
- [ ] 展示 docID、score、snippet
- [ ] 可选：记录点击日志
- [ ] `streamlit run demo/streamlit_demo.py` 可启动
EOF
)"

create_issue "步骤 7: 性能测试与面试文档" "$(cat <<'EOF'
## 目标
补齐性能数字和面试讲解材料。

## 验收
- [ ] 记录索引耗时、索引大小、查询平均延迟 / P95
- [ ] `docs/design.md`：倒排结构、BM25、trade-off
- [ ] README 更新演示步骤与结果
EOF
)"

echo "已创建 8 个 GitHub Issue。"
