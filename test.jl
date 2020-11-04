local a::Bool
local i::Int

a = true
b = false

n = readline()
i = 0
while i < (n+1)
    i = i+1
    
    value = i / 2
    
    if (value*2 )== i
        println("- "*i*" PAR")
    else
        println("- "*i*" IMPAR")
    end

end


    

