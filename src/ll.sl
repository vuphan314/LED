/* exports */

public  numeral,
        add, biMinus, uMinus, mult, div, flr, clng, ab, md, exp;

/* imports */

import <Utilities/Conversion.sl>;
import <Utilities/Math.sl>;
import <Utilities/Sequence.sl>;
import <Utilities/Set.sl>;

/* types */

// Value ::= (kind: char(1), truth: bool, number: int(1), container: Value(1));

/* functions */

/* helpers */

/* constants */

number0 := [0, 1];
number1 := [1, 1];
number10 := [10, 1];

/* numeral */

// getNumeral: int(1) -> char(1);
// getNumeral(n(1)) :=
    // let
        // signN := signNumb(n);
        // abN := ab(n);
        // quot := abN[1] / abN[2];        
        // rem := abN[1] mod abN[2];        
    // in
    
        
// printFraction: int(1) -> char(1);
// printFraction(n(1)) :=
    // let
        // divisor := n[2];
        // rem := n[1];
        // fr := calculateFraction(divisor, [rem], []);
        // rems := fr[1];
        // lastRem := Sequence::last(rems);
        // pos := Sequence::firstIndexOf(rems, lastRem);
    // in


// calculateFraction: int * int(1) * int(1) -> int(2);
// calculateFraction(divisor, rems(1), quots(1)) :=
    // let
        // dividend := Sequence::last(rems) * 10;
        // rem := dividend mod divisor;
        // pos := Sequence::firstIndexOf(rems, rem);
        // rems2 := rems ++ [rem];
        // quot := dividend / divisor;
        // quots2 := quots ++ [quot];
    // in
        // [rems2, quots2] when rem = 0 or pos > 0 else
        // calculateFraction(divisor, rems2, quots2);

// numeral: char(1) -> int(1);
numeral(n(1)) :=
    let dot := Sequence::firstIndexOf(n, '.');
        iN := Sequence::take(n, dot - 1);
        dF := Sequence::drop(n, dot - 1);
        numbIN := intNumeral(iN);
        numbF := fraction(dF);
    in  intNumeral(n) when dot = 0 else
        fraction(n) when dot = 1 else
        add(numbIN, numbF);
        
// intNumeral: char(1) -> int(1);
intNumeral(iN(1)) := [Conversion::stringToInt(iN), 1];

// fraction: char(1) -> int(1);
fraction(dF(1)) :=
    let lPar := Sequence::firstIndexOf(dF, '(');
    in  fractionNoRepeat(dF) when lPar = 0 else
        fractionRepeat(dF);
    
// fractionNoRepeat: char(1) -> int(1);
fractionNoRepeat(fNR(1)) :=
    let iN := Sequence::drop(fNR, 1);
        len := [size(iN), 1];
        shift := exp(number10, uMinus(len));
        numbIN := mult(shift, intNumeral(iN));
    in numbIN;
    
// fractionRepeat: char(1) -> int(1);
fractionRepeat(fR(1)) :=
    let lPar := Sequence::firstIndexOf(fR, '(');
        fNR := Sequence::take(fR, lPar - 1);
        numbFNR := fractionNoRepeat(fNR);
        rB := Sequence::drop(fR, lPar - 1);
        len := [size(fNR) - 1, 1];
        shift := exp(number10, uMinus(len));
        numbRB := mult(shift, repeatBlock(rB));
    in  add(numbFNR, numbRB);

// repeatBlock: char(1) -> int(1);
repeatBlock(rB(1)) :=
    let 
        iN := rB[2 ... size(rB) - 3];
        number := intNumeral(iN);
        len := [size(iN), 1];
        divisor := biMinus(exp(number10, len), number1);
    in  div(number, divisor);
    
/* arithmetic */

// reduce: int(1) -> int(1);
reduce(n(1)) :=
    let signN := signNumb(n);
        abN := Math::abs(n);
        gcdAbN := GCD(abN);
        redAbN := abN / gcdAbN;
    in [signN * redAbN[1], redAbN[2]];
    

//todo comment out signature to make sli run?
// GCD: int(1) -> int;
GCD(n(1)) :=
    n[1] when n[2] = 0 else
    GCD([n[2], n[1] mod n[2]]);
    
signNumb: int(1) -> int;
signNumb(n(1)) := 
    product(Math::sign(n));
    
isInt: int(1) -> bool;
isInt(n(1)) := 
    n[1] mod n[2] = 0;

reciprocal: int(1) -> int(1);
reciprocal(n(1)) := reduce(Sequence::reverse(n));

// nrvalList: int * int -> Value(1);
// nrvalList(int1, int2)[i] :=
    // let n := [i, 1];
    // in (kind: typeNumber, number: n)
    // foreach i within int1 ... int2;

/* LED */
    
/* arithmetic */

add: int(1) * int(1) -> int(1);
add(n1(1), n2(1)) :=
    let int1 := n1[1] * n2[2] + n1[2] * n2[1];
        int2 := n1[2] * n2[2];
        number := [int1, int2];
    in reduce(number);
    
biMinus: int(1) * int(1) -> int(1);
biMinus(n1(1), n2(1)) := add(n1, uMinus(n2));

uMinus: int(1) -> int(1);
uMinus(n(1)) := reduce([-n[1], n[2]]);

mult: int(1) * int(1) -> int(1);
mult(n1(1), n2(1)) := reduce(n1 * n2);

div: int(1) * int(1) -> int(1);
div(n1(1), n2(1)) := mult(n1, reciprocal(n2));

flr: int(1) -> int(1);
flr(n(1)) := [n[1] / n[2], 1];

clng: int(1) -> int(1);
clng(n(1)) := 
    n when isInt(n) else
    [n[1] / n[2] + 1, 1];
    
ab: int(1) -> int(1);
ab(n(1)) := reduce(Math::abs(n));

md: int(1) * int(1) -> int(1);
md(n1(1), n2(1)) := [n1[1] mod n2[1], 1];

exp: int(1) * int(1) -> int(1);
exp(n1(1), n2(1)) :=
    let pow := n2[1];
    in  [1, 1] when pow = 0 else
        mult(n1, exp(n1, [pow - 1, 1])) when pow > 0 else
        exp(reciprocal(n1), uMinus(n2));
    
numbEq: int(1) * int(1) -> bool;
numbEq(n1(1), n2(1)) := not (numbL(n1, n2) or numbGr(n1, n2));
    
numbL: int(1) * int(1) -> bool;
numbL(n1(1), n2(1)) :=
    let diff := biMinus(n1, n2);
    in signNumb(diff) < 0;

numbGr: int(1) * int(1) -> bool;
numbGr(n1(1), n2(1)) :=
    let diff := biMinus(n1, n2);
    in signNumb(diff) > 0;
    
numbLEq: int(1) * int(1) -> bool;
numbLEq(n1(1), n2(1)) := numbL(n1, n2) or numbEq(n1, n2);
    
numbGrEq: int(1) * int(1) -> bool;
numbGrEq(n1(1), n2(1)) := numbGr(n1, n2) or numbEq(n1, n2);

// nrval: int(1) * int(1) -> Value;
// nrval(n1(1), n2(1)) :=
    // let int1 := n1[1];
        // int2 := n2[1];
        // list := nrvalList(int1, int2);
    // in (kind: typeSet, set: list);    

/* set */
    
// biUnion: V alue * Value -> Value;
// biUnion(valSet1, valSet2) :=
    // let set1 := valSet1.set;
        // set2 := valSet2.set;
    // in (kind: typeSet, set: Set::union(set1, set2));
