/* Test with SequenceL interpreter:

pp(initialState_)
pp(rows)
pp(BLACK)
pp(WHITE)
pp(BLUE)
pp(GREEN)
pp(RED)
pp(gridDisplay)
pp(fontSize)
pp(gameBoard)
pp(restartLeft)
pp(restartRight)
pp(restartBottom)
pp(restartTop)
pp(restartBottomLeftPoint)
pp(restartBottomRightPoint)
pp(restartTopLeftPoint)
pp(restartTopRightPoint)
pp(restartMidX)
pp(restartMidY)
pp(restartButton)

(pp: pretty-print) */

initialState_ := 
		se([]);

occupies(p, c, S) := 
		setMem(tu([p, c]), currentState(S));

occupied(c, S) := 
		disj(occupies(at("`x"), c, S), occupies(at("`o"), c, S));

rows := 
	let
		hRows := se([se([nu("1"), nu("2"), nu("3")]), se([nu("4"), nu("5"), nu("6")]), se([nu("7"), nu("8"), nu("9")])]);
		vRows := se([se([nu("1"), nu("4"), nu("7")]), se([nu("2"), nu("5"), nu("8")]), se([nu("3"), nu("6"), nu("9")])]);
		diagonals := se([se([nu("1"), nu("5"), nu("9")]), se([nu("3"), nu("5"), nu("7")])]);
	in
		unn(unn(hRows, vRows), diagonals);

threeInRow(p, S) := 
		AUX_2_A_(p, S);

boardFull(S) := 
		eq(pipesOp(currentState(S)), nu("9"));

gameOver(S) := 
		disj(disj(boardFull(S), threeInRow(at("`x"), S)), threeInRow(at("`o"), S));

playerToMove(S) := 
		at("`x") when valToTrth(even(pipesOp(currentState(S)))) else
		at("`o");

even(n) := 
		eq(md(n, nu("2")), nu("0"));

legalToMoveIn(c, S) := 
		(valFalse when not valToTrth(neg(occupied(c, S))) else neg(gameOver(S)));

BLACK := 
		color_(nu("0"), nu("0"), nu("0"));

WHITE := 
		color_(nu("255"), nu("255"), nu("255"));

BLUE := 
		color_(nu("0"), nu("0"), nu("255"));

GREEN := 
		color_(nu("0"), nu("255"), nu("0"));

RED := 
		color_(nu("255"), nu("0"), nu("0"));

gridDisplay := 
	let
		L1 := segment_(point_(nu("200"), nu("700")), point_(nu("200"), nu("400")), BLACK);
		L2 := segment_(point_(nu("300"), nu("700")), point_(nu("300"), nu("400")), BLACK);
		L3 := segment_(point_(nu("100"), nu("600")), point_(nu("400"), nu("600")), BLACK);
		L4 := segment_(point_(nu("100"), nu("500")), point_(nu("400"), nu("500")), BLACK);
	in
		se([L1, L2, L3, L4]);

fontSize := 
		nu("36");

centerX(c) := 
		plusOp(nu("150"), starOp(nu("100"), md(binaryMinus(c, nu("1")), nu("3"))));

centerY(c) := 
		binaryMinus(nu("650"), starOp(nu("100"), flr(div(binaryMinus(c, nu("1")), nu("3")))));

xImage(c) := 
		text_(st("x"), point_(centerX(c), centerY(c)), fontSize, BLUE);

oImage(c) := 
		text_(st("o"), point_(centerX(c), centerY(c)), fontSize, GREEN);

cellDisplay(c, S) := 
		se([xImage(c)]) when valToTrth(setMem(tu([at("`x"), c]), currentState(S))) else
		se([oImage(c)]) when valToTrth(setMem(tu([at("`o"), c]), currentState(S))) else
		se([]);

gameBoard := 
		iv(nu("1"), nu("9"));

cellDisplays(S) := 
		aggrUnn(AUX_4_AGGR_(S));

currentPlayerDisplay(S) := 
		se([text_(st("x's turn"), point_(nu("100"), nu("750")), fontSize, BLACK)]) when valToTrth(eq(playerToMove(S), at("`x"))) else
		se([text_(st("o's turn"), point_(nu("100"), nu("750")), fontSize, BLACK)]);

restartLeft := 
		nu("350");

restartRight := 
		nu("550");

restartBottom := 
		nu("725");

restartTop := 
		nu("775");

restartBottomLeftPoint := 
		point_(restartLeft, restartBottom);

restartBottomRightPoint := 
		point_(restartRight, restartBottom);

restartTopLeftPoint := 
		point_(restartLeft, restartTop);

restartTopRightPoint := 
		point_(restartRight, restartTop);

mid(a, b) := 
		div(plusOp(a, b), nu("2"));

restartMidX := 
		mid(restartLeft, restartRight);

restartMidY := 
		mid(restartBottom, restartTop);

restartButton := 
	let
		A1 := segment_(restartBottomLeftPoint, restartBottomRightPoint, BLACK);
		A2 := segment_(restartTopLeftPoint, restartTopRightPoint, BLACK);
		A3 := segment_(restartBottomLeftPoint, restartTopLeftPoint, BLACK);
		A4 := segment_(restartBottomRightPoint, restartTopRightPoint, BLACK);
		txt := text_(st("restart"), point_(restartMidX, restartMidY), fontSize, BLACK);
	in
		se([A1, A2, A3, A4, txt]);

gameResultDisplay(S) := 
		se([text_(st("x won"), point_(nu("200"), nu("750")), fontSize, BLUE)]) when valToTrth(threeInRow(at("`x"), S)) else
		se([text_(st("o won"), point_(nu("200"), nu("750")), fontSize, GREEN)]) when valToTrth(threeInRow(at("`o"), S)) else
		se([text_(st("cat got it"), point_(nu("200"), nu("750")), fontSize, RED)]);

