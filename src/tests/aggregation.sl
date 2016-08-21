////////// ////////// ////////// ////////// ////////// //////////

import * from "../libLED.sl" as *;

mySet := iv(nu("1"), nu("2"));

mySet2 := iv(uMns(nu("2")), uMns(nu("1")));

aggrTerm(y) := setCompr(AUX_4_AGGR_(y));

/** AUXILIARY FUNCTIONS */

AUX_1_AGGR_(y) := solSet(mySet);

AUX_2_AGGR_(y) := solSet(mySet2);

AUX_3_AGGR_(y) := solDisj(AUX_1_AGGR_(y), AUX_2_AGGR_(y));

AUX_4_AGGR_(y)[i_] := 
	let
		b_ := AUX_3_AGGR_(y)[i_];
		x := b_[1];
	in
		cross(x, y);

////////// ////////// ////////// ////////// ////////// //////////

/** Copy/paste the block below into SequenceL interpreter to test:

pp(mySet)
pp(mySet2)

(pp: pretty-print) */
