#!/usr/bin/jq -crf
.event as $event|
.members|
to_entries[]|
.value.name as $name|
.value.completion_day_level|
to_entries[]|
(.key|tonumber) as $day|
.value|
to_entries[]|
.key as $star|
((.value.get_star_ts|tonumber)-("\($event)-12-\($day)T05:00:00Z"|fromdateiso8601)) as $totalseconds|
(if $day < 10 then "0\($day)" else "\($day)" end) as $dayfmt|
[
"\($event)d\($dayfmt)",
(if $totalseconds >= 24*3600 then
	if $totalseconds >= 100*24*3600 then
		("\($totalseconds / 3600 / 24|floor)"|"t=" + "0"*(5 - length) + . + "d  ")
	else
		("\($totalseconds / 3600|floor)"|"hrs=" + "0"*(3 - length) + . + " ")
	end
else
	$totalseconds|strftime("%H:%M:%S")
end),
"star\($star)",
$name
]|@tsv
