////////// ////////// ////////// ////////// ////////// //////////

import * from "../libLED.sl" as *;

initialState := 
		se([]);

occupies(p, c) := 
		setMem(tu([p, c]), Gamma);

occupied(c) := 
		disj(occupies(at("`x"), c), occupies(at("`o"), c));

rows := 
	let
		hRows := se([se([nu("1"), nu("2"), nu("3")]), se([nu("4"), nu("5"), nu("6")]), se([nu("7"), nu("8"), nu("9")])]);
		vRows := se([se([nu("1"), nu("4"), nu("7")]), se([nu("2"), nu("5"), nu("8")]), se([nu("3"), nu("6"), nu("9")])]);
		diagonals := se([se([nu("1"), nu("5"), nu("9")]), se([nu("3"), nu("5"), nu("7")])]);
	in
		unn(unn(hRows, vRows), diagonals);

threeInRow(p) := 
		AUX_2_A_(p);

boardFull := 
		eq(pipesOp(Gamma), nu("9"));

gameOver := 
		disj(disj(boardFull, threeInRow(at("`x"))), threeInRow(at("`o")));

playerToMove := 
		at("`x") when valToTrth(even(pipesOp(Gamma))) else
		at("`o");

even(n) := 
		eq(md(n, nu("2")), nu("0"));

legalToMoveIn(c) := 
		conj(neg(occupied(c)), neg(gameOver));

BLACK := 
		color(nu("0"), nu("0"), nu("0"));

WHITE := 
		color(nu("255"), nu("255"), nu("255"));

BLUE := 
		color(nu("0"), nu("0"), nu("255"));

GREEN := 
		color(nu("0"), nu("255"), nu("0"));

RED := 
		color(nu("255"), nu("0"), nu("0"));

gridDisplay := 
	let
		L1 := segment(point(nu("200"), nu("700")), point(nu("200"), nu("400")), BLACK);
		L2 := segment(point(nu("300"), nu("700")), point(nu("300"), nu("400")), BLACK);
		L3 := segment(point(nu("100"), nu("600")), point(nu("400"), nu("600")), BLACK);
		L4 := segment(point(nu("100"), nu("500")), point(nu("400"), nu("500")), BLACK);
	in
		se([L1, L2, L3, L4]);

fontSize := 
		nu("36");

centerX(c) := 
		plusOp(nu("150"), starOp(nu("100"), md(bMns(c, nu("1")), nu("3"))));

centerO(c) := 
		bMns(nu("650"), starOp(nu("100"), flr(div(bMns(c, nu("1")), nu("3")))));

xImage(c) := 
		text("x", point(centerX(c), centerO(c)), fontSize, BLUE);

oImage(c) := 
		tetx("o", point(centerX(c), centerO(c)), fontSize, GREEN);

cellDisplay(c) := 
		se([xImage(c)]) when valToTrth(setMem(tu([at("`x"), c]), Gamma)) else
		se([oImage(c)]) when valToTrth(setMem(tu([at("`o"), c]), Gamma)) else
		se([]);

cellDisplays := 
		aggrUnn(AUX_4_AGGR_);

currentPlayerDisplay := 
		se([text("x's turn", point(nu("100"), nu("750")), fontSize, BLACK)]) when valToTrth(eq(currentPlayer, at("`x"))) else
		se([text("o's turn", point(nu("100"), nu("750")), fontSize, BLACK)]) when valToTrth(eq(currentPlayer, at("`o")));

restartButton := 
	let
		A1 := segment(point(nu("400"), nu("725")), point(nu("500"), nu("725")), BLACK);
		A2 := segment(point(nu("400"), nu("775")), point(nu("500"), nu("775")), BLACK);
		A3 := segment(point(nu("400"), nu("725")), point(nu("400"), nu("775")), BLACK);
		A4 := segment(point(nu("500"), nu("725")), point(nu("500"), nu("775")), BLACK);
		txt := text("restart", point(nu("450"), nu("750")), fontSize, BLACK);
	in
		se([A1, A2, A3, A4, txt]);

