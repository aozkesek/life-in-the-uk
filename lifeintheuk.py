#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 09:49:05 2023

@author: ahmetozkesek
"""

def __fill_qa_from(fname: str)-> tuple:
	import random
	import time

	# qas is a dictionary where key=question, value=answers
	qas = {}
	with open(fname, encoding="unicode-escape") as lituk:
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
				
				qa = ln[:-1]
				# empties, then refills the duplicates
				qas[qa] = [] 
	
	# shuffle the questions
	random.seed(time.clock_gettime_ns(0))
	# FIX: population must be a sequence not a dict!!!
	qi = random.sample(list(qas), len(qas)) 

	return (qas, qi)		

def __lituk_print(qas: dict, qi: list):
	fname = "lituk-tests"
	
	i = 0
	que = {}
	ans = {}
	
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

def __lituk_test(qas: dict, qi: list, ndx: int = 0):
	import os
	
	# ai holds answers (True/False, Question)
	ai = []
	# ask only a set of 24 questions
	p = ndx * 24

	for q in qi[p : p+24]:
		os.system("clear")

		print(f"Life in the UK Test [{p+1} / {len(qi) // 24}]:\n")
		print(f"The tests and {len(qi)} questions are shuffle everytime.\n")
		print(f"Q->{q}")
		
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
	if t / 24 >= 0.75:
		print(t, "C,", 24-t, "W > PASSED.")
	else:
		print(t, "C,", 24-t, "W > FAILED")
	
def __lituk_distance(qas):
	# pick one of the basic algo 
	import textdistance.algorithms.edit_based as td

	i = 0
	sqas = sorted(list(qas))
	for q in sqas:
		print(q)
		i = i + 1
		# skip the ones we already looked in the previous iteration
		subqas = sqas[i:]
		for t in subqas:
			res = td.hamming(q,t)
			# a score of 1 is 100% same, the bigger result the different
			if res < 15:
				print("\t", res, t)
	

if __name__ == "__main__":
	import sys
	
	qas, qi = __fill_qa_from("life-in-the-uk.qa.txt")
	
	if len(sys.argv) > 1:
		if sys.argv[1] == "print":
			__lituk_print(qas, qi)
		elif sys.argv[1] == "dump":
			for q in sorted(list(qas)):
				print(q)
		elif sys.argv[1] == "dist":
			__lituk_distance(qas)
		else:
			print("usage:\n\n\tpython lifeintheuk.py [print|dump|dist]")
		sys.exit(0)
			
	for i in range(len(qas) // 24):
		__lituk_test(qas, qi, i)
		
		print("")
		
		c = input("press C+Enter for continue, or any key to end ->")
		if c != "c" and c != "C":
			break

