////////// ////////// ////////// ////////// ////////// //////////

import * from "../libLED.sl" as *;

c := setCompr(AUX_4_AGGR_);

/** AUXILIARY FUNCTIONS */

AUX_1_AGGR_ := [[nu("4")]];

AUX_2_AGGR_(x)[i_] := [valToSet(iv(x, add(x, nu("1"))))[i_]];

AUX_3_DEEP_[i1_, i2_] := 
	let
		b1_ := AUX_1_AGGR_[i1_];
		x := b1_[1];
		b2_ := AUX_2_AGGR_(x)[i2_];
	in
		unnBinds(b1_, b2_);

AUX_3_AGGR_ := join(AUX_3_DEEP_);

AUX_4_AGGR_[i_] := 
	let
		b_ := AUX_3_AGGR_[i_];
		x := b_[1];
		y := b_[2];
	in
		tu([x, y]);

////////// ////////// ////////// ////////// ////////// //////////

/** Copy/paste the block below into SequenceL interpreter to test:

pp(c)

(pp means PrettyPrint) */
