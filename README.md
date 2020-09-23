# Compilador de Julia
![Diagrama v2.0](/v2.0.png)

### EBNF
```
FACTOR = {{“+”|“-”}, FACTOR} | NUMBER | {“(”, EXPRESSION, “)”}
EXPRESSION = TERM, {(“+”|”-“), TERM} 
TERM = FACTOR, {(“*”|”/“), FACTOR}
NUMBER = [0-9]
```

### Running
```
python3 main.py test.jl
```