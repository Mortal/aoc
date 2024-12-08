#!/bin/bash
exec jq '.event as $event|.members|to_entries[]|.value.name as $name|.value.completion_day_level|to_entries[]|.key as $day|.value|to_entries[]|.key as $star|["\($event)d\($day)",(.value.get_star_ts|todate),"star\($star)",$name]|@tsv' -cr
