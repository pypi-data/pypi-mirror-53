# coding=utf-8
'''
数据可视化.
'''

from __future__ import absolute_import
import numpy as np
import pandas as pd
import pandas_profiling
import matplotlib.pyplot as plt
from matplotlib.font_manager import _rebuild
import seaborn as sns

_rebuild()
plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False

from sklearn.metrics import roc_auc_score

import pyecharts.options as opts
from pyecharts.render import make_snapshot
from pyecharts.charts import Line, Bar, Pie
from snapshot_phantomjs import snapshot
from datetime import datetime, timedelta
import re
import os
import warnings

warnings.filterwarnings('ignore')

from .base_utils import mkdir


class TargetPlot:
    def __init__(self):
        pass

    def run(self):
        pass


class LiftChart:
    def __init__(self):
        pass

    def run(self):
        pass


class PDP:
    def __init__(self):
        pass

    def run(self):
        pass


class PSI:
    def __init__(self):
        pass

    def run(self):
        pass


class ValueOnTime:
    def __init__(self):
        pass

    def run(self):
        pass


class EvaluationOnTime:
    def __init__(self, df=None, label='target', time_field='time',
                 n_bin=5,
                 time_range_list=None,
                 eval_metric='auc', save_path='./image/EvaluationOnTime/'):
        self.df = df
        self.label = label
        self.time_field = time_field
        self.n_bin = n_bin
        self.time_range_list = time_range_list
        self.eval_metric = eval_metric
        self.save_path = save_path
        mkdir(self.save_path)

        self.df = df.sort_values(self.time_field, ascending=True)
        self.ft_list = self.df.columns.tolist()
        if self.label in self.ft_list:
            self.ft_list.remove(self.label)
        else:
            print('警告, 数据不包含目标列.')
        if self.time_field in self.ft_list:
            self.ft_list.remove(self.time_field)
        else:
            print('警告, 数据不包含时间列.')
        if self.time_range_list is None:
            fst_date = self.df[self.time_field].tolist()[0]
            lst_date = self.df[self.time_field].tolist()[-1]
            fst_date = datetime.strptime(fst_date, '%Y-%m-%d')
            lst_date = datetime.strptime(lst_date, '%Y-%m-%d')
            num_day = (lst_date - fst_date).days
            days_in_bin = int(num_day / self.n_bin)
            date_list = [fst_date]
            tmp_date = fst_date
            for i in range(self.n_bin):
                tmp_date = tmp_date + timedelta(days=days_in_bin)
                date_list.append(tmp_date)
            date_list[-1] = lst_date
            date_list = [x.strftime('%Y-%m-%d') for x in date_list]
            self.time_range_list = date_list
        print('时间窗口如下:')
        print(self.time_range_list)

    def run(self):
        for ft in self.ft_list:
            res_list = []
            n_sample_list = []
            miss_rate_list = []
            for i in range(len(self.time_range_list) - 1):
                tmp_df = self.df.loc[(self.df[self.time_field] >= self.time_range_list[i]) &
                                     (self.df[self.time_field] < self.time_range_list[i + 1])]

                tmp_df_notna = tmp_df.loc[tmp_df[ft].notna()]
                n_sample_list.append(tmp_df.shape[0])
                miss_rate_list.append(tmp_df[ft].isnull().mean())

                if self.eval_metric == 'auc':
                    try:
                        res_list.append(roc_auc_score(y_true=tmp_df_notna[self.label],
                                                      y_score=tmp_df_notna[ft]))
                    except:
                        res_list.append(0)
                else:
                    pass
            self.plot(res_list, ft, n_sample_list=n_sample_list, miss_rate_list=miss_rate_list)

    def plot(self, data, title,
             n_sample_list=None, miss_rate_list=None):
        x_tick = [-0.5]
        for i in range(1, len(data) + 1):
            x_tick.append(i - 0.5)
        plt.figure(figsize=(12, 8))
        plt.style.use('ggplot')

        stats_info = ''
        for i in range(len(self.time_range_list) - 1):
            stats_info += '%s~%s 样本量%d 缺失率%.4f %s%.3f\n' % (self.time_range_list[i],
                                                            self.time_range_list[i + 1],
                                                            n_sample_list[i], miss_rate_list[i],
                                                            self.eval_metric, data[i])
        plt.plot(list(range(len(data))), data, label=stats_info)
        plt.legend(fontsize=15)
        plt.title(title, fontsize=25)
        plt.xticks(x_tick, self.time_range_list, fontsize=15, rotation=-15)
        plt.yticks(fontsize=15)
        plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9)
        plt.savefig(self.save_path + title)
        plt.show()


