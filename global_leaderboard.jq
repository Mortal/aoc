#!/usr/bin/jq -crnf
[
	[inputs[]]|sort_by(.id)|group_by(.id)[]|
	([.[]|101-.pos]|add) as $score|
	.[0]|
	del(.day,.star,.pos,.seconds)|
	.score=$score
]|
sort_by(-.score)[]|
[.score,(if .name then .name else .id end)]|@tsv
