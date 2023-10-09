#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 09:49:05 2023

@author: ahmetozkesek
"""

__fname = "life-in-the-uk.qa.txt"
__cname = "life-in-the-uk.qa.cont"

def __fill_qa_from(cont: bool = False)-> tuple:
	import random
	import time

	# qas is a dictionary where key=question, value=answers
	qas = {}
	with open(__fname) as lituk:
		qa = ""
		
		for ln in lituk.readlines():
			# guards itself from some unqualified lines
			if len(ln) < 3:
				continue
			
			# checks if the line is a question or one of the answers
			if len(qa) > 0 and ln[0:4] in ["A   ", "    "]:
				qas[qa].append(ln[:-1])
			else:
				# previous answer set's length must be either 2 or 4
				if len(qa) > 0:
					assert len(qas[qa]) in [2,4], qa
				
				#qa = ln[:-1]
				qa = ln
				# empties, then refills the duplicates
				qas[qa] = [] 
	
	qi = None
	if cont:
		try:
			# fill qi from the file where they left the previous exam
			with open(__cname,"r") as lituk:
				qi = lituk.readlines()
		except FileNotFoundError:
			# skip if the file does not exist, qi will be checked later
			pass
		
	# check qi in case of something went wrong while we try to load it above
	if not cont or qi is None:
		# shuffle the questions
		random.seed(time.clock_gettime_ns(0))
		qi = random.sample(list(qas), len(qas)) 
		qi.append("\n[0]")
		# write qi into a file, so they can continue next time where they left
		with open(__cname,"w") as lituk:
			lituk.writelines(qi)
			
	return (qas, qi)		

def __lituk_print(qas: dict, qi: list):
	
	i = 0
	que = {}
	ans = {}
	fname = "lituk-exams"
	
	# fill each test with a set of 24 questions
	for q in qi:
		t = i // 24
		tq = i % 24
		
		if tq == 0:
			que[t+1] = []
			ans[t+1] = {}
			
		que[t+1].append(f"\nQ:{tq+1}> {q}\n\n")
		j = 0
		ans[t+1][tq+1] = []
		for a in qas[q]:
			j += 1
			que[t+1].append(f"\t{j}) {a[4:]}\n")
			if a[0:1] == "A":
				ans[t+1][tq+1].append(a[4:])
		
		i += 1
	
	__write2txt(fname, que, ans)
	__txt2pdf(fname)
	
def __write2txt(fname, que, ans):
	
	with open(fname+".txt", "w") as fd:
		for q in list(que):
			fd.writelines(["===========================\n"])
			fd.writelines([f"Life In The UK Test {q}\n"])
			fd.writelines(["===========================\n"])
			
			fd.writelines(que[q])
			fd.writelines(["\n"])
		
			fd.writelines(["\n\n++++++++ Answers ++++++++++\n\n"])
		
			fd.writelines([str(ans[q])])
			fd.writelines(["\n\n"])
		

def __txt2pdf(fname):
	import subprocess
	
	# convert txt to the ps first
	cmd = ["enscript", "-p", fname+".ps", "-t Life-In-The-UK", 
		   "--word-wrap", fname+".txt"]
	cp = subprocess.run(cmd)
	if cp.returncode != 0:
		print("Failed TXT to convert PS!")
		return
	
	# then convert ps to the pdf
	cmd = ["ps2pdf", fname+".ps", fname+".pdf"]
	cp = subprocess.run(cmd)
	if cp.returncode != 0:
		print("Failed PS to convert PDF!")
		return
	
	# txt and ps are not needed anymore, remove them
	subprocess.run(["rm", fname+".txt", fname+".ps"])

def __lituk_test(qas: dict, qi: list, prv: int = 0):
	curr = prv
	for i in range(prv, len(qas) // 24):
		try:
			__lituk_exam(qas, qi, i)
			curr = i + 1
		except KeyboardInterrupt:
			break
		
		print("")
		
		try:
			c = input("press C+Enter for continue, or any key to end ->")
			if c != "c" and c != "C":
				break
		except KeyboardInterrupt:
			break
	
	qi[len(qi) - 1] = f"\n[{curr}]"
	with open(__cname,"w") as lituk:
		lituk.writelines(qi)

def __lituk_exam(qas: dict, qi: list, ndx: int = 0):
	import os
	
	# ai holds answers (True/False, Question)
	ai = []
	# ask only a set of 24 questions
	p = ndx * 24
	n = 1
	
	for q in qi[p : p+24]:
		os.system("clear")

		print(f"Life in the UK Test [{(p+1)//24} / {len(qi) // 24}]:\n")
		print(f"The tests and {len(qi)} questions are shuffle everytime.\n")
		print(f"Q-{p%24+n} -> {q}")
		n = n + 1
		
		i = 0
		for j in qas[q]:
			print("\t", i, ")", j[4:])
			i += 1
		
		print("")
		a = input("Choose the answer(s), put [,] between multiples, press Enter -> ")
		b = a.split(",")
		
		# choose first option for invalid entry
		if b[0] not in ["0","1","2","3"]:
			b[0] = "0"
		
		if len(b) == 2 and b[1] not in ["0","1","2","3"]:
			b[1] = "0"
		
		if len(b) == 3 and b[2] not in ["0","1","2","3"]:
			b[2] = "0"
		
		a = qas[q][int(b[0])][0] == "A"
		for k in range(len(b)):
			a = a and qas[q][int(b[k])][0] == "A"
			
		ai.append((a, q))
		
	# dump the False answers
	t = 0
	for i in ai:
		if i[0]:
			t += 1
		else:
			print(i)
			for j in qas[i[1]]:
				print("\t", j)
	# yo have to get right at least 75% correct to PASS the exam.
	print("you have done the exam, the result is;")
	if t / 24 >= 0.75:
		print(t, "Correct,", 24-t, "Wrong > PASSED.")
	else:
		print(t, "Correct,", 24-t, "Wrong > FAILED")
	
def __lituk_distance(qas):
	# pick one of the basic algo 
	import textdistance.algorithms.edit_based as td

	i = 0
	sqas = sorted(list(qas))
	for q in sqas:
		print(q[:-1])
		i = i + 1
		# skip the ones we already looked in the previous iteration
		subqas = sqas[i:]
		for t in subqas:
			res = td.hamming(q,t)
			# a score of 1 is 100% same, the bigger result the different
			if res < 15:
				print("\t", res, t[:-1])

if __name__ == "__main__":
	import sys

	has_arg = len(sys.argv) > 1
	is_cont = has_arg and sys.argv[1] == "cont"
	is_dump = has_arg and sys.argv[1] == "dump"
	is_dist = has_arg and sys.argv[1] == "dist"
	is_prnt = has_arg and sys.argv[1] == "print"
	
	qas, qi = __fill_qa_from(is_cont)
	prv = int(qi[len(qi)-1].replace("\n","").replace("[","").replace("]",""))
	qi = qi[:-1]
	
	if has_arg:
		if is_prnt:
			__lituk_print(qas, qi)
		elif is_dump:
			for q in sorted(list(qas)):
				print(q[:-1])
		elif is_dist:
			__lituk_distance(qas)
		elif is_cont:
			__lituk_test(qas, qi, prv)
		else:
			print("usage:\n\n\tpython lifeintheuk.py [print|dump|dist]")
		sys.exit(0)
			
	__lituk_test(qas, qi, prv)
	