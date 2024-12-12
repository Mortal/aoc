javascript:void(navigator.clipboard.writeText(JSON.stringify(((entries=[...document.querySelectorAll(".leaderboard-entry")],star=3)=>
entries.map((e,i)=>{
let name = e.textContent;
const strings = ["leaderboard-anon","leaderboard-position","leaderboard-time","supporter-badge","sponsor-badge"].map(kl=>e.querySelector("."+kl)?.textContent ?? "");
for (const s of strings) name = name.replace(s, "");
name = name.trim().replace(/\s+/g, " ") || null;
const id = +e.getAttribute("data-user-id");
const pos = parseInt(strings[1]);
if (pos == 1) star--;
const mo = /(\d+) +(\d\d):(\d\d):(\d\d)/.exec(strings[2]);
const day = +mo[1];
const seconds = 3600*mo[2]+60*mo[3]+(+mo[4]);
return {day, star, pos, seconds, id, name};
})
)())))
