/* Test with SequenceL interpreter:

pp(c)

(pp: pretty-print) */

import * from "../led_lib.sl" as *;

c := 
		equiv((valTrue when not valToTrth(disj((valFalse when not valToTrth(tr(true)) else tr(false)), neg(eq(nu("1"), div(nu("2"), nu("2")))))) else tr(false)), uneq(at("`a"), se([])));


