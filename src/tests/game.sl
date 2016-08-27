////////// ////////// ////////// ////////// ////////// //////////

import * from "../lib.sl" as *;

initialState := 
		nu("0");

newState := 
		plusOp(Gamma, nu("1"));

images := 
		se([text("hi", point(nu("500"), nu("500")), nu("50"), dBlue)]);

////////// ////////// ////////// ////////// ////////// //////////

/** Copy/paste the block below into SequenceL interpreter to test:

pp(initialState)
pp(newState)
pp(images)

(pp: pretty-print) */
