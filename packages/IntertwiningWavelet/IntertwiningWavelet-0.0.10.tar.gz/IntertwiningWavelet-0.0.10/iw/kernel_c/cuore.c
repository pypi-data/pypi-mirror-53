#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include "cuore.h"

double wilson(num* nn_p, punto** pt_p) {
	long int i; 	//vertice da cui parte una passeggiata sricciolata
	long int j; 	//punto corrente della passeggiata
	long int k;		//vicino aleatorio di j
	long int n = (*nn_p).n; 	//numero totale di vertici
	long int f = 0; 	//numero di alberi freddi
	long int l, ll; 	//vertici generici

	tutti_svegli_tempo_zero(nn_p, pt_p);
	tutti_radici_da_sistemare(nn_p, pt_p);
	i = 0;	//si parte dal primo vertice
	while (i < n) {	//si deve girare l'insieme di tutti i vertici
		if ((*pt_p)[i].wilson == 2) {	//si controlla che i e` ancora da sistemare
			j = i; 	//si parte da i
			while ((*pt_p)[j].wilson == 2) { 	//finche' j e` una radice non sistemata
				k = vicino_aleatorio(j, nn_p, *pt_p);	//si sceglie un vicino
				if (k < 0) { 	//se k e` il cimetero si congela il camino
					(*pt_p)[j].rad = j;	//la radice non e` piu` sconoscuita
					(*pt_p)[j].attivo = 0;	//e` fredda
					(*pt_p)[j].prima = j;	//la lista dei siti che si sanno collegati in j e` un singleton
					(*pt_p)[j].dopo = j;
					(*pt_p)[j].wilson = 0; 	//j e` sistemata
					((*nn_p).af)[f] = j;	//si inserisce j nella lista degli alberi freddi
					((*nn_p).rg)[j] = f;	//sta al rango f;
					(*nn_p).f = ++f;	//c'e` un albero freddo in piu` nella lista degli alberi freddi
					l = i; 	//da i a j si dichiarono sistemati i siti lungo il cammino
					while(l != j) {	//in j e` appena stato fatto il lavoro
						(*pt_p)[l].wilson = 0;	//l e` sistemato
						l = (*pt_p)[l].succ;	//si passa al sito successivo lungo il cammino	
					}	//lungo il camino i siti sono stati sistemati
				}	//cosi` si chiude il caso k cimetero : j non e` stata spostata ma e` ormai sistemata
				else {	//caso in cui k non è il cimetero 
					if (k != j) {	//altrimenti non c'e` niente da fare
						if ((*pt_p)[k].wilson == 2) {	//caso di un passo fuori dagli alberi
							(*pt_p)[j].succ = k;	//si mette una freccia da j verso k
							(*pt_p)[j].wilson = 1;	//j non e` ancoro sistemato
						}	//rimane da spostare j in k, il che si fa dopo gli altri due casi, in k si e` ancora nello stato 2
						if ((*pt_p)[k].wilson == 1) {	//caso in cui bisogna sricciolare
							l = k;	//si tolgono le freccie in l partendo da k
							while (l != j) {	//il ricciolo si ferma in j, che gia` era una radice non sistemata
								ll = (*pt_p)[l].succ;	//ll sara` il prossimo valore di l
								(*pt_p)[l].succ = -1; 	//si fa di l una radice
								(*pt_p)[l].wilson = 2; 	//da sistemare
								l = ll; 	//si passa al vertice successivo lungo il ricciolo
							}	//fine dello sricciolamento 
						}	//abbiamo sriciolato, lo stato in k e` passato da 1 a 2 e bisogna ancora spostare j in k
						if ((*pt_p)[k].wilson == 0) {	//caso in cui si deve congelare il cammino
							(*pt_p)[j].succ = k;	//si aggiunge una freccia da j verso k 
							l = i;	//si congela partendo da i
							while (l != k) {	//il cammino si ferma in k
								(*pt_p)[l].wilson = 0;	//l e` sistemato
								l = (*pt_p)[l].succ;	//si passa al punto successivo
							} //si e` sistemato tutto il camino
						}	//il camino e` stato congelato e si e` aggiunto una freccia da j verso k
						j = k;	//la passegiata continua da k che sta nello stato 2 o 0	(ultimo caso, quello del congelamento)
					}	//fine del caso j diverso da k	
				}	//cosi` si chiude il caso `vero vicino' : j si e` spostato in k e, possibilmente, si e` sricciolato o congelato il camino
			}	//la passegiata sricciolata e` finita
		}	//non si e` fatto niente se i era sistemato, altrimenti abbiamo seguito la passeggiata sricciolata
	i++; //si passa al vertice successivo
	}	// a quel punto tutt'e` sistemato
	(*nn_p).a = 0; 	//non ci sono alberi attivi;

	return tempo_di_wilson(nn_p); 	//si rinvia il tempo di Wilson
}