images_(S) := 
	let
		alwaysDisplay := unn(unn(gridDisplay, cellDisplays(S)), restartButton);
		inPlayDisplay := unn(alwaysDisplay, currentPlayerDisplay(S));
		gameOverDisplay := unn(alwaysDisplay, gameResultDisplay(S));
	in
		gameOverDisplay when valToTrth(gameOver(S)) else
		inPlayDisplay;

xMin(c) := 
		plusOp(nu("100"), starOp(nu("100"), md(binaryMinus(c, nu("1")), nu("3"))));

xMax(c) := 
		plusOp(nu("200"), starOp(nu("100"), md(binaryMinus(c, nu("1")), nu("3"))));

yMin(c) := 
		binaryMinus(nu("600"), starOp(nu("100"), flr(div(binaryMinus(c, nu("1")), nu("3")))));

yMax(c) := 
		binaryMinus(nu("700"), starOp(nu("100"), flr(div(binaryMinus(c, nu("1")), nu("3")))));

cellClicked(c, I) := 
		(valFalse when not valToTrth((valFalse when not valToTrth((valFalse when not valToTrth((valFalse when not valToTrth(mouseClicked(I)) else greater(mouseX(I), xMin(c)))) else less(mouseX(I), xMax(c)))) else greater(mouseY(I), yMin(c)))) else less(mouseY(I), yMax(c)));

restartClicked(I) := 
		(valFalse when not valToTrth((valFalse when not valToTrth((valFalse when not valToTrth((valFalse when not valToTrth(mouseClicked(I)) else greater(mouseX(I), restartLeft))) else less(mouseX(I), restartRight))) else greater(mouseY(I), restartBottom))) else less(mouseY(I), restartTop));

moveMadeIn(c, I, S) := 
		(valFalse when not valToTrth(cellClicked(c, I)) else legalToMoveIn(c, S));

movesMade(I, S) := 
		setCompr(AUX_8_AGGR_(I, S));

newState_(I, S) := 
		initialState_ when valToTrth(restartClicked(I)) else
		unn(currentState(S), movesMade(I, S));

/* AUXILIARY FUNCTIONS */

AUX_1_A_(p, S, R) := 
		allSet(AUX_1_B_(p, S, R));

AUX_1_B_(p, S, R)[i_] := 
	let
		c := AUX_1_C_(p, S, R)[i_];
	in
		occupies(p, c, S);

AUX_1_C_(p, S, R) := 
		valToSet(R);

AUX_2_A_(p, S) := 
		someSet(AUX_2_B_(p, S));

AUX_2_B_(p, S)[i_] := 
	let
		R := AUX_2_C_(p, S)[i_];
	in
		AUX_1_A_(p, S, R);

AUX_2_C_(p, S) := 
		valToSet(rows);

AUX_3_AGGR_(S) := 
		setMemSol(gameBoard);

AUX_4_AGGR_(S)[i_] := 
	let
		b_ := AUX_3_AGGR_(S)[i_];
		c := b_[1];
	in
		cellDisplay(c, S);

AUX_5_AGGR_(I, S) := 
		setMemSol(gameBoard);

AUX_6_AGGR_(I, S, c) := 
		groundSol(moveMadeIn(c, I, S));

AUX_7_DEEP_(I, S)[i1_, i2_] := 
	let
		workaround1_ := AUX_5_AGGR_(I, S);
		b1_ := workaround1_[i1_];
		c := b1_[1];
		workaround2_ := AUX_6_AGGR_(I, S, c);
		b2_ := workaround2_[i2_];
	in
		unnBindings(b1_, b2_);

AUX_7_AGGR_(I, S) := 
		join(AUX_7_DEEP_(I, S));

AUX_8_AGGR_(I, S)[i_] := 
	let
		b_ := AUX_7_AGGR_(I, S)[i_];
		c := b_[1];
	in
		tu([playerToMove(S), c]);



/*
Easel fragment
*/

/* easel required functions */

initialState: State;
initialState :=
    valToState(initialState_);

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

/* easel default sound */
sounds: Input * State -> char(2);
sounds(I, S) := ["ding"] when I.iClick.clicked else [];

/* ************************************************************************** */
/* SECTION START */

/* COPY OF led_lib.sl */

/* LED library written in SequenceL */

////////////////////////////////////////////////////////////////////////////////

import <Utilities/Conversion.sl>;
import <Utilities/Math.sl>;
import <Utilities/Sequence.sl>;
import <Utilities/Set.sl>;

////////////////////////////////////////////////////////////////////////////////

public
// pretty-print:
  prettyPrint, pp, prettyPrintState, pps,
// Easel:
  strgToVal,
// Easel types:
  Click, Image, Point,
// Easel paramters:
  Input, State,
// Easel helpers:
  currentState, valToState, valToImages,
  text_, point_, color_,
// LED types:
  Val, Numb,
// erroneous value:
  valNull,
// aggregation:
  setCompr, aggrUnn, aggrNrsec, aggrSum, aggrProd,
// solution (set):
  groundSol, eqSol, eqsSol, setMemSol, unnSols, unnBindings,
// quantification:
  someSet, allSet, valToSet,
// when-clauses:
  valToTrth,
// some values:
  valEmptySet, valTrue, valFalse, valZero, valOne, valTen,
// boolean:
  equiv, impl, disj, conj, neg,
// equality:
  eq, uneq,
// relational:
  less, greater, lessEq, greaterEq,
// overloaded:
  pipesOp, plusOp, starOp,
// set:
  setMem, sbset, unn, nrsec, diff, powSet,
// arithmetic:
  binaryMinus, unaryMinus, div, flr, clng, md, exp,
// tuple:
  tuIn, tuSl,
// to value:
  tu, // tuple
  se, // set
  iv, // interval
  st, // string
  at, // atom
  tr, // truth
  nu; // numeral

////////////////////////////////////////////////////////////////////////////////
/* erroneous value */

kindNull: char(1);
kindNull :=
  "null";

valNull: Val;
valNull :=
  (kindLed: kindNull);

////////////////////////////////////////////////////////////////////////////////
/* pretty-print */

