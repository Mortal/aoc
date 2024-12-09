#!/bin/bash
exec jq '
.event as $event|
.members|
to_entries[]|
.value.name as $name|
.value.completion_day_level|
to_entries[]|
.key as $day|
.value|
to_entries[]|
.key as $star|
((.value.get_star_ts|tonumber)-("\($event)-12-\($day)T05:00:00Z"|fromdateiso8601)) as $totalseconds|
[
"\($event)d\($day)",
(if $totalseconds >= 24*3600 then "+24" else $totalseconds|strftime("%H:%M:%S") end),
"star\($star)",
$name
]|@tsv' -cr
