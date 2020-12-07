# Compilador de Julia
![Diagrama v2.2](/v2.2.png)

### EBNF
```
PROGRAM = { FUNCTION | BLOCK };
BLOCK  = {COMMAND}
FUNCTION = DECLARE_FUNCTION, IDENTIFIER, "(",(IDENTIFIER,"::",TYPE), {",",IDENTIFIER,"::",TYPE},")","::",TYPE,BLOCK,"end";
COMMAND = ( λ | LOCAL | ASSIGNMENT | PRINT | IF | WHILE | CALL | RETURN), "\n" ;
CALL = IDENTIFIER,"(",(IDENTIFIER,"::",TYPE),{",",REL_EXPRESSION},")";
RETURN = "return",REL_EXPRESSION;
LOCAL = "local",identifier,"::",TYPE;
DECLARE = "local", IDENTIFIER, "::", TYPE;
ASSIGNMENT = IDENTIFIER, "=", REL_EXPRESSION | READLINE, "(",")";
PRINT = "println", "(", REL_EXPRESSION, ")" ;
EXPRESSION = TERM, { ("+" | "-" | "||"), TERM } ;
REL_EXPRESSION = EXPRESSION, { ("==" | ">" | "<"), EXPRESSION };
WHILE = "while", REL_EXPRESSION, "\n", BLOCK, "end";
IF = "if", REL_EXPRESSION, "\n", BLOCK, { ELSEIF | ELSE }, "end";
ELSEIF = "elseif", REL_EXPRESSION, "\n", BLOCK, { ELSEIF | ELSE };
ELSE = "else", "\n", BLOCK;
TERM = FACTOR, { ("*" | "/" | "&&"), FACTOR } ;
FACTOR = (("+" | "-" | "!"), FACTOR) | NUMBER | "(", REL_EXPRESSION, ")" | IDENTIFIER ;
IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;
TYPE = "Int" | "Bool" | "String"; 
STRING = '"', (.*?), '"';
BOOLEAN = "true" | "false";
NUMBER = DIGIT, { DIGIT } ;
LETTER = ( a ~ z | A ~ Z ) ;
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;
DECLARE_FUNCTION = "function";
```

### Running
```
python3 main.py test.jl
```
