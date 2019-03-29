from string import ascii_uppercase
import numpy as np
from sympy import mod_inverse
import re
import random


LETTERS = {letter: index for index, letter in enumerate(ascii_uppercase, start=0)}
def stringToNumber(string):
	""" Conversione da testo(stringa) a numeri
	:param string: stringa da convertire in numero
	:return: lista contenente la conversione della stringa
	"""
	text = adjustText(string)
	numbers = [LETTERS[character] for character in text if character in LETTERS]
	return numbers


def numberToString(list):
	""" Conversione da numeri a testo(stringa)
	:param list: lista di numeri da convertire in lettere
	:return string: stringa ottenuta dalla conversione della list
	"""
	string = ''
	for i in range(len(list)):
		for letter, number in LETTERS.items():
			if number == list[i]:
				string = string + letter
	return string


def adjustText(text):
	text = text.upper()  # conversione in maiuscolo
	text = re.sub(r"['\",.;:_@#()”“’—?!&$\n]+\ *", " ", text)  # conversione dei caratteri speciali in uno spazio
	text = text.replace("-", " ")  # conversione del carattere - in uno spazio
	text = text.replace(" ", "")  # rimozione spazi
	return text


def get_M_blocks(text,m):
	"""Prende un lista che è stata generata dalla conversione in numeri di una stringa e ritorna la lista spezzettata in sottoliste di dimensione m
	:param text: lista che è stata generata dalla conversione in numeri di una stringa
	:param m: valore con cui spezzare la lista
	:return textBlocks: lista spezzettata in sottoliste di dimensione m
	"""
	textBlocks = [text[i:i + m] for i in range(0, len(text), m)]  # divido il plaintext in blocchi di m lettere
	while len(textBlocks[len(textBlocks) - 1]) != m:  # inserisco lettere A nell'ultimo blocco se la dimensione non è corretta
		textBlocks[len(textBlocks) - 1].append(0)
	return textBlocks


# Generazione della chiave
def mcd(a, b):
	"""Restituisce il Massimo Comune Divisore tra a e b
  	:param a: primo numero
  	:param b: secondo numero
  	"""
	while b:
		a, b = b, a % b
	return a


def getKey(blockDim):
	""" Creazione della chiave
	:param blockDim: dimensione m della matrice mxm
	:return: una matrice mxm invertibile
	"""
	det = 0
	while det <= 0 or (mcd(det, len(LETTERS)) != 1):
		key = np.random.randint(26, size=(blockDim, blockDim))
		det = np.linalg.det(key)
	return key


def encryption(plaintext, chiave):
	""" Cripta un testo in chiaro
	:param plaintext: stringa di plaintext
	:param chiave: matrice di dimensione m usata per criptare
	:param m: dimensione del blocco
	:return: stringa contenente il ciphertext
	"""
	m = chiave.shape[0]
	plaintext = stringToNumber(plaintext)  # ritorna una lista contenente la conversione da lettere a numeri
	plainBlocks = get_M_blocks(plaintext,m)

	P = (np.array(plainBlocks)).transpose()
	K = chiave
	C = K.dot(P) % 26
	ciphertext = list(C.flatten('F'))

	return(numberToString(ciphertext))


def minor(arr, i, j):
	"""Sottomatrice di matrix, ottenuta rimuovendo la riga i e la colonna j"""
	return arr[np.array(list(range(i)) + list(range(i + 1, arr.shape[0])))[:, np.newaxis], np.array(
		list(range(j)) + list(range(j + 1, arr.shape[1])))]


def invMatModN(matrix, n):
	invDet = mod_inverse(round(np.linalg.det(matrix)), 26)
	result = np.zeros(shape=(np.size(matrix, 0), np.size(matrix, 1)), dtype=int)

	for i in range(np.size(matrix, 0)):
		for j in range(np.size(matrix, 1)):
			result[i][j] = ((-1) ** ((i + 1) + (j + 1)) * round(np.linalg.det(minor(matrix, j, i))) * invDet) % n

	return np.array(result)


