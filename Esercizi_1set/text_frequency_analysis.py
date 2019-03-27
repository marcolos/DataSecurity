import matplotlib.pyplot as plt
import re
import math


def adjustText(text):
	text = text.upper()  # conversione in maiuscolo
	text = re.sub(r"['\",.;:_@#()”“’—?!&$\n]+\ *", " ", text)  # conversione dei caratteri speciali in uno spazio
	text = text.replace("-", " ")  # conversione del carattere - in uno spazio
	text = text.replace(" ", "")  # rimozione spazi
	return text


def get_Mgrams(text, m):
	txt = adjustText(text)
	m_grams = []
	for i in range(0, len(txt)):
		m_grams.append(txt[i * m:(i * m) + m])

	return m_grams

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
	if p=='plot':
		plot(freqdict)

	return freqdict

def plot(dict):
	# PLOT il contenuto di un dizionario
	x = list(dict.keys())
	y = list(dict.values())
	centers = range(len(x))
	plt.bar(centers, y, align='center', tick_label=x)
	plt.show()


def m_gramms_distibutions(text, m, p=None):
	""" Calcola la distribuzione delle lettere o serie di lettere in una stringa
	:param text: stringa di testo
	:param m: parametro per divisione stringa in m_grams
	:param p: se p = 'plot' stampo il diagramma
	:return: un dizionario con le keys = m_grams , values = distribuzione di quella m_grams
	"""
	freqdict = frequency_analysis(text, m)
	tot_m_grams = sum(freqdict.values())
	
	distdict={}
	for k in freqdict.keys():  # scorro tutte le chiavi del dizionario
		distdict[k] = freqdict[k]/tot_m_grams # freqdict[k] mi ritorna il valore della chiave k

	if p=='plot':
		plot(distdict)
	return distdict


def indexOfCoincidence(text,m):
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
		for value in frequency.values():
			index_of_confidence = index_of_confidence + (  (value * (value - 1)) / (n * (n - 1)))
		print("{}° riga: ".format(i+1),index_of_confidence)

def entropy(text, m):
	""" Calcolo dell'entropia
	:param text: testo su cui calcolare l'entropia
	:param k: dimensione dei blocchi in cui il testo va suddiviso
	:return entropy: entropia
	"""
	frequencies = frequency_analysis(text, m)  # nelle key ho gli m_grams
	entropy = 0.0
	n = math.ceil(len(text)/m)

	for value in frequencies.values():
		entropy += (value/n) * math.log((value/n),2)

	entropy = -(entropy)
	return entropy

def main():

	textFile = open("./Moby_Dick_chapter_one.txt", "r")
	text = textFile.read()
	text = adjustText(text)

	for i in range(1,5):
		frequency_analysis(text, i, p='plot')
		m_gramms_distibutions(text, i, p ='plot')
		indexOfCoincidence(text,i)
		print("Entropy = ",entropy(text,i),"\n")



if __name__ == '__main__':
	main()