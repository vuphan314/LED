////////// ////////// ////////// ////////// ////////// //////////

import * from "../libLED.sl" as l::*;

c := l::equiv(l::impl(l::disj(l::conj(l::tr(true), l::tr(false)), l::neg(l::eq(l::nu("1"), l::div(l::nu("2"), l::nu("2"))))), l::tr(false)), l::uneq(l::at("`a"), l::se([])));

////////// ////////// ////////// ////////// ////////// //////////
