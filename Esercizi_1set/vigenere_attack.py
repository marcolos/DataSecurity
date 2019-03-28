import math
from string import ascii_lowercase
import numpy as np
import re

alphabet = [letter for letter in ascii_lowercase]


# TEST KASISKI
def mcd(a, b):
	"""Restituisce il Massimo Comune Divisore tra a e b"""
	if a * b == 0: return 1
	if a == b:
		return a
	elif a > b:
		return mcd(a - b, b)
	else:
		return mcd(b - a, a)


def mcdForList(lst):
	mcdOld = 0
	mcd1 = 0
	for i in range(len(lst) - 1):
		mcd1 = mcd(lst[i], lst[i + 1])
		if mcd1 == 1: return 1
		if (mcdOld == 0): mcdOld = mcd1
		if (mcdOld > 0):
			if (mcd1 < mcdOld): mcdOld = mcd1
	return mcdOld


def generateTriple(txt):
	for i in range(len(txt) - 2):
		if i < len(txt) - 2:
			yield txt[i:i + 3]


def Kasiski(txt):
	triple = generateTriple(txt)
	dic = {}
	"""Analizzo tutte le triple e le conto"""
	for i in range(len(txt) - 2):
		tri = next(triple)
		if (tri in dic):
			vaule = dic.get(tri)
			vaule = vaule + 1
			dic[tri] = vaule
		else:
			dic.setdefault(tri, 1)
	"""Cerco la frequenza massima tra le triple"""
	maxN = 0
	maxLbl = ""
	for i in dic:
		if (dic.get(i) > maxN):
			maxN = dic.get(i)
			maxLbl = i
	"""calcolo le distanze tra la prima occorenza e le altre triple"""
	texd = generateTriple(txt)
	dist = []
	first = 0
	for i in range(len(txt) - 2):
		if (maxLbl == next(texd)):
			if first > 0:
				dist.append(i - vaule)
			if first == 0:
				vaule = i
				first = 1
	"""restituisco il MCD delle distanze"""
	return mcdForList(dist)
# FINE TEST KASISKI


def stringToNumpyArray(string):
	""" Converte una stringa in un array numpy contenente i numeri relativi alle varie lettere
	:param string: stringa da convertire
	"""
	letters = [alphabet.index(letter) for letter in string]  # conversione da lettere a numeri
	letters = np.array(letters)
	return letters


def numpyArrayToString(array):
	""" Converte un array numpy in una stringa di testo
	:param array: array da convertire
	"""
	letters = array.tolist()
	letters = [alphabet[i] for i in letters]  # conversione da numeri a lettere
	text = "".join(letters)  # creazione stringa unica
	return text


def getSubstrings(text, m):
	""" Divide il testo in sottostringhe, ognuna di dimensione ceil(len(text)/m))
	Il testo viene diviso scrivendo "per colonne"
	:param text: testo da suddividere
	:param m: numero di righe in cui suddividere il testo
	:return: lista di sottostringhe scritte per colonna
	"""

	substrings = []
	for i in range(0,m):
		txt = ''
		for j in range(i,len(text),m):
			txt = txt + text[j]
		substrings.append(txt)

	return substrings



def shiftEncryption(string, k):
	""" Shift Encryption di :param string di :param k.
	:return: Stringa dove ogni lettera subisce uno shift di k posizioni
	"""
	stringArray = stringToNumpyArray(string)
	shiftedStringArray = [None] * len(stringArray)

	for i in range(len(stringArray)):
		shiftedStringArray[i] = (stringArray[i] - k) % 26

	shiftedString = numpyArrayToString(np.array(shiftedStringArray))
	return shiftedString


def findKeyElement(substring):
	"""
	Prende in input la stringa :param substring, su cui si suppone che sia risultato di uno shift encryption di paramentro k
	Si cerca quel valore k che massimizza il prodotto scalare tra il vettore frequenze della stringa risultato di uno shift encryption k e il vettore delle frequenze delle lettere della lingua inglese
	:return: i-esima lettera della chiave di encryption
	"""
	# frequenze delle lettere nella lingua inglese
	en_lett_freqs = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702,
					 0.02228, 0.02015, 0.06094, 0.06966, 0.00153,
					 0.00772, 0.04025, 0.02406, 0.06749, 0.07507,
					 0.01929, 0.00095, 0.05987, 0.06327, 0.09056,
					 0.02758, 0.00978, 0.02360, 0.00150, 0.01974, 0.00074]

	maxDotProd = 0
	maxKey = None

	for letter in alphabet:
		letterValue = alphabet.index(letter)
		shiftedSubString = shiftEncryption(substring,letterValue)  # shift encryption basato sull' i-esima lettera dell'alfabeto
		dotProd = np.dot(computeLetterFrequencies(shiftedSubString), en_lett_freqs)  # calcolo del prodotto scalare
		if dotProd > maxDotProd:
			maxDotProd = dotProd
			maxKey = letter

	return maxKey