def decryptions(ciphertext, chiave):
	""" Decripta un testo cifrato
	:param ciphertext: stringa di ciphertext
	:param chiave: matrice di dimensione m usata per criptare
	:param m: dimensione del blocco
	:return: stringa contenente il plaintext
	"""
	m = chiave.shape[0]
	ciphertext = stringToNumber(ciphertext)  # ritorna una lista contenente la conversione da lettere a numeri
	cipherBlocks = get_M_blocks(ciphertext, m)
	C = np.array(cipherBlocks).transpose()
	K = invMatModN(chiave, 26)
	P = K.dot(C) % 26
	plaintext = list(P.flatten('F'))

	return(numberToString(plaintext))

# Attacco Known-Plaintext

def getPStarAndCStar(PTblocks, CTblocks, n):
	""" Genera due matrici P* e C* (in relazione a P*), di dimensione nxn in modo tale che P* sia invertibile modulo 26
	"""
	Pstar = np.zeros(shape=(n, n), dtype=int)
	Cstar = np.zeros(shape=(n, n), dtype=int)
	index = 0
	det = 0

	"""
	Si generano matrici fino a quando si ottiene una matrice P* nxn invertibile.
	P* è invertibile se il suo determinante è positivo e se esso è coprimo con 26
	"""
	while det <= 0 or (mcd(det, len(LETTERS)) != 1):
		"""
		Genera n numeri random su cui prendere i blocchi
		l'ultimo blocco è volutamente escluso, dato che protrebbe contenere caratteri di padding
		"""
		chosenBlocks = random.sample(range(np.size(PTblocks, 0)), n)
		chosenBlocks.sort()
		for i in chosenBlocks:
			Pstar[index] = PTblocks[i]
			Cstar[index] = CTblocks[i]
			index += 1
		Pstar = Pstar.transpose()
		Cstar = Cstar.transpose()
		det = round(np.linalg.det(Pstar)) # calcolo del determinante
		index = 0
	return (Pstar, Cstar)

def attack(plaintext, ciphertext, m):
	plaintext = stringToNumber(plaintext)  # ritorna una lista contenente la conversione da lettere a numeri
	plainBlocks = get_M_blocks(plaintext, m)
	P = (np.array(plainBlocks))

	ciphertext = stringToNumber(ciphertext)  # ritorna una lista contenente la conversione da lettere a numeri
	cipherBlocks = get_M_blocks(ciphertext, m)
	C = (np.array(cipherBlocks))


	Pstar, Cstar = getPStarAndCStar(P, C , m)
	"""
	La chiave K è data da: K = C* x P*^-1
	Si calcola prima l'inverso modulo 26 della matrice P* e successivamente si calcola il prodotto
	"""
	inversePStar = invMatModN(Pstar, 26)
	key = Cstar.dot(inversePStar)%26
	#key = dotModN(Cstar, inversePStar, 26)

	return key


def main():

	# LEGGO IL PLAINTEXT
	plaintext = open("./Moby_dick_chapter_one.txt")
	plaintext = plaintext.read()
	plaintext = adjustText(plaintext)
	print("Plaintext\n-----\n" + plaintext + "\n-----\n")

	# CRIPTO IL PLAINTEXT
	K = getKey(4)
	print("Key\n-----\n" + str(K) + "\n-----\n")
	ciphertext = encryption(plaintext, K)
	print("Ciphertext\n-----\n" + ciphertext + "\n-----\n")

	# DECRIPTO IL CIPHERTEXT
	plaintext_return = decryptions(ciphertext, K)
	print("Plaintext_returned\n-----\n" + plaintext_return + "\n-----\n")

	# ATTACCO ALLA CHIAVE
	newKey = attack(plaintext, ciphertext, 4)

	if (np.array_equal(K, newKey)):
		print("Key Found\n-----")
		print("Key\n-----\n" + str(newKey) + "\n-----\n")


if __name__ == '__main__':
	main()
