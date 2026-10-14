# search-recommend-cn
搜广推路线

> 📚 **深度学习推荐系统 6 个月学习计划(国内方向)** 已整理在 [`学习计划/`](./学习计划/README.md) 目录下,按月按周拆解,可直接对照推进。

## 当前进度（步骤 0 + 步骤 1）

仓库脚手架和中文语料预处理已经可用。在项目根目录执行：

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python scripts/check_env.py
python scripts/preprocess.py --input data/corpus.txt --output data/corpus_cleaned.txt
python -m unittest tests.test_preprocess
```

把 8 个后续步骤建成 GitHub Issue（本机需已 `gh auth login`）：

```bash
bash scripts/create_github_issues.sh
```

### 目录结构

```
data/corpus.txt                 # 示例中文语料（每行一篇）
data/stopwords.txt              # 停用词
data/userdict.txt               # jieba 自定义词典（保护「倒排索引」等短语）
scripts/preprocess.py           # 分词 + 去停用词
scripts/check_env.py            # Python / C++ / CMake / jieba 自检
scripts/create_github_issues.sh # 创建 8 个步骤 Issue
cpp/CMakeLists.txt              # C++ 索引器占位，步骤 2 再补 indexer
tests/test_preprocess.py
requirements.txt
```

---

好 — 我把整个项目的“端到端流程 + 所需环境 + 每一步可以参考的开源仓库与要看目录/文件”整理成一份可执行的清单，便于你按之前的两周计划推进。考虑到你每周的可投入时间（工作日每天 1 小时，周末较多），我在每一步给出大致耗时建议和优先参考仓库/目录。

如果要我把其中某一步展开成详细的代码模板或把某个 repo 的关键文件拉出来逐行解读，告诉我我来做。

一、总体流程（高层）
1. 环境准备（C++ 工具链、Python 虚拟环境等）  
2. 准备中文语料并预处理（jieba 分词、停用词）  
3. 实现并构建倒排索引（C++ indexer：term→postings，支持存盘/加载）  
4. 实现检索与排序（首先 TF-IDF，再替换为 BM25）  
5. Python 与 C++ 集成（subprocess 或 pybind11）并写评测脚本（Precision@K、NDCG）  
6. 做一个交互式 Demo（Streamlit）并进行简单性能测试（索引耗时、查询延迟）  
7. 撰写文档与面试要点，总结改进方向（并行/压缩/向量检索扩展等）

二、环境与依赖（快速命令）
- 系统：Linux 或 WSL / macOS（开发推荐 Linux）
- C++：g++ (>=9) 或 clang，CMake >= 3.10
  - 常用安装（Ubuntu）：
    - sudo apt update && sudo apt install build-essential cmake git
- Python：3.8+，建议用 venv 或 conda
  - 建议包：jieba, pandas, streamlit（见 requirements.txt）
  - 示例：
    - python3 -m venv venv && source venv/bin/activate
    - pip install -r requirements.txt
- 可选（后续）：pybind11（C++ 与 Python 绑定）、valgrind / perf（性能分析）
- 本地测试建议内存 >= 8GB（小语料足够）

三、每一步的细化、耗时估计与推荐参考仓库

步骤 0 — 准备仓库与目录（0.5–1 小时）
- 目标：创建 repo 目录、.gitignore、requirements.txt、CMakeLists.txt（基础）
- 输出：README 初稿、目录结构
- 参考：无特定代码参考（快速初始化）

步骤 1 — 语料准备与预处理（2–6 小时）
- 工作内容：
  - 收集中文语料（新闻、维基、短文）放 data/corpus.txt（每行一篇）
  - 写 preprocess.py（jieba 分词、去停用词、可选自定义词典），输出每行分词后以空格分隔
- 耗时：根据语料规模，初版脚本 1–3 小时；clean & sample 另需 1–3 小时
- 参考仓库：
  - [jieba (分词库)](https://github.com/fxsjy/jieba) — 看 README、常见自定义词典用法
  - 示例项目（数据处理流程）：[Microsoft Recommenders](https://github.com/microsoft/recommenders) — 看 examples 和 notebooks（处理 pipeline 思路）

步骤 2 — C++ 倒排索引实现（8–20 小时）
- 工作内容：
  - 设计内存数据结构：term -> postings(list of (docID, tf [, positions]))
  - 实现 indexer：读取分词后语料、构建倒排、统计文档长度 & 全文档数
  - 支持序列化/反序列化（先文本格式，后可换为二进制或压缩）
  - 加入简单单元测试（小样本）
- 耗时：基础实现 6–12 小时，序列化/测试再 2–8 小时
- 参考仓库 / 阅读建议：
  - [Anserini (基于 Lucene 的 IR 工具包)](https://github.com/castorini/anserini) — 看 index 和 retrieval 设计（Java，但逻辑很典型）。重点目录：src/main/java/io/anserini/index 和 io/anserini/search
  - [Apache Lucene](https://github.com/apache/lucene) — 看核心索引/倒排的设计说明与术语（lucene 的 indexing 模块）
  - 如果想看 C++ 实现思路，可参考一些小型实现或论文的伪代码（市面上成熟 C++ 搜索库偏少，更多是 Java/Rust/Go 实现）

步骤 3 — 检索与 BM25 排序（6–12 小时）
- 工作内容：
  - 先实现简单 TF-IDF 得分作为 baseline（快速返回 top-k）
  - 再实现 BM25（熟悉公式，调参：k1, b）
  - 支持布尔查询（AND/OR），以及 snippet 输出（doc title/片段）
- 耗时：实现 TF-IDF 1–3 小时，BM25 3–8 小时，测试/调参 2–4 小时
- 参考仓库：
  - [Anserini 的检索实现](https://github.com/castorini/anserini) — BM25 的用法示例
  - Lucene 的 BM25 源码位置（了解排名实现细节）
  - 学术/工程资料：BM25 公式说明（网页/博客）

步骤 4 — Python ⇄ C++ 集成与批量评测（2–6 小时）
- 工作内容：
  - 简单方案：用 subprocess CLI（最省时）  
  - 更进阶：用 pybind11 绑定 C++ searcher 到 Python（方便批量评测与部署）
  - 写 eval.py：读取 results/qrels，计算 Precision@K、NDCG@K
- 耗时：subprocess 方案 1–2 小时；pybind11 绑定 4–8 小时
- 参考仓库：
  - [pybind11](https://github.com/pybind/pybind11) — 官方示例
  - 评测脚本思路：参考 [Anserini evaluation scripts](https://github.com/castorini/anserini/tree/master/src/main/python)（评估流程）

步骤 5 — Streamlit 前端 Demo（3–8 小时）
- 工作内容：
  - 简单 web：输入查询、选择 Top-K、显示结果（docID、score、snippet）
  - 可选：记录点击日志（用于模拟点击反馈）
- 耗时：基础界面 1–2 小时，完整交互 &日志 3–6 小时
- 参考仓库：
  - [Streamlit examples](https://github.com/streamlit/example-apps) — 看交互组件和布局
  - 项目 demo 参考：微软/开源的 demo notebooks（Microsoft Recommenders examples）

步骤 6 — 测试、性能测量与文档（3–8 小时）
- 工作内容：
  - 测试索引构建时间、索引文件大小、查询平均延迟 / P95
  - 写 README、docs/design.md（数据结构、BM25 解释、面试要点）
- 耗时：测量 1–3 小时、文档 2–5 小时
- 参考仓库：
  - [Anserini benchmarks](https://github.com/castorini/anserini) — 看 eval/benchmark 思路
  - [Microsoft Recommenders 文档](https://github.com/microsoft/recommenders) — 写项目文档的范例

四、每一步可直接参考的开源仓库（汇总）
- 检索（索引与排名概念、BM25）
  - Anserini — https://github.com/castorini/anserini (非常适合了解检索 pipeline、BM25 在实践中的用法)
  - Apache Lucene — https://github.com/apache/lucene (检索/倒排索引原理与成熟实现，虽为 Java)
  - OpenSearch / Elasticsearch — https://github.com/opensearch-project/opensearch , https://github.com/elastic/elasticsearch （工程级搜索架构与分布式设计）
- 推荐 / 两阶段（若后续做召回+排序）
  - Microsoft Recommenders — https://github.com/microsoft/recommenders (召回/排序 pipeline 与 notebook 案例)
  - RecBole — https://github.com/RUCAIBox/RecBole (推荐算法集合，适合学习召回/排序模型)
  - Faiss（向量召回，C++/Python） — https://github.com/facebookresearch/faiss (若后续做向量检索)
- CTR / 排序模型（若拓展到广告/CTR）
  - DeepCTR — https://github.com/shenweichen/DeepCTR
  - Vowpal Wabbit — https://github.com/VowpalWabbit/vowpal_wabbit (在线学习)
  - LightGBM / XGBoost — https://github.com/microsoft/LightGBM , https://github.com/dmlc/xgboost
- 工程化 / 性能
  - 查看 Anserini/Elasticsearch 的 benchmark、indexing 流程与 shard/replica 设计
  - Faiss 性能优化文档（向量召回优化）

五、常用命令示例（快速 copy）
- Python 环境：
  - python3 -m venv venv && source venv/bin/activate
  - pip install -r requirements.txt
- C++ build：
  - cd cpp && mkdir -p build && cd build && cmake .. && make
- 运行预处理：
  - python scripts/preprocess.py --input data/corpus.txt --output data/corpus_cleaned.txt
- 构建索引（示例 CLI）：
  - ./cpp/build/indexer data/corpus_cleaned.txt data/index.txt
- 查询（示例 CLI）：
  - ./cpp/build/searcher "查询 词语" 10 data/index.txt
- 启动 demo：
  - streamlit run demo/streamlit_demo.py
- 评估：
  - python scripts/eval.py --results results.json --qrels qrels.json --k 10

六、优先级与时间建议（基于你每周可投入）
- 两周压缩路线（赶基础 demo）：
  - Week1：环境 + 语料预处理 + C++ indexer 基础（TF-IDF）  
  - Week2：完善 searcher（BM25）、Python 集成、Streamlit demo、评估与文档
- 若周末时间有限可延长到 3–4 周，按每周模块推进（每周完成 1–2 个 Issue）

七、面试展示要点（你在准备 README & docs 时必写）
- 解释倒排索引数据结构（term→postings，存储 docID/tf/position 的理由）
- BM25 的工作原理与参数含义（k1、b）
- 设计 trade-off：内存 vs 磁盘、压缩策略（varint/gamma）、并发索引的基本思路
- 如果实现了 pybind11：说明为何选择绑定、线上调用延迟/序列化考虑
- 性能数据（索引时间、索引大小、查询平均延迟）

八、下一步建议（任选）
- 我可以把上面的每个步骤拆成 GitHub Issue（你已经有 8 条草稿，可追加 starter 代码文件到一个提交脚本供你复制粘贴）。  
- 或者我可以把你感兴趣的参考仓库中“最重要的 5 个文件/目录”列出来（并说明为何看这些文件），便于你针对性阅读与模仿实现。
- 或者我直接把 BM25 的 C++ 实现示例发给你，供替换目前的 TF-IDF scoring。

你想先要哪个？（回答 “拆 Issue 并给我 push 脚本” / “列参考仓库关键文件” / “BM25 C++ 实现示例” / “其他”）
