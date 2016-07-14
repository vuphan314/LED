import "../lib.sl";

c1 := lib::flr(lib::numeral("0.(9..)"));

c2 := lib::clng(lib::uMinus(lib::numeral("2.(9..)")));

c3 := lib::biMinus(lib::add(lib::biMinus(lib::add(lib::numeral("1"), lib::numeral("2")), lib::numeral("3.2")), lib::div(lib::mult(lib::uMinus(lib::numeral("0.(2..)")), lib::numeral("2.5")), lib::numeral("2.(3..)"))), lib::md(lib::abs(lib::uMinus(lib::numeral("1.2"))), lib::exp(lib::numeral("2"), lib::numeral("3"))));


