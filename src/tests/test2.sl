////////// ////////// ////////// ////////// ////////// //////////

import * from "../ledlib.sl" as *;

c0 := uneq(n("3"), n("5"));

c1 := greaterEq(uMns(n("2.(6..)")), mult(uMns(n("2")), n("1.(3..)")));

c2 := eq(a("`a"), a("`a"));

c3 := eq(a("`a"), a("`b"));

c4 := eq(tr(true), tr(false));

c5 := eq(tr(true), tr(true));

c6 := eq(tu([n("1"), n("2")]), tu([n("1"), n("2"), n("4")]));

c7 := eq(tu([n("1"), n("2")]), tu([n("1"), mult(n("2"), n("1"))]));

c8 := eq(s([n("1")]), s([s([n("1"), n("3")]), n("5")]));

c9 := eq(s([s([])]), s([s([]), s([])]));

c10 := uneq(tr(true), s([]));

////////// ////////// ////////// ////////// ////////// //////////
