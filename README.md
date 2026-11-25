# Nand to Tetris I - Capstone Project: Make the Computer Draw a Box

**Course:** Nand to Tetris – I (ETCNTC301)  
**School:** School of Engineering & Technology, K.R. Mangalam University  
**Student Name:** Tanish Tyagi  
**Roll Number:** 2501730414  
**Personal Parameter (K):** `14` (Last two digits of Roll Number)

---

## 📌 Project Overview

This repository contains the complete implementation for the Nand to Tetris I Capstone Project:

1. **Hack Computer Hardware (HDL):** `CPU.hdl`, `Memory.hdl`, and `Computer.hdl`.
2. **Two-Pass Hack Assembler (Python 3):** `assembler.py` with a custom extra feature for `K mod 3 = 2` (Duplicate label declaration warning) and symbol table export.
3. **Interactive Box Program (Hack Assembly):** `Box.asm` compiled to `Box.hack`, which continuously polls the keyboard (`RAM[24576]`) and renders a 48-pixel-wide, 20-row-tall black rectangular box starting at Screen Row 14 while any key is pressed, erasing it when released.
4. **Validation Tool:** `compare.py` testing against official benchmark files (`Add`, `Max`, `Rect`, `Pong`).

---

## 📐 Personal Parameter Calculations (K = 14)

| Parameter | Formula | Value |
| :--- | :--- | :--- |
| **Roll Number** | `2501730414` | Last two digits = **14** |
| **K** | Personal Number | **14** |
| **Starting Screen Row** | Row K | **Row 14** (Rows 14 to 33) |
| **Box Height** | Fixed specification | **20 screen rows** |
| **Box Width** | `16 × ((K mod 4) + 1)` | `16 × (2 + 1) = 48 pixels` |
| **Words per Row** | Width / 16 | **3 words (16-bit memory registers)** |
| **Starting Screen Address** | `SCREEN + 32 × K` | `16384 + 32 × 14 = 16832` |
| **Last Row Address** | `16384 + 32 × 33` | **17440** |
| **Extra Assembler Feature** | `K mod 3` | `14 mod 3 = 2` → Duplicate label declaration warning |

---

## 📁 Repository Structure

```text
Capstone_nand/
├── README.md                          # Top-level project documentation
└── capstone/
    ├── assembler.py                   # Two-pass Hack Assembler in Python 3
    ├── Box.asm                        # Fully commented Hack Assembly source
    ├── Box.hack                       # Assembled 16-bit binary machine code
    ├── symbols.txt                    # Symbol table export
    ├── compare.py                     # Machine code comparison testing tool
    ├── CPU.hdl                        # Hack CPU implementation
    ├── Memory.hdl                     # Memory-mapped RAM, Screen, Keyboard
    ├── Computer.hdl                   # Top-level Hack Computer chip
    ├── NOTES.md