int tutti_radici_da_sistemare(num* nn_p, punto** pt_p) {
	long int i;	//i e` un vertice generico

	for(i = 0; i < (*nn_p).n; i++){	//si fa d'ogni punto una radice da sistemare, dimenticando dove si radica 
		(*pt_p)[i].rad = -1;	//si dimentica dove si radica
		(*pt_p)[i].wilson = 2;	//e lo si segna come radice da sistemare
	}

	return EXIT_SUCCESS;
}

double tempo_di_wilson(num* nn_p){
	return (*nn_p).tu / ((*nn_p).q + (*nn_p).ttm);
}

int frammentazione(long int k, long int j, num* nn_p, punto** pt_p){	//sposta la radice k in j, radicata in k, e frammenta l'albero
	long int i;	//i e` un vertice
	long int ii;	//ii sara` un prossimo valore per i

	i = (*pt_p)[k].dopo;	//si percorre il ciclo dei punti che si sapevano radicati in k e gli si dice che non si sa piu` dove sono radicati
	while(i != k){		//ci si ferma a k: k era radica e rimarra` radicata in se stessa
		(*pt_p)[i].rad = -1;
		i = (*pt_p)[i].dopo;
	}
	i = j;	//si perc. il ciclo dei punti che dev. divent. rad., li si fa rad., si restr. a un singl. la cat. di chi si sa rad. in loro e si agg. le liste
	while(i != k){
		ii = (*pt_p)[i].succ;
		(*pt_p)[i].succ = -1;
		(*pt_p)[i].rad = i;
		(*pt_p)[i].prima = i;
		(*pt_p)[i].dopo = i;
		((*nn_p).aa)[(*nn_p).a] = i;
		((*nn_p).rg)[i] = (*nn_p).a;
		(*nn_p).a++;
		i = ii;
	}
	(*pt_p)[k].prima = k;	//siccome k era gia` radice l'unica cosa da fare per k e` restringere la sua catena a un singleton
	(*pt_p)[k].dopo = k;

	return EXIT_SUCCESS;
}


int coalescenza(long int k, long int j, num* nn_p, punto** pt_p){	//attacca la radice k in j, su di un albero distinto
	long int i, kk, ll;	//vertici
	long int l = radice(j, pt_p);

	(*nn_p).a--;	//si ha un albero attivo di meno
	if (((*nn_p).rg)[k] < (*nn_p).a){	//si sistema la lista degli alberi attivi e quella dei ranghi
		i = ((*nn_p).aa)[(*nn_p).a];
		((*nn_p).aa)[((*nn_p).rg)[k]] = i;
		((*nn_p).rg)[i] = ((*nn_p).rg)[k];
	}

	(*pt_p)[k].succ = j;	//da k si va ora in j
	i = k;	//si percorre il ciclo di chi era radicato in k per informare che si e` ora radicato in l, radice di j
	do{
		(*pt_p)[i].rad = l;
		i = (*pt_p)[i].dopo;
	} while(i != k);
	ll = (*pt_p)[l].prima;	//si inserice il ciclo di chi si sapeva collegato a k nel ciclo di chi si sa radicato in l
	kk = (*pt_p)[k].prima;
	(*pt_p)[ll].dopo = k;
	(*pt_p)[k].prima = ll;
	(*pt_p)[kk].dopo = l;
	(*pt_p)[l].prima = kk;
	
	return EXIT_SUCCESS;
}

	
int tutti_svegli_tempo_zero(num* nn_p, punto** pt_p){
	long int i;	//i e` un vertice generico

	(*nn_p).a = (*nn_p).n;	//perche' ogni punto sara` un albero attivo 
	(*nn_p).f = 0;	//non ci sono alberi freddi
	(*nn_p).tu = (double) 0;	//il tempo riparte a 0

	for(i = 0; i < (*nn_p).n; i++){	//si fa d'ogni punto un albero attivo
		((*nn_p).aa)[i] = i;	//ogni albero e` attivo
		((*nn_p).rg)[i] = i;	//gli diamo la sua posizione naturale nella lista degli alberi attivi
		(*pt_p)[i].succ = -1;	//ciascun punto e` radice
		(*pt_p)[i].rad = i;		//radicato in se stesso
		(*pt_p)[i].attivo = 1;	//e` anche attivo
		(*pt_p)[i].prima = i;	//e la catena di chi si sa collegato a lui e` un singleton
		(*pt_p)[i].dopo = i;
	}
	return EXIT_SUCCESS;
}


