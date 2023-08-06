# cloudhealth-fluent

# Overview
This is a [fluent](https://en.wikipedia.org/wiki/Fluent_interface) API that allows users to export CloudHealth data to Excel.

# Quickstart
```
$ pip install cloudhealth-fluent
```
Here's a couple quick examples that shows all the features of the fluent API.

## Option 1: Request a Report With Code

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
    c.write_excel('report.xlsx')
```

## Option 2: Request One or More Reports With YAML

You can define your report requests with yaml and pass in all the reports at one time.

Create a file called `reports.yaml`:

```
cost_instance:
    report: olap_reports/cost/current/instance
    measures:
        - cost
        - ec2_cost_compute
        - ec2_cost_transfer
    time: daily
    dimensions:
        - time
        - EC2-Instance-Types
    select_filters:
        AWS-Account:
            - 1234567890

cost_report:
    report: olap_reports/cost/history/amortization
    measures:
        - cost
        - cost_amortized
    time: daily
    dimensions:
        - time
        - AWS-Service-Category
    reject_filters:
        AWS-Account:
            - 1234567890
```
Then you just call `get_report_data()` with `reports.yaml` and it will generate one Excel file per report. Each measure gets its own worksheet.

```
from cloudhealth import CloudHealth
c = CloudHealth(ApiKey='XXX')
j = c.with_report_files(['reports.yaml']).get_report_data()
c.write_excel()
```
