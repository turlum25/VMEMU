# vmemu.py
# made 5/23/2026


import os 
import time
import argparse
import subprocess
import sys

print("VMEMU | Version 0.1-PoC | By Turlum25")
print()

parser = argparse.ArgumentParser()
parser.add_argument(
    '-l', '--load',
    metavar='FILE',
    type=str,
    help='path to a <NAME>.py file to run'
)
args = parser.parse_args()

try:
	from RAM import EditRAM, ReadRAM
	ram_available = True
	print("sys: RAM found")
except ImportError:
	ram_available = False
	print("sys: error: RAM not found, not using.")

debug = 1

x0 = 0
x1 = 0
x2 = 0
x3 = 0
x4 = 0

flags = {"eq": False, "ne": True}
instructions = []
# dictionary to hold label mappings (e.g., {"_yay": 4})
labels = {}
pc = 0

if args.load:
    result = subprocess.run([sys.executable, args.load], capture_output=True, text=True)
    instructions = [line.strip() for line in result.stdout.split('\n') if line.strip()]
    print("sys: loaded pre-boot code")
else:
    instructions = []


while True:
	if args.load:
		if pc < len(instructions):
			main = instructions[pc]
			pc += 1
		else:
			print("sys: done executing pre-boot code")
			break
	else:
		main = input("> ").strip()
		if not main:
			continue

	
	if main.strip().lower() == "run":
		# LABEL PASS
		# first pass: find all labels and map them to their execution index
		execution_idx = 0
		temp_instructions = []
		for instr in instructions:
			clean_instr = instr.strip()
			if clean_instr.startswith("_") and clean_instr.endswith(":"):
				label_name = clean_instr[:-1].lower()
				labels[label_name] = execution_idx
			else:
				temp_instructions.append(instr)
				execution_idx += 1
		instructions = temp_instructions
		# END OF LABEL PASS

		while pc < len(instructions):
			current_instr = instructions[pc]
			pc += 1
			
			parts = current_instr.split()
			anyInt = 0
			
			# LABEL RESOLUTION
			# check if the branch destination is a known label name
			has_label = False
			for part in parts:
				clean_part = part.replace(",", "").lower()
				if clean_part in labels:
					anyInt = labels[clean_part]
					has_label = True
					break
			
			if not has_label:
				for part in parts:
					clean_part = part.replace(",", "")
					if clean_part.isdigit():
						anyInt = int(clean_part)
						break
			# END OF LABEL RESOLUTION

			# EDR
			if "edr" in current_instr:
				if not ram_available:
					print("\nhalt: panic: RAM module not found or missing")
					exit(1)
				clean_main = current_instr.replace(",", " ")
				words = clean_main.split()
				if len(words) >= 4:
					EditRAM(words[1], words[2], words[3])
			# END OF EDR

			# RDE
			elif "rde" in current_instr:
				if not ram_available:
					print("\nhalt: panic: RAM module not found or missing")
					exit(1)
				clean_main = current_instr.replace(",", " ")
				words = clean_main.split()
				if len(words) >= 3:
					dest_reg = words[1].lower()
					ram_addr = words[2].lower()
					raw_bytes = ReadRAM(ram_addr)
					combined_binary = raw_bytes.replace(" ", "")
					decimal_val = int(combined_binary, 2)
					if dest_reg == "x0": x0 = decimal_val
					elif dest_reg == "x1": x1 = decimal_val
					elif dest_reg == "x2": x2 = decimal_val
					elif dest_reg == "x3": x3 = decimal_val
					elif dest_reg == "x4": x4 = decimal_val
			# END OF RDE

			# MOV
			elif "mov" in current_instr:
				src_val = anyInt
				if "x0" in current_instr[6:]: src_val = x0
				elif "x1" in current_instr[6:]: src_val = x1
				elif "x2" in current_instr[6:]: src_val = x2
				elif "x3" in current_instr[6:]: src_val = x3
				elif "x4" in current_instr[6:]: src_val = x4

				if "x0" in current_instr[:6]: x0 = src_val
				elif "x1" in current_instr[:6]: x1 = src_val
				elif "x2" in current_instr[:6]: x2 = src_val
				elif "x3" in current_instr[:6]: x3 = src_val
				elif "x4" in current_instr[:6]: x4 = src_val
			# END OF MOV

			# MATH
			elif "add" in current_instr or "sub" in current_instr or "mul" in current_instr:
				dest, src1, src2 = "", "", ""
				clean_main = current_instr.replace(",", " ")
				words = clean_main.split()
				for word in words:
					if word in ["x0", "x1", "x2", "x3", "x4"]:
						if not dest: dest = word
						elif not src1: src1 = word
						elif not src2: src2 = word
				val1 = 0
				if src1 == "x0": val1 = x0
				elif src1 == "x1": val1 = x1
				elif src1 == "x2": val1 = x2
				elif src1 == "x3": val1 = x3
				elif src1 == "x4": val1 = x4
				val2 = anyInt if anyInt != 0 else 0
				if src2 == "x0": val2 = x0
				elif src2 == "x1": val2 = x1
				elif src2 == "x2": val2 = x2
				elif src2 == "x3": val2 = x3
				elif src2 == "x4": val2 = x4
				if "add" in current_instr: result = val1 + val2
				elif "sub" in current_instr: result = val1 - val2
				elif "mul" in current_instr: result = val1 * val2
				if dest == "x0": x0 = result
				elif dest == "x1": x1 = result
				elif dest == "x2": x2 = result
				elif dest == "x3": x3 = result
				elif dest == "x4": x4 = result
			# END OF MATH

			# CMP
			elif "cmp" in current_instr:
				clean_main = current_instr.replace(",", " ")
				words = clean_main.split()
				regs = [w for w in words if w in ["x0", "x1", "x2", "x3", "x4"]]
				val1 = 0
				val2 = anyInt
				if len(regs) >= 1:
					if regs[0] == "x0": val1 = x0
					elif regs[0] == "x1": val1 = x1
					elif regs[0] == "x2": val1 = x2
					elif regs[0] == "x3": val1 = x3
					elif regs[0] == "x4": val1 = x4
				if len(regs) == 2:
					if regs[1] == "x0": val2 = x0
					elif regs[1] == "x1": val2 = x1
					elif regs[1] == "x2": val2 = x2
					elif regs[1] == "x3": val2 = x3
					elif regs[1] == "x4": val2 = x4
				flags["eq"] = (val1 == val2)
				flags["ne"] = (val1 != val2)
			# END OF CMP

			# BRANCH
			elif "b.eq" in current_instr:
				if flags["eq"]: pc = anyInt
			elif "b.ne" in current_instr:
				if flags["ne"]: pc = anyInt
			elif "b" in current_instr:
				pc = anyInt
			# END OF BRANCH

			# NOP
			elif "nop" in current_instr:
				pass
			# END OF NOP

			# RET
			elif "ret" in current_instr:
				print("\nhalt")
				exit(0)
			# END OF RET

			else:
				print("\nhalt: panic: incorrect syntax")
				exit(1)
				
			if debug == 1:
				print(f"DEBUG LABELS: {labels}")

			print(f"x0 = {x0}")
			print(f"x1 = {x1}")
			print(f"x2 = {x2}")
			print(f"x3 = {x3}")
			print(f"x4 = {x4}")
		break

	if main.strip():
		if main.strip().lower() == "al.r":
			# LABEL PASS FOR AL.R
			execution_idx = 0
			temp_instructions = []
			for instr in instructions:
				clean_instr = instr.strip()
				if clean_instr.startswith("_") and clean_instr.endswith(":"):
					label_name = clean_instr[:-1].lower()
					labels[label_name] = execution_idx
				else:
					temp_instructions.append(instr)
					execution_idx += 1
			instructions = temp_instructions
			# END OF LABEL PASS FOR AL.R

			while pc < len(instructions):
				current_instr = instructions[pc]
				pc += 1
				
				parts = current_instr.split()
				anyInt = 0
				
				# LABEL RESOLUTION FOR AL.R
				has_label = False
				for part in parts:
					clean_part = part.replace(",", "").lower()
					if clean_part in labels:
						anyInt = labels[clean_part]
						has_label = True
						break
				
				if not has_label:
					for part in parts:
						clean_part = part.replace(",", "")
						if clean_part.isdigit():
							anyInt = int(clean_part)
							break
				# END OF LABEL RESOLUTION FOR AL.R

				# EDR
				if "edr" in current_instr:
					if not ram_available:
						print("\nhalt: panic: RAM module not found or missing")
						exit(1)
					clean_main = current_instr.replace(",", " ")
					words = clean_main.split()
					if len(words) >= 4:
						EditRAM(words[1], words[2], words[3])
				# END OF EDR

				# RDE
				elif "rde" in current_instr:
					if not ram_available:
						print("\nhalt: panic: RAM module not found or missing")
						exit(1)
					clean_main = current_instr.replace(",", " ")
					words = clean_main.split()
					if len(words) >= 3:
						dest_reg = words[1].lower()
						ram_addr = words[2].lower()
						raw_bytes = ReadRAM(ram_addr)
						combined_binary = raw_bytes.replace(" ", "")
						decimal_val = int(combined_binary, 2)
						if dest_reg == "x0": x0 = decimal_val
						elif dest_reg == "x1": x1 = decimal_val
						elif dest_reg == "x2": x2 = decimal_val
						elif dest_reg == "x3": x3 = decimal_val
						elif dest_reg == "x4": x4 = decimal_val
				# END OF RDE

				# MOV
				elif "mov" in current_instr:
					src_val = anyInt
					if "x0" in current_instr[6:]: src_val = x0
					elif "x1" in current_instr[6:]: src_val = x1
					elif "x2" in current_instr[6:]: src_val = x2
					elif "x3" in current_instr[6:]: src_val = x3
					elif "x4" in current_instr[6:]: src_val = x4

					if "x0" in current_instr[:6]: x0 = src_val
					elif "x1" in current_instr[:6]: x1 = src_val
					elif "x2" in current_instr[:6]: x2 = src_val
					elif "x3" in current_instr[:6]: x3 = src_val
					elif "x4" in current_instr[:6]: x4 = src_val
				# END OF MOV

				# MATH
				elif "add" in current_instr or "sub" in current_instr or "mul" in current_instr:
					dest, src1, src2 = "", "", ""
					clean_main = current_instr.replace(",", " ")
					words = clean_main.split()
					for word in words:
						if word in ["x0", "x1", "x2", "x3", "x4"]:
							if not dest: dest = word
							elif not src1: src1 = word
							elif not src2: src2 = word
					val1 = 0
					if src1 == "x0": val1 = x0
					elif src1 == "x1": val1 = x1
					elif src1 == "x2": val1 = x2
					elif src1 == "x3": val1 = x3
					elif src1 == "x4": val1 = x4
					val2 = anyInt if anyInt != 0 else 0
					if src2 == "x0": val2 = x0
					elif src2 == "x1": val2 = x1
					elif src2 == "x2": val2 = x2
					elif src2 == "x3": val2 = x3
					elif src2 == "x4": val2 = x4
					if "add" in current_instr: result = val1 + val2
					elif "sub" in current_instr: result = val1 - val2
					elif "mul" in current_instr: result = val1 * val2
					if dest == "x0": x0 = result
					elif dest == "x1": x1 = result
					elif dest == "x2": x2 = result
					elif dest == "x3": x3 = result
					elif dest == "x4": x4 = result
				# END OF MATH

				# CMP
				elif "cmp" in current_instr:
					clean_main = current_instr.replace(",", " ")
					words = clean_main.split()
					regs = [w for w in words if w in ["x0", "x1", "x2", "x3", "x4"]]
					val1 = 0
					val2 = anyInt
					if len(regs) >= 1:
						if regs[0] == "x0": val1 = x0
						elif regs[0] == "x1": val1 = x1
						elif regs[0] == "x2": val1 = x2
						elif regs[0] == "x3": val1 = x3
						elif regs[0] == "x4": val1 = x4
					if len(regs) == 2:
						if regs[1] == "x0": val2 = x0
						elif regs[1] == "x1": val2 = x1
						elif regs[1] == "x2": val2 = x2
						elif regs[1] == "x3": val2 = x3
						elif regs[1] == "x4": val2 = x4
					flags["eq"] = (val1 == val2)
					flags["ne"] = (val1 != val2)
				# END OF CMP

				# BRANCH
				elif "b.eq" in current_instr:
					if flags["eq"]: pc = anyInt
				elif "b.ne" in current_instr:
					if flags["ne"]: pc = anyInt
				elif "b" in current_instr:
					pc = anyInt
				# END OF BRANCH

				# NOP
				elif "nop" in current_instr:
					pass
				# END OF NOP

				# RET
				elif "ret" in current_instr:
					print("\nsys: halt")
					exit(0)
				# END OF RET

				else:
					print("\nsys: halt: panic: incorrect syntax")
					exit(1)
				
				print()	
				print(f"x0 = {x0}")
				print(f"x1 = {x1}")
				print(f"x2 = {x2}")
				print(f"x3 = {x3}")
				print(f"x4 = {x4}")
				print()
		else:
			instructions.append(main)

