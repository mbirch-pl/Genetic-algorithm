import pandas as np
import numpy as np
import random
import copy
import matplotlib.pyplot as plt
import seaborn as sns

def wypisz(populacja):
    for i in populacja:
        print(i)


def macierz_wag(N):
    macierz = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            if i == j:
                pass
            else:
                macierz[i][j] = np.random.randint(1, 10)

    ax = sns.heatmap(macierz)
    plt.show()

    return macierz


def nowy_osobnik(macierz, start, koniec):
    N = len(macierz)
    droga = [start]  # index wierzchołka startowego
    warunek = True

    i = 1
    while warunek == True:

        mozliwe_wartosci = []  # tworzy listę możliwych wartosć na podstawie tych których nie zostały jeszcze wykorzystane
        for i in range(len(macierz)):
            if i in droga:
                pass
            else:
                mozliwe_wartosci.append(i)

        if len(mozliwe_wartosci) == 0:
            droga.append(start)
            warunek = False

        else:
            proponowana_wartosc = random.randint(0,
                                                 len(mozliwe_wartosci) - 1)  # losuje wierzcholek, który zostanie dodany
            droga.append(mozliwe_wartosci[proponowana_wartosc])  # dołacza wylosowany wierzcholek do drogi
            i += 1

    return droga

def populacja_startowa(rozmiar,macierz,start,koniec): #tworzę populacje startową o danej wielkości

    populacja = []
    for i in range(0,rozmiar):
        populacja.append(nowy_osobnik(macierz,start,koniec))
    return populacja


def zmierz_dlugosc(droga, macierz):
    wynik = 0

    for i in range(1, len(droga)):
        if macierz[droga[i - 1]][droga[i]] == 0:
            print("zła droga")
            print(droga)
            print(macierz)
        wynik = wynik + macierz[droga[i - 1]][droga[i]]
    return wynik


def krzyzowanie(droga_a, droga_b):
    start = droga_a[0]
    koniec = start
    lista_sasiadow = []

    for i in range(len(droga_a) - 1):
        mozliwe_elementy_a = copy.deepcopy(droga_a[i:len(droga_a) - 1])
        mozliwe_elementy_b = []

        for j in range(len(droga_b) - 1):
            if droga_a[i] == droga_b[j]:
                mozliwe_elementy_b = copy.deepcopy(droga_b[j:len(droga_b) - 1])

        mozliwe_elementy = []
        powtarzalne_elementy = []
        x = 0

        while len(mozliwe_elementy_b) > 0:

            if mozliwe_elementy_b[x] in mozliwe_elementy_a:
                powtarzalne_elementy.append(mozliwe_elementy_b[x])
                mozliwe_elementy_a.remove(mozliwe_elementy_b[x])
                mozliwe_elementy_b.remove(mozliwe_elementy_b[x])

            else:
                mozliwe_elementy.append(mozliwe_elementy_b[x])
                mozliwe_elementy_b.pop(x)

        mozliwe_elementy = mozliwe_elementy + mozliwe_elementy_a
        mozliwe_elementy = sorted(mozliwe_elementy)
        powtarzalne_elementy = sorted(powtarzalne_elementy)
        lista_sasiadow.append([droga_a[i], mozliwe_elementy, powtarzalne_elementy])

    lista_sasiadow = sorted(lista_sasiadow, key=lambda sasiad: sasiad[0])

    nowa_droga = [start]
    lista_sasiadow[start][2].remove(0)

    warunek = True
    while warunek == True:

        kolejny_wierzcholek = None

        if len(nowa_droga) == len(droga_a) - 1:

            nowa_droga.append(0)
            warunek = False
            break


        elif len(nowa_droga) <= 1:

            proponowana_wartosc = random.randint(0, len(lista_sasiadow[nowa_droga[-1]][2]) - 1)
            kolejny_wierzcholek = lista_sasiadow[nowa_droga[-1]][2][proponowana_wartosc]

        else:

            if len(lista_sasiadow[nowa_droga[-1]][2]) > 0:
                proponowana_wartosc = random.randint(0, len(lista_sasiadow[nowa_droga[-1]][2]) - 1)

                kolejny_wierzcholek = lista_sasiadow[nowa_droga[-1]][2][proponowana_wartosc]

            elif len(lista_sasiadow[nowa_droga[-1]][1]) > 0:

                liczba_sasiadow = 10000000
                index = None

                for b in range(len(lista_sasiadow[nowa_droga[-1]][1])):
                    liczba = len(lista_sasiadow[lista_sasiadow[nowa_droga[-1]][1][b]][1]) + len(
                        lista_sasiadow[lista_sasiadow[nowa_droga[-1]][1][b]][2])
                    if liczba < liczba_sasiadow:
                        index = b
                        liczba_sasiadow = liczba
                kolejny_wierzcholek = lista_sasiadow[nowa_droga[-1]][1][index]

            else:
                mozliwosci = []  # tworzy listę możliwych wartosć na podstawie tych których nie zostały jeszcze wykorzystane
                for i in range(len(lista_sasiadow)):
                    if i in nowa_droga:
                        pass
                    else:
                        mozliwosci.append(i)

                proponowana_wartosc = random.randint(0,
                                                     len(mozliwosci) - 1)  # losuje wierzcholek, który zostanie dodany
                kolejny_wierzcholek = (mozliwosci[proponowana_wartosc])  # dołacza wylosowany wierzcholek do drogi

        for a in range(len(lista_sasiadow)):
            if kolejny_wierzcholek in lista_sasiadow[a][2]:
                lista_sasiadow[a][2].remove(kolejny_wierzcholek)
            elif kolejny_wierzcholek in lista_sasiadow[a][1]:
                lista_sasiadow[a][1].remove(kolejny_wierzcholek)

        nowa_droga.append(kolejny_wierzcholek)

    return nowa_droga