int congelare_tutto(num* nn_p, punto** pt_p){
	long int i;	//vertice generico

	(*nn_p).a = 0;	//non ci saranno piu` alberi attivi
	(*nn_p).f = (*nn_p).n;	//avremo n alberi freddi

	for(i = 0; i < (*nn_p).n; i++){	//ogni punto e` radicato in se stesso, albero freddo
		((*nn_p).af)[i] = i;
		((*nn_p).rg)[i] = i;
		(*nn_p).tu += - log(drand48());	//vedi la formula nella funzione vicino_aleatorio con q = infinito

		(*pt_p)[i].succ = -1;
		(*pt_p)[i].rad = i;
		(*pt_p)[i].attivo = 0;
		(*pt_p)[i].prima = i;
		(*pt_p)[i].dopo = i;
	}		

	return EXIT_SUCCESS;
}


int svegliare(long int k, num* nn_p, punto** pt_p){
	long int i;	//vertice generico 

	(*nn_p).f--;	//si ha un albero freddo di meno 
	if (((*nn_p).rg)[k] < (*nn_p).f){	//si sistema la lista degli alberi freddi e quella dei ranghi
		i = ((*nn_p).af)[(*nn_p).f];
		((*nn_p).af)[((*nn_p).rg)[k]] = i;
		((*nn_p).rg)[i] = ((*nn_p).rg)[k];
	}
	((*nn_p).aa)[(*nn_p).a] = k;	//si sistema la lista degli alberi attivi
	((*nn_p).rg)[k] = (*nn_p).a;
	(*nn_p).a ++;

	(*pt_p)[k].attivo = 1;	//si sveglia k

	return EXIT_SUCCESS;
}	
	

int congelare(long int k, num* nn_p, punto** pt_p){
	long int i;	//vertice generico

	(*nn_p).a--;	//si ha un albero attivo di meno
	if (((*nn_p).rg)[k] < (*nn_p).a){	//si sistema la lista degli alberi attivi e quella dei ranghi
		i = ((*nn_p).aa)[(*nn_p).a];
		((*nn_p).aa)[((*nn_p).rg)[k]] = i;
		((*nn_p).rg)[i] = ((*nn_p).rg)[k];
	}
	((*nn_p).af)[(*nn_p).f] = k;	//si sistema la lista degli alberi freddi
	((*nn_p).rg)[k] = (*nn_p).f;
	(*nn_p).f++;

	(*pt_p)[k].attivo = 0;	//si congela k

	return EXIT_SUCCESS;
}


long int radice(long int i, punto** pt_p){
	long int j;	//vertice dopo il quale i si va a inserire prima della sua radice k nel caso in cui questa era inizialmente sconosciuta
	long int k = (*pt_p)[i].rad;	//negativo se sconosciuta

	if(k < 0){
		k = radice((*pt_p)[i].succ, pt_p);	//si va a trovare la radice del vicino di i a cui i e` collegato
		(*pt_p)[i].rad = k;	//i condivide la stessa radice
		j = (*pt_p)[k].prima;	//j precede k nel ciclo di chi si sapeva collegato a k
		(*pt_p)[j].dopo = i;	//si inserice i in quel ciclo	
		(*pt_p)[i].prima = j; 
		(*pt_p)[i].dopo = k;
		(*pt_p)[k].prima = i;
	}	

	return k;	//k e` la radice di i
}


