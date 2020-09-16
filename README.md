# Compilador de Julia
![Diagrama v1.2](/v1.2.png)

### EBNF
```
FACTOR = {{“+”|“-”}, FACTOR} | NUMBER | {“(”, EXPRESSION, “)”}}
EXPRESSION = TERM, {(“+”|”-“), TERM} 
TERM = FACTOR, {(“*”|”/“), FACTOR}
NUMBER = [0-9]
```
