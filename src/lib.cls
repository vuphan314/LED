\LoadClass[12pt]{extarticle} % 8pt, 9pt, 10pt, 11pt, 12pt, 14pt, 17pt, 20pt

\usepackage[scale=.9]{geometry}
\usepackage[yyyymmdd]{datetime}
\usepackage{amssymb}
\usepackage{amsmath}
\usepackage{breqn}
\usepackage{blindtext}

\setlength{\parindent}{0pt}
\setlength{\parskip}{.2in}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newenvironment{ledCmnt}{}{}

\newenvironment{ledDef}{\begin{dmath}}{\end{dmath} \medskip}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% CLS_CMDS

% DEF_LABELS
\newcommand{\funDefNoWhere}[2]{\defNoWhere{#1}{#2}{:=}}
\newcommand{\funDefWhere}[3]{\funDefNoWhere{#1}{#2} \whereClause{#3}}
\newcommand{\relDefNoWhere}[2]{\defNoWhere{#1}{#2}{\equiv}}
\newcommand{\relDefWhere}[3]{\relDefNoWhere{#1}{#2} \whereClause{#3}}

% IF_CLAUSES
\newcommand{\termIfBoolTerm}[2]{#1 & \textKeyword{if} #2 \\}
\newcommand{\termOw}[1]{#1 & \textKeyword{otherwise} \\}

% QUANT_OPS
\newcommand{\exist}[2]{\exists \infixNoPar{#1}{#2}{.}}
\newcommand{\univ}[2]{\forall \infixNoPar{#1}{#2}{.}}

% AGGR_OPS
\newcommand{\setCompr}[2]{\braces{\infixNoPar{#1}{#2}{|}}}
\newcommand{\aggrUnn}[2]{\bigcup_{#1}{#2}}
\newcommand{\aggrNrsec}[2]{\bigcap_{#1}{#2}}
\newcommand{\aggrSum}[2]{\sum_{#1}{#2}}
\newcommand{\aggrProd}[2]{\prod_{#1}{#2}}

% OVERLOADED_OPS
\newcommand{\pipesOp}[1]{\pipes{#1}}
\newcommand{\plusOp}[2]{\infixPar{#1}{#2}{+}}
\newcommand{\starOp}[2]{\infixPar{#1}{#2}{\times}}

% BOOL_OPS
\newcommand{\equivLED}[2]{\infixPar{#1}{#2}{\Leftrightarrow}}
\newcommand{\impl}[2]{\infixPar{#1}{#2}{\Rightarrow}}
\newcommand{\disj}[2]{\infixPar{#1}{#2}{\vee}}
\newcommand{\conj}[2]{\infixPar{#1}{#2}{\wedge}}
% use default: \neg
\newcommand{\eq}[2]{\infixPar{#1}{#2}{=}}
\newcommand{\uneq}[2]{\infixPar{#1}{#2}{\ne}}
\newcommand{\less}[2]{\infixPar{#1}{#2}{<}}
\newcommand{\greater}[2]{\infixPar{#1}{#2}{>}}
\newcommand{\lessEq}[2]{\infixPar{#1}{#2}{\le}}
\newcommand{\greaterEq}[2]{\infixPar{#1}{#2}{\ge}}

% AR_OPS
\newcommand{\unaryMinus}[1]{- #1}
\newcommand{\binaryMinus}[2]{\infixPar{#1}{#2}{-}}
\renewcommand{\div}[2]{\infixPar{#1}{#2}{/}}
\newcommand{\md}[2]{\infixPar{#1}{#2}{\textKeyword{mod}}}
\renewcommand{\exp}[2]{{(#1)} ^ {#2}}
\newcommand{\flr}[1]{\floors{#1}}
\newcommand{\clng}[1]{\ceils{#1}}

% TUPLE_LABELS
\newcommand{\tpl}[1]{\parentheses{#1}}
\newcommand{\tuIn}[2]{#1 \brackets{#2}}
\newcommand{\tuSl}[3]{#1 \brackets{\infixNoPar{#2}{#3}{..}}}

% SET_LABELS
\newcommand{\powSet}[1]{\wp \parentheses{#1}}
\newcommand{\setEmpty}{\varnothing}
\newcommand{\setNonempty}[1]{\braces{#1}}
\newcommand{\iv}[2]{\braces{\infixNoPar{#1}{#2}{..}}}
\newcommand{\unn}[2]{\infixPar{#1}{#2}{\cup}}
\newcommand{\diff}[2]{\infixPar{#1}{#2}{\setminus}}
\newcommand{\nrsec}[2]{\infixPar{#1}{#2}{\cap}}
\newcommand{\sbset}[2]{\infixPar{#1}{#2}{\subseteq}}
\newcommand{\setMem}[2]{\infixPar{#1}{#2}{\in}}
\newcommand{\symsInSet}[2]{\setMem{#1}{#2}}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% surrounders
\newcommand{\parentheses}[1]{\left( #1 \right)}
\newcommand{\braces}[1]{\left\{ #1 \right\}}
\newcommand{\brackets}[1]{\left[ #1 \right]}
\newcommand{\pipes}[1]{\left| #1 \right|}
\newcommand{\floors}[1]{\lfloor #1 \rfloor}
\newcommand{\ceils}[1]{\lceil #1 \rceil}

% infix
\newcommand{\infixNoPar}[3]{{#1}\ {#3}\ {#2}}
\newcommand{\infixPar}[3]{\infixNoPar{\parentheses{#1}}{\parentheses{#2}}{#3}}

% misc
\newcommand{\defNoWhere}[3]{\infixNoPar{#1}{#2}{#3}}
\newcommand{\whereClause}[1]{\\ \textKeyword{where} #1}
\newcommand{\textKeyword}[1]{\text{ #1 }}
