// imports

import <Utilities/Conversion.sl>;
import <Utilities/Math.sl>;
import <Utilities/Sequence.sl>;
import <Utilities/Set.sl>;

// types

Value ::= ( type: char(1), 
            number: int(1), truth: bool, 
            tuple: Value(1), set: Value(1));      
            
typeNumber := "number";
typeTruth := "truth";
typeTuple := "tuple";
typeSet := "set";
        
// functions

/// helpers

//// constants

number0 := [0, 1];
number1 := [1, 1];
number10 := [10, 1];

//// numeral

intNumeral: char(1) -> int(1);
intNumeral(iN(1)) := [Conversion::stringToInt(iN), 1];

repeatBlock: char(1) -> int(1);
repeatBlock(rB(1)) :=
    let iN := rB[2 ... size(rB) - 3];
        number := intNumeral(iN);
        len := [size(iN), 1];
        div := subtract(exp(number10, len), number1);
    in  quot(number, div);
    
decFractionNoRepeat: char(1) -> int(1);
decFractionNoRepeat(dFNR(1)) :=
    let iN := Sequence::drop(dFNR, 1);
        len := [size(iN), 1];
        shift := exp(number10, uMinus(len));
        numbIN := prod(shift, intNumeral(iN));
    in numbIN;
    
decFractionRepeat: char(1) -> int(1);
decFractionRepeat(dFR(1)) :=
    let lPar := Sequence::firstIndexOf(dFR, '(');
        dFNR := Sequence::take(dFR, lPar - 1);
        rB := Sequence::drop(dFR, lPar - 1);
        numbDFNR := decFractionNoRepeat(dFNR);
        len := [size(dFNR) - 1, 1];
        shift := exp(number10, uMinus(len));
        numbRB := prod(shift, repeatBlock(rB));
    in  add(numbDFNR, numbRB);
    
decFraction: char(1) -> int(1);
decFraction(dF(1)) :=
    let lPar := Sequence::firstIndexOf(dF, '(');
    in  decFractionNoRepeat(dF) when lPar = 0 else
        decFractionRepeat(dF);
        
numeral: char(1) -> int(1);
numeral(n(1)) :=
    let dot := Sequence::firstIndexOf(n, '.');
        iN := Sequence::take(n, dot - 1);
        dF := Sequence::drop(n, dot - 1);
        numbIN := intNumeral(iN);
        numbDF := decFraction(dF);
    in  intNumeral(n) when dot = 0 else
        decFraction(n) when dot = 1 else
        add(numbIN, numbDF);

//// arithmetic

GCD: int(1) -> int;
GCD(n(1)) :=
    n[1] when n[2] = 0 else
    GCD([n[2], n[1] mod n[2]]);
    
numberReduce: int(1) -> int(1);
numberReduce(n(1)) :=
    let signN := product(Math::sign(n));
        absN := Math::abs(n);
        gcdAbsN := GCD(absN);
        redAbsN := absN / gcdAbsN;
    in [signN * redAbsN[1], redAbsN[2]];
    
numberSign: int(1) -> int;
numberSign(n(1)) := 
    let int1 := numberReduce(n)[1];
    in Math::sign(int1);
    
isInt: int(1) -> bool;
isInt(n(1)) := numberReduce(n)[2] = 1;

reciprocal: int(1) -> int(1);
reciprocal(n(1)) := numberReduce(Sequence::reverse(n));

nrvalList: int * int -> Value(1);
nrvalList(int1, int2)[i] :=
    let n := [i, 1];
    in (type: typeNumber, number: n)
    foreach i within int1 ... int2;

/// LED
    
//// arithmetic

add: int(1) * int(1) -> int(1);
add(n1(1), n2(1)) :=
    let int1 := n1[1] * n2[2] + n1[2] * n2[1];
        int2 := n1[2] * n2[2];
        number := [int1, int2];
    in numberReduce(number);
    
subtract: int(1) * int(1) -> int(1);
subtract(n1(1), n2(1)) := add(n1, uMinus(n2));

uMinus: int(1) -> int(1);
uMinus(n(1)) := numberReduce([-n[1], n[2]]);

prod: int(1) * int(1) -> int(1);
prod(n1(1), n2(1)) := numberReduce(n1 * n2);

quot: int(1) * int(1) -> int(1);
quot(n1(1), n2(1)) := prod(n1, reciprocal(n2));

flr: int(1) -> int(1);
flr(n(1)) := [n[1] / n[2], 1];

ceil: int(1) -> int(1);
ceil(n(1)) := 
    n when isInt(n) else
    [n[1] / n[2] + 1, 1];
    
ab: int(1) -> int(1);
ab(n(1)) := numberReduce(Math::abs(n));

md: int(1) * int(1) -> int(1);
md(n1(1), n2(1)) := [n1[1] mod n2[1], 1];

exp: int(1) * int(1) -> int(1);
exp(n1(1), n2(1)) :=
    let pow := n2[1];
    in  [1, 1] when pow = 0 else
        prod(n1, exp(n1, [pow - 1, 1])) when pow > 0 else
        exp(reciprocal(n1), uMinus(n2));
    
numbEq: int(1) * int(1) -> bool;
numbEq(n1(1), n2(1)) := not (numbL(n1, n2) or numbGr(n1, n2));
    
numbL: int(1) * int(1) -> bool;
numbL(n1(1), n2(1)) :=
    let diff := subtract(n1, n2);
    in numberSign(diff) < 0;

numbGr: int(1) * int(1) -> bool;
numbGr(n1(1), n2(1)) :=
    let diff := subtract(n1, n2);
    in numberSign(diff) > 0;
    
numbLEq: int(1) * int(1) -> bool;
numbLEq(n1(1), n2(1)) := numbL(n1, n2) or numbEq(n1, n2);
    
numbGrEq: int(1) * int(1) -> bool;
numbGrEq(n1(1), n2(1)) := numbGr(n1, n2) or numbEq(n1, n2);

nrval: int(1) * int(1) -> Value;
nrval(n1(1), n2(1)) :=
    let int1 := n1[1];
        int2 := n2[1];
        list := nrvalList(int1, int2);
    in (type: typeSet, set: list);    

//// set
    
biUnion: Value * Value -> Value;
biUnion(valSet1, valSet2) :=
    let set1 := valSet1.set;
        set2 := valSet2.set;
    in (type: typeSet, set: Set::union(set1, set2));
