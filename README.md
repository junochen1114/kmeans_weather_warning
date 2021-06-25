# kmeans_weather_warning

主要就是mongodb数据库的读取+可视化

数据是师父之前爬的城市气象灾害+预警

我统计了一下城市灾害的天数做了可视化 bokeh库做的在analysisWeather里

之后根据天数套用kmeans分类，以学习为主就自己写kmeans了，在kmeans文件里，再可视化了一下结果，kmeans_dv里

做的时候cluster数字一开始设的4，（南北，内陆沿海）但效果不好，写了个图看SSE，“找拐点” 肘部 确定cluster=6

之后结果就比较好了

[海豚大数据 实习]

[感谢师父 @ygl]
