
# Nand to Tetris I - Capstone Project Notes & Viva Preparation Guide

**Course:** Nand to Tetris – I (ETCNTC301)  
**Institution:** School of Engineering & Technology, K.R. Mangalam University  
**Student Name:** Tanish Tyagi  
**Roll Number:** 2501730414  
**Personal Parameter (K):** `14` (Last two digits of roll number)

---

## 1. Parameter Calculations (Based on K = 14)

| Parameter | Formula | Calculated Value |
|---|---|---|
| K | Last 2 digits of Roll Number | **14** |
| Starting Row | Row K | **Row 14** |
| Box Height | Fixed requirement | **20 screen rows** |
| Ending Row | Starting Row + Height - 1 | **Row 33** |
| Box Width | 16 × ((K mod 4) + 1) | 14 mod 4 = 2 → 16 × 3 = **48 pixels** |
| Words per Row | Width / 16 | **3 words per row** |
| First Row Base Address | SCREEN + 32 × K | 16384 + 32 × 14 = **16832** |
| Last Row Base Address | 16384 + 32 × 33 | **17440** |
| Extra Assembler Feature | K mod 3 | 14 mod 3 = 2 → **Duplicate-label warning** |

**Total screen words used:** 20 × 3 = 60 words.

---

## 2. Understanding Hack Screen Memory Architecture

- **Screen Dimensions:** 256 rows high × 512 pixels wide.
- **Screen Base Address:** `16384` (`0x4000`).
- **Words per Row:** 512 pixels / 16 bits per word = 32 words.
- **Row Address Formula:**

  `Address = 16384 + 32 × row`

- **Pixel Colors:**
  - `0` = `0000000000000000` → White / Clear.
  - `-1` = `1111111111111111` → Black.
- **Memory-Mapped Keyboard:** Address `24576` (`KBD`).
  - If no key is pressed, `RAM[24576] == 0`.
  - If a key is pressed, `RAM[24576] != 0`.

---

## 3. How the Files Work

### A. `assembler.py` (Two-Pass Python Assembler)

The assembler translates Hack assembly instructions (`.asm`) into 16-bit binary machine instructions (`.hack`).

**Pass 1 – Label Collection and Duplicate Detection**

1. Reads the assembly file line by line.
2. Removes comments (`// ...`) and unnecessary whitespace.
3. Maintains a ROM instruction counter.
4. Identifies labels such as `(MAIN_LOOP)`.
5. Checks whether a label has already been defined.
6. If a duplicate label is found, displays a warning with its line number and previous address.

**Pass 2 – Binary Code Generation**

- **A-Instructions (`@value` or `@symbol`):**
  - Numeric values are converted into 15-bit binary and prefixed with `0`.
  - Predefined symbols such as `@KBD`, `@SCREEN`, and `@R0` use standard addresses.
  - Labels use their ROM addresses from Pass 1.
  - New variables receive RAM addresses starting from 16.

- **C-Instructions (`dest=comp;jump`):**
  - Follow the 16-bit Hack instruction format.
  - Begin with `111`.
  - Contain computation, destination, and jump fields.
  - Use lookup tables to generate binary machine code.

**Symbols Export**

The assembler generates `symbols.txt`, containing labels and variables with their assigned addresses.

Examples:

```text
MAIN_LOOP = 0
color = 16
row_addr = 17
```

**Extra Feature for K mod 3 = 2:**

The assembler detects duplicate user-defined labels and prints a warning instead of silently replacing the original label address.

### B. `Box.asm` (Screen Drawing Program)

This program continuously checks the keyboard and draws or clears a rectangular area on the Hack screen.

**Keyboard Polling**

- Checks the keyboard using `@KBD`.
- If `D == 0`, sets `color = 0` (white).
- If `D != 0`, sets `color = -1` (black).

**Outer Loop (`ROW_LOOP`)**

- Executes for 20 rows.
- Starts at screen address `16832` (row 14).
- Advances by 32 words after each row.
- Covers rows 14 through 33.

**Inner Loop (`COL_LOOP`)**

- Executes for 3 words per row.
- Writes the selected color into screen memory.
- Advances horizontally by one word each iteration.
- Each word represents 16 horizontal pixels.

**Result:**

A 48-pixel-wide rectangular area, 20 screen rows tall, is continuously drawn in black while a key is pressed and cleared when no key is pressed.

### C. `compare.py` (Validation Tool)

- Compares generated `.hack` files with official reference files.
- Checks machine instructions line by line.
- Displays matching instructions or differences.
- Supports individual file comparisons and batch comparisons.

Supported standard test programs:

- `Add`
- `Max`
- `Rect`
- `Pong`

**Important:** A test is considered passed only after the corresponding official reference file is available and the comparison reports `PERFECT MATCH`.

---

## 4. Live Viva Modification Cheat Sheet

The examiner may ask you to move the box, change its size, or invert its colors.

### 1. Move the Box Down or Up

Find the starting address instruction in `Box.asm`:

```hack
@16832
```

Formula:

`SCREEN + (32 × Starting Row)`

Examples:

**Move to row 20:**

`16384 + (32 × 20) = 17024`

