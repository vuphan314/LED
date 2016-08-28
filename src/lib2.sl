/* Easel required functions */

initialState: State;
initialState := valToState(initialState_);

newState: Input * State -> State;
newState(I, S) :=
    let
        v := newState_(I, S);
    in
        valToState(v);

images: State -> Image(1);
images(S) :=
    let
        v := images_(S);
    in
        valToImages(v);

/* default sound */
sounds: Input * State -> char(2);
sounds(I, S) := ["ding"] when I.iClick.clicked else [];

/* Easel template */
// State ::= (time: int);
// initialState := (time: 0);
// newState(I, S) := (time: S.time + 1);
// images(S) := [  text("Time: " ++ Conversion::intToString(S.time / 30),
                // point(500, 400), 30, dBlue)];
// sounds(I, S) := ["ding"] when I.iClick.clicked else [];
