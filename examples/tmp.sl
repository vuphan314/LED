
/* Copy/paste the block below into the SequenceL interpreter to test:

pp(e)

(pp: pretty-print) */

import * from "../lib.sl" as *;

e := 
		equiv((valTrue when not valToTrth(disj((valFalse when not valToTrth(tr(false)) else eq(div(nu("0"), nu("0")), nu("0"))), tr(false))) else eq(div(nu("0"), nu("0")), nu("0"))), tr(true));


