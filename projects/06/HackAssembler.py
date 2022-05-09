import sys
import os

comp = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
}

dest = {
    "null": "000",
    "M": "001",
    "D": "010",
    "A": "100",
    "MD": "011",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

jump = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

table = {
    "SCREEN": 16384,
    "KBD": 24576,
}

for i in range(0,16):
  label = "R" + str(i)
  table[label] = i

counter = 16

def clean(line):
    char = line[0]
    if char == "/" or char == "\n":
        return ""
    elif char == " ":
        return clean(line[1:])
    else:
        return char + clean(line[1:])

def c_instruction_template(line):
    line = line[:-1]
    if not ";" in line:
        line += ";empty"
    if not "=" in line:
        line = "empty=" + line
    return line

def add_variable_to_table(label):
    global counter
    table[label] = counter
    counter += 1
    return table[label]

def a_instruction(line):
    if line[1].isalpha():
        label = line[1:-1]
        a_value = table.get(label, -1)
        if a_value == -1:
            a_value = add_variable_to_table(label)
    else:
        a_value = int(line[1:])
    binary = bin(a_value)[2:].zfill(16)
    return binary

def c_instruction(line):
    line = c_instruction_template(line)
    tmp = line.split("=")
    dest_value = dest.get(tmp[0], "000")
    tmp = tmp[1].split(";")
    comp_value = comp.get(tmp[0], "000")
    jump_value = jump.get(tmp[1], "000")
    return "111" + comp_value + dest_value + jump_value

def skim():
    file = open(sys.argv[1], 'r')
    temp_file = open("temp.txt", 'w')
    counter = 0
    for line in file:
        stripped_line = clean(line)
        if stripped_line != "":
            if stripped_line[0] == "(":
                label = stripped_line[1:-1]
                table[label] = counter
                stripped_line = ""
            else:
                counter += 1
                temp_file.write(stripped_line + "\n")
    file.close()
    temp_file.close()

def parser(line):
    if line[0] == '@':
        return a_instruction(line)
    else:
        return c_instruction(line)


def main():
    skim()
    file = open("temp.txt", 'r')
    dest_file = open("HackAssembler.hack", 'w')
    for line in file:
        new_line = parser(line)
        dest_file.write(new_line + "\n")

    file.close()
    dest_file.close()

main()