prettyPrint: Val -> char(1);
prettyPrint(v) :=
  let
    s := valToStrg(v);
    a := valToAtm(v);
    numl := valToNuml(v);
    t := valToTrth(v);
    c := valToColl(v);
  in
    "ERRONEOUS VALUE"
      when valOfKind(v, kindNull) else
    s
      when valOfKind(v, kindStrg) else
    a
      when valOfKind(v, kindAtm) else
    numl
      when valOfKind(v, kindNumb) else
    Conversion::boolToString(t)
      when valOfKind(v, kindTrth) else
    prettyPrintColl(c, valToKind(v))
      when valOfKinds(v, kindsColl) else
    "an Easel " ++ valToKind(v)
      when valOfKinds(v, kindsEasel) else
    "CANNOT PRETTY-PRINT THIS TYPE";

pp: Val -> char(1);
pp(v) :=
  prettyPrint(v);

prettyPrintColl: Val(1) * char(1) -> char(1);
prettyPrintColl(vs(1), k(1)) :=
  let
    len := size(vs);
    isSet := equalList(k, kindSet);
    h := prettyPrint(head(vs));
    t := prettyPrintTail(tail(vs));
    s := h ++ join(t);
  in
    "{}" when isSet and len = 0 else
    "{" ++ s ++ "}" when isSet else
    "()" when len = 0 else
    "(" ++ s ++ ",)" when len = 1 else
    "(" ++ s ++ ")";

prettyPrintTail: Val(1) -> char(2);
prettyPrintTail(vs(1))[i] :=
  let
    v := vs[i];
    s := prettyPrint(v);
  in
    ", " ++ s;

////////////////////////////////////////////////////////////////////////////////
/* Easel */

/* Easel types */
Point ::= (x: int, y: int);
Color ::= (red: int, green: int, blue: int);
Image ::=
  (kind: char(1), iColor: Color,
  vert1: Point, vert2: Point, vert3: Point,
  center: Point, radius: int, height: int, width: int,
  message: char(1), source: char(1));
Click ::= (clicked: bool, clPoint: Point);
Input ::= (iClick: Click, keys: char(1));

/* Easel constructors */

point: int * int -> Point;
point(a, b) :=
  (x: a, y: b);

point_: Val * Val -> Val;
point_(v1, v2) :=
  let
    a := valToInt(v1);
    b := valToInt(v2);
    p := point(a, b);
  in
    pointToVal(p);

color: int * int * int -> Color;
color(r, g, b) :=
  (red: r, green: g, blue: b);

color_: Val * Val * Val -> Val;
color_(v1, v2, v3) :=
  let
    r := valToInt(v1);
    g := valToInt(v2);
    b := valToInt(v3);
    c := color(r, g, b);
  in
    colorToVal(c);

click: bool * Point -> Click;
click(cl, p) :=
  (clicked: cl, clPoint: p);

input: Click * char(1) -> Input;
input(cl, k(1)) :=
  (iClick: cl, keys: k);

segment: Point * Point * Color -> Image;
segment(e1, e2, c) :=
  (kind: "segment", vert1: e1, vert2: e2, iColor: c);

segment_: Val * Val * Val -> Val;
segment_(v1, v2, v3) :=
  let
    e1 := valToPoint(v1);
    e2 := valToPoint(v2);
    c := valToColor(v3);
    i := segment(e1, e2, c);
  in
    imageToVal(i);

circle: Point * int * Color -> Image;
circle(ce, rad, c) :=
  (kind: "circle", center: ce, radius: rad, iColor: c);

text: char(1) * Point * int * Color -> Image;
text(mes(1), cen, he, c) :=
  (kind: "text", center: cen, height: he,
  iColor: c, message: mes);

text_: Val * Val * Val * Val -> Val;
text_(v1, v2, v3, v4) :=
  let
    mes := valToStrg(v1);
    cen := valToPoint(v2);
    he := valToInt(v3);
    c := valToColor(v4);
    t := text(mes, cen, he, c);
  in
    imageToVal(t);

disc: Point * int * Color -> Image;
disc(ce, rad, c) :=
  (kind: "disc", center: ce, radius: rad, iColor: c);

fTri: Point * Point * Point * Color -> Image;
fTri(v1, v2, v3, c) :=
  (kind: "triangle", vert1: v1, vert2: v2, vert3: v3,
  iColor: c);

graphic: char(1) * Point * int * int -> Image;
graphic(graphicFile(1), c, w, h) :=
  (kind: "graphic", source: graphicFile, radius: 0,
  height: h, width: w, center: c);

/* Easel origin-point */
originPoint := point(0,0);

/* Easel colors */
dBlack := color(0, 0, 0);
dRed := color(255, 0, 0);
dOrange := color(255, 128, 0);
dYellow := color(255, 255, 0);
dGreen := color(0, 255, 0);
dBlue := color(0, 0, 255);
dIndigo := color(70, 0, 130);
dViolet := color(148, 0, 211);
dWhite := color(255, 255, 255);

/* type: Easel game-state */

State ::= (val: Val);

valToState: Val -> State;
valToState(v) :=
  (val: v);

stateToVal: State -> Val;
stateToVal(s) :=
  s.val;

prettyPrintState: State -> char(1);
prettyPrintState(s) :=
  prettyPrint(stateToVal(s));

pps: State -> char(1);
pps(s) :=
  prettyPrintState(s);

/* Easel global variables: Input/State -> Val */

currentState: State -> Val;
currentState(S) :=
  stateToVal(S);

mouseClicked: Input -> Val;
mouseClicked(I) :=
  let
    c := I.iClick;
    t := c.clicked;
  in
    trthToVal(t);

mouseX: Input -> Val;
mouseX(I) :=
  let
    c := I.iClick;
    p := c.clPoint;
    i := p.x;
  in
    intToVal(i);

mouseY: Input -> Val;
mouseY(I) :=
  let
    c := I.iClick;
    p := c.clPoint;
    i := p.y;
  in
    intToVal(i);

////////////////////////////////////////////////////////////////////////////////
/* value kinds: char(1) */

