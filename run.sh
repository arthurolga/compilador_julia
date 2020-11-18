python3 main.py 'test.jl'
nasm -f elf32 -F dwarf -g program.asm
ld -m elf_i386 -o program program.o
./program