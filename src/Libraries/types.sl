public
    Val, Numb;

Val ::= 
    (kind: char(1), 
    numb: Numb, trth: bool, atm: char(1), tpl: Val(1), 
    set: Val(1), lmbd: (Val(1) -> Val));
        
Numb ::= 
    (Numr: int64, Denr: int64);
