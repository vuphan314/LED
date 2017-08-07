/* Test with SequenceL interpreter:

pp(thisIsLEDSyntax)

(pp: pretty-print) */

import * from "../led_lib.sl" as *;

thisIsLEDSyntax := 
		aggrSum(AUX_2_AGGR_);

/* AUXILIARY FUNCTIONS */

AUX_1_AGGR_ := 
		setMemSol(iv(nu("1"), nu("3")));

AUX_2_AGGR_[i_] := 
	let
		b_ := AUX_1_AGGR_[i_];
		x := b_[1];
	in
		exp(x, nu("2"));


