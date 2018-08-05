import random
import base64
from flask import Flask, request, render_template, redirect, make_response
import sqlite3
import string
import requests
import sys
#a=string.digits + string.ascii_letters #'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def GetCRC(g):
	
	num1 = ord(g[0])
	num2 = ord(g[1])
	num3 = ord(g[2])
	return (num1 * num2 + num2 * num3 + num3 * (num1 + 1) + num1 * num2 * num3 % 1373)

num1=32900
num2=33900
num3=37673
num4=31649
num5=35996

aa = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ{}_";
ff = "3290033900376733164935996"


for i in aa:
	for j in aa:
		for k in aa:
			tmp = i + j + k
			bb=GetCRC(tmp)
			if bb==num1:
				print("num1:")
				print(tmp)
			if bb==num2:
				print("num2:")
				print(tmp)
			if bb==num3:
				print("num3:")
				print(tmp)
			if bb==num4:
				print("num4:")
				print(tmp)
			if bb==num5:
				print("num5:")
				print(tmp)
				