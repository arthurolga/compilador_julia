# Compilador de Julia
![Diagrama v1.1](/v1.1.svg)

### EBNF
```
EXPRESSION = TERM, {(“+”|”-“), TERM} 
TERM = NUMBER, {(“*”|”/“), NUMBER}
```