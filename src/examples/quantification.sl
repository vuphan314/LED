
/* 
Copy/paste the block below into
the SequenceL interpreter to test:

pp(c1)
pp(c2)
pp(c3)
pp(c4)

(pp: pretty-print) */

import * from "../led_lib.sl" as *;

c1 := 
		AUX_1_A_;

c2 := 
		AUX_2_A_;

c3 := 
		AUX_5_A_;

c4 := 
		AUX_7_A_;

/* AUXILIARY FUNCTIONS */

AUX_1_A_ := 
		someSet(AUX_1_B_);

AUX_1_B_[i_] := 
	let
		v := AUX_1_C_[i_];
	in
		setMem(v, se([nu("2"), nu("4"), nu("6")]));

AUX_1_C_ := 
		valToSet(se([nu("1"), nu("2"), nu("3")]));

AUX_2_A_ := 
		allSet(AUX_2_B_);

AUX_2_B_[i_] := 
	let
		v := AUX_2_C_[i_];
	in
		(valFalse when not valToTrth(setMem(v, iv(uMns(nu("5")), nu("5")))) else eq(md(v, nu("2")), nu("1")));

AUX_2_C_ := 
		valToSet(se([nu("1"), nu("3")]));

AUX_3_A_(x) := 
		someSet(AUX_3_B_(x));

AUX_3_B_(x)[i_] := 
	let
		z := AUX_3_C_(x)[i_];
	in
		tr(true);

AUX_3_C_(x) := 
		valToSet(se([]));

AUX_4_A_(x) := 
		someSet(AUX_4_B_(x));

AUX_4_B_(x)[i_] := 
	let
		y := AUX_4_C_(x)[i_];
	in
		(valFalse when not valToTrth(less(x, nu("1.5"))) else y);

AUX_4_C_(x) := 
		valToSet(se([AUX_3_A_(x)]));

AUX_5_A_ := 
		someSet(AUX_5_B_);

AUX_5_B_[i_] := 
	let
		x := AUX_5_C_[i_];
	in
		AUX_4_A_(x);

AUX_5_C_ := 
		valToSet(iv(nu("1"), nu("2")));

AUX_6_A_(x) := 
		someSet(AUX_6_B_(x));

AUX_6_B_(x)[i_] := 
	let
		y := AUX_6_C_(x)[i_];
	in
		less(y, nu("0"));

AUX_6_C_(x) := 
		valToSet(iv(x, plusOp(x, nu("3"))));

AUX_7_A_ := 
		allSet(AUX_7_B_);

AUX_7_B_[i_] := 
	let
		x := AUX_7_C_[i_];
	in
		disj(greater(x, nu("0")), AUX_6_A_(x));

AUX_7_C_ := 
		valToSet(se([]));