kindNumb := "numb";
kindTrth := "trth";
kindStrg := "strg";
kindAtm := "atm";
kindTpl := "tpl";
kindSet := "set";
kindPoint := "point";
kindColor := "color";
kindImage := "image";

////////////////////////////////////////////////////////////////////////////////
/* value kind-lists: char(2) */

kindsColl := [kindTpl, kindSet];
kindsEasel := [kindPoint, kindColor, kindImage];

////////////////////////////////////////////////////////////////////////////////
/* type: value */

Val ::=
  (kindLed: char(1),
  chars: char(1),
  numb: Numb, trth: bool, coll: Val(1),
  ePoint: Point, eColor: Color, eImage: Image); // Easel

valToKind: Val -> char(1);
valToKind(v) :=
  v.kindLed;

valOfKind: Val * char(1) -> bool;
valOfKind(v, k(1)) :=
  equalList(valToKind(v), k);

valOfKinds: Val * char(2) -> bool;
valOfKinds(v, ks(2)) :=
  some(valOfKind(v, ks));

valsOfKind: Val * Val * char(1) -> bool;
valsOfKind(v1, v2, k(1)) :=
  valOfKind(v1, k) and valOfKind(v2, k);

////////////////////////////////////////////////////////////////////////////////
/* value to thing */

valToTrth: Val -> bool;
valToTrth(v) :=
  v.trth;

valToNuml: Val -> char(1);
valToNuml(v) :=
  numbToNuml(valToNumb(v));

valToNumb: Val -> Numb;
valToNumb(v) :=
  v.numb;

valToStrg: Val -> char(1);
valToStrg(v) :=
  v.chars;

valToAtm: Val -> char(1);
valToAtm(v) :=
  v.chars;

valToColl: Val -> Val(1);
valToColl(v) :=
  v.coll;

valToTpl: Val -> Val(1);
valToTpl(v) :=
  valToColl(v);

valToSet: Val -> Val(1);
valToSet(v) :=
  valToColl(v);

valToPoint: Val -> Point;
valToPoint(v) :=
  v.ePoint;

valToColor: Val -> Color;
valToColor(v) :=
  v.eColor;

valToImage: Val -> Image;
valToImage(v) :=
  v.eImage;

valToImages: Val -> Image(1);
valToImages(v)[i] :=
  let
    vs := valToSet(v);
    v2 := vs[i];
  in
    valToImage(v2);

////////////////////////////////////////////////////////////////////////////////
/* thing to value */

numlToVal: char(1) -> Val;
numlToVal(n(1)) :=
  numbToVal(numlToNumb(n));

nu: char(1) -> Val;
nu(n(1)) :=
  numlToVal(n);

numbToVal: Numb -> Val;
numbToVal(n) :=
  (kindLed: kindNumb, numb: n);

trthToVal: bool -> Val;
trthToVal(t) :=
  (kindLed: kindTrth, trth: t);

tr: bool -> Val;
tr(t) :=
  trthToVal(t);

strgToVal: char(1) -> Val;
strgToVal(s(1)) :=
  (kindLed: kindStrg, chars: s);

st: char(1) -> Val;
st(s(1)) :=
  strgToVal(s);

atmToVal: char(1) -> Val;
atmToVal(a(1)) :=
  (kindLed: kindAtm, chars: a);

at: char(1) -> Val;
at(a(1)) :=
  atmToVal(a);

tplToVal: Val(1) -> Val;
tplToVal(t(1)) :=
  (kindLed: kindTpl, coll: t);

tu: Val(1) -> Val;
tu(t(1)) :=
  tplToVal(t);

setToVal: Val(1) -> Val;
setToVal(s(1)) :=
  (kindLed: kindSet, coll: removeDups(s));

se: Val(1) -> Val;
se(s(1)) :=
  setToVal(s);

pointToVal: Point -> Val;
pointToVal(p) :=
  (kindLed: kindPoint, ePoint: p);

colorToVal: Color -> Val;
colorToVal(c) :=
  (kindLed: kindColor, eColor: c);

imageToVal: Image -> Val;
imageToVal(i) :=
  (kindLed: kindImage, eImage: i);

////////////////////////////////////////////////////////////////////////////////
/* aggregation */

setCompr: Val(1) -> Val;
setCompr(vs(1)) :=
  setToVal(vs);

aggrUnn: Val(1) -> Val;
aggrUnn(vs(1)) :=
  valEmptySet when size(vs) = 0 else
  Sequence::fold(vs, unn);

aggrNrsec: Val(1) -> Val;
aggrNrsec(vs(1)) :=
  valEmptySet when size(vs) = 0 else
  Sequence::fold(vs, nrsec);

aggrSum: Val(1) -> Val;
aggrSum(vs(1)) :=
  valZero when size(vs) = 0 else
  Sequence::fold(vs, add);

aggrProd: Val(1) -> Val;
aggrProd(vs(1)) :=
  valOne when size(vs) = 0 else
  Sequence::fold(vs, mult);

////////////////////////////////////////////////////////////////////////////////
/* solution (set) */

groundSol: Val -> Val(2);
groundSol(v) :=
  let
    isTrue := valToTrth(v);
  in
    [[]] when isTrue else [];

eqSol: Val -> Val(2);
eqSol(v) :=
  [[v]];

eqsSol: Val -> Val(2);
eqsSol(v) :=
  [valToTpl(v)];

setMemSol: Val -> Val(2);
setMemSol(v)[i] :=
  let
    vs := valToSet(v);
  in
    [vs[i]];

unnSols: Val(2) * Val(2) -> Val(2);
unnSols(s1(2), s2(2)) :=
  removeDups(s1 ++ s2);

unnBindings: Val(1) * Val(1) -> Val(1);
unnBindings(b1(1), b2(1)) :=
  b1 ++ b2;

////////////////////////////////////////////////////////////////////////////////
/* quantification */

someSet: Val(1) -> Val;
someSet(vs(1)) :=
  let
    n := size(vs);
    h := head(vs);
    t := tail(vs);
  in
    valFalse when n = 0 else
    h when n = 1 else
    disj(h, someSet(t));

