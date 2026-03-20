
一个基于 `Streamlit + LangChain + Chroma` 的智能客服示例项目，面向扫地机器人/扫拖一体机问答场景，支持知识库检索、工具调用、天气查询、用户使用报告生成等能力。

适合用于以下场景：

- 搭建垂直领域智能客服 Demo
- 学习 LangChain Agent + RAG 的组合方式
- 演示知识库问答、外部工具调用、动态 Prompt 切换

## 核心功能

- `RAG 知识库问答`：从 `txt/pdf` 文档中构建向量库，回答产品选购、使用、维护、故障排查等问题
- `Agent 工具调用`：支持天气查询、用户位置获取、用户 ID 获取、月度报告数据查询
- `动态 Prompt 切换`：普通问答与“使用报告生成”场景使用不同提示词
- `外部数据接入示例`：通过 `data/external/records.csv` 模拟用户历史使用记录
- `对话式前端`：基于 Streamlit 提供聊天界面
- `日志记录`：运行日志按天输出到 `logs/`

## 项目结构

```text
agent/
├─ app.py                  # Streamlit 入口
├─ react_agent.py          # Agent 封装
├─ config/                 # YAML 配置
├─ data/                   # 知识库源文件与外部数据
├─ model/                  # 大模型与向量模型工厂
├─ prompts/                # 系统提示词 / RAG 提示词 / 报告提示词
├─ rag/                    # 向量库与检索摘要逻辑
├─ tools/                  # Agent 工具与中间件
├─ utils/                  # 配置、日志、路径、文件处理
├─ logs/                   # 日志输出目录
└─ md5.txt                 # 已入库文件的 MD5 记录
```

## 技术栈

- Python 3.10+，推荐 3.12
- Streamlit
- LangChain
- LangGraph
- Chroma
- DashScope / 通义千问模型接口
- PyYAML

## 快速开始

### 1. 安装依赖

当前仓库未提供 `requirements.txt`，可先按下面方式安装基础依赖：

```bash
pip install streamlit langchain langgraph langchain-community langchain-chroma langchain-text-splitters chromadb pypdf pyyaml uapi dashscope
```

### 2. 配置模型与工具

请修改以下配置文件，并替换成你自己的密钥与路径：

- `config/rag.yml`：聊天模型、Embedding 模型、API Key
- `config/agent.yml`：天气接口 Key、外部数据路径
- `config/chroma.yml`：向量库目录、切片参数、检索参数
- `config/prompts.yml`：提示词文件路径

推荐配置示例：

```yml
# config/rag.yml
chat_model_name: qwen3-max
embedding_model_name: text-embedding-v4
api: your_api_key
```

```yml
# config/agent.yml
weather_api_key: your_weather_api_key
external_data_path: data/external/records.csv
```

### 3. 准备知识库文件

将业务资料放入 `data/` 目录，当前支持：

- `.txt`
- `.pdf`

项目会根据 `config/chroma.yml` 中的配置进行切片、向量化和入库。

### 4. 初始化向量库

首次运行前建议先构建向量库。以下命令需要在“项目父目录”执行，且默认项目目录名为 `agent`：

```bash
python -c "from agent.rag.vector_store import VectorStoreService; VectorStoreService().load_document()"
```

如果你修改了项目目录名，请把命令中的 `agent` 改成对应的 Python 包名。

### 5. 启动项目

在项目根目录执行：

```bash
streamlit run app.py
```

启动后在浏览器打开默认地址即可开始对话。

## 使用示例

你可以尝试下面这些问题：

- 小户型适合哪种扫拖机器人？
- 地毯清洁时有哪些注意事项？
- 机器出现常见故障时应该怎么排查？
- 北京今天的天气适合让机器人频繁清扫吗？
- 帮我生成本月的使用情况报告

## 运行说明

- `rag/vector_store.py` 负责知识库加载、切片、向量化和持久化
- `rag/rag_service.py` 负责检索并基于参考资料生成摘要回答
- `tools/agent_tools.py` 提供天气、定位、用户数据、报告上下文等工具
- `tools/middleware.py` 负责工具监控、日志记录和动态 Prompt 切换
- `react_agent.py` 负责组装 Agent、工具和中间件

## 注意事项

- 上传到 GitHub 前，请务必移除或替换真实 API Key，不要把生产密钥直接提交到仓库
- `logs/`、`md5.txt`、本地向量库目录属于运行产物，建议通过 `.gitignore` 排除
- 当前“用户 ID”和“月份”获取逻辑为示例实现，使用了随机值，更适合 Demo 场景
- 如果知识库未初始化，RAG 问答效果会受到影响

## 后续可优化方向

- 补充 `requirements.txt` 或 `pyproject.toml`
- 使用环境变量管理密钥
- 增加 `.gitignore`
- 为知识库构建增加独立脚本
- 接入真实用户系统与业务数据库

## License

如需开源发布，建议补充项目许可证，例如 `MIT`。
=======
# RAG_Helper
基于 LangChain 的 RAG 智能客服 Agent 系统
>>>>>>> d7ffa7752790bcb9ee3b50ee1d878fecb97c04cf