class EvaluationOnGroup:
    def __init__(self, df=None, label='target',
                 group_field=None, group_list=None,
                 eval_metric='auc', save_path='./image/EvaluationOnGroup/',
                 map_dict=None):
        self.df = df
        self.label = label
        self.group_field = group_field
        self.group_list = group_list
        self.eval_metric = eval_metric
        self.save_path = save_path
        mkdir(self.save_path)

        self.ft_list = self.df.columns.tolist()
        if self.label in self.ft_list:
            self.ft_list.remove(self.label)
        else:
            print('警告, 数据不包含目标列.')
        if self.group_field in self.ft_list:
            self.ft_list.remove(self.group_field)
        else:
            print('警告, 数据不包含分组列.')
        if self.group_list is None:
            self.group_list = self.df[self.group_field].unique().tolist()

        self.map_dict = map_dict
        if self.map_dict is not None:
            self.group_list_map = []
            for g in self.group_list:
                self.group_list_map.append(self.map_dict[g])
        else:
            self.group_list_map = self.group_list

    def run(self):
        for ft in self.ft_list:
            res_list = []
            n_sample_list = []
            miss_rate_list = []
            for group in self.group_list:
                tmp_df = self.df.loc[self.df[self.group_field] == group]
                tmp_df_notna = tmp_df.loc[tmp_df[ft].notna()]

                if self.eval_metric == 'auc':
                    try:
                        res_list.append(roc_auc_score(y_true=tmp_df_notna[self.label],
                                                      y_score=tmp_df_notna[ft]))
                    except:
                        res_list.append(0)
                else:
                    pass
                n_sample_list.append(tmp_df.shape[0])
                miss_rate_list.append(tmp_df[ft].isnull().mean())
            self.plot(res_list, ft, n_sample_list=n_sample_list, miss_rate_list=miss_rate_list)

    def plot(self, data, title,
             n_sample_list=None, miss_rate_list=None):
        plt.figure(figsize=(12, 8))
        plt.style.use('ggplot')
        stats_info = ''
        for i in range(len(self.group_list)):
            stats_info += '%s 样本量%d 缺失率%.4f %s%.3f\n' % (self.group_list[i],
                                                         n_sample_list[i], miss_rate_list[i],
                                                         self.eval_metric, data[i])
        plt.plot(list(range(len(data))), data, label=stats_info)
        plt.legend(fontsize=15)
        plt.title(title, fontsize=25)
        plt.xticks(list(range(len(data))), self.group_list_map, fontsize=15, rotation=-15)
        plt.yticks(fontsize=15)
        plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9)
        plt.savefig(self.save_path + title)
        plt.show()


class Mchart:
    def __init__(self,
                 save_path='./image/'):
        self.save_path = save_path
        mkdir(save_path)

    def hist(self, x=None, bins=20,
             hist=True, kde=True, figsize=(12, 8),
             title='test', x_name=None,
             is_x_time=False, time_fmt='%Y-%m-%d'):
        plt.figure(figsize=figsize)
        if is_x_time:
            # 把日期转换为时间戳.
            try:
                x = [datetime.strptime(i, time_fmt) for i in x]
            except:
                pass
            x = [i.timestamp() for i in x]
            # 利用时间戳画直方图.
            sns.distplot(a=x, bins=bins, hist=hist, kde=kde)

            # 修改直方图横轴刻度.
            x_ticks = [np.percentile(x, i) for i in [0, 20, 40, 60, 80, 100]]
            x_label = [datetime.fromtimestamp(i).strftime(time_fmt) for i in x_ticks]
            plt.xticks(x_ticks, x_label, rotation=-15)
        else:
            sns.distplot(a=x, bins=bins, hist=hist, kde=kde)
            plt.xlabel(xlabel=x_name, fontsize=15)
        # 配置.
        plt.title(title, fontsize=25)
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)
        plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9)
        plt.savefig(self.save_path + title)
        plt.show()


