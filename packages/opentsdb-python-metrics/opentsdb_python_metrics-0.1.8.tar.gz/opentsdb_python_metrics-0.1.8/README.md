#**opentsdb_python_metrics**

This library supports wrapping python methods in decorators that collect and store metrics using the opentsdb

It automatically setups up a connection to opentsdb and provides a helper method to write a metric to those places with some tags added.
It provides a decorator function to create a timing metric, and arbitrary additional metrics based on the return value.

##Environment Variables:
The library checks some environment variables on the system to determine where to send metrics too.

``` OPENTSDB_PYTHON_METRICS_TEST_MODE=False # If not false, library will not send any metrics```
``` OPENTSDB_HOSTNAME=my-opentsdb.my.url # Specifies the hostname of the opentsdb you want to connect to```

##Usage:
First, set the metrics_wrappers.project_name variable to be your projects name, i.e. "my_project_name". This name will
be prepended to each metrics name.

Add ```@metric_timer_with_tags(metric_name='metric_name',retval_functions={'additional_metric_type':lambda_function_mapping_method_return_value_to_metric_value}, asynchronous=True, tag_1=tag_1_value, ..., tag_6=tag_6_value)``` to each method you want to time
This generates an automatic metric_name.runtime metric for the duration, as well as any additional metrics you specify as functions on the return value of
the method being wrapped. For example, if the method returns a list of requests, you might want a key/value argument of
```'num_requests':(lambda x: len(x))``` as part of the retval_functions dictionary for the metric_timer wrapping that method. This would save
 metric_name.runtime and metric_name.num_requests. You can then add up to 6 tag name/value pairs to the function to save those tags with the metric in opentsdb.
 Opentsdb has a hard limit of 8 tag names per metric, and 2 are used by default for 'class_path' and 'host'. In general, you should only use tags where their
 usage will help you to make generic queries in the data by using wildcards or groupings on the different tag values for a tag name. If you just want to pass some
 static string information along with the metric that you will not need to differentiate in queries, then work that info into the metric_name instead of tags.
 The async optional keyword determines if your metrics will be sent asynchronously (default), or synchronously.

A simplified decorator can be used when individual tag values do not need to be specified.
An example is: ```@metric_timer('metric_name', additional_metric_type=lambda_function_mapping_method_return_value_to_metric_value)``` which is exactly like the example above except with no tags specified.

There are two special cases of additional metric_type for the metric_timer.
Using metric_type 'rate' will yield the time per value while using 'frequency' will yield the values per 1 second.
Both use the function given to get the value from the return value, and then use that along with the runtime to derive
the rate or frequency metric.

There is an optional method called `metric_name_modifier(metric_name, method, *args, **kwargs)` which can be overwritten
in a project to do some special transformation on the the metric name given the method and its arguments.

There are library parameters project_name and global_tags which can be set with a string and dictionary respectively,
and are applied to any metrics sent via send_tsdb_metric as additional tags.

There is a class mixin called SendMetricMixin that can be included in classes that would otherwise call send_tsdb_metric()
within its methods. The mixin automatically adds tags for class_path, so the user just needs to supply
the metric_name and value.