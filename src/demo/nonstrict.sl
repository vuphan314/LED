/* Test with SequenceL interpreter:

pp(c1)
pp(c2)
pp(c3)

(pp: pretty-print) */

import * from "../src/led_lib.sl" as *;

c1 := 
		(valFalse when not valToTrth(tr(false)) else eq(div(nu("0"), nu("0")), nu("0")));

c2 := 
		(valTrue when not valToTrth(tr(false)) else eq(div(nu("0"), nu("0")), nu("0")));

c3 := 
		equiv(tr(true), (valTrue when not valToTrth(disj(tr(false), (valFalse when not valToTrth(tr(false)) else eq(div(nu("0"), nu("0")), nu("0"))))) else eq(div(nu("0"), nu("0")), nu("0"))));