long int radice_fredda_aleatoria(num* nn_p){
	return ((*nn_p).af)[(long int) floor(drand48() * (*nn_p).f)];	//si utilizza la lista degli alberi freddi
}


long int radice_attiva_aleatoria(num* nn_p){
	return ((*nn_p).aa)[(long int) floor(drand48() * (*nn_p).a)];	//si utilizza la lista degli alberi attivi
}


long int vicino_aleatorio_senza_uccisione(long int k, num* nn_p, punto* pt){
	int i, j, c;	//per percorrere la tabella dei vicini di k per dichotomia
	double x = drand48() * (*nn_p).ttm ;	//x e` uniforme tra 0 e il tasso totale massimale 
	long int l;	//vertice scelto


	if (x >= pt[k].tt) l = k;	//j = k con la probabilita` data dalla diagonale della matrice stochastica che descrive le scheletro 
	else{
		i = 0;
		j = pt[k].nv;
		c = (i + j) / 2;
		while (c > i){
			if ((pt[k].somm_parz_tass)[c - 1] <= x) i = c;
			else j = c;
			c = (i + j) / 2;
		}		
		l = (pt[k].vic)[c];
	}

	return l;	//l e` il vicino scelto
}


long int vicino_aleatorio(long int k, num* nn_p, punto* pt){
	int i, j, c;	//per percorrere la tabella dei vicini di k per dichotomia
	double x = drand48() * (pt[k].tt + (*nn_p).q);	//x e` uniforme tra 0 e il tasso totale + q
	long int l;	//vertice scelto
	double den = pt[k].tt + (*nn_p).q;	//denominatore nel calcolo del tempo utile a fare la mossa sapendo che k fu scelto uniformemente
	
	if (x >= pt[k].tt){
		 l = -1;
	}
	else {
		i = 0;
		j = pt[k].nv;
		c = (i + j) / 2;
		while (c > i){
			if ((pt[k].somm_parz_tass)[c - 1] <= x) i = c;
			else j = c;
			c = (i + j) / 2;
		}		
		l = (pt[k].vic)[c];
	}
			
	if (den > 0) (*nn_p).tu += - log(drand48()) * ((*nn_p).ttm + (*nn_p).q) / den;	//vedi la declarazione di den, che va come q per q molto grande

	return l;	//l e` il vicino scelto
}

int archi_ordinati(arco* lista, int lunghezza){ 	

	double pivot = lista[lunghezza / 2].potenziale;	//per dividere in due gli elementi della lista
	arco* testa = malloc(lunghezza * sizeof(*testa));	//per segnarsi gli archi di potenziale piu` piccolo del pivot
	arco* corpo = malloc(lunghezza * sizeof(*corpo));	//per segnarsi gli archi di potenziale uguale al pivot
	arco* coda = malloc(lunghezza * sizeof(*coda));		//per segnarsi gli archi di potenziale piu` grande del pivot 
	int ordinata = 1;	//per controllare se la lista e` ordinata
	int	i, j, k, l;	//per percorrere le liste testa, corpo, coda e lista respettivamente
	double ultimo;	//ultimo valore letto
	double pot;	//potenziale corrente

	i = j = k = l = 0; //si percorre la lista, riempiendo testa, corpo e coda e cotrollando l'ordinamento
	ultimo = lista[l].potenziale;
	while (l < lunghezza) {
		pot = lista[l].potenziale;
		if (pot < ultimo) {
			ordinata = 0; }
		if (pot < pivot) {
			testa[i] = lista[l];
			i++; }
		if (pot == pivot) {
			corpo[j] = lista[l];
			j++; }
		if (pot > pivot) {
			coda[k] = lista[l];
			k++; }
		ultimo = pot;
		l++; }

	if (ordinata) {	 //se e` ordinata non c'e` niente da fare se non liberare la memoria
		free(testa);
		free(corpo);
		free(coda); }
	else {	//se non e` ordinata si ordinano testa e coda e si ricostruisce una lista ordinata
		for(l = i; l < i + j; l++) {
			lista[l] = corpo[l - i] ;}
		free(corpo);
		if (i > 0) { 	//la testa potrebbe essere vuota
			archi_ordinati(testa, i);
			for(l = 0; l < i; l++) { 
				lista[l] = testa[l] ;} }
		free(testa);
		if (k > 0) {	//la coda potrebbe essere vuota
			archi_ordinati(coda, k); 
			for(l = i + j; l < lunghezza; l++) {
				lista[l] = coda[l - i - j] ; } } 
		free(coda); }

	//for (l = 0; l < lunghezza; l++) { printf("%e ", lista[l].potenziale); } printf("\n"); fflush(stdout);
	
	return ordinata; }