allSet: Val(1) -> Val;
allSet(vs(1)) :=
  let
    n := size(vs);
    h := head(vs);
    t := tail(vs);
  in
    valTrue when n = 0 else
    h when n = 1 else
    conj(h, allSet(t));

////////////////////////////////////////////////////////////////////////////////
/* tuple operations */

tuConc: Val * Val -> Val;
tuConc(v1, v2) :=
  let
    t1 := valToTpl(v1);
    t2 := valToTpl(v2);
    t := t1 ++ t2;
  in
    tplToVal(t);

tuIn: Val * Val -> Val;
tuIn(valT, valI) :=
  let
    tplT := valToTpl(valT);
    intI := valToInt(valI);
  in
    tplT[intI];

tuSl: Val * Val * Val -> Val;
tuSl(valT, valI1, valI2) :=
  let
    t := valToTpl(valT);
    i1 := valToInt(valI1);
    i2 := valToInt(valI2);
    t2 := t[i1...i2];
  in
    tplToVal(t2);

tuLen: Val -> Val;
tuLen(v) :=
  let
    t := valToTpl(v);
    n := size(t);
  in
    intToVal(n);

////////////////////////////////////////////////////////////////////////////////
/* equality operations */

eq: Val * Val -> Val;
eq(v1, v2) :=
  trthToVal(trthEq(v1, v2));

uneq: Val * Val -> Val;
uneq(v1, v2) :=
  trthToVal(not trthEq(v1, v2));

trthEq: Val * Val -> bool;
trthEq(v1, v2) :=
  let
    n1 := valToNumb(v1); n2 := valToNumb(v2);
    a1 := valToAtm(v1); a2 := valToAtm(v2);
    tr1 := valToTrth(v1); tr2 := valToTrth(v2);
    c1 := valToColl(v1); c2 := valToColl(v2);
  in
    eqNumb(n1, n2)
      when valsOfKind(v1, v2, kindNumb) else
    equalList(a1, a2)
      when valsOfKind(v1, v2, kindAtm) else
    tr1 = tr2
      when valsOfKind(v1, v2, kindTrth) else
    equalList(c1, c2)
      when valsOfKind(v1, v2, kindTpl) else
    equalSet(c1, c2)
      when valsOfKind(v1, v2, kindSet) else
    false;

eqNumb: Numb * Numb -> bool;
eqNumb(numb1, numb2) :=
  sgn(binaryMinusNumb(numb1, numb2)) = 0;

////////////////////////////////////////////////////////////////////////////////
/* relational operations */

less: Val * Val -> Val;
less(v1, v2) :=
  stdNumbNumbToTrth(lessNumb, v1, v2);

lessNumb: Numb * Numb -> bool;
lessNumb(numb1, numb2) :=
  sgn(binaryMinusNumb(numb1, numb2)) < 0;

greater: Val * Val -> Val;
greater(v1, v2) :=
  stdNumbNumbToTrth(greaterNumb, v1, v2);

greaterNumb: Numb * Numb -> bool;
greaterNumb(numb1, numb2) :=
  not (lessNumb(numb1, numb2) or eqNumb(numb1, numb2));

lessEq: Val * Val -> Val;
lessEq(v1, v2) :=
  stdNumbNumbToTrth(lessEqNumb, v1, v2);

lessEqNumb: Numb * Numb -> bool;
lessEqNumb(numb1, numb2) :=
  lessNumb(numb1, numb2) or eqNumb(numb1, numb2);

greaterEq: Val * Val -> Val;
greaterEq(v1, v2) :=
  stdNumbNumbToTrth(greaterEqNumb, v1, v2);

greaterEqNumb: Numb * Numb -> bool;
greaterEqNumb(numb1, numb2) :=
  greaterNumb(numb1, numb2) or eqNumb(numb1, numb2);

////////////////////////////////////////////////////////////////////////////////
/* overloaded operations */

plusOp: Val * Val -> Val;
plusOp(v1, v2) :=
  add(v1, v2) when valsOfKind(v1, v2, kindNumb) else
  tuConc(v1, v2) when valsOfKind(v1, v2, kindTpl) else
  valNull;

starOp: Val * Val -> Val;
starOp(v1, v2) :=
  mult(v1, v2) when valsOfKind(v1, v2, kindNumb) else
  cross(v1, v2) when valsOfKind(v1, v2, kindSet) else
  valNull;

pipesOp: Val -> Val;
pipesOp(v) :=
  ab(v) when valOfKind(v, kindNumb) else
  card(v) when valOfKind(v, kindSet) else
  tuLen(v) when valOfKind(v, kindTpl) else
  valNull;

////////////////////////////////////////////////////////////////////////////////
/* set operations (value) */

setMem: Val * Val -> Val;
setMem(v1, v2) :=
  stdValSetToTrth(setMemSet, v1, v2);

sbset: Val * Val -> Val;
sbset(v1, v2) :=
  stdSetSetToTrth(sbsetSet, v1, v2);

unn: Val * Val -> Val;
unn(v1, v2) :=
  stdSetSetToSet(unnSet, v1, v2);

nrsec: Val * Val -> Val;
nrsec(v1, v2) :=
  stdSetSetToSet(nrsecSet, v1, v2);

diff: Val * Val -> Val;
diff(v1, v2) :=
  stdSetSetToSet(diffSet, v1, v2);

cross: Val * Val -> Val;
cross(v1, v2) :=
  stdSetSetToSet(crossSet, v1, v2);

powSet: Val -> Val;
powSet(v) :=
  stdSetToSet(powSetSet, v);

card: Val -> Val;
card(v) :=
  stdSetToInt(cardSet, v);

////////////////////////////////////////////////////////////////////////////////
/* boolean operations (value) */

equiv: Val * Val -> Val;
equiv(v1, v2) :=
  stdTrthTrthToTrth(equivTrth, v1, v2);

impl: Val * Val -> Val;
impl(v1, v2) :=
  stdTrthTrthToTrth(implTrth, v1, v2);

