
"""
assembler.py - Two-pass Hack Assembler in Python 3
Author: Tanish Tyagi (Roll Number: 2501730414, K=14)
Translates Hack assembly (.asm) into Hack machine code (.hack).

Extra Features (K=14, 14 mod 3 = 2):
1. Detects and prints a clear warning if the same label is declared more than once.
2. Saves all labels and variables with their addresses into symbols.txt.
"""

import sys
import os

# -------------------------------------------------------------
# 1. Lookup Tables for C-Instructions
# -------------------------------------------------------------

# Comp field translates to 7 bits
COMP_TABLE = {
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

    # Operations using RAM memory register M
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101",
}

# Dest field translates to 3 bits: [A, D, M]
DEST_TABLE = {
    "": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "DM": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111",
    "ADM": "111",
}

# Jump field translates to 3 bits
JUMP_TABLE = {
    "": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}


def get_predefined_symbols():
    """Returns the default predefined Hack symbols and their addresses."""

    symbols = {
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
        "SCREEN": 16384,
        "KBD": 24576,
    }

    # Add virtual registers R0 through R15
    for i in range(16):
        symbols[f"R{i}"] = i

    return symbols


def clean_line(line):
    """
    Strips inline comments (// ...) and trailing/leading whitespace.
    Returns the cleaned instruction string.
    """

    comment_idx = line.find("//")

    if comment_idx != -1:
        line = line[:comment_idx]

    return line.strip()


# -------------------------------------------------------------
# 2. Assembler Implementation
# -------------------------------------------------------------

def assemble(asm_filepath):
    """
    Assembles a Hack .asm file into 16-bit binary .hack instructions.

    Extra feature for K=14 (14 mod 3 = 2):
    Duplicate label warning and symbols.txt export.
    """

    # Initialize symbol table with predefined symbols
    symbol_table = get_predefined_symbols()

    # Track user-defined labels and variables
    user_labels = {}
    user_variables = {}

    # Read input assembly file
    with open(asm_filepath, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    # ---------------------------------------------------------
    # PASS 1: Symbol resolution for labels like (LOOP)
    # ---------------------------------------------------------

    rom_address = 0
    duplicate_label_warnings = []

    for line_idx, line in enumerate(raw_lines, start=1):

        cleaned = clean_line(line)

        if not cleaned:
            continue

        if cleaned.startswith("(") and cleaned.endswith(")"):

            # Label declaration
            label_name = cleaned[1:-1].strip()

            # EXTRA FEATURE (K=14, 14 mod 3 = 2)
            # Warn if a label is declared more than once
            if label_name in user_labels:

                prev_addr = user_labels[label_name]

                warning_msg = (
                    f"[WARNING] Line {line_idx}: "
                    f"Label '({label_name})' is already defined "
                    f"(pointing to ROM address {prev_addr})!"
                )

                duplicate_label_warnings.append(warning_msg)
                print(warning_msg)

            else:

                # Label points to the next actual instruction
                symbol_table[label_name] = rom_address
                user_labels[label_name] = rom_address

        else:

            # Each A-instruction or C-instruction uses one ROM address
            rom_address += 1

    # ---------------------------------------------------------
    # PASS 2: Code translation to 16-bit binary
    # ---------------------------------------------------------

    machine_code = []

    # Variable allocation starts at RAM address 16
    next_variable_address = 16

    for line_idx, line in enumerate(raw_lines, start=1):

        cleaned = clean_line(line)

        if not cleaned:
            continue

        # Labels do not generate machine code
        if cleaned.startswith("(") and cleaned.endswith(")"):
            continue

        # -----------------------------------------------------
        # CASE A: A-instruction, e.g. @value or @symbol
        # -----------------------------------------------------

        if cleaned.startswith("@"):

            symbol_part = cleaned[1:].strip()

            if symbol_part.isdigit():

                # Direct constant number
                address = int(symbol_part)

            else:

                # Symbol name: predefined, label or variable
                if symbol_part in symbol_table:

                    address = symbol_table[symbol_part]

                else:

                    # Allocate a new RAM variable
                    address = next_variable_address

                    symbol_table[symbol_part] = address
                    user_variables[symbol_part] = address

                    next_variable_address += 1

            # A-instruction: 0 followed by 15-bit binary
            if not 0 <= address <= 32767:
                raise ValueError(
                    f"Invalid A-instruction address at line {line_idx}: {address}"
                )

            binary_instruction = f"0{address:015b}"
            machine_code.append(binary_instruction)

        # -----------------------------------------------------
        # CASE C: C-instruction, e.g. dest=comp;jump
        # -----------------------------------------------------

        else:

            dest_str = ""
            comp_str = ""
            jump_str = ""

            rest = cleaned

            # Parse destination
            if "=" in rest:
                dest_str, rest = rest.split("=", 1)
                dest_str = dest_str.strip()

            # Parse computation and jump
            if ";" in rest:
                comp_str, jump_str = rest.split(";", 1)

                comp_str = comp_str.strip()
                jump_str = jump_str.strip()

            else:
                comp_str = rest.strip()

            # Validate instruction components
            if comp_str not in COMP_TABLE:
                raise ValueError(
                    f"Invalid computation at line {line_idx}: {comp_str}"
                )

            if dest_str not in DEST_TABLE:
                raise ValueError(
                    f"Invalid destination at line {line_idx}: {dest_str}"
                )

            if jump_str not in JUMP_TABLE:
                raise ValueError(
                    f"Invalid jump instruction at line {line_idx}: {jump_str}"
                )

            # Convert components into binary
            comp_bits = COMP_TABLE[comp_str]
            dest_bits = DEST_TABLE[dest_str]
            jump_bits = JUMP_TABLE[jump_str]

            # C-instruction format:
            # 111 + comp (7 bits) + dest (3 bits) + jump (3 bits)
            binary_instruction = (
                f"111{comp_bits}{dest_bits}{jump_bits}"
            )

            machine_code.append(binary_instruction)

    # ---------------------------------------------------------
    # WRITE OUTPUT .hack FILE
    # ---------------------------------------------------------

    base_name = os.path.splitext(asm_filepath)[0]
    out_hack_filepath = base_name + ".hack"

    with open(out_hack_filepath, "w", encoding="utf-8") as f:

        for code_line in machine_code:
            f.write(code_line + "\n")

    print(
        f"[OK] Assembled {len(machine_code)} instructions "
        f"-> {out_hack_filepath}"
    )

    # ---------------------------------------------------------
    # SAVE LABELS AND VARIABLES IN symbols.txt
    # ---------------------------------------------------------

    out_dir = os.path.dirname(asm_filepath) or "."
    symbols_filepath = os.path.join(out_dir, "symbols.txt")

    with open(symbols_filepath, "w", encoding="utf-8") as f:

        for label, addr in user_labels.items():
            f.write(f"{label} = {addr}\n")

        for var, addr in user_variables.items():
            f.write(f"{var} = {addr}\n")

    print(
        f"[OK] Symbols: Wrote {len(user_labels)} labels "
        f"and {len(user_variables)} variables -> {symbols_filepath}"
    )

    return out_hack_filepath, symbols_filepath


# -------------------------------------------------------------
# 3. Main Entry Point
# -------------------------------------------------------------

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python assembler.py <File.asm>")
        sys.exit(1)

    asm_file = sys.argv[1]

    if not os.path.exists(asm_file):
        print(f"Error: File not found: {asm_file}")
        sys.exit(1)

    assemble(asm_file)
