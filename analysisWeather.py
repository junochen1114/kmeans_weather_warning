######################################
# Data Visualization #################
######################################

import weatherLearn
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.layouts import widgetbox as wbox, layout
from bokeh.models import ColumnDataSource, LabelSet
import bokeh.models.widgets as widget

wl = weatherLearn.weatherLearn()
mp = wl.mp


def access_data_type(attr, old, new):
    global tab1_data_dict, tab1_source
    data = mp.read_mongo({'largeLocation': new}, False)['warnType'].value_counts()
    for wt, count in data.items():
        idx = tab1_data_dict['warnType'].index(wt)
        tab1_data_dict['count'][idx] = count
    tab1_source.data = tab1_data_dict


def access_data_color(attr, old, new):
    global tab2_data_dict, tab2_source
    data = mp.read_mongo({'largeLocation': new}, False)['warnColor'].value_counts()
    for wc, count in data.items():
        idx = tab2_data_dict['warnColor'].index(wc)
        tab2_data_dict['count'][idx] = count
    tab2_source.data = tab2_data_dict


# def date_list(begin, end):
#     # beginDate, endDate是形如‘20160601’的字符串或datetime格式
#     dlist = [datetime.strftime(x, '%Y-%m-%d') for x in list(pd.date_range(start=begin, end=end))]
#     return dlist


# Tab1 layout
location1_select = widget.Select(options=wl.places, title='Locations', value='')
warntype_list = mp.count('warnType')
tab1_data_dict = dict(
    warnType=warntype_list,
    count=[0]*len(warntype_list)
)

tab1_source = ColumnDataSource(data=tab1_data_dict)
tab1_picture = figure(x_range=warntype_list, plot_width=6000, plot_height=500, title='Warn Color Counts',
                      toolbar_location=None, tools='')
tab1_labels = LabelSet(x='warnType', y='count', text='count', level='glyph',
                       x_offset=-13.5, y_offset=0, source=tab1_source, render_mode='canvas')

tab1_picture.vbar(x='warnType', top='count', width=0.9, source=tab1_source)
tab1_picture.add_layout(tab1_labels)

tab1_picture.y_range.start = 0
tab1_picture.y_range.end = 40

# Tab2 layout
location2_select = widget.Select(options=wl.places, title='Locations', value='')
warncolor_list = mp.count('warnColor')
tab2_data_dict = dict(
    warnColor=warncolor_list,
    count=[0]*len(warncolor_list)
)

tab2_source = ColumnDataSource(data=tab1_data_dict)
tab2_picture = figure(x_range=warncolor_list, plot_width=3000, plot_height=500, title='Warn Type',
                  toolbar_location=None, tools='')
tab2_picture.vbar(x='warnColor', top='count', width=0.9, source=tab2_source)

tab2_labels = LabelSet(x='warnColor', y='count', text='count', level='glyph',
                       x_offset=-13.5, y_offset=0, source=tab2_source, render_mode='canvas')

tab2_picture.add_layout(tab2_labels)
tab2_picture.y_range.start = 0
tab2_picture.y_range.end = 50

# Tab3 Layout
# datelist = date_list('20201119', '20210531')
# day_select = widget.Select(options=datelist, title='Date', value='')
# tab3_data_dict = dict(
#     locations=wl.places,
#     warnType=['0']*len(wl.places),
#     warnColor=['0']*len(wl.places)
# )


# Tab1 Warn Type
layout_tab1 = layout(
    [[wbox(location1_select, width=250), tab1_picture]],
)

# Tab2 Warn Color
layout_tab2 = layout(
    [[wbox(location2_select, width=250), tab2_picture]],
)

# Tab3 Date Query

# layout
tab1 = widget.Panel(child=layout_tab1, title='Warn Color')
tab2 = widget.Panel(child=layout_tab2, title='Warn Type')
# tab3 = widget.Panel(child=layout_tab3, title='Date Query')
tabs = widget.Tabs(tabs=[tab1, tab2])

curdoc().add_root(tabs)

# interactive
# tab1
location1_select.on_change('value', access_data_type)
# tab2
location2_select.on_change('value', access_data_color)
# tab3




