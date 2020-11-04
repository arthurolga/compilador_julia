# Compilador de Julia
![Diagrama v2.2](/v2.2.png)

### EBNF
```
BLOCK = { COMMAND } ;
COMMAND = ( λ | ASSIGNMENT | PRINT | IF | WHILE), "\n" ;
DECLARE = "local", IDENTIFIER, "::", TYPE;
ASSIGNMENT = IDENTIFIER, "=", (REL_EXPRESSION | readline, "(", ")" ) ;
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
LETTER = ( a | ... | z | A | ... | Z ) ;
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;
```

### Running
```
python3 main.py test.jl
```
