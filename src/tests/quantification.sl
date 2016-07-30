////////// ////////// ////////// ////////// ////////// //////////

import * from "../libLED.sl" as *;

c1 := setMem(AUX_1_A_, se([nu("2"), nu("4"), nu("6")]));

c2 := AUX_2_A_;

c3 := AUX_5_A_;

/** AUXILIARY FUNCTIONS */

/** quantification 5 */

AUX_5_A_ := someSet(AUX_5_B_);

AUX_5_B_[i1] := 
	let
		x := AUX_5_C_[i1];
	in
		AUX_4_A_(x);

AUX_5_C_ := valToSet(iv(nu("1"), nu("2")));

/** quantification 4 */

AUX_4_A_(x) := someSet(AUX_4_B_(x));

AUX_4_B_(x)[i1] := 
	let
		y := AUX_4_C_(x)[i1];
	in
		conj(less(x, nu("1.5")), y);

AUX_4_C_(x) := valToSet(se([AUX_3_A_]));

/** quantification 3 */

AUX_3_A_ := someSet(AUX_3_B_);

AUX_3_B_[i1] := 
	let
		z := AUX_3_C_[i1];
	in
		tr(true);

AUX_3_C_ := valToSet(se([]));

/** quantification 2 */

AUX_2_A_ := allSet(AUX_2_B_);

AUX_2_B_[i1] := 
	let
		v := AUX_2_C_[i1];
	in
		conj(setMem(v, iv(uMns(nu("5")), nu("5"))), eq(md(v, nu("2")), nu("1")));

AUX_2_C_ := valToSet(se([nu("1"), nu("3")]));

/** quantification 1 */

AUX_1_A_ := someSet(AUX_1_B_);

AUX_1_B_[i1] := 
	let
		v := AUX_1_C_[i1];
	in
		v;

AUX_1_C_ := valToSet(se([nu("1"), nu("2"), nu("3")]));

////////// ////////// ////////// ////////// ////////// //////////

/** Copy/paste the block below into SequenceL interpreter to test:

pp(c1)
pp(c2)
pp(c3)

(pp means PrettyPrint) */
