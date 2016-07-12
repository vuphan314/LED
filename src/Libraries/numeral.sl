/* importing */

import <Utilities/String.sl>;
import <Utilities/Sequence.sl>;
import <Utilities/Math.sl>;
import <Utilities/Conversion.sl>;
import "helper.sl";

/* exporting */

public
    addNumb, biMinusNumb, uMinusNumb, multNumb, divNumb, flrNumb, clngNumb, abNumb, mdNumb, expNumb;

/* number arithmetic operations */

addNumb: Numb * Numb -> Numb;
addNumb(numb1, numb2) :=
    let
        numr := 
            numbToNumr(numb1) * numbToDenr(numb2) + 
            numbToDenr(numb1) * numbToNumr(numb2);
        denr := numbToDenr(numb1) * numbToDenr(numb2);
    in
        intsToNumb(numr, denr);
        
biMinusNumb: Numb * Numb -> Numb;
biMinusNumb(numb1, numb2) :=
    addNumb(numb1, uMinusNumb(numb2));
    
uMinusNumb: Numb -> Numb;
uMinusNumb(numb) :=    
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

