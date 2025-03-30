### Mofa_Search_Project

使用说明：

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 设置环境变量（创建.env文件）：
```
OPENAI_API_KEY=your_openai_key
SERPER_API_KEY=your_serper_api_key
```

3. 运行应用：
```bash
streamlit run main.py
```

更新说明：

1. 新增分布式搜索功能：
- 支持同时调用Google和DuckDuckGo的搜索API
- 使用线程池并行执行多个搜索请求
- 自动处理不同搜索引擎的响应格式

2. 新增元搜索功能：
- 聚合来自多个搜索引擎的结果
- 实现结果去重和排序策略
- 综合不同来源的信息进行整合

3. 增强智能体功能：
- 自动判断是否需要搜索
- 支持搜索结果预览
- 结合上下文生成最终回答

4. 改进UI界面：
- 增加搜索过程可视化
- 显示原始搜索结果
- 优化交互体验
