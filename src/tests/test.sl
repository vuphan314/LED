import * from "../lib.sl" as *;

c := 
		nu("0") when valToTrth(tr(false)) else
		printNull;

d := 
		nu("0") when valToTrth(tr(false)) else
		nu("1");

/* Copy/paste the block below into SequenceL interpreter to test:

pp(c)
pp(d)

(pp: pretty-print) */
