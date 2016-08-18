////////// ////////// ////////// ////////// ////////// //////////

import * from "../libLED.sl" as *;

c := setCompr(AUX_2_AGGR_);

/** AUXILIARY FUNCTIONS */

AUX_1_AGGR_[i_] := [valToSet(iv(nu("1"), nu("3")))[i_]];

AUX_2_AGGR_[i_] := 
	let
		b_ := AUX_1_AGGR_[i_];
		x := b_[1];
	in
		nu("4");

////////// ////////// ////////// ////////// ////////// //////////

/** Copy/paste the block below into SequenceL interpreter to test:

pp(c)

(pp means PrettyPrint) */