disj: Val * Val -> Val;
disj(v1, v2) :=
  stdTrthTrthToTrth(disjTrth, v1, v2);

conj: Val * Val -> Val;
conj(v1, v2) :=
  stdTrthTrthToTrth(conjTrth, v1, v2);

neg: Val -> Val;
neg(v) :=
  stdTrthToTrth(negTrth, v);

////////////////////////////////////////////////////////////////////////////////
/* arithmetic operations (value) */

add: Val * Val -> Val;
add(v1, v2) :=
  stdNumbNumbToNumb(addNumb, v1, v2);

binaryMinus: Val * Val -> Val;
binaryMinus(v1, v2) :=
  stdNumbNumbToNumb(binaryMinusNumb, v1, v2);

unaryMinus: Val -> Val;
unaryMinus(v) :=
  stdNumbToNumb(unaryMinusNumb, v);

mult: Val * Val -> Val;
mult(v1, v2) :=
  stdNumbNumbToNumb(multNumb, v1, v2);

div: Val * Val -> Val;
div(v1, v2) :=
  stdNumbNumbToNumb(divNumb, v1, v2);

flr: Val -> Val;
flr(v) :=
  stdNumbToInt(flrNumb, v);

clng: Val -> Val;
clng(v) :=
  stdNumbToInt(clngNumb, v);

ab: Val -> Val;
ab(v) :=
  stdNumbToNumb(abNumb, v);

md: Val * Val -> Val;
md(v1, v2) :=
  stdIntIntToInt(mdNumb, v1, v2);

exp: Val * Val -> Val;
exp(v1, v2) :=
  stdNumbIntToNumb(expNumb, v1, v2);

////////////////////////////////////////////////////////////////////////////////
/* interval */

intervalToVal: Val * Val -> Val;
intervalToVal(v1, v2) :=
  let
    i1 := valToInt(v1);
    i2 := valToInt(v2);
    s := twoIntsToSet(i1, i2);
  in
    setToVal(s);

iv: Val * Val -> Val;
iv(v1, v2) :=
  intervalToVal(v1, v2);

twoIntsToSet: int32 * int32 -> Val(1);
twoIntsToSet(i1, i2)[ind] :=
  intToVal(ind) foreach ind within i1...i2;

////////////////////////////////////////////////////////////////////////////////
/* type: number */

Numb ::= (Numr: int32, Denr: int32);

twoIntsToNumbRed: int32 * int32 -> Numb;
twoIntsToNumbRed(i1, i2) :=
  reduce(i1, i2);

twoIntsToNumb: int32 * int32 -> Numb;
twoIntsToNumb(i1, i2) :=
  (Numr: i1, Denr: i2);

numbToNumr: Numb -> int32;
numbToNumr(numb) :=
  numb.Numr;

numbToDenr: Numb -> int32;
numbToDenr(numb) :=
  numb.Denr;

////////////////////////////////////////////////////////////////////////////////
/* pseudotype: integer */

numbIsInt: Numb -> bool;
numbIsInt(numb) :=
  numbToDenr(numb) = 1;

intToNumb: int32 -> Numb;
intToNumb(i) :=
  twoIntsToNumb(i, 1);

numbToInt: Numb -> int32;
numbToInt(numb) :=
  numbToNumr(numb);

intToVal: int32 -> Val;
intToVal(i) :=
  numbToVal(intToNumb(i));

valToInt: Val -> int32;
valToInt(v) :=
  numbToInt(valToNumb(v));

////////////////////////////////////////////////////////////////////////////////
/* some values: Val */

valEmptySet := setToVal([]);

valTrue := trthToVal(true);
valFalse := trthToVal(false);

valZero := numbToVal(numbZero);
valOne := numbToVal(numbOne);
valTen := numbToVal(numbTen);

////////////////////////////////////////////////////////////////////////////////
/* some numbers: Numb */

numbZero := intToNumb(0);
numbOne := intToNumb(1);
numbTen := intToNumb(10);

////////////////////////////////////////////////////////////////////////////////
/* arithmetic helper functions */

recipr: Numb -> Numb;
recipr(numb) :=
  twoIntsToNumbRed(numbToDenr(numb), numbToNumr(numb));

sgn: Numb -> int8;
sgn(numb) :=
  Math::sign(numbToNumr(numb));

reduce: int32 * int32 -> Numb;
reduce(i1, i2) :=
  let
    signOfNumb := Math::sign(i1) * Math::sign(i2);
    absNumr := Math::abs(i1);
    absDenr := Math::abs(i2);
    gcdNumb := gcd(absNumr, absDenr);
    redAbsNumr := absNumr / gcdNumb;
    redAbsDenr := absDenr / gcdNumb;
    redNumr := signOfNumb * redAbsNumr;
  in
    twoIntsToNumb(redNumr, redAbsDenr);

gcd: int32 * int32 -> int32;
gcd(i1, i2) :=
  i1 when i2 = 0 else
  gcd(i2, i1 mod i2);

////////////////////////////////////////////////////////////////////////////////
/* number to numeral */

numbToNuml: Numb -> char(1);
numbToNuml(numb) :=
  let
    negative := sgn(numb) < 0;
    absNumr := Math::abs(numbToNumr(numb));
    denr := numbToDenr(numb);
  in
    "-" ++ getAbsNuml(absNumr, denr) when negative else
    getAbsNuml(absNumr, denr);

getAbsNuml: int32 * int32 -> char(1);
getAbsNuml(absNumr, denr) :=
  let
    integralPart := Conversion::intToString(absNumr / denr);
    minAbsNumr := absNumr mod denr;
  in
    integralPart when minAbsNumr = 0 else
    integralPart ++ getFr(minAbsNumr, denr);

getFr: int32 * int32 -> char(1);
getFr(minAbsNumr, denr) :=
  let
    remsQuots := getRemsQuots(denr, [minAbsNumr], []);
    rems := remsQuots.l1;
    lastRem := Sequence::last(rems);
    rep := lastRem /= 0;
    repRemPos := Sequence::firstIndexOf(rems, lastRem);
    quots := remsQuots.l2;
  in
    getFrRep(repRemPos, quots) when rep else
    getFrNRep(quots);

