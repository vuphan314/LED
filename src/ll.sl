/* importing */

import <Utilities/Math.sl>;

/* number type */

Numb ::= (Numr: int, Denr: int);

newNumb: int * int -> Numb;
newNumb(i1, i2) :=
    reduce((Numr: i1, Denr: i2));

getNumr: Numb -> int;
getNumr(numb) :=
    numb.Numr;
    
getDenr: Numb -> int;
getDenr(numb) :=
    numb.Denr;
    
/* integer pseudotype */

newInt: int -> Numb;
newInt(i) :=
    newNumb(i, 1);
    
getInt: Numb -> int;
getInt(numb) :=
    getNumr(reduce(numb));
    
/* LED arithmetic */

add: Numb * Numb -> Numb;
add(numb1, numb2) :=
    let
        numr := 
            getNumr(numb1) * getDenr(numb2) + 
            getDenr(numb1) * getNumr(numb2);
        denr := getDenr(numb1) * getDenr(numb2);
    in
        newNumb(numr, denr);
        
biMinus: Numb * Numb -> Numb;
biMinus(numb1, numb2) :=
    add(numb1, uMinus(numb2));
    
uMinus: Numb -> Numb;
uMinus(numb) :=    
    newNumb(-getNumr(numb), getDenr(numb));
    
mult: Numb * Numb -> Numb;
mult(numb1, numb2) :=
    let
        numr := getNumr(numb1) * getNumr(numb2);
        denr := getDenr(numb1) * getDenr(numb2);
    in
        newNumb(numr, denr);
        
div: Numb * Numb -> Numb;
div(numb1, numb2) := 
    mult(numb1, recipr(numb2));
        
flr: Numb -> Numb;
flr(numb) := 
    newInt(getNumr(numb) / getDenr(numb));

clng: Numb -> Numb;
clng(numb) :=
    numb when isInt(numb) else
    newInt(getInt(flr(numb)) + 1);

ab: Numb -> Numb;
ab(numb) :=
    let
        absNumr := Math::abs(getNumr(numb));
        absDenr := Math::abs(getDenr(numb));
    in
        newNumb(absNumr, absDenr);

/* arithmetic helpers */

recipr: Numb -> Numb;
recipr(numb) :=
    newNumb(getDenr(numb), getNumr(numb));

reduce: Numb -> Numb;
reduce(numb) :=
    let
        signOfNumb := signNumb(numb);
        absNumr := Math::abs(getNumr(numb)); absDenr := Math::abs(getDenr(numb));
        gcdNumb := gcd(absNumr, absDenr);
        redAbsNumr := absNumr / gcdNumb; redAbsDenr := absDenr / gcdNumb;
        redNumr := signOfNumb * redAbsNumr;
    in
        (Numr: redNumr, Denr: redAbsDenr);

gcd: int * int -> int;
gcd(i1, i2) :=
    i1 when i2 = 0 else
    gcd(i2, i1 mod i2);
    
signNumb: Numb -> int;
signNumb(numb) :=
    Math::sign(getNumr(numb)) * Math::sign(getDenr(numb));
    
isInt: Numb -> bool;
isInt(numb) :=
    getNumr(numb) mod getDenr(numb) = 0;
    
/* numbers */

zero := newInt(0);
one := newInt(1);
ten := newInt(10);
