////////// ////////// ////////// ////////// ////////// ////////// 

/* importing */

import <Utilities/Math.sl>;
import <Utilities/Conversion.sl>;
import <Utilities/Sequence.sl>;

/* exporting */

public
    Val, Numb,
    numbToNumr, numbToDenr, intsToNumb, numbIsInt, numbToInt, intToNumb,
    valToNumb, valToTrth,
    trthToVal,
    valIsNumb,
    sgn, recipr,
    numbOne, numbTen,
    stdNumbNumbToTrth, stdNumbNumbToNumb, stdNumbToNumb, stdNumbToInt, stdIntIntToInt,
    stdNumbIntToNumb;

/* type: value */

Val ::= 
    (kind: char(1), 
    numb: Numb, trth: bool, atm: char(1), tpl: Val(1), 
    set: Val(1), lmbd: (Val(1) -> Val));
        
valToKind: Val -> char(1);
valToKind(v) :=
    v.kind;

valIsNumb: Val -> bool;
valIsNumb(v) :=
    equalList(valToKind(v), kindNumb);
    
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
    
valToTpl: Val -> Val(1);
valToTpl(v) :=
    v.tpl;
   
/* thing to value */

numlToVal: char(1) -> Val;
numlToVal(n(1)) :=
    numbToVal(numlToNumb(n));
n: char(1) -> Val;
n(numl(1)) :=
    numlToVal(numl);
    
numbToVal: Numb -> Val;
numbToVal(n) :=
    (kind: kindNumb, numb: n);
    
trthToVal: bool -> Val;
trthToVal(t) :=
    (kind: kindTrth, trth: t);
t: bool -> Val;
t(tr) :=
    trthToVal(tr);
    
atmToVal: char(1) -> Val;
atmToVal(a(1)) :=
    (kind: kindAtm, atm: a);
    
tplToVal: Val(1) -> Val;
tplToVal(t(1)) :=
    (kind: kindTpl, tpl: t);

/* type: number */

Numb ::= 
    (Numr: int64, Denr: int64);
    
numbToNumr: Numb -> int64;
numbToNumr(numb) :=
    numb.Numr;
    
numbToDenr: Numb -> int64;
numbToDenr(numb) :=
    numb.Denr;
    
intsToNumb: int64 * int64 -> Numb;
intsToNumb(i1, i2) :=
    reduce(i1, i2);

/* pseudotype: integer */

valToInt: Val -> int64;
valToInt(v) :=
    numbToInt(valToNumb(v));
    
intToVal: int64 -> Val;
intToVal(i) :=
    numbToVal(intToNumb(i));

intToNumb: int64 -> Numb;
intToNumb(i) :=
    intsToNumb(i, 1);
    
numbToInt: Numb -> int64;
numbToInt(numb) :=
    numbToNumr(numb);
    
numbIsInt: Numb -> bool;
numbIsInt(numb) :=
    numbToDenr(numb) = 1;
    
/* kinds */
    
kindNumb: char(1);
kindNumb :=
    "numb";
    
kindTrth: char(1);
kindTrth :=
    "trth";
    
kindAtm: char(1);
kindAtm :=
    "atm";
    
kindTpl: char(1);
kindTpl :=
    "tpl";
    
/* some values */

valOne: Val;
valOne :=
    numbToVal(numbOne);
    
valTen: Val;
valTen :=
    numbToVal(numbTen);
       
/* some numbers */

numbOne: Numb;
numbOne := 
    intToNumb(1);
    
numbTen: Numb;
numbTen :=
    intToNumb(10);

/* arithmetic helper functions */

recipr: Numb -> Numb;
recipr(numb) :=
    intsToNumb(numbToDenr(numb), numbToNumr(numb));

sgn: Numb -> int8;
sgn(numb) :=
    Math::sign(numbToNumr(numb));
    
reduce: int64 * int64 -> Numb;
reduce(i1, i2) :=
    let
        signOfNumb := Math::sign(i1) * Math::sign(i2);
        absNumr := Math::abs(i1); absDenr := Math::abs(i2);
        gcdNumb := gcd(absNumr, absDenr);
        redAbsNumr := absNumr / gcdNumb; redAbsDenr := absDenr / gcdNumb;
        redNumr := signOfNumb * redAbsNumr;
    in
        (Numr: redNumr, Denr: redAbsDenr);

gcd: int64 * int64 -> int64;
gcd(i1, i2) :=
    i1 when i2 = 0 else
    gcd(i2, i1 mod i2);

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
    
getAbsNuml: int64 * int64 -> char(1);
getAbsNuml(absNumr, denr) :=
    let
        integralPart := Conversion::intToString(absNumr / denr);        
        minAbsNumr := absNumr mod denr;        
    in
        integralPart when minAbsNumr = 0 else
        integralPart ++ getFr(minAbsNumr, denr);
        
getFr: int64 * int64 -> char(1);
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
    
getFrRep: int64 * int64(1) -> char(1);
getFrRep(repRemPos, quots(1)) :=
    let
        nRepQuots := Sequence::take(quots, repRemPos - 1);
        repQuots := Sequence::drop(quots, repRemPos - 1);
    in
        getFrNRep(nRepQuots) ++ getRepBl(repQuots);
        
getRepBl: int64(1) -> char(1);
getRepBl(repQuots(1)) :=
    "(" ++ getIntNuml(repQuots) ++ "..)";

getFrNRep: int64(1) -> char(1);
getFrNRep(quots(1)) :=
    "." ++ getIntNuml(quots);
    
getIntNuml: int64(1) -> char(1);
getIntNuml(quots(1)) :=
    join(Conversion::intToString(quots));

getRemsQuots: int64 * int64(1) * int64(1) -> TwoIntLists;
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
        
TwoIntLists ::= 
    (l1: int64(1), l2: int64(1));        
    
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
        lPar := Sequence::firstIndexOf(f, '(');
    in  
        frNRepToNumb(f) when lPar = 0 else
        frRepToNumb(f);
    
frRepToNumb: char(1) -> Numb;
frRepToNumb(fR(1)) :=
    let 
        lPar := Sequence::firstIndexOf(fR, '(');
        fNR := Sequence::take(fR, lPar - 1);
        numbFNR := frNRepToNumb(fNR);
        shift := size(fNR) - 1;
        factor := expNumb(numbTen, -shift);
        rB := Sequence::drop(fR, lPar - 1);
        numbRB := multNumb(factor, repBlToNumb(rB));
    in  
        addNumb(numbFNR, numbRB);

repBlToNumb: char(1) -> Numb;
repBlToNumb(rB(1)) :=
    let 
        iN := rB[2 ... size(rB) - 3];
        rept := intNumlToNumb(iN);
        lenRept := size(iN);
        divisor := biMinusNumb(expNumb(numbTen, lenRept), numbOne);
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
    
/* standardizer functions */
    
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
        
stdNumbToInt: (Numb -> int64) * Val -> Val;
stdNumbToInt(f, v) :=
    let
        n := valToNumb(v);
        i := f(n);
        n2 := intToNumb(i);
    in
        numbToVal(n2);
        
stdIntIntToInt: (int64 * int64 -> int64) * Val * Val -> Val;
stdIntIntToInt(f, v1, v2) :=
    let
        i1 := valToInt(v1);
        i2 := valToInt(v2);
        i := f(i1, i2);
    in
        intToVal(i);
        
stdNumbIntToNumb: (Numb * int64 -> Numb) * Val * Val -> Val;
stdNumbIntToNumb(f, v1, v2) :=
    let
        n := valToNumb(v1);
        i := valToInt(v2);
        n2 := f(n, i);
    in
        numbToVal(n2);
