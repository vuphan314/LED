/* 
LED library written in SequenceL
*/

////////// ////////// ////////// ////////// ////////// ////////// 
/* importing */

import <Utilities/Conversion.sl>;
import <Utilities/Math.sl>;
import <Utilities/Sequence.sl>;
import <Utilities/String.sl>;

////////// ////////// ////////// ////////// ////////// ////////// 
/* exporting */

public 
    Val, Numb, // types
    eq, uneq,
    less, greater, lessEq, greaterEq,
    add, bMns, uMns, mult, div, flr, clng, ab, md, exp,
    tuIn,
    tu, // tuple to value
    se, // set to value
    at, // atom to value
    tr, // truth to value
    nu, // numeral to value
    valToNuml, valToSet;
        
////////// ////////// ////////// ////////// ////////// ////////// 
/* tuple indexing */

tuIn: Val * Val -> Val;
tuIn(valT, valI) :=
    let
        tplT := valToTpl(valT);
        intI := valToInt(valI);
    in
        tplT[intI];

////////// ////////// ////////// ////////// ////////// ////////// 
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
        eqNumb(n1, n2) when valsOfKind(v1, v2, kindNumb) else
        equalList(a1, a2) when valsOfKind(v1, v2, kindAtm) else
        tr1 = tr2 when valsOfKind(v1, v2, kindTrth) else
        equalList(c1, c2) when valsOfKind(v1, v2, kindTpl) else
        equalSet(c1, c2) when valsOfKind(v1, v2, kindSet) else
        false;
    
eqNumb: Numb * Numb -> bool;
eqNumb(numb1, numb2) :=
    sgn(bMnsNumb(numb1, numb2)) = 0;
    
////////// ////////// ////////// ////////// ////////// ////////// 
/* relational operations */

less: Val * Val -> Val;
less(v1, v2) :=
    stdNumbNumbToTrth(lessNumb, v1, v2);
    
lessNumb: Numb * Numb -> bool;
lessNumb(numb1, numb2) :=
    sgn(bMnsNumb(numb1, numb2)) < 0;

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

////////// ////////// ////////// ////////// ////////// ////////// 
/* arithmetic operations (value) */

add: Val * Val -> Val;
add(v1, v2) :=
    stdNumbNumbToNumb(addNumb, v1, v2);

bMns: Val * Val -> Val;
bMns(v1, v2) :=
    stdNumbNumbToNumb(bMnsNumb, v1, v2);
        
uMns: Val -> Val;
uMns(v) :=
    stdNumbToNumb(uMnsNumb, v);
    
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

////////// ////////// ////////// ////////// ////////// ////////// 
/* type: value */

Val ::= 
    (kind: char(1), 
    atm: char(1), numb: Numb, trth: bool, 
    coll: Val(1), //todo
    lmbd: (Val(1) -> Val));
        
valToKind: Val -> char(1);
valToKind(v) :=
    v.kind;

valOfKind: Val * char(1) -> bool;
valOfKind(v, k(1)) :=
    equalList(valToKind(v), k);
    
valsOfKind: Val * Val * char(1) -> bool;
valsOfKind(v1, v2, k(1)) :=
    valOfKind(v1, k) and valOfKind(v2, k);
    
////////// ////////// ////////// ////////// ////////// ////////// 
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
    
valToAtm: Val -> char(1);
valToAtm(v) :=
    v.atm;
    
valToColl: Val -> Val(1);
valToColl(v) :=
    v.coll;  
valToTpl: Val -> Val(1);
valToTpl(v) :=
    valToColl(v);
valToSet: Val -> Val(1);
valToSet(v) :=
    valToColl(v);

////////// ////////// ////////// ////////// ////////// ////////// 
/* thing to value */

numlToVal: char(1) -> Val;
numlToVal(n(1)) :=
    numbToVal(numlToNumb(n));
nu: char(1) -> Val;
nu(n(1)) :=
    numlToVal(n);
    
numbToVal: Numb -> Val;
numbToVal(n) :=
    (kind: kindNumb, numb: n);
    
trthToVal: bool -> Val;
trthToVal(t) :=
    (kind: kindTrth, trth: t);
tr: bool -> Val;
tr(t) :=
    trthToVal(t);
    
atmToVal: char(1) -> Val;
atmToVal(a(1)) :=
    (kind: kindAtm, atm: a);
at: char(1) -> Val;
at(a(1)) :=
    atmToVal(a);

tplToVal: Val(1) -> Val;
tplToVal(t(1)) :=
    (kind: kindTpl, coll: t);