def mutacja(droga, prawodpodobienstwo, macierz):
    koniec = droga[-1]
    start = droga[0]
    nowa_droga = copy.deepcopy(droga)

    for i in range(1, len(nowa_droga)):
        if random.random() < prawodpodobienstwo:

            warunek = True
            while warunek == True:

                mozliwe_wartosci = []  # tworzy listę możliwych wartosć na podstawie tych których nie zostały jeszcze wykorzystane
                for i in range(len(macierz)):
                    if i in droga:
                        pass
                    else:
                        mozliwe_wartosci.append(i)

                if len(mozliwe_wartosci) == 0:
                    droga.append(start)
                    warunek = False

                else:
                    proponowana_wartosc = random.randint(0, len(
                        mozliwe_wartosci) - 1)  # losuje wierzcholek, który zostanie dodany
                    droga.append(mozliwe_wartosci[proponowana_wartosc])  # dołacza wylosowany wierzcholek do drogi
                    i += 1

    return (nowa_droga)


def wynik_populacji(populacja, macierz):
    wyniki = []
    for i in range(0, len(populacja)):
        wyniki += [zmierz_dlugosc(populacja[i], macierz)]

    return (wyniki)


def znajdz_kolege(wyniki):  # metoda ruletki

    tablica = np.array(wyniki)
    temp = tablica.argsort()  # posortowane od najmniejszego do największego indexy wynikow
    rank = np.empty_like(temp)
    rank[temp] = np.arange(len(tablica))

    dopasowanie = [len(rank) - x for x in rank]

    c_wyniki = copy.deepcopy(dopasowanie)

    for i in range(1, len(c_wyniki)):
        c_wyniki[i] = dopasowanie[i] + c_wyniki[i - 1]

    prawd = [x / c_wyniki[-1] for x in c_wyniki]

    rand = random.random()

    for i in range(0, len(prawd)):
        if rand < prawd[i]:
            return i


def alg():
    start = 0
    koniec = start
    rozmiar_macierzy_wag = 30
    rozmiar_populacji = 30
    liczba_iteracji = 1000
    liczba_par = 9
    liczba_najlepszych_rozwiazan = 2
    prawdopodobienstwo_mutacji = 0.05
    liczba_grup = 1

    macierz = macierz_wag(rozmiar_macierzy_wag)
    populacja = populacja_startowa(rozmiar_populacji, macierz, start, koniec)
    ostatnia_odl = 10000000
    najlepsze_wyniki = []

    for i in range(liczba_iteracji):
        nowa_populacja = []

        # drogi bieżącej populacji
        wyniki = wynik_populacji(populacja, macierz)
        najlepszy = populacja[np.argmin(wyniki)]  # najkrotsza droga
        liczba_ruchow = len(najlepszy)
        odleglosc = zmierz_dlugosc(najlepszy, macierz)

        if odleglosc != ostatnia_odl:
            print('Iteracja %i: droga wynosi %f' % (i, odleglosc))

        # rozmnażanie się członków na podstawanie wyników podobieństwa/metoda ruletki
        for j in range(liczba_par):
            nowy_1 = krzyzowanie(list(populacja[znajdz_kolege(wyniki)]), list(populacja[znajdz_kolege(wyniki)]))
            nowa_populacja = nowa_populacja + [nowy_1]

        # mutacja
        for j in range(len(nowa_populacja)):
            nowa_populacja[j] = np.copy(mutacja(nowa_populacja[j], prawdopodobienstwo_mutacji, macierz))

        # zatrzymanie członków starej populacjiw w nowej
        nowa_populacja += [populacja[np.argmin(wyniki)]]
        for j in range(1, liczba_najlepszych_rozwiazan):
            przechowawca = znajdz_kolege(wyniki)
            nowa_populacja += [populacja[przechowawca]]

        # uzupełnienianie populacji randmowymi członkami
        while len(nowa_populacja) < rozmiar_populacji:
            nowa_populacja += [nowy_osobnik(macierz, start, koniec)]

        populacja = copy.deepcopy(nowa_populacja)
        ostatnia_odl = odleglosc
        najlepsze_wyniki.append([i, odleglosc])

alg()

