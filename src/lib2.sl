/* todo test by Bryant */

// noinput := input(click(false, point(0, 0)), "");
// ni := noinput;

// main(args(2)) :=
    // newState(noinput, initialState);

// pointCell(c) := point(centerX(c), centerY(c));

/* easel required functions */

initialState: State;
initialState := valToState(initialState_);
is := initialState;

newState: Input * State -> State;
newState(I, S) :=
    let
        v := newState_(I, S);
    in
        valToState(v);
ns(I, S) := newState(I, S);

images: State -> Image(1);
images(S) :=
    let
        v := images_(S);
    in
        valToImages(v);

/* default sound */
sounds: Input * State -> char(2);
sounds(I, S) := ["ding"] when I.iClick.clicked else [];

/* easel template */
// State ::= (time: int);
// initialState := (time: 0);
// newState(I, S) := (time: S.time + 1);
// images(S) := [  text("Time: " ++ Conversion::intToString(S.time / 30),
                // point(500, 400), 30, dBlue)];
// sounds(I, S) := ["ding"] when I.iClick.clicked else [];