int kruskall(num* nn_p, punto** pt_p, arco** arc_p, int m){	
	
	long int a;	//arco generico
	long int i;	//contattore o vertice
	long int piede, testa;	//estemita` di a

	
	tutti_svegli_tempo_zero(nn_p, pt_p);	//si parte con la foresta seminale di alberi attivi 
	//printf("tempo azzerato, tutti svegli\n"); fflush(stdout);

	a = 0;	//si aggiungono n - m archi partendo dalle radici, dal meno costoso in su 
	for(i = 0; i < (*nn_p).n - m; i++) {
		piede = (*arc_p)[a].piede;
		testa = ((*pt_p)[piede].vic)[(*arc_p)[a].testa]; 
		while(radice(testa, pt_p) == radice(piede, pt_p)) {	//si controlla che si possa aggiungere l'arco a, senno` si passa all'arco successivo
			a++;
			piede = (*arc_p)[a].piede;
			testa = ((*pt_p)[piede].vic)[(*arc_p)[a].testa]; }
		//printf("Si piglia l'arco %d, di piede %ld e testa %ld, %do vicino, rimangono %d archi da scegliere\n", a, (*arc_p)[a].piede, ((*pt_p)[(*arc_p)[a].piede].vic)[(*arc_p)[a].testa], (*arc_p)[a].testa, (int) (*nn_p).n - m - i -1 ); fflush(stdout);
		//printf("La radice del piede %ld e` %ld di rango %ld\n", piede, radice(piede, pt_p), ((*nn_p).rg)[radice(piede, pt_p)]);
		sposta_radice(piede, nn_p, pt_p);
		coalescenza(piede, testa, nn_p, pt_p); 
		a++; }
	while ((*nn_p).a > 0) {
		congelare((*nn_p).aa[(*nn_p).a - 1], nn_p, pt_p); 
		}	//si congelano gli alberi	

	return EXIT_SUCCESS; }


int sposta_radice(long int i, num* nn_p, punto** pt_p) { 
	long int j, k, l;	//per percorrere i vertici la cui freccia va rovesciata : j per il nuovo successore, k per il punto corrente, l per il vecchio successore
	long int radice_originale; //radice dell'albero che copre i, all'inizio
	long int rango;	//posto in classifica della radice dell'albero attivo che copre i

	radice_originale = radice(i, pt_p);		
	rango = ((*nn_p).rg)[radice_originale];

	//si rovesciano le frecce
	j = -1;
	k = i;
	do {
		l = (*pt_p)[k].succ;
		(*pt_p)[k].succ = j;
		j = k;
		k = l;
	} while (l >= 0);

	//si fa il giro di chi si sapeva radicato in radice_originale per informare che si e` ora radicato in i
	k = i;
	do {
		(*pt_p)[k].rad =i;
		k = (*pt_p)[k].dopo;
	} while (k != i);

	//si mette a posto la lista degli alberi attivi
	((*nn_p).aa)[rango] = i;
	((*nn_p).rg)[i] = rango; //e si mette a posto il la lista dei ranghi

	return EXIT_SUCCESS;
}

	
