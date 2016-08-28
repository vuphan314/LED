////////// ////////// ////////// ////////// ////////// //////////

import * from "../lib.sl" as *;

initialState_ := 
	se([]);

newState_(I, S) := 
	se([CURRENT_STATE_]);

images_(S) := 
	se([text_(st("hi"), point_(nu("500"), nu("500")), nu("50"), color_(nu("0"), nu("0"), nu("255")))]);

////////// ////////// ////////// ////////// ////////// //////////
