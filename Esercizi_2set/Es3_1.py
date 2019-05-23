import random
import math
import timeit
import re
import sys
sys.setrecursionlimit(1500)
from string import ascii_lowercase

alphabet = [letter for letter in ascii_lowercase]
alphabet.insert(0, ' ')

DEFAULT_P_ERROR = 0.01

# 1) Algoritmo di euclide esteso con funzione per calcolare l'inverso modulare
def egcd(a, b):
	"""
		Calcolo dei coefficienti x e y dell'identità di Bezout e del MCD
		:param a:
		:param b:
		:return: (d, x, y) tali che MCD(a, b) = d = ax + by
		"""
	x0, x1, y0, y1 = 0, 1, 1, 0
	while a != 0:
		q, b, a = b // a, a, b % a
		y0, y1 = y1, y0 - q * y1
		x0, x1 = x1, x0 - q * x1
	return b, x0, y0

def mulinv(a, b):
	g, x, _ = egcd(a, b)
	if g == 1:
		return x % b

#print('Inverso moltiplicativo: 17^-1 mod60 = ',mulinv(17,60))


#2) Algoritmo di esponenziazione modulare veloce
def expMod(a,n,m):
	d=1
	n=bin(n).lstrip('0b')
	for i in n:
		d=(d*d)%m
		if i=='1':
			d=(d*a)%m
	return d

#print('\nAlgoritmo di esponenziazione veloce: 3^11 mod10 =',expMod(3,11,10))


#3) Test di Miller-Rabin
def numberDecomposition(n):
	"""
		Decomposizione di un numero in forma 2^r * m
		:param n:
		:return: [r, m] tali che n = 2^r * m
		"""
	exp=[0,0]
	while(n%2==0):
		exp[0]=exp[0]+1
		n=n//2
	exp[1]=n
	return exp

def rabin(n):
	"""
		Esegue il test di Miller-Rabin. Se esso restituisce True, il numero è sicuramente composto, altrimenti potrebbe essere primo
		:param number:
		:return: True, se il numero è composto; False se il numero è probabilmente positivo
		"""
	if(n==1):
		return False
	x=random.randint(1,n-1)
	if(egcd(n,x)[0]>1):
		return True
	esp=numberDecomposition(n-1)
	for i in range(esp[0]+1):
		if(i==0):
			x=expMod(x,esp[1],n)
			if(x==1 or (x-n)==-1 ):
				return False
		else:
			x=expMod(x,2,n)
			if(x==1):
				return True
			if(i<esp[0] and (x-n)==-1):
				return False
	return True

def MR(n,perr):
	"""
		Si esegue il test di rabin k volte in modo da soddisfare la probabilità di errore perr immessa
		:param n:
		:param perr:
		:return:
	"""
	k=int(math.ceil(-math.log(perr)/math.log(4))) # numero di volte che deve essere eseguito l'algoritmo rabin
	for i in range(k):
		if(rabin(n)):
			return True
	return False

#4) Algoritmo per la generazione di numeri primi
def genPrim(k,perr=DEFAULT_P_ERROR):
	"""
		Generazione numero primo di k bit
		:param k:
		:return r: numero primo
	"""
	if (k<1):
		return 1
	while(True):
		# un numero di k bit è compreso tra 2^(k-1) e 2^k - 1
		r=random.randrange(2**(k-1),(2**k)-1)
		if((r%2)==0):
			r=r+1
		if(MR(r,perr)==False):
			return r

#n_primo = genPrim(50)
#print('\nGenerazione numero primo di ordine 2^50:', n_primo,bin(n_primo).strip('0b'))


