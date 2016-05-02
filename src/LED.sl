// imports

import <Utilities/Conversion.sl>;
import <Utilities/Math.sl>;
import <Utilities/Sequence.sl>;
import <Utilities/Set.sl>;

// types

Val ::= (	type: char(1), 
			numb: int(1), truth: bool, 
			tup: Val(1), set: Val(1));			
			
// functions

/// helpers

//// constants

numb0 := [0, 1];

//// numeral

repBl: char(1) -> int(1);
repBl(bl(1)) :=
	let 
		ind1 := Sequence::firstIndexOf(bl, '(') + 1;
		ind2 := Sequence::firstIndexOf(bl, '.') - 1;
		trim := bl[ind1...ind2];
		patt := Conversion::stringToInt(trim);
		len := size(trim);
		div := subtr(exp([10, 1], [len, 1]), [1, 1]);
	in  red([patt, div[1]]) when size(bl) > 0 else
		numb0;

//// arithmetic

gcd: int(1) -> int;
gcd(n(1)) :=
	n[1] when n[2] = 0 else
	gcd([n[2], n[1] mod n[2]]);
	
red: int(1) -> int(1);
red(n(1)) :=
	let signN := product(Math::sign(n));
		absN := Math::abs(n);
		gcdAbsN := gcd(absN);
		redAbsN := absN / gcdAbsN;
	in [signN * redAbsN[1], redAbsN[2]];
	
numbSign: int(1) -> int;
numbSign(n(1)) := 
	let int1 := red(n)[1];
	in Math::sign(int1);
	
isInt: int(1) -> bool;
isInt(n(1)) := red(n)[2] = 1;

recipr: int(1) -> int(1);
recipr(n(1)) := red(Sequence::reverse(n));

nrvalList: int * int -> Val(1);
nrvalList(int1, int2)[i] :=
	let n := [i, 1];
	in (type: "Numb", numb: n)
	foreach i within int1...int2;

/// LED
	
//// arithmetic

add: int(1) * int(1) -> int(1);
add(n1(1), n2(1)) :=
	let int1 := n1[1] * n2[2] + n1[2] * n2[1];
		int2 := n1[2] * n2[2];
		numb := [int1, int2];
	in red(numb);
	
subtr: int(1) * int(1) -> int(1);
subtr(n1(1), n2(1)) := add(n1, uMinus(n2));

uMinus: int(1) -> int(1);
uMinus(n(1)) := red([-n[1], n[2]]);

prod: int(1) * int(1) -> int(1);
prod(n1(1), n2(1)) := red(n1 * n2);

quot: int(1) * int(1) -> int(1);
quot(n1(1), n2(1)) := prod(n1, recipr(n2));

flr: int(1) -> int(1);
flr(n(1)) := [n[1] / n[2], 1];

ceil: int(1) -> int(1);
ceil(n(1)) := 
	n when isInt(n) else
	[n[1] / n[2] + 1, 1];
	
ab: int(1) -> int(1);
ab(n(1)) := red(Math::abs(n));

md: int(1) * int(1) -> int(1);
md(n1(1), n2(1)) := [n1[1] mod n2[1], 1];

exp: int(1) * int(1) -> int(1);
exp(n1(1), n2(1)) :=
	let pow := n2[1];
	in  [1, 1] when pow = 0 else
		prod(n1, exp(n1, [pow - 1, 1])) when pow > 0 else
		exp(recipr(n1), uMinus(n2));
		
numbEq: int(1) * int(1) -> bool;
numbEq(n1(1), n2(1)) := not (numbL(n1, n2) or numbGr(n1, n2));
	
numbL: int(1) * int(1) -> bool;
numbL(n1(1), n2(1)) :=
	let diff := subtr(n1, n2);
	in numbSign(diff) < 0;

numbGr: int(1) * int(1) -> bool;
numbGr(n1(1), n2(1)) :=
	let diff := subtr(n1, n2);
	in numbSign(diff) > 0;
	
numbLEq: int(1) * int(1) -> bool;
numbLEq(n1(1), n2(1)) := numbL(n1, n2) or numbEq(n1, n2);
	
numbGrEq: int(1) * int(1) -> bool;
numbGrEq(n1(1), n2(1)) := numbGr(n1, n2) or numbEq(n1, n2);

nrval: int(1) * int(1) -> Val;
nrval(n1(1), n2(1)) :=
	let int1 := n1[1];
		int2 := n2[1];
		list := nrvalList(int1, int2);
	in (type: "set", set: list);	

//// set
	
biUnion: Val * Val -> Val;
biUnion(valSet1, valSet2) :=
	let	set1 := valSet1.set;
		set2 := valSet2.set;
	in (type: "Set", set: Set::union(set1, set2));
	
// tests

typeNumb := "Numb";

numbHalf := [1, 2];
valNumbHalf := (type: typeNumb, numb: numbHalf);

truthTrue := true;
valTruthTrue := (type: "bool", truth: truthTrue);

tupHalfTrue := [valNumbHalf, valTruthTrue];
valTupHalfTrue := (type: "Tup", tup: tupHalfTrue);

setValTupHalfTrue := [valTupHalfTrue];
valSetValTupHalfTrue := (type: "Set", set: setValTupHalfTrue);

setEmpty := [];
valSetEmpty := (type: "Set", set: setEmpty);

setValSetEmptyValTupHalfTrue := 
	(type: "Set", set: [valSetEmpty, valSetValTupHalfTrue]);
