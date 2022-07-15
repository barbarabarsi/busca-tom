import numpy as np
from scipy.io import wavfile
from tom_app import download
import os
from tom_app.alg_linear import cosine
from pytube import YouTube

class Etapas (object):
    def __init__(self, freq, alt):
        self.freq = freq
        self.alt = alt

class Gap (object):
    def __init__(self, freq):
        self.centro = freq
        self.min = freq-4
        self.max = freq+4

def matriz_notas():
    vetor = []
    for i in range(0, 12):
        copia = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
        for j in range(0, i):
            primeiro = copia.pop()
            copia.insert(0, primeiro)
        vetor.append(copia)
    return vetor

def aproximar(value, array):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def faz_gaps():

    gaps = []
    n = 0
    j = 440

    while 440/1.0595**n>16:
        j = 440/1.0595**n
        gap = Gap(freq = j)
        n+=1
        gaps.append(gap)
    j = 440 
    n = 1
    while 440*1.0595**n<32000:
        j = 440*1.0595**n
        gap = Gap(freq = j)
        n+=1
        gaps.append(gap)
    gaps.sort(key=lambda x:x.centro)
    return gaps

def analisa_gaps(array,gaps):
    resultado  = []
    for freq in array:
        for gap in gaps:
            if freq.freq<gap.max and freq.freq>gap.min:
                aux = Etapas(freq=gap.centro, alt= freq.alt)
                resultado.append(aux)
                break
    return resultado

def notas_frequentes(array):

    notas = [16.319163621138436,17.290153856596177,18.31891801106365,19.408893632721938,
    20.5637228038689,21.7872643106991,23.083606537185698,24.457081126148253,
    25.912277453154072,27.45405796161674,29.08757441033294,30.818285087747757]
    resultado = [0,0,0,0,0,0,0,0,0,0,0,0]

    for elemento in array:
        div = elemento.freq
        while div/2 >16:
            div/=2
        aprox = aproximar(div, notas)
        resultado[notas.index(aprox)] += elemento.alt 
    return resultado

def faz_vetor(link):

    download.download_audio('audio',link)
    inicial = []
    sampFreq, sound = wavfile.read("./tom_app/audio.wav") 
    sound = sound / 2.0**15
    signal = sound[:,0]
    fft_spectrum = np.fft.rfft(signal)
    freq = np.fft.rfftfreq(signal.size, d=1./sampFreq)
    fft_spectrum_abs = np.abs(fft_spectrum)

    for i in range(0,len(freq)):   
        if freq[i]>130 and freq[i]<32000:
            temp = Etapas(freq = freq[i], alt= fft_spectrum_abs[i])
            inicial.append(temp)
    inicial.sort(key=lambda x:x.alt, reverse=True)
    
    gaps = faz_gaps()
    notas = analisa_gaps(inicial, gaps)
    resultado  = notas_frequentes(notas)
    os.remove("./tom_app/audio.wav")

    return resultado

def busca_tom(link):

    vetor_amp = faz_vetor(link)
    video = YouTube(link)

    matriz_escalas = matriz_notas()

    cossenos = []

    for escala in matriz_escalas:
        cossenos.append(cosine(vetor_amp,escala))
    
    index_tom = cossenos.index(max(cossenos))

    if index_tom == 0:
        tom_maior = "C"
        tom_menor = "Am"
    elif index_tom == 1:
        tom_maior = "C#"
        tom_menor = "A#m"
    elif index_tom == 2:
        tom_maior = "D"
        tom_menor = "Bm"
    elif index_tom == 3:
        tom_maior = "D#"
        tom_menor = "Cm"
    elif index_tom == 4:
        tom_maior = "E"
        tom_menor = "C#m"
    elif index_tom == 5:
        tom_maior = "F"
        tom_menor = "Dm"
    elif index_tom == 6:
        tom_maior = "F#"
        tom_menor = "D#m"
    elif index_tom == 7:
        tom_maior = "G"
        tom_menor = "Em"
    elif index_tom == 8:
        tom_maior = "G#"
        tom_menor = "Fm"
    elif index_tom == 9:
        tom_maior = "A"
        tom_menor = "F#m"
    elif index_tom == 10:
        tom_maior = "A#"
        tom_menor = "Gm"
    elif index_tom == 11:
        tom_maior = "B"
        tom_menor = "G#m"

    return tom_maior, tom_menor, vetor_amp, video.title, video.thumbnail_url, link
