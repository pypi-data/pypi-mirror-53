# wmonitor #
## wmonitor ##
+ wmonitor会从环境变量中获取"BUILD_TYPE"与"CONFIG_DIR"

demo.py
```python
from metric import Metric

Metric.counter("demo_counter").send()
Metric.counter("demo_counter").tags("business=123").send()
Metric.counter("demo_counter", 2).send()
Metric.gauge("demo_gauge").send()
Metric.state("demo_state").send()

```
## config ##
| BUILD_TYPE | 文件名称 |
| :----:| :----:|
| BETA | wmonitor_beta.cfg|
| DEV| wmonitor_dev.cfg|
| PROD| wmonitor_prod.cfg|
| DEFAULT or '' | wmonitor.cfg|

wmonitor.cfg
```text
[web]
domain = http://b1.wmonitor-adaptor.beta.wormpex.com
[app]
app_code = ai_vision_vision_dynamic_cabinet_service
```