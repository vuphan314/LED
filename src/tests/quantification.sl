////////// ////////// ////////// ////////// ////////// //////////

import * from "../libLED.sl" as *;

c := AUX_2_A_;

/** AUXILIARY FUNCTIONS */

/** auxiliary function family: quantification 2 */

AUX_2_A_ := someSet(AUX_2_B_);

AUX_2_B_[i1] := 
	let
		x := AUX_2_C_[i1];
	in
		AUX_1_A_(x);

AUX_2_C_ := valToSet(iv(nu("1"), nu("1")));

/** auxiliary function family: quantification 1 */

AUX_1_A_(x) := someSet(AUX_1_B_(x));

AUX_1_B_(x)[i1] := 
	let
		y := AUX_1_C_(x)[i1];
	in
		eq(x, y);

AUX_1_C_(x) := valToSet(iv(nu("1"), nu("1")));

////////// ////////// ////////// ////////// ////////// //////////

/** Copy/paste the block below into SequenceL interpreter to test:

pp(c)

(pp means PrettyPrint) */
