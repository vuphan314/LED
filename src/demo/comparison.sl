/* Test with SequenceL interpreter:

pp(c0)
pp(c1)
pp(c2)
pp(c3)
pp(c4)
pp(c5)
pp(c6)
pp(c7)
pp(c8)
pp(c9)
pp(c10)

(pp: pretty-print) */

import * from "../led_lib.sl" as *;

c0 := 
		uneq(nu("3"), nu("5"));

c1 := 
		greaterEq(unaryMinus(nu("2.(6..)")), starOp(unaryMinus(nu("2")), nu("1.(3..)")));

c2 := 
		eq(at("`a"), at("`a"));

c3 := 
		eq(at("`a"), at("`b"));

c4 := 
		eq(tr(true), tr(false));

c5 := 
		eq(tr(true), tr(true));

c6 := 
		eq(tu([nu("1"), nu("2")]), tu([nu("1"), nu("2"), nu("4")]));

c7 := 
		eq(tu([nu("1"), nu("2")]), tu([nu("1"), starOp(nu("2"), nu("1"))]));

c8 := 
		eq(se([nu("1")]), se([se([nu("1"), nu("3")]), nu("5")]));

c9 := 
		eq(se([se([])]), se([se([]), se([])]));

c10 := 
		uneq(tr(true), se([]));


