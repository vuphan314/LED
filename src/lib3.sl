/* todo test newState() manually */

pointCell: int -> Point;
pointCell(c) :=
    let
        v := intToVal(c);
        x := centerX(v);
        y := centerY(v);
        x2 := valToInt(x);
        y2 := valToInt(y);
    in
        point(x2, y2);

inputCell: int -> Input;
inputCell(c) :=
    let
        p := pointCell(c);
        cl := click(true, p);
    in
        input(cl, "");

ic(c) := inputCell(c);

is := initialState;

ns(I, S) := newState(I, S);

x1 := ns(ic(1), is);
o4 := ns(ic(4), x1);
x2 := ns(ic(2), o4);
o5 := ns(ic(5), x2);
x3 := ns(ic(3), o5);
