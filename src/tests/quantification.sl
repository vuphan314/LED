////////// ////////// ////////// ////////// ////////// //////////

import * from "../libLED.sl" as *;

c := AUX_3_A_;

/** AUXILIARY FUNCTIONS */

/** auxiliary function family: quantification 3 */

AUX_3_A_ := someSet(AUX_3_B_);

AUX_3_B_[i1] := 
	let
		x := AUX_3_C_[i1];
	in
		AUX_2_A_(x);

AUX_3_C_ := valToSet(iv(nu("1"), nu("2")));

/** auxiliary function family: quantification 2 */

AUX_2_A_(x) := allSet(AUX_2_B_(x));

AUX_2_B_(x)[i1] := 
	let
		y := AUX_2_C_(x)[i1];
	in
		AUX_1_A_(x, y);

AUX_2_C_(x) := valToSet(iv(x, mult(x, nu("2"))));

/** auxiliary function family: quantification 1 */

AUX_1_A_(x, y) := someSet(AUX_1_B_(x, y));

AUX_1_B_(x, y)[i1] := 
	let
		z := AUX_1_C_(x, y)[i1];
	in
		greater(add(div(y, x), z), nu("1"));

AUX_1_C_(x, y) := valToSet(iv(x, y));

////////// ////////// ////////// ////////// ////////// //////////

/** Copy/paste the block below into SequenceL interpreter to test:

pp(c)

(pp means PrettyPrint) */
