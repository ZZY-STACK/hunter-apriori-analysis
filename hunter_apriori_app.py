import streamlit as st
import pandas as pd

# ==========================================
# 页面基础配置
# ==========================================
st.set_page_config(
    page_title="Hunter超市关联规则分析",
    page_icon="🛒",
    layout="wide"  # 宽屏布局，展示更多内容
)

# 页面标题与说明
st.title("🛒 Hunter超市关联规则分析平台")
st.markdown("""
    基于Apriori算法挖掘的商品关联规则，支持自定义阈值筛选、规则可视化，
    并提供可落地的陈列/促销建议，助力精准运营。
""")
st.divider()

# ==========================================
# 1. 加载数据（核心修复：手动解析商品名称）
# ==========================================
@st.cache_data  # 缓存数据，提升加载速度
def load_rules():
    """加载并解析规则数据（修复ast解析失败问题）"""
    # 加载核心规则（单商品→单商品）
    core_rules = pd.read_csv('hunter_core_rules.csv')
    
    # 手动解析frozenset字符串（核心修复逻辑）
    def extract_product_name(s):
        """从frozenset字符串中提取商品名称（适配单商品场景）"""
        if pd.isna(s):
            return ""
        # 移除frozenset标识和括号，提取商品名
        s_clean = s.replace('frozenset({', '').replace('})', '').replace("'", "").strip()
        # 处理可能的空格/特殊字符
        return s_clean if s_clean else ""
    
    # 解析前项/后项商品名称
    core_rules['antecedent_name'] = core_rules['antecedents'].apply(extract_product_name)
    core_rules['consequent_name'] = core_rules['consequents'].apply(extract_product_name)
    
    # 保留核心列并简化
    core_rules_simple = core_rules[['antecedent_name', 'consequent_name', 'support', 'confidence', 'lift']].copy()
    # 过滤空值
    core_rules_simple = core_rules_simple[
        (core_rules_simple['antecedent_name'] != "") & 
        (core_rules_simple['consequent_name'] != "")
    ].reset_index(drop=True)
    
    # 加载全量规则（若没有，复用核心规则）
    try:
        all_rules = pd.read_csv('hunter_rules_lightweight.csv')
        all_rules['antecedent_name'] = all_rules['antecedents'].apply(extract_product_name)
        all_rules['consequent_name'] = all_rules['consequents'].apply(extract_product_name)
        all_rules_simple = all_rules[['antecedent_name', 'consequent_name', 'support', 'confidence', 'lift']].copy()
        all_rules_simple = all_rules_simple[
            (all_rules_simple['antecedent_name'] != "") & 
            (all_rules_simple['consequent_name'] != "")
        ].reset_index(drop=True)
    except:
        all_rules_simple = core_rules_simple.copy()
    
    return core_rules_simple, all_rules_simple

# 加载数据
core_rules, all_rules = load_rules()

# ==========================================
# 2. 侧边栏：交互筛选控件（阈值调节+规则类型筛选）
# ==========================================
st.sidebar.title("🔧 筛选条件")

# 阈值调节滑动条（基于最优阈值范围）
min_support = st.sidebar.slider(
    "最小支持度",
    min_value=0.005,
    max_value=0.025,
    value=0.01,  # 最优阈值默认值
    step=0.001,
    help="支持度越高，规则覆盖的订单数越多"
)

min_confidence = st.sidebar.slider(
    "最小置信度",
    min_value=0.15,
    max_value=0.40,
    value=0.2,   # 最优阈值默认值
    step=0.01,
    help="置信度越高，前项带动后项购买的概率越大"
)

min_lift = st.sidebar.slider(
    "最小提升度",
    min_value=1.0,
    max_value=5.0,
    value=1.2,   # 最优阈值默认值
    step=0.1,
    help="提升度越高，商品关联度越强（>1为正相关）"
)

# 规则类型筛选（简化，仅核心规则）
rule_type = st.sidebar.radio(
    "规则类型",
    options=["核心业务规则（单商品→单商品）"],
    index=0,
    help="仅展示可直接落地的单商品关联规则"
)

# ==========================================
# 3. 规则筛选逻辑
# ==========================================
# 按阈值筛选
filtered_rules = all_rules[
    (all_rules['support'] >= min_support) &
    (all_rules['confidence'] >= min_confidence) &
    (all_rules['lift'] >= min_lift)
].copy()