class Echart:
    def __init__(self,
                 mode='html',
                 save_path='./image/'):
        '''
        :param mode: str, 指定模式,
            默认html, 可选notebook(nb), static.
        '''

        self.mode = mode
        self.save_path = save_path

        mkdir(save_path)

    def output(self, painter, title='test'):
        if self.mode == 'html':
            painter.render(path=self.save_path + title + '.html')
        elif self.mode == 'nb':
            painter.render_notebook()
        elif self.mode == 'static':
            make_snapshot(engine=snapshot,
                          file_name=painter.render(),
                          output_name=self.save_path + title + '.png',
                          pixel_ratio=2,
                          is_remove_html=True)
        else:
            print('模式输入错误, 可选模式: \nhtml\nnb\nstatic')

    def line(self, x=None, y=None, title='test',
             is_max_show=False, is_min_show=False,
             is_avg_show=False, is_x_time=False,
             x_name='X', y_name='Y',
             y_name_list=None):
        # 初始化.
        painter = Line(init_opts=opts.InitOpts(width='900px',
                                               height='500px',
                                               page_title=title))
        # 配置.
        painter.set_global_opts(title_opts=opts.TitleOpts(title=title),
                                tooltip_opts=opts.TooltipOpts(trigger='axis',
                                                              axis_pointer_type='line'),
                                xaxis_opts=opts.AxisOpts(
                                    type_='time' if is_x_time else ('category' if isinstance(x[0], str) else 'value'),
                                    name=x_name,
                                    is_scale=True),
                                yaxis_opts=opts.AxisOpts(name=y_name,
                                                         is_scale=True),
                                legend_opts=opts.LegendOpts(is_show=True if isinstance(y[0], list) else False))
        # 添加数据.
        painter.add_xaxis(xaxis_data=x)
        if isinstance(y[0], list):
            for i, y_ in enumerate(y):
                painter.add_yaxis(series_name=y_name_list[i] if y_name_list is not None else '',
                                  y_axis=y_,
                                  is_connect_nones=True,
                                  label_opts=opts.LabelOpts(is_show=False),
                                  symbol_size=10)
        else:
            painter.add_yaxis(series_name='',
                              y_axis=y,
                              is_connect_nones=True,
                              label_opts=opts.LabelOpts(is_show=False),
                              symbol_size=10,
                              markline_opts=opts.MarkLineOpts(
                                  data=[opts.MarkAreaItem(type_='average')]) if is_avg_show else None,
                              markpoint_opts=opts.MarkPointOpts(
                                  data=[opts.MarkPointItem(type_='max' if is_max_show else 'min')]) if (
                                      is_max_show or is_min_show) else None)

        # 输出.
        self.output(painter=painter, title=title)

    def bar(self, x=None, y=None, title='test',
            is_max_show=False, is_min_show=False,
            is_reversal=False, is_stack=False,
            is_order=False,
            x_name='X', y_name='Y',
            y_name_list=None):
        # 数据预处理.
        if is_order:
            x_y = sorted(zip(x, y), key=lambda p: p[1], reverse=True)
            x = [x[0] for x in x_y]
            y = [x[1] for x in x_y]

        # 初始化.
        painter = Bar(init_opts=opts.InitOpts(width='900px',
                                              height='500px',
                                              page_title=title))

        # 配置.
        painter.set_global_opts(title_opts=opts.TitleOpts(title=title),
                                xaxis_opts=opts.AxisOpts(name=x_name,
                                                         is_scale=True),
                                yaxis_opts=opts.AxisOpts(name=y_name,
                                                         is_scale=True),
                                legend_opts=opts.LegendOpts(is_show=True if isinstance(y[0], list) else False))

        # 添加数据.
        painter.add_xaxis(xaxis_data=x)
        if isinstance(y[0], list):
            for i, y_ in enumerate(y):
                painter.add_yaxis(series_name=y_name_list[i] if y_name_list is not None else '',
                                  yaxis_data=y_,
                                  gap='0%' if not is_stack else None,
                                  stack='stack1' if is_stack else None)

        else:
            painter.add_yaxis(series_name='', yaxis_data=y,
                              markpoint_opts=opts.MarkPointOpts(
                                  data=[opts.MarkPointItem(name='MAX' if is_max_show else 'MIN',
                                                           type_='max' if is_max_show else 'min')]) if (
                                      is_max_show or is_min_show) else None)
        if is_reversal:
            painter.reversal_axis()
        if is_stack:
            painter.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        if is_reversal and not is_stack:
            painter.set_series_opts(label_opts=opts.LabelOpts(position='right'))

        # 输出.
        self.output(painter=painter, title=title)

    def hist(self, x=None, title='test', bins=20,
             x_name='X'):
        # 预处理.
        df = pd.DataFrame({'interval': pd.cut(x, bins=bins).tolist()})
        df['mean'] = df['interval'].apply(lambda x: (x.left + x.right) / 2)
        df_g = df.groupby('mean').agg(count_=('interval', 'count'))
        x = [round(i, 4) for i in df_g.index.tolist()]
        y = df_g['count_'].tolist()

        # 初始化.
        painter = Bar(init_opts=opts.InitOpts(width='900px',
                                              height='500px',
                                              page_title=title))

        # 配置.
        painter.set_global_opts(title_opts=opts.TitleOpts(title=title),
                                xaxis_opts=opts.AxisOpts(is_scale=True, name=x_name),
                                yaxis_opts=opts.AxisOpts(is_scale=True),
                                legend_opts=opts.LegendOpts(is_show=False))

        # 添加数据.
        painter.add_xaxis(xaxis_data=x)
        painter.add_yaxis(series_name='', yaxis_data=y,
                          label_opts=opts.LabelOpts(is_show=False),
                          category_gap=0)

        # 输出.
        self.output(painter=painter, title=title)

        pass


