"""
TMDB-TOP300电影榜单数据统计

1. 准备工作：导入依赖库、加载数据、创建子图完成基本布局
2. 统计TOP300的电影中，每一年上映的电影数量的变化（折线图）
3. 统计对比不同语言电影数量（柱状图）
4. 统计对比不同类型电影数量（柱状图）
5. 统计对比各个电影评分的比例（饼状图）
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

# 展示中文
plt.rcParams['font.sans-serif'] = ['SimHei']

DATA_FILE = 'data/movies.csv'
OUTPUT_IMAGE = 'data/DMTB-TOP300.png'
USED_COLS = ['电影名', '年份', '上映时间', '类型', '评分', '语言']


def load_data():
    """加载电影数据，并预处理年份列的缺失值。"""
    # int64: 普通整型，不支持空值；Int64: 带缺失值的整型；float64: 浮点型(支持空值)
    data = pd.read_csv(DATA_FILE, usecols=USED_COLS, dtype={'年份': 'Int64'})
    # 用「上映时间」的前4位填补「年份」的缺失值
    data['年份'] = data['年份'].fillna(data['上映时间'].str[0:4])
    return data


def create_figure():
    """创建 2x2 子图画布，返回画布和4个子图对象。"""
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(20, 12), dpi=100)
    fig.suptitle('TMDB-TOP300电影榜单数据统计', fontsize=24, x=0.5, y=0.98)
    fig.subplots_adjust(hspace=0.5, wspace=0.2)

    axes1: Axes = axes[0, 0]
    axes2: Axes = axes[0, 1]
    axes3: Axes = axes[1, 0]
    axes4: Axes = axes[1, 1]
    return fig, axes1, axes2, axes3, axes4


def plot_year_count(ax, data):
    """子图1：每年上映的电影数量变化（折线图）。"""
    year_count = data.groupby('年份')['年份'].count()

    min_year = int(year_count.index.min())
    max_year = int(year_count.index.max())
    x = list(range(min_year, max_year + 1))          # 连续年份
    y = [int(year_count.get(i, 0)) for i in x]       # 缺失年份补 0

    ax.plot(x, y, color='g')
    ax.set_title('每年上映的电影数量变化', fontsize=14, x=0.5, y=1.05)
    ax.set_xlabel('年份', fontsize=12)
    ax.set_ylabel('电影数量', fontsize=12)
    ax.set_xticks(x[::10])
    ax.set_yticks([i for i in range(0, 31, 3)])
    ax.grid(linestyle="--", alpha=0.5)


def plot_language_count(ax, data):
    """子图2：不同语言电影数量对比（柱状图）。"""
    data['语言'] = data['语言'].fillna('其他')

    language_count = data.groupby('语言')['语言'].count().sort_values(ascending=False)
    x = language_count.index.tolist()
    y = language_count.values.tolist()

    ax.bar(x, y, color='b', width=0.7)
    ax.set_title('不同语言电影数量对比', fontsize=14, x=0.5, y=1.05)
    ax.set_xlabel('语言', fontsize=12)
    ax.set_ylabel('电影数量', fontsize=12)
    ax.tick_params(axis='x', rotation=90)
    ax.grid(linestyle="--", alpha=0.5)


def count_types(data):
    """统计每种类型（逗号分隔）对应的电影数量，并按数量降序返回字典。"""
    type_count = {}
    for types in data['类型'].str.split(','):       # 如 ['剧情', '犯罪']
        for t in types:
            type_count[t] = type_count.get(t, 0) + 1
    return dict(sorted(type_count.items(), key=lambda item: item[1], reverse=True))


def plot_type_count(ax, data):
    """子图3：不同类型电影数量对比（柱状图）。"""
    data['类型'] = data['类型'].fillna('其他')

    type_count = count_types(data)
    x = list(type_count.keys())
    y = list(type_count.values())

    ax.bar(x, y, color='purple', width=0.7)
    ax.set_title('不同类型的电影数量对比', fontsize=14, x=0.5, y=1.05)
    ax.set_xlabel('类型', fontsize=12)
    ax.set_ylabel('电影数量', fontsize=12)
    ax.grid(linestyle="--", alpha=0.5)


def merge_small_ratings(rating_count, threshold=0.06):
    """把占比低于 threshold 的评分合并为「其他」，避免饼图碎块过多。"""
    total = rating_count.sum()
    large_rating = rating_count.loc[rating_count >= total * threshold]
    small_rating = rating_count.loc[rating_count < total * threshold]
    if small_rating.shape[0] > 0:
        large_rating['其他'] = small_rating.sum()
    return large_rating


def plot_rating_pie(ax, data):
    """子图4：不同评分电影数量占比（饼状图）。"""
    data['评分'] = data['评分'].fillna(0)

    rating_count = data.groupby('评分')['评分'].count()
    large_rating = merge_small_ratings(rating_count)

    labels = large_rating.index.tolist()
    sizes = large_rating.values.tolist()

    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, radius=1.2)
    ax.set_title('不同评分电影数量占比', fontsize=14, x=0.5, y=1.05)
    ax.legend(loc='lower center', ncol=4, bbox_to_anchor=(0.5, -0.2))


def main():
    data = load_data()
    fig, axes1, axes2, axes3, axes4 = create_figure()

    plot_year_count(axes1, data)
    plot_language_count(axes2, data)
    plot_type_count(axes3, data)
    plot_rating_pie(axes4, data)

    plt.savefig(OUTPUT_IMAGE)
    plt.show()


if __name__ == '__main__':
    main()
