////////// ////////// ////////// ////////// ////////// //////////

import * from "../libLED.sl" as *;

c := equiv(impl(disj(conj(tr(true), tr(false)), neg(eq(nu("1"), div(nu("2"), nu("2"))))), tr(false)), uneq(at("`a"), se([])));

////////// ////////// ////////// ////////// ////////// //////////

/** Copy/paste the block below into SequenceL interpreter to test:

pp(c)

(pp means PrettyPrint) */
