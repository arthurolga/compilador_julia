function lala(n::Int)::Bool
    if (n == 3)
        return true
    end
    local a::Bool
    a = lulu(n)
    return a
end

function lulu(n::Int)::Bool
    if (n==5)
        return true
    end
    return false
end




local x::Int
x = lala(4)
println(x)