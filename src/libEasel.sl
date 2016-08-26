import <Utilities\\Conversion.sl>;

//region Types

Point ::= (x: int, y: int);

Color ::= (red: int, green: int, blue: int);

Image ::= ( kind: char(1), iColor: Color, vert1: Point, vert2: Point, vert3: Point,
            center: Point, radius: int, height: int, width: int, message: char(1),
            source: char(1));

Click ::= (clicked: bool, clPoint: Point);

Input ::= (iClick: Click, keys: char(1));

//endregion

//region Helpers======================================================================

//region Constructor-Functions-------------------------------------------------
point(a, b) := (x: a, y: b);
color(r, g, b) := (red: r, green: g, blue: b);
click(cl, p) := (clicked: cl, clPoint: p);
input(cl, k(1)) := (iClick: cl, keys: k);
segment(e1, e2, c) := (kind: "segment", vert1: e1, vert2: e2, iColor: c);
circle(ce, rad, c) := (kind: "circle", center: ce, radius: rad, iColor: c);
text(mes(1), cen, he, c) := 
    (kind: "text", center: cen, height: he, iColor: c, message: mes);
disc(ce, rad, c) := (kind: "disc", center: ce, radius: rad, iColor: c);
fTri(v1, v2, v3, c) := (kind: "triangle", vert1: v1, vert2: v2, vert3: v3, iColor: c);
graphic(graphicFile(1), c, w, h) := 
    (kind: "graphic", source: graphicFile, radius: 0, height: h, width: w, center: c);
//endregion----------------------------------------------------------------------

originPoint := point(0,0);

//region Colors----------------------------------------------------------------
dBlack := color(0, 0, 0);
dRed := color(255, 0, 0);
dOrange := color(255, 128, 0);
dYellow := color(255, 255, 0);
dGreen := color(0, 255, 0);
dBlue := color(0, 0, 255);
dIndigo := color(70, 0, 130);
dViolet := color(148, 0, 211);
dWhite := color(255, 255, 255);
//endregion----------------------------------------------------------------------

//endregion=============================================================================

//=================Easel=Functions=============================================

State ::= (time: int); //Fill in this struct with the game state members.

initialState := (time: 0);

newState: Input * State -> State;
newState(I, S) := (time: S.time + 1);

sounds(I, S) := ["ding"] when I.iClick.clicked else [];

images(S) := [  text("Time: " ++ Conversion::intToString(S.time / 30), 
                point(500, 400), 30, dBlue)];

//=============End=Easel=Functions=============================================
