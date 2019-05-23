import re as re
import math
from string import ascii_lowercase
import random
import string

def shiftEnglishText(string,n):
	#converto stringa in lista
	list = [s for s in string]
	# converto da lettera a numero e aggiungo lo shift
	for i in range(len(list)):
		list[i] = (ascii_lowercase.index(list[i]) + n)%26
	# riconverto da numero a lettera
	for i in range(len(list)):
		list[i] = ascii_lowercase[list[i]]
	# converto da lista a stringa e ritorno
	return ''.join(list)

def randomString(stringLength):
	""" Genera una stringa casuale di lunghezza fissata
	:param stringLength: Lunghezza della stringa da generare
	:return: Stringa generata casualmente di stringLength caratteri
	"""
	letters = string.ascii_lowercase
	return ''.join(random.choice(letters) for i in range(stringLength))

def divergence(p,q):
	"""  Calcola la divergenza tra due distribuzioni
	:param p: distibuzione di probabilità
	:param q: distibuzione di probabilità
	:return:
	"""
	result = 0
	for i in range(len(p)):
		a = p[i]
		b = p[i]/q[i]
		c = math.log(b,2)
		result = result + (a*c)

	return result


def entropy(probabilities):
	"""  Calcola entropia della distribuzione di probabilità
	:param probabilities: lista contenente una distribuzione di probabilità
	:return: valore dell'entropia relativa alla distribuzione in input
	"""
	entropy = 0.0

	for i in range(len(probabilities)):
		entropy += probabilities[i] * math.log(probabilities[i], 2)

	entropy = -(entropy)
	return entropy


# Effettua il preprocessing del testo
def preprocessing(text):
	text = text.lower()
	text = re.sub(r"['\",.;:_@#()”“’—?!&$\n]+\ *", " ", text) # conversione dei caratteri speciali in uno spazio
	text = text.replace("-", "") # conversione del carattere - in uno spazio
	text = text.replace(" ", "") # rimozione spazi
	return text

def meanLogLikelihoodRatio(string,p,q):
	length = len(string)
	value = 0
	div_p_q = divergence(p, q)
	div_q_p = divergence(q, p)

	for i in range(length):
		j = ascii_lowercase.index(string[i])
		a = p[j]/q[j]
		value += math.log(a,2)

	value = value / length

	x = math.fabs(value - div_p_q)  #vicinanza di value con la div_p_q
	y = math.fabs(value - (- div_q_p))  #vicinanza di value con la -div_q_p

	if x <= y: # value è piu vicino a div_p_q  => si avvicina di più alla distibuzione p
		alpha = 2**(-length * div_q_p)
		return("English String", value, alpha)
	else:  # value è più vicino a -div_q_p  => si avvicina di più alla distibuzione q
		beta =  2**(-length * div_p_q)
		return("Random String", value, beta)


def meanLogLikelihoodRatioWithControlShift(string,en_lett_probs,ran_lett_probs):
	# Controllo che il testo non sia una shift encryptions
	result, value, error_prob = meanLogLikelihoodRatio(string,en_lett_probs,ran_lett_probs)
	r,v,e = result,value,error_prob
	en_lett_probs_shiftable = en_lett_probs.copy()
	if result == "Random String":
		for i in range(1,26):
			en_lett_probs_shiftable.append(en_lett_probs_shiftable[0])  # appendo in coda il 1°elemento della lista
			en_lett_probs_shiftable.remove(en_lett_probs_shiftable[0])  # cancello il 1° elemento della lista
			result, value, error_prob = meanLogLikelihoodRatio(string, en_lett_probs_shiftable, ran_lett_probs)
			if result == "English String":
				result = "English String Shifted-{}".format(-i+26)  #mi dice di quante posizioni ho shiftato. Siccome la en_lett_probs shifta a sx e l'indice i va verso destra devo aggiustare l'indice i
				return result, value, error_prob
	return r,v,e


def main():
	# Frequenza delle lettere lingua inglese
	en_lett_probs = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702,
					 0.02228, 0.02015, 0.06094, 0.06966, 0.00153,
					 0.00772, 0.04025, 0.02406, 0.06749, 0.07507,
					 0.01929, 0.00095, 0.05987, 0.06327, 0.09056,
					 0.02758, 0.00978, 0.02360, 0.00150, 0.01974,
					 0.00074]

	en_entropy = entropy(en_lett_probs)
	ran_entropy = math.log(26,2)
	ran_lett_probs = [1/26 for letter in ascii_lowercase]

	# costruisco le 50 stringhe casuali di 100 caratteri ciascuna
	index = 0
	ran_strings = []
	while index < 50:
		stringa = randomString(100)
		ran_strings.append(stringa)
		index += 1
	ran_strings[49] = ran_strings[49][0:50] #metto nell'ultima stringa 50 caratteri invece che 100

	# costruisco 50 stringhe di lingua inglese di 100 caratteri ciascuna
	f = open("en_text",'r')
	en_text = f.read()
	en_text = preprocessing(en_text)
	en_strings = []
	while len(en_strings)!=50 and en_text!="":
		en_strings.append(en_text[0:100])
		en_text = en_text[100:]

	print("Test on random text")
	ran_err_counter = 0
	for string in ran_strings:
		result, value, error_prob = meanLogLikelihoodRatioWithControlShift(string,en_lett_probs,ran_lett_probs)
		print(result,value,error_prob)
		if result != "Random String":
			ran_err_counter += 1
	print("recognition errors of random strings :",ran_err_counter)


	print("Test on english text")
	en_err_counter = 0
	en_strings[48] = en_strings[48][0:50] # metto nella 49 stringa 50 caratteri anziche 100
	en_strings[49] = shiftEnglishText(en_strings[0],2) #metto nell'ultima stringa un testo inglese che ha subito un shiftencripton
	for string in en_strings:
		result, value, error_prob = meanLogLikelihoodRatioWithControlShift(string, en_lett_probs, ran_lett_probs)
		print(result, value, error_prob)
		if result == "Random String" :
			en_err_counter += 1

	print("recognition errors of english strings",en_err_counter)
	return


if __name__ == '__main__':
	main()