# 5) Schema RSA, con e senza ottimizzazione CRT
def RSA(k, crt):
	"""

	:param k: numero di bit per la generazione di p e q
	:param crt: se TRUE utilizza il CRT altrimenti no
	:return: se crt = TRUE kpub, kpriv, (valori per CRT) altrimenti solo kpub e kpriv
	"""
	p = genPrim(k)  # genero p
	q = genPrim(k)  # genero q
	if (p == q):
		RSA(k, crt)
	n = p * q  # calcolo n
	phi = (p - 1) * (q - 1)  # calcolo la funzione di eulero
	while True:
		d = random.randrange(2, phi // 2) # prendo un d a caso
		g, _, _ = egcd(d, phi) # d deve essere relativamente primo con phi
		if g == 1:  # se g = 1 sono relativamente primi
			e = mulinv(d, phi)  # calcolo e come l'inverso moltiplicativo di d mod phi
			kpub = [e, n]
			kpriv = [d, n]
			if crt:  # se crt è True
				_, x, y = egcd(p, q)
				return kpub, kpriv, (p, q, x % q, y % p)
			return kpub, kpriv


# 6) test della funzione di decryption su 100 ciphertext scelti casualmente e confronto delle prestazioni, in termini di tempo di esecuzione, delle versione senza e con CRT
def EncRSA(M,kpub):
	C = []
	for m in M:
		C.append(expMod(m, kpub[0], kpub[1]))  # keys[0]=e , keys[1]=n  => calcolo il ciphertext per ogni plaintext e lo aggiungo nella lista

	return C


def DecRSA(C, key):
	"""
	Decripta i ciphertexts
	:param C: lista contente 100 ciphertexts
	:param key: chiave privata kpriv  key[0]=d , key[1]=n
	:return: lista contente 100 plaintexts
	"""
	M = []
	for c in C:
		M.append(expMod(c, key[0], key[1]))
	return M


def DecRSAcrt(C, kpriv, cq, cp, p, q):
	M = []
	for c in C:
		mp = expMod(c, kpriv[0], p)
		mq = expMod(c, kpriv[0], q)
		M.append((mp * cp + mq * cq) % kpriv[1])
	return M


# Encoding e Decoding di Messaggi
def encoding(string):
	"""
		:param string: stringa da codificare
		:return: Stringa contenente 2 cifre per ogni lettera (con eventuale padding) immessa in input
			es: input='marcoo' ; output='231128132525'
		"""
	encoded = ""

	for char in string:
		encoded += str(alphabet.index(char) + 10)

	return encoded


def decoding(string):
	decoded = ""

	for i in range(0, len(string), 2):
		decoded += alphabet[int(string[i:i + 2])-10]

	return decoded

# Preproccessing del testo
def textPreprocessing(text):
	""" Rimozione dei caratteri speciali e conversione in minuscolo
		:param text: testo da preprocesssare
		"""

	text = text.lower()  # conversione in minuscolo
	text = re.sub(r"['\",.;:_@#()”“’—?!&$\n]+\ *", " ", text)  # conversione dei caratteri speciali in uno spazio
	text = text.replace("-", "")  # conversione del carattere - in uno spazio
	text = ' '.join(text.split())
	return text

def getRandomPlaintext(length=20):
	return ''.join(random.choice(alphabet) for i in range(length))


def testRSA(k):
	keys = RSA(k, True)  # keys[0] = kpub=[e,n]  ,  keys[1] = kpriv=[d,n]  ,  se True c'è anche keys[2] per CRT
	M = [] # lista di 100 plaintext
	C = []  # lista di 100 ciphertext
	for i in range(100):
		m = random.randrange(1, keys[0][1])  # keys[0][1] = n
		M.append(m)  # riempio la lista di plaintext
	C = EncRSA(M,keys[0]) # cifro i plaintext


	# Decriptazione senza CRT
	start_time = timeit.default_timer()
	DecRSA(C, keys[1])  # keys[1] = kpriv = [d,n]
	print(timeit.default_timer() - start_time)

	# Decriptazione con CRT
	start_time = timeit.default_timer()
	DecRSAcrt(C, keys[1], (keys[2][0] * keys[2][2]), (keys[2][1] * keys[2][3]), keys[2][0], keys[2][1])
	# DecRSAcrt(C, kpriv, (p* p^-1modq), (q * q^-1modp), p, q)
	print(timeit.default_timer() - start_time)

def testRSA2(k):
	keys = RSA(k, False)
	M = ['marco','mario', 'gianni']
	P = []
	M_returned = []
	for m in M:
		P.append(int(encoding(m)))
	C = EncRSA(P,keys[0])
	P_returned = DecRSA(C,keys[1])
	for p in P_returned:
		M_returned.append(decoding(str(p)))

	print('serie di messaggi:',M)
	print('plaintext:',P)
	print('ciphertext:',C)
	print('plaintext returned:',P_returned)
	print('serie di messaggi returned:',M_returned)

if __name__ == '__main__':
	testRSA(1024)
	#testRSA2(20)