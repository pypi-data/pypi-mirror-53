# itime
`itime` is an awesome converter to help converting various time formats in Python

<p align="center">
	<img alt="Last version" src="https://img.shields.io/github/tag/slxiao/itime.svg?style=flat-square" />
	<a href="https://travis-ci.org/slxiao/itime">
		<img alt="Build Status" src="http://img.shields.io/travis/slxiao/itime/master.svg?style=flat-square" />
	</a>
</p>

# installation
`pip install itime`
or
`python setup.py install`

# usage
```python
# import itime
from itime import *

# get diff hours of two str time
print get_difftime_in_hours("2019-10-01T23:41:09", "2019-10-02T01:07:11")
# output: 1.4

# get UTC str time of any-timezone str time
print get_utc_strtime("2019-10-01T23:41:09.000+02:00")
# output: "2019-10-01T21:41:09.000"

# get timestamp of str day
print get_timestamp_from_strday("2019-10-01")
# output: 1569888000000

# get timestamp of str time
print get_timestamp_from_strtime("2019-10-01T23:41:09.000+02:00") 
# output: 1569966069000

# get str time of timestamp
print get_strtime_from_timestamp(1569966069000)
# output: "2019-10-02T05:41:09.000+08:00"

# get str time of another timezone
print convert_strtime_by_tz("2019-10-01T23:41:09.000+02:00")
# output: "2019-10-02T05:41:09.000+08:00"
```

# testing
UT is based on `pytest`, run this command to execute all UT cases:
```sh
pytest
```

# lisense
MIT