# 按提升度降序排序
filtered_rules = filtered_rules.sort_values('lift', ascending=False).reset_index(drop=True)

# ==========================================
# 4. 主页面：结果展示（核心规则+业务建议）
# ==========================================
# 4.1 规则统计
st.subheader(f"📊 筛选结果（共 {len(filtered_rules)} 条规则）")
st.markdown(f"当前筛选条件：支持度≥{min_support} | 置信度≥{min_confidence} | 提升度≥{min_lift}")

# 4.2 规则表格展示
st.dataframe(
    filtered_rules[['antecedent_name', 'consequent_name', 'support', 'confidence', 'lift']].head(20),
    column_config={
        "antecedent_name": st.column_config.TextColumn("前项商品", width="medium"),
        "consequent_name": st.column_config.TextColumn("后项商品", width="medium"),
        "support": st.column_config.NumberColumn("支持度", format="%.4f"),
        "confidence": st.column_config.NumberColumn("置信度", format="%.4f"),
        "lift": st.column_config.NumberColumn("提升度", format="%.4f")
    },
    use_container_width=True
)

# 4.3 核心规则可视化（TOP5 + 业务建议）
if len(filtered_rules) > 0:
    st.divider()
    st.subheader("🔥 TOP 5 高价值规则 + 业务落地建议")
    
    # 生成TOP5规则的业务建议
    business_suggestions = {
        "pasta sauce → dry pasta": "意面酱和意面做「意式套餐」捆绑促销，陈列在同一货架，提升连带率",
        "dry pasta → pasta sauce": "意面商品详情页推荐意面酱，购物车加购意面时弹窗推荐意面酱",
        "canned jarred vegetables → canned meals beans": "罐装蔬菜旁陈列罐装豆类，推出「速食蔬菜组合」满减",
        "canned meals beans → canned jarred vegetables": "罐装豆类区域设置「搭配购买」提示，引导选购罐装蔬菜",
        "preserved dips spreads → chips pretzels": "蘸酱和薯片做「休闲零食组合」，早高峰/晚高峰定向推送优惠券",
        "spices seasonings → fresh herbs": "调味料旁陈列新鲜香草，贴合西餐烹饪场景，提升客单价",
        "fruit vegetable snacks → energy granola bars": "果蔬零食和能量棒做「健康零食包」，主打早餐/下午茶场景",
        "canned jarred vegetables → soup broth bouillon": "罐装蔬菜+高汤做「速食汤组合」，陈列在速食区核心位置",
        "canned jarred vegetables → fresh herbs": "罐装蔬菜旁摆放新鲜香草，满足「速食+调味」一站式采购",
        "breakfast bakery → other creams cheeses": "烘焙早餐旁陈列奶油奶酪，主打早餐场景，推出「早餐组合价」"
    }
    
    # 展示TOP5规则+建议
    for idx in range(min(5, len(filtered_rules))):
        row = filtered_rules.iloc[idx]
        ante = row['antecedent_name']
        conse = row['consequent_name']
        rule_key = f"{ante} → {conse}"
        # 获取对应业务建议（无则生成通用建议）
        suggestion = business_suggestions.get(
            rule_key.lower(),
            f"{ante}和{conse}做关联陈列，购物车加购{ante}时推荐{conse}"
        )
        
        # 卡片式展示
        with st.expander(f"规则 {idx+1}：{ante} → {conse}（提升度：{row['lift']:.2f}）", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                    - 支持度：{row['support']:.4f}（覆盖约{int(row['support']*18743)}个订单）
                    - 置信度：{row['confidence']:.4f}（购买{ante}的用户中{row['confidence']*100:.1f}%会买{conse}）
                    - 提升度：{row['lift']:.4f}（关联度远超随机水平）
                """)
            with col2:
                st.markdown(f"**业务建议**：{suggestion}")

# 4.4 无规则时的提示
else:
    st.warning("⚠️ 未找到符合条件的规则，请降低阈值重试！")

# ==========================================
# 5. 底部说明
# ==========================================
st.divider()
st.markdown("""
    ### 📌 运营建议总结
    1. 优先落地提升度＞3的核心规则（如意面酱+意面、罐装蔬菜+罐装豆类），ROI最高；
    2. 休闲零食类规则（蘸酱+薯片）适合在晚高峰/周末做定向促销；
    3. 速食类规则（罐装蔬菜+高汤）可陈列在「速食区」，贴合快节奏消费需求。
""")