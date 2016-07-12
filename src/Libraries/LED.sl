/* 
LED Library written in SequenceL
*/

/* importing */

import <Utilities/Math.sl>;
import "helper.sl";
import "numeral.sl";

/* exporting */

public 
    Val, Numb, // types
    add, biMinus, uMinus, mult, div, flr, clng, ab, md, exp,
    n, // numeral to value
    t, // truth to value
    valToNuml;
        
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

/* value arithmetic operations */

add: Val * Val -> Val;
add(v1, v2) :=
    stdNumbNumbToNumb(addNumb, v1, v2);

biMinus: Val * Val -> Val;
biMinus(v1, v2) :=
    stdNumbNumbToNumb(biMinusNumb, v1, v2);
        
uMinus: Val -> Val;
uMinus(v) :=
    stdNumbToNumb(uMinusNumb, v);
    
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
