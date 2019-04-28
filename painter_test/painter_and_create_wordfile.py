from pyecharts import Bar

api1 = 'http://219.224.134.225:9099/backstage_detail/warning_describe/?id=300266201708031&end_date=2018-09-03'
api2 = 'http://219.224.134.225:9099/backstage_detail/large_trans_line/?id=002252201711011&start_date=2017-11-01&end_date=2018-08-15'

bar = Bar("主标题", "副标题", is_animation=False)
bar.add('衣服', [1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
bar.render()

from snapshot_selenium import snapshot


snapshot.make_snapshot(html_path="render.html", file_type='png')
