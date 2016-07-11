valIsNumb: Val -> bool;
valIsNumb(v) :=
    equalList(valToKind(v), kindNumb);
    
/* 
LED Library written in SequenceL
*/

/* exporting */

public  
    Val, Numb, // types
    add, biMinus, uMinus, mult, div, flr, clng, ab, md, exp,
    atmToVal,
    n, // numeral to value
    t, // truth to value
    valToNuml;
        
/* type: value */

valToKind: Val -> char(1);
valToKind(v) :=
    v.kind;

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
    
/* equality operations */

eq: Val * Val -> Val;
eq(v1, v2) :=
    let
        bothNumbs := valIsNumb(v1) and valIsNumb(v2);
        equalNumbs := eqNumb(valToNumb(v1), valToNumb(v2));
        equalTrths := valToTrth(v1) = valToTrth(v2);
    in
        trthToVal(equalNumbs) when bothNumbs else
        trthToVal(equalTrths);
    
uneq: Val * Val -> Val;
uneq(v1, v2) :=
    let
        equalVal := eq(v1, v2);
        unequalTrth := not valToTrth(eq(v1, v2));
    in
        trthToVal(unequalTrth);

eqNumb: Numb * Numb -> bool;
eqNumb(numb1, numb2) :=
    sgn(biMinusNumb(numb1, numb2)) = 0;
    
uneqNumb: Numb * Numb -> bool;
uneqNumb(numb1, numb2) :=
    not eqNumb(numb1, numb2);
    
/* relational operations */

less: Val * Val -> Val;
less(v1, v2) :=
    stdNumbNumbToTrth(lessNumb, v1, v2);
    
lessNumb: Numb * Numb -> bool;
lessNumb(numb1, numb2) :=
    sgn(biMinusNumb(numb1, numb2)) < 0;

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

/* arithmetic operations */

add: Val * Val -> Val;
add(v1, v2) :=
    stdNumbNumbToNumb(addNumb, v1, v2);

addNumb: Numb * Numb -> Numb;
addNumb(numb1, numb2) :=
    let
        numr := 
            numbToNumr(numb1) * numbToDenr(numb2) + 
            numbToDenr(numb1) * numbToNumr(numb2);
        denr := numbToDenr(numb1) * numbToDenr(numb2);
    in
        intsToNumb(numr, denr);
        
biMinus: Val * Val -> Val;
biMinus(v1, v2) :=
    stdNumbNumbToNumb(biMinusNumb, v1, v2);
        
biMinusNumb: Numb * Numb -> Numb;
biMinusNumb(numb1, numb2) :=
    addNumb(numb1, uMinusNumb(numb2));
    
uMinus: Val -> Val;
uMinus(v) :=
    stdNumbToNumb(uMinusNumb, v);
    
uMinusNumb: Numb -> Numb;
uMinusNumb(numb) :=    
    intsToNumb(-numbToNumr(numb), numbToDenr(numb));
    
mult: Val * Val -> Val;
mult(v1, v2) :=
    stdNumbNumbToNumb(multNumb, v1, v2);
    
multNumb: Numb * Numb -> Numb;
multNumb(numb1, numb2) :=
    let
        numr := numbToNumr(numb1) * numbToNumr(numb2);
        denr := numbToDenr(numb1) * numbToDenr(numb2);
    in
        intsToNumb(numr, denr);
        
div: Val * Val -> Val;
div(v1, v2) :=
    stdNumbNumbToNumb(divNumb, v1, v2);
        
divNumb: Numb * Numb -> Numb;
divNumb(numb1, numb2) := 
    multNumb(numb1, recipr(numb2));
    
flr: Val -> Val;
flr(v) :=
    stdNumbToInt(flrNumb, v);

flrNumb: Numb -> int64;
flrNumb(numb) := 
    let        
        quot := numbToNumr(numb) / numbToDenr(numb);
        badCase := not numbIsInt(numb) and sgn(numb) < 0;
    in
        quot - 1 when badCase else
        quot;
        
clng: Val -> Val;
clng(v) :=
    stdNumbToInt(clngNumb, v);
        
clngNumb: Numb -> int64;
clngNumb(numb) :=
    numbToInt(numb) when numbIsInt(numb) else
    flrNumb(numb) + 1;
    
ab: Val -> Val;
ab(v) :=
    stdNumbToNumb(abNumb, v);
        
abNumb: Numb -> Numb;
abNumb(numb) :=
    intsToNumb(Math::abs(numbToNumr(numb)), numbToDenr(numb));
    
md: Val * Val -> Val;
md(v1, v2) :=
    stdIntIntToInt(mdNumb, v1, v2);
        
mdNumb: int64 * int64 -> int64;
mdNumb(i1, i2) :=
    i1 mod i2;
    
exp: Val * Val -> Val;
exp(v1, v2) :=
    stdNumbIntToNumb(expNumb, v1, v2);
    
expNumb: Numb * int64 -> Numb;
expNumb(numb, i) :=
    numbOne when i = 0 else
    multNumb(numb, expNumb(numb, i - 1)) when i > 0 else
    expNumb(recipr(numb), -i);

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
    
/* importing */

import <Utilities/Set.sl>;
