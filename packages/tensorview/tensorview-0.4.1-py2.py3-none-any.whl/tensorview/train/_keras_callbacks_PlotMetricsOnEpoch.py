from collections import defaultdict

import tensorflow as tf
import matplotlib.pyplot as plt
from IPython.display import clear_output
from pyecharts.charts import Line
from pyecharts.charts import Page
from pyecharts.charts import Timeline
from pyecharts import options as opts
from pandas import Series

__all__ = ['PlotMetricsOnEpoch']

class PlotMetricsOnEpoch(tf.keras.callbacks.Callback):
    """
    Arguments:
        metrics_name : list, Customized evaluation indicator name list,
                      sequentially created according to loss function and measurement function;
        columns : int, default 2，The number of sub graphs that the width of metrics
                 visualiztion image to accommodate at most;
        iter_num : int, default None，Pre-specify the maximum value of x-axis in each
                  sub-picture to indicate the maximum number of epoch training;
        wait_num : int, default 1, Indicates how many epoch are drawn each time a graph is drawn;
        figsize : tuple, default None, Represents the customize image size;
        cell_size : tuple, default (6, 4), Indicates the customize image size, which is used when figsize=None;
        valid_fmt : str, default "val_{}", The string preceding the underscore is used to
                   implement the validation set indicator naming;
        visual_name : str, default 'model_visual', save plot image with html file name.
        visual_name_gif : str, default 'model_visual_gif', save plot gif with html file name.
        visual_path : str, default None, train end save last image or gif file with html format to path;
        visual_image : bool, default True, if visual_image=False, train end not save image.
        visual_gif : bool, default False, if save_gif=True, train end save all image to gif;
    """
    def __init__(self, metrics_name, columns=2, iter_num=None, wait_num=1, figsize=None,
                 cell_size=(6, 4), valid_fmt="val_{}", visual_name='model_visual', visual_name_gif='model_visual_gif',
                 visual_path=None, visual_image=True, visual_gif=False):
        super(PlotMetricsOnEpoch, self).__init__()
        self.metrics_name = metrics_name
        self.columns = columns
        self.iter_num = iter_num
        self.wait_num = wait_num
        self.figsize = figsize
        self.cell_size = cell_size
        self.valid_fmt = valid_fmt
        self.epoch_logs = defaultdict(list)
        self.visual_name = visual_name
        self.visual_name_gif = visual_name_gif
        self.visual_path = visual_path
        self.visual_image = visual_image
        self.visual_gif = visual_gif

    def on_epoch_end(self, epoch, logs=None):
        self.epoch = epoch
        if len(logs)==len(self.metrics_name):
            old_all_name = self.model.metrics_names
            new_all_name = self.metrics_name
        else:
            old_all_name = self.model.metrics_names+['val_'+i for i in self.model.metrics_names]
            new_all_name = self.metrics_name+[self.valid_fmt.split('_')[0]+'_'+i for i in self.metrics_name]
        for old_name, new_name in zip(old_all_name, new_all_name):
            logs[new_name] = logs.pop(old_name)
        self.metrics = list(filter(lambda x: self.valid_fmt.split('_')[0] not in x.lower(), logs))
        if self.figsize is None:
            self.figsize = (self.columns*self.cell_size[0], ((len(self.metrics)+1)//self.columns+1)*self.cell_size[1])
        for metric in logs:
            self.epoch_logs[metric] += [logs[metric]]
        self.draw(metrics=self.metrics, logs=self.epoch_logs, plot_num=self.epoch, epoch=self.epoch,
                  columns=self.columns, iter_num=self.iter_num, wait_num=self.wait_num,
                  figsize=self.figsize, cell_size=self.cell_size, valid_fmt=self.valid_fmt)

    def on_train_end(self, logs=None):
        if self.visual_image:
            self.visual(name=self.visual_name, path=self.visual_path, gif=False)
        if self.visual_gif:
            self.visual(name=self.visual_name_gif, path=self.visual_path, gif=True)
        self.draw(metrics=self.metrics, logs=self.epoch_logs, plot_num=self.wait_num, epoch=self.epoch,
                  columns=self.columns, iter_num=self.iter_num, wait_num=self.wait_num,
                  figsize=self.figsize, cell_size=self.cell_size, valid_fmt=self.valid_fmt)
    
    def draw(self, metrics, logs, plot_num, epoch, columns, iter_num, wait_num, figsize, cell_size, valid_fmt):
        if plot_num%wait_num==0:
            clear_output(wait=True)
            plt.figure(figsize=figsize)
            for metric_id, metric in enumerate(metrics):
                plt.subplot((len(metrics)+1)//columns+1, columns, metric_id+1)
                if iter_num is not None:
                    plt.xlim(1, iter_num)
                plt.plot(range(1, len(logs[metric])+1), logs[metric], label="train")
                if valid_fmt.format(metric) in logs:
                    plt.plot(range(1, len(logs[metric])+1), logs[valid_fmt.format(metric)], label=valid_fmt.split('_')[0])
                plt.title(metric)
                plt.xlabel('epoch')
                plt.legend(loc='center right')
            plt.tight_layout()
            plt.show()
    
    def visual(self, name='model_visual', path=None, gif=False):
        """
        Arguments:
        name : str, train end save last image or gif file with html format name.
        path : str, train end save last image or gif file with html format to path;
        save_gif : bool, default False, if save_gif=True, train end save all image to gif;
        
        Return:
            a html file path.
        """
        if path is not None:
            assert tf.io.gfile.exists(path), "`path` not exist."
            file = path+'/'+'{}.html'.format(name)
        else:
            file = '{}.html'.format(name)
        page = Page(interval=1, layout=Page.SimplePageLayout)
        plot_list = []
        width_len = '750px'
        height_len = '450px'
        for metric_id, metric in enumerate(self.metrics):
            if not gif:
                line = Line(opts.InitOpts(width=width_len, height=height_len))
                line = line.add_xaxis(list(range(1, self.epoch+1)))
                line = line.add_yaxis('train', Series(self.epoch_logs[metric]).round(4).tolist(), is_smooth=True)
                if self.valid_fmt.format(metric) in self.epoch_logs:
                    line = line.add_yaxis(self.valid_fmt.split('_')[0],
                                          Series(self.epoch_logs[self.valid_fmt.format(metric)]).round(4).tolist(), is_smooth=True)
                line = line.set_series_opts(label_opts=opts.LabelOpts(is_show=False),
                                            markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='max', name='max_value'),
                                                                                    opts.MarkPointItem(type_='min', name='min_value')]))
                line = line.set_global_opts(title_opts=opts.TitleOpts(title=metric),
                                            xaxis_opts=opts.AxisOpts(name='Epoch', name_location='center', is_scale=True),
                                            datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=100)],
                                            toolbox_opts=opts.ToolboxOpts())
                plot_list.append(line)
            else:
                timeline = Timeline(opts.InitOpts(width=width_len, height=height_len)).add_schema(play_interval=100, is_auto_play=True)
                for i in range(1, self.epoch+1):
                    line = Line(opts.InitOpts(width=width_len, height=height_len))
                    line = line.add_xaxis(list(range(1, i+1)))
                    line = line.add_yaxis('train', Series(self.epoch_logs[metric])[:i].round(4).tolist(), is_smooth=True)
                    if self.valid_fmt.format(metric) in self.epoch_logs:
                        line = line.add_yaxis(self.valid_fmt.split('_')[0],
                                              Series(self.epoch_logs[self.valid_fmt.format(metric)])[:i].round(4).tolist(), is_smooth=True)
                    line = line.set_series_opts(label_opts=opts.LabelOpts(is_show=False),
                                                markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='max', name='max_value'),
                                                                                        opts.MarkPointItem(type_='min', name='min_value')]))
                    line = line.set_global_opts(title_opts=opts.TitleOpts(title=metric),
                                                xaxis_opts=opts.AxisOpts(name='Epoch', name_location='center', is_scale=True))
                    timeline.add(line, str(i))
                plot_list.append(timeline)
        page.add(*plot_list).render(file)
        return file
