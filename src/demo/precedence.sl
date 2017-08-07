/* Test with SequenceL interpreter:

pp(zero)

(pp: pretty-print) */

import * from "../src/led_lib.sl" as *;

zero := 
		starOp(nu("0"), plusOp(nu("1"), nu("2")));