tu: Val(1) -> Val;
tu(t(1)) :=
    tplToVal(t);
    
setToVal: Val(1) -> Val;
setToVal(s(1)) :=
    (kind: kindSet, coll: removeDups(s));
se(s(1)) :=
    setToVal(s);

////////// ////////// ////////// ////////// ////////// ////////// 
/* type: number */

Numb ::= 
    (Numr: int64, Denr: int64);
    
intsToNumb: int64 * int64 -> Numb;
intsToNumb(i1, i2) :=
    reduce(i1, i2);

numbToNumr: Numb -> int64;
numbToNumr(numb) :=
    numb.Numr;
    
numbToDenr: Numb -> int64;
numbToDenr(numb) :=
    numb.Denr;
    
////////// ////////// ////////// ////////// ////////// ////////// 
/* pseudotype: integer */

numbIsInt: Numb -> bool;
numbIsInt(numb) :=
    numbToDenr(numb) = 1;
    
intToNumb: int64 -> Numb;
intToNumb(i) :=
    intsToNumb(i, 1);
    
numbToInt: Numb -> int64;
numbToInt(numb) :=
    numbToNumr(numb);
    
intToVal: int64 -> Val;
intToVal(i) :=
    numbToVal(intToNumb(i));

valToInt: Val -> int64;
valToInt(v) :=
    numbToInt(valToNumb(v));
    
////////// ////////// ////////// ////////// ////////// ////////// 
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
    
kindSet: char(1);
kindSet :=
    "set";
    
////////// ////////// ////////// ////////// ////////// ////////// 
/* some values */

valOne: Val;
valOne :=
    numbToVal(numbOne);
    
valTen: Val;
valTen :=
    numbToVal(numbTen);
       
////////// ////////// ////////// ////////// ////////// ////////// 
/* some numbers */

numbOne: Numb;
numbOne := 
    intToNumb(1);
    
numbTen: Numb;
numbTen :=
    intToNumb(10);

////////// ////////// ////////// ////////// ////////// ////////// 
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

////////// ////////// ////////// ////////// ////////// ////////// 
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
    
////////// ////////// ////////// ////////// ////////// ////////// 
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
        divisor := bMnsNumb(expNumb(numbTen, lenRept), numbOne);
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
    
////////// ////////// ////////// ////////// ////////// ////////// 
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

////////// ////////// ////////// ////////// ////////// ////////// 
/* arithmetic operations (number) */

addNumb: Numb * Numb -> Numb;
addNumb(numb1, numb2) :=
    let
        numr := 
            numbToNumr(numb1) * numbToDenr(numb2) + 
            numbToDenr(numb1) * numbToNumr(numb2);
        denr := numbToDenr(numb1) * numbToDenr(numb2);
    in
        intsToNumb(numr, denr);
        
bMnsNumb: Numb * Numb -> Numb;
bMnsNumb(numb1, numb2) :=
    addNumb(numb1, uMnsNumb(numb2));
    
uMnsNumb: Numb -> Numb;
uMnsNumb(numb) :=    
    intsToNumb(-numbToNumr(numb), numbToDenr(numb));
    
multNumb: Numb * Numb -> Numb;
multNumb(numb1, numb2) :=
    let
        numr := numbToNumr(numb1) * numbToNumr(numb2);
        denr := numbToDenr(numb1) * numbToDenr(numb2);
    in
        intsToNumb(numr, denr);
        
divNumb: Numb * Numb -> Numb;
divNumb(numb1, numb2) := 
    multNumb(numb1, recipr(numb2));
    
flrNumb: Numb -> int64;
flrNumb(numb) := 
    let        
        quot := numbToNumr(numb) / numbToDenr(numb);
        badCase := not numbIsInt(numb) and sgn(numb) < 0;
    in
        quot - 1 when badCase else
        quot;
        
clngNumb: Numb -> int64;
clngNumb(numb) :=
    numbToInt(numb) when numbIsInt(numb) else
    flrNumb(numb) + 1;
    
abNumb: Numb -> Numb;
abNumb(numb) :=
    intsToNumb(Math::abs(numbToNumr(numb)), numbToDenr(numb));
    
mdNumb: int64 * int64 -> int64;
mdNumb(i1, i2) :=
    i1 mod i2;
    
expNumb: Numb * int64 -> Numb;
expNumb(numb, i) :=
    numbOne when i = 0 else
    multNumb(numb, expNumb(numb, i - 1)) when i > 0 else
    expNumb(recipr(numb), -i);
