////////// ////////// ////////// ////////// ////////// //////////

import * from "../libLED.sl" as l::*;

c0 := l::uneq(l::nu("3"), l::nu("5"));

c1 := l::greaterEq(l::uMns(l::nu("2.(6..)")), l::mult(l::uMns(l::nu("2")), l::nu("1.(3..)")));

c2 := l::eq(l::at("`a"), l::at("`a"));

c3 := l::eq(l::at("`a"), l::at("`b"));

c4 := l::eq(l::tr(true), l::tr(false));

c5 := l::eq(l::tr(true), l::tr(true));

c6 := l::eq(l::tu([l::nu("1"), l::nu("2")]), l::tu([l::nu("1"), l::nu("2"), l::nu("4")]));

c7 := l::eq(l::tu([l::nu("1"), l::nu("2")]), l::tu([l::nu("1"), l::mult(l::nu("2"), l::nu("1"))]));

c8 := l::eq(l::se([l::nu("1")]), l::se([l::se([l::nu("1"), l::nu("3")]), l::nu("5")]));

c9 := l::eq(l::se([l::se([])]), l::se([l::se([]), l::se([])]));

c10 := l::uneq(l::tr(true), l::se([]));

////////// ////////// ////////// ////////// ////////// //////////