gameResultDisplay := 
		se([text("x won", point(nu("100"), nu("750")), fontSize, BLUE)]) when valToTrth(threeInRow(at("`x"))) else
		se([text("o won", point(nu("100"), nu("750")), fontSize, GREEN)]) when valToTrth(threeInRow(at("`o"))) else
		se([text("cat got it", point(nu("100"), nu("750")), fontSize, RED)]);

xMin(c) := 
		plusOp(nu("100"), starOp(nu("100"), md(bMns(c, nu("1")), nu("3"))));

xMax(c) := 
		plusOp(nu("200"), starOp(nu("100"), md(bMns(c, nu("1")), nu("3"))));

yMin(c) := 
		bMns(nu("600"), starOp(nu("100"), flr(div(bMns(c, nu("1")), nu("3")))));

yMax(c) := 
		bMns(nu("700"), starOp(nu("100"), flr(div(bMns(c, nu("1")), nu("3")))));

xCoord(pt) := 
		tuIn(pt, nu("1"));

yCoord(pt) := 
		tuIn(pt, nu("2"));

cellClicked(c) := 
		conj(conj(conj(conj(neg(eq(tuIn(click, nu("1")), at("`nil"))), greater(xCoord(click), xMin(c))), less(xCoord(click), xMax(c))), greater(yCoord(click), yMin(c))), less(yCoord(click), yMax(c)));

restartClicked := 
		conj(conj(conj(greater(xCoord(click), nu("400")), less(xCoord(click), nu("500"))), greater(yCoord(click), nu("725"))), less(yCoord(click), nu("775")));

moveMadeIn(c) := 
		conj(cellClicked(c), legalToMoveIn(c));

movesMade := 
		setCompr(AUX_8_AGGR_);

newState := 
		initialState when valToTrth(restartClicked) else
		unn(Gamma, movesMade);

/** AUXILIARY FUNCTIONS */

/** quantification 1 */

AUX_1_A_(p, R) := 
		allSet(AUX_1_B_(p, R));

AUX_1_B_(p, R)[i_] := 
		let
		c := AUX_1_C_(p, R)[i_];
	in
		occupies(p, c);

AUX_1_C_(p, R) := 
		valToSet(R);

/** quantification 2 */

AUX_2_A_(p) := 
		someSet(AUX_2_B_(p));

AUX_2_B_(p)[i_] := 
		let
		R := AUX_2_C_(p)[i_];
	in
		AUX_1_A_(p, R);

AUX_2_C_(p) := 
		valToSet(rows);

AUX_3_AGGR_ := 
		solSet(gameBoard);

AUX_4_AGGR_[i_] := 
		let
		b_ := AUX_3_AGGR_[i_];
		c := b_[1];
		gameBoard := b_[2];
	in
		cellDisplay(c);

AUX_5_AGGR_ := 
		solSet(iv(nu("1"), nu("9")));

AUX_6_AGGR_(c) := 
		solGround(moveMadeIn(c));

AUX_7_DEEP_[i1_, i2_] := 
		let
		b1_ := AUX_5_AGGR_[i1_];
		c := b1_[1];
		b2_ := AUX_6_AGGR_(c)[i2_];
	in
		unnBinds(b1_, b2_);

AUX_7_AGGR_ := 
		join(AUX_7_DEEP_);

AUX_8_AGGR_[i_] := 
		let
		b_ := AUX_7_AGGR_[i_];
		c := b_[1];
	in
		tu([playerToMove, c]);

////////// ////////// ////////// ////////// ////////// //////////

/** Copy/paste the block below into SequenceL interpreter to test:

pp(initialState)
pp(rows)
pp(boardFull)
pp(gameOver)
pp(playerToMove)
pp(BLACK)
pp(WHITE)
pp(BLUE)
pp(GREEN)
pp(RED)
pp(gridDisplay)
pp(fontSize)
pp(cellDisplays)
pp(currentPlayerDisplay)
pp(restartButton)
pp(gameResultDisplay)
pp(restartClicked)
pp(movesMade)
pp(newState)

(pp: pretty-print) */
