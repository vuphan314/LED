/* exports */

// public  numeral,
        // add, biMinus, uMinus, mult, div, flr, clng, ab, md, exp;

/* imports */

import <Utilities/Conversion.sl>;
import <Utilities/Sequence.sl>;
import <Utilities/Set.sl>;

/* structures */

Val ::= (typ: char(1), atom: char(1), truth: bool, numb: Numb, cont: Val(1), lam: (Val(1) -> Val));

/* functions */

/* helpers */

/* constants */

/* number */

// dec: Numb -> char(1);
dec(n) :=
    let
        signN := signNumb(n);
        abN := ab(n);
        quot := abN.num / abN.den;        
        rem := abN.num mod abN.den;        
    in
    
        
// printFraction: Numb -> char(1);
// printFraction(n(1)) :=
    // let
        // divisor := n.den;
        // rem := n.num;
        // fr := calculateFraction(divisor, [rem], []);
        // rems := fr.num;
        // lastRem := Sequence::last(rems);
        // pos := Sequence::firstIndexOf(rems, lastRem);
    // in


// calculateFraction: int * Numb * Numb -> int(2);
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
            
// nrvalList: int * int -> Val(1);
// nrvalList(int1, int2)[i] :=
    // let n := [i, 1];
    // in (typ: typeNumber, number: n)
    // foreach i within int1 ... int2;

/* LED */
    
/* arithmetic */

ab(n) := reduce(Math::abs(n));

md: Numb * Numb -> Numb;
md(n1, n2) := [n1.num mod n2.num, 1];

exp: Numb * Numb -> Numb;
exp(n1, n2) :=
    let pow := n2.num;
    in  one when pow = 0 else
        mult(n1, exp(n1, [pow - 1, 1])) when pow > 0 else
        exp(reciprocal(n1), uMinus(n2));
        
/* comparison */
    
numbGrEq: Numb * Numb -> bool;
numbGrEq(n1, n2) := numbGr(n1, n2) or numbEq(n1, n2);
    
numbLEq: Numb * Numb -> bool;
numbLEq(n1, n2) := numbL(n1, n2) or numbEq(n1, n2);

numbEq: Numb * Numb -> bool;
numbEq(n1, n2) := not (numbL(n1, n2) or numbGr(n1, n2));

numbGr: Numb * Numb -> bool;
numbGr(n1, n2) :=
    let diff := biMinus(n1, n2);
    in signNumb(diff) > 0;
    
numbL: Numb * Numb -> bool;
numbL(n1, n2) :=
    let diff := biMinus(n1, n2);
    in signNumb(diff) < 0;

// nrval: Numb * Numb -> Val;
// nrval(n1(1), n2(1)) :=
    // let int1 := n1.num;
        // int2 := n2.num;
        // list := nrvalList(int1, int2);
    // in (typ: typeSet, set: list);    

/* set */
    
// biUnion: V alue * Val -> Val;
// biUnion(valSet1, valSet2) :=
    // let set1 := valSet1.set;
        // set2 := valSet2.set;
    // in (typ: typeSet, set: Set::union(set1, set2));
