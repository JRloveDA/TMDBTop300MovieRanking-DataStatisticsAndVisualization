# TMDB TOP300 电影榜单数据统计与可视化

使用 pandas 与 matplotlib 对 TMDB TOP300 电影榜单数据进行统计，并绘制 2×2 组合图表。

## 统计内容

1. **折线图**：每年上映的电影数量变化
2. **柱状图**：不同语言电影数量对比
3. **柱状图**：不同类型电影数量对比
4. **饼状图**：不同评分电影数量占比（占比小于 6% 的合并为"其他"）

## 运行方法

```bash
# 安装依赖
pip install -r requirements.txt

# 在项目根目录下运行
python 10.TMDB-TOP300电影榜单数据统计.py
```

> 注意：数据文件 `data/movies.csv` 使用相对路径加载，请在仓库根目录下运行脚本。

运行后会在 `data/` 目录下生成 `DMTB-TOP300.png` 图片。

## 数据来源

TMDB（The Movie Database）高分电影榜单数据，共 300 部电影，包含电影名、年份、上映时间、类型、评分、语言等字段。

## 代码结构

- `load_data()`：加载数据 + 年份缺失值处理（用上映时间前 4 位填补）
- `create_figure()`：创建 2×2 子图画布
- `plot_year_count()`：每年电影数量折线图
- `plot_language_count()`：语言数量柱状图
- `count_types()`：统计各类型电影数量
- `plot_type_count()`：类型数量柱状图
- `merge_small_ratings()`：合并小占比评分
- `plot_rating_pie()`：评分占比饼状图
- `main()`：主流程

仅用于学习交流。