def findKey(subStrings):
	""" Date delle :param subStrings, su cui si suppone che ogni strnga sia frutto di uno shift encryption,
	:return: la chiave contenente le componenti utilizzate per cifrare il messaggiRs
	"""
	key = ""

	for i in range(len(subStrings)):
		key = key + str(findKeyElement(subStrings[i]))

	return key


def decripther(ciphertext, keys):
	j = 0
	planetext = ""
	for i in ciphertext:
		if (j == len(keys)): j = 0
		k = ord(i)
		k = k - keys[j]
		if (k < 97): k = 123 - (97 - k)
		planetext = planetext + chr(k)
		j = j + 1
	return planetext


def adjustText(text):
	text = text.lower()  # conversione in minuscolo
	text = re.sub(r"['\",.;:_@#()”“’—?!&$\n]+\ *", " ", text)  # conversione dei caratteri speciali in uno spazio
	text = text.replace("-", " ")  # conversione del carattere - in uno spazio
	text = text.replace(" ", "")  # rimozione spazi
	return text


def computeLetterFrequencies(string):
	""" Calcola la frequenza delle varie lettere in una stringa. L'algoritmo è piuttosto primitivo
	:param string:
	:return: lista delle frequenze delle varie lettere
	"""
	frequencies = []

	for letter in alphabet:
		count = 0
		for i in string:
			if i == letter:
				count += 1
		frequencies.append(count)

	return frequencies


def frequency_analysis(text, m, p = None):
	""" Calcola la frequenza(occorrenze) delle lettere o serie di lettere in una stringa
	:param text: stringa di testo
	:param m: parametro per divisione stringa in m_grams
	:param p: se p = 'plot' stampo il diagramma
	:return: un dizionario con le keys = m_grams , values = frequenza di quella m_grams
	"""
	txt = adjustText(text)
	# le keys sono le lettere, i value sono le frequenze
	freqdict={}
	for i in range(0,len(txt)):
		t = txt[i*m:(i*m)+m]
		if len(t) == m:
			if t in freqdict:
				freqdict[t] = freqdict[t] + 1
			else:
				freqdict[t] = 1

	return freqdict


#INDICE DI INCIDENZA UTILE PER VIGENERE
def indexOfCoincidenceVigenere(text,m):
	""" Calcola l'indice di concidenza di una stringa. Se passo un valore di m>1 allora si stampano m indici di concidenza
	:param text: stringa di testo
	:param m: valore con il quale si prendo i valori della stringa(ad esempio se m = 2 prendo s[0],s[2],s[4],...  e  s[1],s[3],s[5],... dove s è la stinga)
	:return: niente, stampo e basta
	"""
	text = adjustText(text)

	for i in range(0,m):
		txt = ''
		for j in range(i,len(text),m):
			txt = txt + text[j]

		frequency = frequency_analysis(txt, 1)  # nelle key ho gli m_grams(per l'indice di incidenza gli m_grams sono le singole lettere)
		n = len(txt)
		index_of_confidence = 0
		ic=[]
		for value in frequency.values():
			index_of_confidence = index_of_confidence + (  (value * (value - 1)) / (n * (n - 1)))
			ic.append(index_of_confidence)
		#print("{}° riga: ".format(i+1),index_of_confidence)
		return ic



def main():
	ciphertext = "kbrvdlikdihpbxhzenugntvnrfydttvvuihviwikvltgvmgfdgrtkbecfhgjmzvvrnpqthvujwegmgeyfofgebjvtlvvqveccsrzifmevxnuggxyvnvewmxvijrnbmsnvfnplbrrgyagbkekzhtupkmccpbkkxhvtfntmwmklhskbmsftwhrgttcrwrkvaiisugjzhsdkbrukkivenugvwmjgfnamwlvivnvpksfduafxbgbvxhrokewwcgkwglvivnvpksfdqnntmsfkbruifiwrgvnqtvjtlnytmlzjnvomkirucaitxeefprtbaisfqycvwxyvhgcsxeuzprcteswpihczxhvrxvcutpzmy"

	key_len = Kasiski(ciphertext)
	print("Test Kasiski\n-----\n" + str(key_len) + "\n-----\n")

	substrings = getSubstrings(ciphertext, key_len)

	key = findKey(substrings)
	print("Key\n-----\n" + key + "\n-----\n")


	plaintext = decripther(ciphertext,stringToNumpyArray(key))
	print("Plaintext\n-----\n" + plaintext + "\n-----\n")


if __name__ == '__main__':
	main()
