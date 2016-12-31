
/* 
Copy/paste the block below into
the SequenceL interpreter to test:

pp(c1)
pp(c2)
pp(c3)
pp(c4)
pp(c5)

(pp: pretty-print) */

import * from "../led_lib.sl" as *;

f(t) := 
		setCompr(AUX_4_AGGR_(t));

c1 := 
		f(nu("1"));

c2 := 
		aggrSum(AUX_8_AGGR_);

c3 := 
		aggrProd(AUX_10_AGGR_);

c4 := 
		aggrUnn(AUX_14_AGGR_);

r(s, t) := 
		eq(aggrNrsec(AUX_18_AGGR_(s, t)), se([nu("1")]));

c5 := 
		r(unaryMinus(nu("1")), nu("1"));

/* AUXILIARY FUNCTIONS */

AUX_1_AGGR_(t) := 
		solSet(iv(t, starOp(nu("2"), t)));

AUX_2_AGGR_(t, x) := 
		solEqs(tu([exp(x, nu("2")), exp(x, nu("3"))]));

AUX_3_DEEP_(t)[i1_, i2_] := 
	let
		workaround1_ := AUX_1_AGGR_(t);
		b1_ := workaround1_[i1_];
		x := b1_[1];
		workaround2_ := AUX_2_AGGR_(t, x);
		b2_ := workaround2_[i2_];
	in
		unnBinds(b1_, b2_);

AUX_3_AGGR_(t) := 
		join(AUX_3_DEEP_(t));

AUX_4_AGGR_(t)[i_] := 
	let
		b_ := AUX_3_AGGR_(t)[i_];
		x := b_[1];
		y := b_[2];
		z := b_[3];
	in
		tu([x, y, z]);

AUX_5_AGGR_(x) := 
		solSet(se([exp(x, nu("2"))]));

AUX_6_AGGR_(x)[i_] := 
	let
		b_ := AUX_5_AGGR_(x)[i_];
		y := b_[1];
	in
		starOp(x, y);

AUX_7_AGGR_ := 
		solSet(iv(nu("1"), nu("2")));

AUX_8_AGGR_[i_] := 
	let
		b_ := AUX_7_AGGR_[i_];
		x := b_[1];
	in
		aggrSum(AUX_6_AGGR_(x));

AUX_9_AGGR_ := 
		solSet(iv(nu("1"), unaryMinus(nu("1"))));

AUX_10_AGGR_[i_] := 
	let
		b_ := AUX_9_AGGR_[i_];
		x := b_[1];
	in
		exp(x, x);

AUX_11_AGGR_ := 
		solSet(iv(unaryMinus(nu("2")), nu("2")));

AUX_12_AGGR_(x) := 
		solGround(eq(md(x, nu("2")), nu("1")));

AUX_13_DEEP_[i1_, i2_] := 
	let
		workaround1_ := AUX_11_AGGR_;
		b1_ := workaround1_[i1_];
		x := b1_[1];
		workaround2_ := AUX_12_AGGR_(x);
		b2_ := workaround2_[i2_];
	in
		unnBinds(b1_, b2_);

AUX_13_AGGR_ := 
		join(AUX_13_DEEP_);

AUX_14_AGGR_[i_] := 
	let
		b_ := AUX_13_AGGR_[i_];
		x := b_[1];
	in
		se([pipesOp(x)]);

AUX_15_AGGR_(s, t) := 
		solEq(s);

AUX_16_AGGR_(s, t) := 
		solEq(t);

AUX_17_AGGR_(s, t) := 
		solDisj(AUX_15_AGGR_(s, t), AUX_16_AGGR_(s, t));

AUX_18_AGGR_(s, t)[i_] := 
	let
		b_ := AUX_17_AGGR_(s, t)[i_];
		x := b_[1];
	in
		se([exp(x, nu("2"))]);


