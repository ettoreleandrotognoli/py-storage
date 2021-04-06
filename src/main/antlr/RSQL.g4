grammar RSQL;

options {
    language = Python37;
}

statement
    : left=statement op=AND_OPERATOR right=statement
    | left=statement op=OR_OPERATOR right=statement
    | '('  wrapped=statement ')'
    | node=comparison
    ;


comparison
    : left=expression op=comparator right=expression
    ;


expression
    : value
    | IDENTIFIER
    ;

TRUE: 'true' | 'True' | 't' | 'T' ;
FALSE: 'false' | 'False' | 'f' | 'F' ;
AND_OPERATOR: ';' | '&';
OR_OPERATOR: ',' | '|';
EQ: '=eq=' | '==';
NE: '=ne=' | '!=';


IDENTIFIER
 : [a-zA-Z_] [a-zA-Z_0-9]*
 ;

CMP_IDENTIFIER
   : [a-zA-Z_]+
   ;

comparator
    : op=EQ
    | op=NE
    | '=' op=CMP_IDENTIFIER '='
    ;

value
    : boolean=boolean_literal
    | string=string_literal
    | number=numeric_literal
    | array=array_value
    ;

array_value
    : '(' value ( ',' value ) * ')'
    | '[' value ( ',' value ) * ']'
    ;

boolean_literal
    : TRUE
    | FALSE
    ;

numeric_literal
    : INT_LITERAL
    | DECIMAL_LITERAL
    ;

string_literal
    : STRING_LITERAL
    ;

INT_LITERAL
    : [-+]? DIGIT+
    ;

DECIMAL_LITERAL
    : [-+]? DIGIT+ ( '.' DIGIT*)
    ;

STRING_LITERAL
    : '\'' ( STRING_ESCAPE_SEQ | ~[\\\r\n'] )* '\''
    | '"' ( STRING_ESCAPE_SEQ | ~[\\\r\n"] )* '"'
    ;
STRING_ESCAPE_SEQ
    : '\\' .
    ;
fragment DIGIT : [0-9];