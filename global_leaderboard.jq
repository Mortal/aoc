#!/usr/bin/jq -crnf
[
	[inputs[]]|sort_by(.id)|group_by(.id)[]|
	map(.score=101-.pos)|
	(map(.score)|add) as $score|
	[.[]|del(.name,.id)] as $points|
	.[0]|
	del(.day,.star,.pos,.seconds)|
	.points=$points|
	.score=$score
]
|sort_by(-.score)[]|[
	.score,
	(if .name then .name else .id end),
	(.points|map(select(.star==1)|.seconds)|sort|join(",")),
	(.points|map(select(.star==2)|.seconds)|sort|join(",")),
	(.points|sort_by(.day*2+.star)|map("\(.day)\(if .star == 1 then "₁" else "₂" end)")|join(","))
]|@tsv