Change `@16832` to `@17024`.

**Move to row 10:**

`16384 + (32 × 10) = 16704`

Change `@16832` to `@16704`.

### 2. Change the Box Width

Find the instruction:

```hack
@3
```

This represents 3 words per row.

Examples:

- 16 pixels: Change `@3` to `@1`.
- 32 pixels: Change `@3` to `@2`.
- 64 pixels: Change `@3` to `@4`.
- 128 pixels: Change `@3` to `@8`.

Formula:

`Width = Number of Words × 16`

### 3. Change the Box Height

Find the instruction:

```hack
@20
```

This represents the number of screen rows.

Examples:

- 10 rows: Change `@20` to `@10`.
- 30 rows: Change `@20` to `@30`.
- 40 rows: Change `@20` to `@40`.

Remember: the height should remain within the available screen boundaries.

### 4. Invert the Colors

Find these instructions in `Box.asm`:

```hack
// When a key is pressed
M=-1

// When no key is pressed
M=0
```

Swap them:

```hack
// When a key is pressed
M=0

// When no key is pressed
M=-1
```

Now the selected area will be white while a key is pressed and black when released.

### 5. Move the Box Horizontally

Each screen word represents 16 horizontal pixels.

The current starting address is:

`16832`

To move 14 words (224 pixels) to the right:

`16832 + 14 = 16846`

Change:

```hack
@16832
```

to:

```hack
@16846
```

This places the 48-pixel-wide box approximately in the horizontal center of the screen.

---

## 5. Likely Viva Questions and Answers

**Q1. Why is an assembler built in two passes instead of one?**

An assembler uses two passes because a program can jump to a label that appears later in the code. This is called a forward reference.

In Pass 1, the assembler collects all labels and their ROM addresses. In Pass 2, it translates the instructions into binary using the collected addresses.

**Q2. Why do user variables start at RAM address 16?**

RAM addresses 0 to 15 are reserved for registers R0 to R15. Therefore, general-purpose variables start at RAM address 16.

**Q3. Why do we add 32 to move down one screen row?**

The Hack screen has 512 pixels per row. Each memory word stores 16 pixels.

`512 / 16 = 32 words`

Therefore, moving down one row requires adding 32 to the screen memory address.

**Q4. How does memory-mapped I/O work in Hack?**

Hack uses memory addresses to communicate with input and output devices.

- Screen memory occupies addresses 16384–24575.
- Keyboard input is mapped to address 24576.

The CPU reads or writes these addresses to interact with the devices.

**Q5. What extra feature did you implement in your assembler?**

My roll number ends in 14.

`14 mod 3 = 2`

Therefore, my extra feature is duplicate-label detection. If the same user-defined label is declared more than once, the assembler prints a warning containing the duplicate label and its line number.

**Q6. What is the difference between `.asm` and `.hack` files?**

- `.asm` contains human-readable Hack assembly instructions.
- `.hack` contains 16-bit binary machine instructions that the Hack computer can execute.

**Q7. What does the A-instruction do?**

An A-instruction loads a 15-bit value or address into the A register.

Example:

```hack
@16384
```

**Q8. What does the C-instruction do?**

A C-instruction performs a computation, optionally stores the result in a destination, and optionally performs a jump.

Example:

```hack
D=M
```

It copies the value stored at the memory address in A into the D register.

**Q9. What is the purpose of the ALU?**

The Arithmetic Logic Unit performs arithmetic and logical operations such as addition, subtraction, AND, and NOT.

**Q10. What is the purpose of the Program Counter (PC)?**

The PC stores the address of the next instruction to execute. It normally increments after each instruction or loads a new address when a jump occurs.

---

## 6. How to Re-Assemble and Test

After modifying `Box.asm`, open the terminal in your capstone directory.

**Step 1 – Assemble the program**

```cmd
python assembler.py Box.asm
```

This generates:

1. `Box.hack` – Binary machine code.
2. `symbols.txt` – Symbol table containing labels and variables.

**Step 2 – Compare official test files**

```cmd
python compare.py
```

The comparison tool checks Add, Max, Rect, and Pong when their source and official reference files are available.

**Step 3 – Test the Hack computer**

1. Open the official Nand2Tetris Hardware Simulator.
2. Load and test `CPU.hdl`, `Memory.hdl`, and `Computer.hdl` using the corresponding official test scripts.
3. Open the CPU Emulator.
4. Load `Box.hack`.
5. Run the program.
6. Press and release keys to verify that the rectangle changes between black and white.

---

## 7. Important Project Values – Quick Revision

| Item | Value |
|---|---|
| Student | Tanish Tyagi |
| Roll Number | 2501730414 |
| K | 14 |
| Starting Screen Row | 14 |
| Ending Screen Row | 33 |
| Height | 20 rows |
| Width | 48 pixels |
| Words per Row | 3 |
| Starting Screen Address | 16832 |
| Last Row Base Address | 17440 |
| Screen Base Address | 16384 |
| Keyboard Address | 24576 |
| Extra Feature | Duplicate-label warning |
| Assembler Type | Two-pass assembler |
| Box Machine Code | 53 instructions |

