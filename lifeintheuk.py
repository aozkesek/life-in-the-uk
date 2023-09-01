#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 09:49:05 2023

@author: ahmetozkesek
"""

def fill_qa_from(fname: str)-> dict:
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
				
	return qas		

def lituk_test(qas: dict, qi: list, ndx: int = 0):
	import os
	
	# ai is a list of tuples of true and false answers (True/False, Question)
	ai = []
	# ask only 24 questions
	p = ndx * 24

	for q in list(qi)[p : p+24]:
		os.system("clear")

		print("Life in the UK Test [", p+1 , "..", p+24, "] /", len(qi), ":\n")
		print("Q->", q)
		
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
		
	if t / 24 >= 0.75:
		print(t/24, "PASSED.")
	else:
		print(t/24, "FAILED")
	
if __name__ == "__main__":
	import random
	import time
	
	qas = fill_qa_from("life-in-the-uk.qa.txt")
	
	# shuffle the questions
	random.seed(time.clock_gettime_ns(0))
	qi = random.sample(list(qas), len(qas)) # population must be a sequence not a dict!!!
	
	for i in range(len(qas) // 24):
		lituk_test(qas, qi, i)
		
		print("")
		
		c = input("press C+Enter for continue, or any other key for finish ->")
		if c != "c" and c != "C":
			break

