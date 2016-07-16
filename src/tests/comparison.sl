////////// ////////// ////////// ////////// ////////// //////////

import * from "../ledlib.sl" as *;

c0 := uneq(nu("3"), nu("5"));

c1 := greaterEq(uMns(nu("2.(6..)")), mult(uMns(nu("2")), nu("1.(3..)")));

c2 := eq(at("`a"), at("`a"));

c3 := eq(at("`a"), at("`b"));

c4 := eq(tr(true), tr(false));

c5 := eq(tr(true), tr(true));

c6 := eq(tu([nu("1"), nu("2")]), tu([nu("1"), nu("2"), nu("4")]));

c7 := eq(tu([nu("1"), nu("2")]), tu([nu("1"), mult(nu("2"), nu("1"))]));

c8 := eq(se([nu("1")]), se([se([nu("1"), nu("3")]), nu("5")]));

c9 := eq(se([se([])]), se([se([]), se([])]));

c10 := uneq(tr(true), se([]));

////////// ////////// ////////// ////////// ////////// //////////
