import pandas as pd
from pyecharts.charts import Line
from pyecharts import options as opts

df = pd.read_csv('./API_SP.POP.GROW_DS2_en_csv_v2_2594848.csv')
print(df.head())
print(df.isna().sum())

df = df.fillna(df.iloc[:, 2:].mean())
print(df.isna().sum())

df = pd.DataFrame(df)

# 选择要展示的国家
country_name = 'Aruba'
country_data = df[df['Country Name'] == country_name].drop(['Country Name', 'Country Code'], axis=1)
years = country_data.columns
values = country_data.values.flatten()

# 创建 ECharts 图表
line = (
    Line(init_opts=opts.InitOpts(width="1200px", height="600px"))
    .add_xaxis(list(years))
    .add_yaxis(country_name, list(values))
    .set_global_opts(
        title_opts=opts.TitleOpts(title=f"{country_name}每年增长率"),
        xaxis_opts=opts.AxisOpts(type_="category", name='年份'),
        yaxis_opts=opts.AxisOpts(type_="value", name='增长率（%）'),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
    )
)

# 渲染图表
line.render(f'{country_name}的人口增长.html')

# 计算每个国家的总人口增长
df['Total Growth'] = df.loc[:, '1961':'2023'].sum(axis=1)
print(df['Total Growth'])

# 选择前10和后10的国家
top_10_countries = df.nlargest(10, 'Total Growth')
bottom_10_countries = df.nsmallest(10, 'Total Growth')


def create_line_chart(countries, title):
    years = countries.columns[2:-1].tolist()  # 从1961到2023的年份
    line = Line()
    for i in countries.index:
        line.add_xaxis(years)
        line.add_yaxis(
            series_name=countries.loc[i, 'Country Name'],
            y_axis=countries.loc[i, '1961':'2023'].tolist(),
            label_opts=opts.LabelOpts(is_show=False)
        )
    line.set_global_opts(
        title_opts=opts.TitleOpts(title=title),
        xaxis_opts=opts.AxisOpts(
            type_="category",
            name="年份",
            axislabel_opts=opts.LabelOpts(rotate=45),  # 旋转X轴标签以适应长年份
        ),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            name="增长率 (%)",
        ),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        datazoom_opts=opts.DataZoomOpts(),  # 添加数据缩放
    )
    return line


# 创建图表
top_10_chart = create_line_chart(top_10_countries, "人口增长前10的国家")
bottom_10_chart = create_line_chart(bottom_10_countries, "人口增长最低的10个国家")

# 渲染图表
top_10_chart.render('人口增长前10的国家.html')
bottom_10_chart.render('人口增长最低的10个国家.html')