getFrRep: int32 * int32(1) -> char(1);
getFrRep(repRemPos, quots(1)) :=
  let
    nRepQuots := Sequence::take(quots, repRemPos - 1);
    repQuots := Sequence::drop(quots, repRemPos - 1);
  in
    getFrNRep(nRepQuots) ++ getRepBl(repQuots);

getRepBl: int32(1) -> char(1);
getRepBl(repQuots(1)) :=
  "(" ++ getIntNuml(repQuots) ++ "..)";

getFrNRep: int32(1) -> char(1);
getFrNRep(quots(1)) :=
  "." ++ getIntNuml(quots);

getIntNuml: int32(1) -> char(1);
getIntNuml(quots(1)) :=
  join(Conversion::intToString(quots));

getRemsQuots: int32 * int32(1) * int32(1) -> TwoIntLists;
getRemsQuots(divisor, rems(1), quots(1)) :=
  let
    dividend := Sequence::last(rems) * 10;
    rem := dividend mod divisor;
    rems2 := rems ++ [rem];
    quot := dividend / divisor;
    quots2 := quots ++ [quot];
    posRem := Sequence::firstIndexOf(rems, rem);
    rep := posRem > 0;
  in
    (l1: rems2, l2: quots2) when rem = 0 or rep else
    getRemsQuots(divisor, rems2, quots2);

TwoIntLists ::= (l1: int32(1), l2: int32(1));

////////////////////////////////////////////////////////////////////////////////
/* numeral to number */

numlToNumb: char(1) -> Numb;
numlToNumb(numl(1)) :=
  let
    dot := Sequence::firstIndexOf(numl, '.');
    iN := Sequence::take(numl, dot - 1);
    f := Sequence::drop(numl, dot - 1);
    numbIN := intNumlToNumb(iN);
    numbF := frToNumb(f);
  in
    intNumlToNumb(numl) when dot = 0 else
    frToNumb(numl) when dot = 1 else
    addNumb(numbIN, numbF);

frToNumb: char(1) -> Numb;
frToNumb(f(1)) :=
  let
    lParenth := Sequence::firstIndexOf(f, '(');
  in
    frNRepToNumb(f) when lParenth = 0 else
    frRepToNumb(f);

frRepToNumb: char(1) -> Numb;
frRepToNumb(fR(1)) :=
  let
    lParenth := Sequence::firstIndexOf(fR, '(');
    fNR := Sequence::take(fR, lParenth - 1);
    numbFNR := frNRepToNumb(fNR);
    shift := size(fNR) - 1;
    factor := expNumb(numbTen, -shift);
    rB := Sequence::drop(fR, lParenth - 1);
    numbRB := multNumb(factor, repBlToNumb(rB));
  in
    addNumb(numbFNR, numbRB);

repBlToNumb: char(1) -> Numb;
repBlToNumb(rB(1)) :=
  let
    iN := rB[2 ... size(rB) - 3];
    rept := intNumlToNumb(iN);
    lenRept := size(iN);
    divisor := binaryMinusNumb(expNumb(numbTen, lenRept),
      numbOne);
  in
    divNumb(rept, divisor);

frNRepToNumb: char(1) -> Numb;
frNRepToNumb(fNR(1)) :=
  let
    iN := Sequence::drop(fNR, 1);
    lenIN := size(iN);
    factor := expNumb(numbTen, -lenIN);
  in
    multNumb(factor, intNumlToNumb(iN));

intNumlToNumb: char(1) -> Numb;
intNumlToNumb(iN(1)) :=
  intToNumb(Conversion::stringToInt(iN));

////////////////////////////////////////////////////////////////////////////////
/* standardizer functions */

stdValSetToTrth: (Val * Val(1) -> bool) * Val * Val -> Val;
stdValSetToTrth(f, v, v2) :=
  let
    s := valToSet(v2);
    t := f(v, s);
  in
    trthToVal(t);

stdSetSetToTrth: (Val(1) * Val(1) -> bool) * Val * Val ->
  Val;
stdSetSetToTrth(f, v1, v2) :=
  let
    s1 := valToSet(v1);
    s2 := valToSet(v2);
    t := f(s1, s2);
  in
    trthToVal(t);

stdSetSetToSet: (Val(1) * Val(1) -> Val(1)) * Val * Val ->
  Val;
stdSetSetToSet(f, v1, v2) :=
  let
    s1 := valToSet(v1);
    s2 := valToSet(v2);
    s := f(s1, s2);
  in
    setToVal(s);

stdSetToSet: (Val(1) -> Val(1)) * Val -> Val;
stdSetToSet(f, v) :=
  let
    s := valToSet(v);
    s2 := f(s);
  in
    setToVal(s2);

stdSetToInt: (Val(1) -> int32) * Val -> Val;
stdSetToInt(f, v) :=
  let
    s := valToSet(v);
    i := f(s);
  in
    intToVal(i);

stdTrthTrthToTrth: (bool * bool -> bool) * Val * Val -> Val;
stdTrthTrthToTrth(f, v1, v2) :=
  let
    t1 := valToTrth(v1);
    t2 := valToTrth(v2);
    t := f(t1, t2);
  in
    trthToVal(t);

stdTrthToTrth: (bool -> bool) * Val -> Val;
stdTrthToTrth(f, v) :=
  let
    t := valToTrth(v);
    t2 := f(t);
  in
    trthToVal(t2);

stdNumbNumbToTrth: (Numb * Numb -> bool) * Val * Val -> Val;
stdNumbNumbToTrth(f, v1, v2) :=
  let
    n1 := valToNumb(v1);
    n2 := valToNumb(v2);
    t := f(n1, n2);
  in
    trthToVal(t);

stdNumbNumbToNumb: (Numb * Numb -> Numb) * Val * Val -> Val;
stdNumbNumbToNumb(f, v1, v2) :=
  let
    n1 := valToNumb(v1);
    n2 := valToNumb(v2);
    n := f(n1, n2);
  in
    numbToVal(n);

