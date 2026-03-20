
# Hunter 超市关联规则分析平台

<div align=center>

🛒 基于 Apriori 算法的商品关联规则挖掘与可视化分析平台  
📊 从购物篮数据中发现商品间的购买关联性，为零售运营提供数据驱动决策

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://hunter-apriori-analysis-mabvhet5bun6bjci7vkdk7.streamlit.app/)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

</div>

## 📋 项目简介

本项目使用 Python 的 `mlxtend` 库实现 Apriori 算法，对 Hunter 超市的真实购物篮数据进行关联规则挖掘。通过 Streamlit 构建交互式 Web 应用，用户可以动态调整支持度、置信度、提升度等参数，实时查看商品间的关联规则，并获得可落地的运营建议。

### 🔍 核心功能
- **关联规则挖掘**：基于 Apriori 算法发现商品组合规律
- **交互式筛选**：滑动条动态调整挖掘阈值
- **规则可视化**：TOP 规则展示与业务建议
- **运营指导**：提供可落地的商品陈列/促销策略

## 🚀 快速开始

### 本地运行
1. 克隆项目
   ```bash
   git clone https://github.com/zzy-stack/hunter-apriori-analysis.git
   cd hunter-apriori-analysis
   ```

2. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

3. 运行应用
   ```bash
   streamlit run app.py
   ```

### 在线体验
[![](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://hunter-apriori-analysis-mabvhet5bun6bjci7vkdk7.streamlit.app/)

## 📁 项目结构

```
hunter-apriori-analysis/
├── hunter_apriori_app.py    # Streamlit 主应用
├── requirements.txt        # Python 依赖列表
├── hunter_core_rules.csv   # 核心关联规则数据
├── hunter_rules_lightweight.csv # 全量规则数据（轻量化）
└── README.md               # 项目说明文档
```

## 🛠️ 技术栈

- **数据处理**: `pandas`, `numpy`
- **关联规则**: `mlxtend` (Apriori 算法)
- **可视化**: `streamlit` (交互式 Web 应用)
- **部署**: Streamlit Community Cloud

## ⚙️ 依赖安装

```bash
pip install streamlit pandas numpy 
```

## 📊 数据来源与处理

- **数据集**: Hunter 超市购物篮交易数据
- **预处理**: 商品名称标准化、购物篮格式转换
- **算法**: Apriori 算法挖掘频繁项集与关联规则

## 📈 分析指标

- **支持度 (Support)**: 规则覆盖的订单比例
- **置信度 (Confidence)**: 前项商品购买后后项商品被购买的概率
- **提升度 (Lift)**: 衡量商品间关联强度的指标（>1 为正相关）

## 🎯 业务价值

1. **商品陈列优化**: 发现高频共现商品，优化货架布局
2. **精准营销**: 个性化推荐与交叉销售策略
3. **库存管理**: 基于关联性预测需求波动

## 📝 使用说明

1. 在侧边栏调整 **最小支持度**、**最小置信度**、**最小提升度** 参数
2. 查看主界面的筛选结果表格
3. 查看 TOP 5 高价值规则及其业务建议
4. 根据规则制定相应的运营策略

## 🤝 贡献

欢迎提出 Issue 或 Pull Request！

## 📄 许可证

MIT License

---

<div align=center>
  Made with ❤️ for Data Science Course Project
</div>
```
