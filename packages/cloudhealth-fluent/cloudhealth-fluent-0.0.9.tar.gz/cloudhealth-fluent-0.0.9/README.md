# cloudhealth-fluent

# Overview
This is a [fluent](https://en.wikipedia.org/wiki/Fluent_interface) API that allows users to export CloudHealth data to Excel.

#Quickstart
```
$ pip install cloudhealth-fluent
```
Here's a quick example that shows all the features of the fluent API.

```
from cloudhealth import CloudHealth
c = CloudHealth(ApiKey='CLOUDHEALTH API KEY')
data = c.new().with_measures(['cost', 'ec2_cost_compute', 'ec2_cost_transfer']) \
         .with_select_filter(('AWS-Account',
                              ['012345678901'])) \
         .with_report('olap_reports/cost/current/instance') \
         .with_time('daily') \
         .with_dimension('time') \
         .with_dimension('EC2-Instance-Types') \
         .get_report()
    c.build_data(data)
    c.write_excel('report.xlsx')
```