stdNumbToNumb: (Numb -> Numb) * Val -> Val;
stdNumbToNumb(f, v) :=
  let
    n := valToNumb(v);
    n2 := f(n);
  in
    numbToVal(n2);

stdNumbToInt: (Numb -> int32) * Val -> Val;
stdNumbToInt(f, v) :=
  let
    n := valToNumb(v);
    i := f(n);
    n2 := intToNumb(i);
  in
    numbToVal(n2);

stdIntIntToInt: (int32 * int32 -> int32) * Val * Val -> Val;
stdIntIntToInt(f, v1, v2) :=
  let
    i1 := valToInt(v1);
    i2 := valToInt(v2);
    i := f(i1, i2);
  in
    intToVal(i);

stdNumbIntToNumb: (Numb * int32 -> Numb) * Val * Val -> Val;
stdNumbIntToNumb(f, v1, v2) :=
  let
    n := valToNumb(v1);
    i := valToInt(v2);
    n2 := f(n, i);
  in
    numbToVal(n2);

////////////////////////////////////////////////////////////////////////////////
/* set operations (non-value) */

setMemSet: Val * Val(1) -> bool;
setMemSet(v, vs(1)) :=
  Set::elementOf(v, vs);

sbsetSet: Val(1) * Val(1) -> bool;
sbsetSet(v1(1), v2(1)) :=
  subset(v1, v2);

unnSet: Val(1) * Val(1) -> Val(1);
unnSet(v1(1), v2(1)) :=
  Set::union(v1, v2);

nrsecSet: Val(1) * Val(1) -> Val(1);
nrsecSet(v1(1), v2(1)) :=
  Set::intersection(v1, v2);

diffSet: Val(1) * Val(1) -> Val(1);
diffSet(v1(1), v2(1))[i] :=
  let
    v := v1[i];
  in
    v when not setMemSet(v, v2);

crossSet: Val(1) * Val(1) -> Val(1);
crossSet(v1(1), v2(1)) :=
  let
    collSet := Set::cartesianProduct(v1, v2);
  in
    collSetToValSet(collSet, kindTpl);

powSetSet: Val(1) -> Val(1);
powSetSet(v(1)) :=
  let
    collSet := Set::powerSet(v);
  in
    collSetToValSet(collSet, kindSet);

collSetToValSet: Val(2) * char(1) -> Val(1);
collSetToValSet(M(2), k(1))[i] :=
  let
    c := M[i];
  in
    tplToVal(c) when equalList(k, kindTpl) else
    setToVal(c);

cardSet: Val(1) -> int32;
cardSet(v(1)) :=
  size(v);

////////////////////////////////////////////////////////////////////////////////
/* boolean operations (truth) */

equivTrth: bool * bool -> bool;
equivTrth(t1, t2) :=
  let
    if := implTrth(t1, t2);
    onlyIf := implTrth(t2, t1);
  in
    conjTrth(if, onlyIf);

implTrth: bool * bool -> bool;
implTrth(t1, t2) :=
  disjTrth(negTrth(t1), t2);

disjTrth: bool * bool -> bool;
disjTrth(t1, t2) :=
  true when t1 else
  t2;

conjTrth: bool * bool -> bool;
conjTrth(t1, t2) :=
  false when not t1 else
  t2;

negTrth: bool -> bool;
negTrth(t) :=
  not t;

////////////////////////////////////////////////////////////////////////////////
/* arithmetic operations (number) */

addNumb: Numb * Numb -> Numb;
addNumb(numb1, numb2) :=
  let
    numr :=
      numbToNumr(numb1) * numbToDenr(numb2) +
      numbToDenr(numb1) * numbToNumr(numb2);
    denr := numbToDenr(numb1) * numbToDenr(numb2);
  in
    twoIntsToNumbRed(numr, denr);

binaryMinusNumb: Numb * Numb -> Numb;
binaryMinusNumb(numb1, numb2) :=
  addNumb(numb1, unaryMinusNumb(numb2));

unaryMinusNumb: Numb -> Numb;
unaryMinusNumb(numb) :=
  twoIntsToNumbRed(-numbToNumr(numb), numbToDenr(numb));

multNumb: Numb * Numb -> Numb;
multNumb(numb1, numb2) :=
  let
    numr := numbToNumr(numb1) * numbToNumr(numb2);
    denr := numbToDenr(numb1) * numbToDenr(numb2);
  in
    twoIntsToNumbRed(numr, denr);

divNumb: Numb * Numb -> Numb;
divNumb(numb1, numb2) :=
  multNumb(numb1, recipr(numb2));

flrNumb: Numb -> int32;
flrNumb(numb) :=
  let
    quot := numbToNumr(numb) / numbToDenr(numb);
    badCase := not numbIsInt(numb) and sgn(numb) < 0;
  in
    quot - 1 when badCase else
    quot;

clngNumb: Numb -> int32;
clngNumb(numb) :=
  numbToInt(numb) when numbIsInt(numb) else
  flrNumb(numb) + 1;

abNumb: Numb -> Numb;
abNumb(numb) :=
  twoIntsToNumbRed(Math::abs(numbToNumr(numb)),
    numbToDenr(numb));

mdNumb: int32 * int32 -> int32;
mdNumb(i1, i2) :=
  i1 mod i2;

expNumb: Numb * int32 -> Numb;
expNumb(numb, p) :=
  let
    numr := numbToNumr(numb);
    denr := numbToDenr(numb);
  in
    expTwoInts(numr, denr, p);

expTwoInts: int32 * int32 * int32 -> Numb;
expTwoInts(numr, denr, p) :=
  let
    numr2 := Math::integerPower(numr, p);
    denr2 := Math::integerPower(denr, p);
  in
    twoIntsToNumb(numr2, denr2) when p >= 0 else
    expTwoInts(denr, numr, -p);

/* SECTION END */
/* ************************************************************************** */


