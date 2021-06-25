import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Geo

######################################
# Data Visualization #################
######################################

cluster = 7
data = pd.read_excel('kmeans_7.xlsx')

c = (
    Geo(init_opts=opts.InitOpts(width="1400px", height="700px"))  # 图表大小, 主题风格
    .add_schema(maptype="china",  # 地图
                itemstyle_opts=opts.ItemStyleOpts(color="#28527a",  # 背景颜色
                                                  border_color="#9ba4b4"))  # 边框颜色, 可在 https://colorhunt.co/选择颜色
    .add(
        "",  # 系列名称, 可不设置
        [(i, j) for i, j in zip(data['location'], data['cluster'])],  # 数据
        effect_opts=opts.EffectOpts(symbol_size=2),  # 标记大小
    )

    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))  # 不显示标签
    .set_global_opts(title_opts=opts.TitleOpts(title="分类",  # 图表标题
                                               pos_left='center'),  # 标题位置
                     visualmap_opts=opts.VisualMapOpts(max_=cluster-1, min_=0),
                     )
)

c.render("kmeans分类_7.html")



