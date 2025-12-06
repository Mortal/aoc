#!/usr/bin/jq -ncrf
[inputs]
|group_by("\(.event)\(.dayfmt)\(.name)")
|map(
	map({key:.star,value:.})
	|from_entries
	|(
		if .["2"] then
		.["2"] + {delta: .["2"].seconds-.["1"].seconds, firstsfmt: .["1"].secondsfmt}
		else
		.["1"] + {delta: "--", firstsfmt: .["1"].secondsfmt, secondsfmt: "--:--:--"}
		end
	)|["\(.event)d\(.dayfmt)", .firstsfmt, .secondsfmt, .delta, .name]
)
|[.[],["day", "   star1", "   star2", "delta", "name"]]
#|map([.[3],.[0],.[1],.[2],.[4]])
|sort[]
|@tsv
