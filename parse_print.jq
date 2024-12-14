#!/usr/bin/jq -crf
[
"\(.event)d\(.dayfmt)",
.secondsfmt,
"star\(.star)",
.name
]|@tsv
