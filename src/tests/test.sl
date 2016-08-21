////////// ////////// ////////// ////////// ////////// //////////

import * from "../libLED.sl" as *;

t := tu([nu("1"), nu("2"), nu("3")]);

t0 := tuSl(t, nu("1"), nu("2"));

t1 := tuSl(t, nu("1"), nu("1"));

t2 := tuSl(t, nu("2"), nu("1"));

////////// ////////// ////////// ////////// ////////// //////////

/** Copy/paste the block below into SequenceL interpreter to test:

pp(t)
pp(t0)
pp(t1)
pp(t2)

(pp means PrettyPrint) */