def EDA(df=None, title='EDA.html', max_sample=10000):
    # 若数据过大, 则抽样后再进行报告生成.
    if df.shape[0] > max_sample:
        df = df.sample(n=max_sample)
    profile = df.profile_report(title=title)
    mkdir('./log/')
    profile.to_file(output_file='./log/' + title)
    print('./log/' + title + '生成完毕.')


def make_html_report(image_dir_path='./image/',
                     md_html_path='md.html'):
    '''
    把echart图片插进markdown生成的html文件.
    '''
    print('开始插入html.')
    # 加载js语句.
    javascript = '''<script type="text/javascript" src="https://assets.pyecharts.org/assets/echarts.min.js"></script>'''
    # 读取md_html文本.
    with open(md_html_path, 'r', encoding='utf-8') as f:
        html = f.read()
        f.close()
    # 添加js语句.
    html = html.replace(r'''<meta charset='UTF-8'>''',
                        r'''<meta charset='UTF-8'><meta name="viewport" content="width=device-width, initial-scale=1">''' + javascript)
    # 遍历指定图片路径中的图片, 将图片插入html.
    for file in os.listdir(image_dir_path):
        if file.endswith('.html'):
            if '<p>@' + file[: -5] + '@</p>' in html:
                with open(image_dir_path + file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    f.close()
                    # 匹配.
                    image_js = re.search(r'<div.*</script>', content, flags=re.M | re.DOTALL).group()

                    # 替换.
                    html = html.replace('<p>@' + file[: -5] + '@</p>', image_js)

    # 保存.
    with open(md_html_path, 'w', encoding='utf-8') as f:
        f.write(html)
        f.close()
    print('插入完毕.')


if __name__ == '__main__':
    make_html_report(md_html_path='首贷无运营商-融合模型-说明.html')

    pass
