# -*-coding:utf-8-*-
import pandas as pd
from Data.Tushare_StockData import get_k_data
import requests, json


def create_html(ts_code, start, end):
    data_df = get_k_data(code=ts_code, start=start, end=end, ktype='D', autype=None)

    print(data_df)

    from pyecharts import options as opts
    from pyecharts.charts import Kline, Line, Bar, Grid
    from pyecharts.commons.utils import JsCode

    date_data = data_df['date'].values.tolist()
    data = data_df[['open', 'close', 'low', 'high']]

    # （1）KLine线
    k_line = Kline()
    k_line.add_xaxis(date_data)
    k_line.add_yaxis("kline", data.values.tolist())
    k_line.set_global_opts(
        xaxis_opts=opts.AxisOpts(is_scale=True),
        # yaxis_opts=opts.AxisOpts(is_scale=True),
        yaxis_opts=opts.AxisOpts(
            is_scale=True,
            splitarea_opts=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=0)
            ),
        ),
        # 两个图的datazoom连到一起
        datazoom_opts=[
            opts.DataZoomOpts(is_show=False, type_='inside', xaxis_index=[0, 0], range_end=100),
            opts.DataZoomOpts(is_show=False, xaxis_index=[0, 1], range_end=100),
            opts.DataZoomOpts(is_show=True, xaxis_index=[0, 2], pos_top="96%", range_end=100),
        ],
        title_opts=opts.TitleOpts(title=ts_code)
    )

    fastPeriod = 6
    slowPeriod = 30
    signalPeriod = 6

    # Ma均线
    maLine = Line()
    maLine.add_xaxis(date_data)
    maLine.add_yaxis(
        series_name="Closing Price",
        y_axis=data['close'].rolling(1).mean(),
        is_smooth=True,
        linestyle_opts=opts.LineStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
    )
    maLine.add_yaxis(
        series_name="MA" + str(fastPeriod),
        y_axis=data['close'].rolling(fastPeriod).mean(),
        is_smooth=True,
        linestyle_opts=opts.LineStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
    )
    maLine.add_yaxis(
        series_name="MA" + str(slowPeriod),
        y_axis=data['close'].rolling(slowPeriod).mean(),
        is_smooth=True,
        linestyle_opts=opts.LineStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
    )
    maLine.set_global_opts(
        xaxis_opts=opts.AxisOpts(
            type_="category",
            grid_index=1,
            axislabel_opts=opts.LabelOpts(is_show=False),
        ),
        yaxis_opts=opts.AxisOpts(
            grid_index=1,
            split_number=3,
            axisline_opts=opts.AxisLineOpts(is_on_zero=False),
            axistick_opts=opts.AxisTickOpts(is_show=False),
            splitline_opts=opts.SplitLineOpts(is_show=False),
            axislabel_opts=opts.LabelOpts(is_show=True),
        ),
    )
    # Overlap Kline + ma
    overlap_kline_ma = k_line.overlap(maLine)

    # （2）成交量bar
    volumeFlag = data['close'] - data['open']
    barVolume = Bar()
    barVolume.add_xaxis(date_data)
    barVolume.add_yaxis(
        series_name="Volumn",
        y_axis=data_df['volume'].values.tolist(),
        xaxis_index=1,
        yaxis_index=1,
        label_opts=opts.LabelOpts(is_show=False),
        itemstyle_opts=opts.ItemStyleOpts(
            color=JsCode(
                """
                    function(params) {
                        var colorList;
                        if (volumeFlag[params.dataIndex] > 0) {
                            colorList = '#ef232a';
                        } else {
                            colorList = '#14b143';
                        }
                        return colorList;
                    }
                """
            )
        )
    )
    barVolume.set_global_opts(
        xaxis_opts=opts.AxisOpts(
            type_="category",
            grid_index=1,
            axislabel_opts=opts.LabelOpts(is_show=False),
        ),
        yaxis_opts=opts.AxisOpts(position='right'),
        legend_opts=opts.LegendOpts(is_show=False),
    )

    # （3）画macd指标图
    def calculateMACD(closeArray, fastPeriod=12, slowPeriod=24, signalPeriod=9):
        ema12 = closeArray.rolling(fastPeriod).mean()
        ema26 = closeArray.rolling(slowPeriod).mean()
        # diff正负差（快线和慢线差值）
        diff = (ema12 - ema26) * 2
        # dea异同平均数
        dea = diff.rolling(signalPeriod).mean()
        macd = (diff - dea)

        fast_values = diff
        slow_values = dea
        diff_values = macd

        return fast_values, slow_values, diff_values

    dw = pd.DataFrame()
    dw['DIF'], dw['DEA'], dw['MACD'] = calculateMACD(data['close'], fastPeriod=fastPeriod, slowPeriod=slowPeriod,
                                                     signalPeriod=signalPeriod)

    bar_2 = Bar()
    bar_2.add_xaxis(date_data)
    bar_2.add_yaxis(
        series_name="MACD",
        y_axis=dw["MACD"].values.tolist(),
        xaxis_index=1,  # 用于合并显示时排列位置，单独显示不要添加
        yaxis_index=1,  # 用于合并显示时排列位置，单独显示不要添加
        label_opts=opts.LabelOpts(is_show=False),
        itemstyle_opts=opts.ItemStyleOpts(
            color=JsCode(
                """
                    function(params) {
                        var colorList;
                        if (params.data >= 0) {
                            colorList = '#ef232a';
                        } else {
                            colorList = '#14b143';
                        }
                        return colorList;
                    }
                    """
            )
        ),
    )
    bar_2.set_global_opts(
        xaxis_opts=opts.AxisOpts(
            type_="category",
            grid_index=1,  # 用于合并显示时排列位置，单独显示不要添加
            axislabel_opts=opts.LabelOpts(is_show=False),
        ),
        yaxis_opts=opts.AxisOpts(
            grid_index=1,  # 用于合并显示时排列位置，单独显示不要添加
            split_number=4,
            axisline_opts=opts.AxisLineOpts(is_on_zero=False),
            axistick_opts=opts.AxisTickOpts(is_show=False),
            splitline_opts=opts.SplitLineOpts(is_show=False),
            axislabel_opts=opts.LabelOpts(is_show=True),
        ),
        legend_opts=opts.LegendOpts(is_show=False),
    )
    line_2 = Line()
    line_2.add_xaxis(date_data)
    line_2.add_yaxis(
        series_name="DIF",
        y_axis=dw["DIF"],
        xaxis_index=1,
        yaxis_index=2,
        label_opts=opts.LabelOpts(is_show=False),
    )
    line_2.add_yaxis(
        series_name="DEA",
        y_axis=dw["DEA"],
        xaxis_index=1,
        yaxis_index=2,
        label_opts=opts.LabelOpts(is_show=False),
    )
    line_2.set_global_opts(legend_opts=opts.LegendOpts(is_show=False))
    overlap_bar_line = bar_2.overlap(line_2)

    # 总gird
    grid_chart = Grid(init_opts=opts.InitOpts(width="100%", height="100%"))
    grid_chart.add_js_funcs(
        "var volumeFlag = {}".format(volumeFlag.values.tolist()))  # 传递涨跌数据给vomume绘图，用红色显示上涨成交量，绿色显示下跌成交量
    grid_chart.add(
        overlap_kline_ma,
        grid_opts=opts.GridOpts(height="55%")
    )
    grid_chart.add(
        barVolume,
        grid_opts=opts.GridOpts(pos_top="63%", height="16%"),
    )
    grid_chart.add(
        overlap_bar_line,
        grid_opts=opts.GridOpts(pos_top="80%", height="16%")
    )
    grid_chart.render("/Users/zhangwh/Desktop/量化/MyServer/SpringBootServer/src/main/resources/static/main/tab2/data_html/" + ts_code + ".html")
    # grid_chart.render("Data/data_html/" + ts_code + ".html")

    send_info('1', ts_code)


def send_info(if_get, ts_code):
    """
    推送消息给客户端
    :param  if_get: 是否成功生成html
            ts_code： 合约代码
    :return:
    """
    res = {'if_get': if_get, 'ts_code': ts_code}
    url = "http://192.168.3.229:8001/sendHTML"
    headers = {'Content-type': 'application/json; charset=utf8'}

    res = requests.put(url, data=json.dumps(res), headers=headers)