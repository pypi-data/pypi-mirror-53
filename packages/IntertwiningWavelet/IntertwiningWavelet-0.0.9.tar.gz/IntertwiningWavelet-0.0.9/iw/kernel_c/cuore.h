#ifndef _CUORE_
#define _CUORE_

typedef struct{	//la struttura punto descrive tutti gli attributi di un vertice, pt[i] sara` un punto associato al vertice i
	int nv;					//numero di vicini
	long int* vic; 			//tabella dei vicini
	double* tass;			//tassi dei vicini
	double* somm_parz_tass;	//tabella delle somme parziali dei tassi
	double tt;				//tasso totale
	double pot;				//-1 nel caso non rev., pot. d'eq. nel caso rev., prop. al - log della mis. d'eq. ammeno di una cost. add., spalm. tra 0 e 1 oppure = 1 dappertut.
	double massa;			//0 prima del calcolo del potenziale, poi massa d'equilibrio nel caso reversibile, $1 / nn.n$ altrimenti
	long int succ;			//per successore: punto successivo nell'albero, negativo alla radice
	long int rad;			//radice collegata, NB: negativo se sconoscuita (va calcolato solo quando serve)
	int attivo;				//se il punto e` radice, vale 1 se attiva, 0 senno`. NB: non e` definito quando il punto non e` radice.
	long int prima;			//punto precedente incatenato per descrivere la partizione in alberi (rilevante soltanto quando la radice a cui e` collegata e` nota)
	long int dopo;			//punto successivo incatenato
	int x; 					//ascissa -- rilevante per una visulizzaione grafica
	int y; 					//ordinata -- rilevante per una visulizzaione grafica
	int intens;				//intensita` del colore dell'albero radicato in quel punto -- rilevante per una visualizzazione grafica
	int wilson;				//intero fra 0, 1 e 2 : serve soltanto nell'agoritmo di Wilson semplice (0 per i siti sistemati, 2 per le radici da sistemare, 1 altrimenti)
} punto;

typedef struct{	//la struttura num contiene tutti i dati globali del sistema, come il tempo corrente, q o la lista degli alberi attivi
	long int n; 	//numero di punti
	long int na;	//numero di archi del grafo
	double ttm;		//tasso totale massimo
	double tu;		//tempo universale, il tempo di Wilson si ottienne dividendo per (.ttm + .q)
	long int a;		//numero di alberi attivi
	long int* aa;	//lista degli alberi attivi
	long int f;		//numero di alberi freddi
	long int* af; 	//lista degli alberi freddi
	long int* rg;	//lista dei ranghi (= posto in classifica) delle radici nelle proprie liste (attive e fredde)
	double q;		//tasso di raffredamento, negativo per infinito
	double tmp_inv;	//negativa prima del calcolo poi temperatura inversa t.c. $\mu (i) = e^{-(.temp_inv) pt[i].pot} / Z$ nel caso rev, non uniforme, altrimenti .tmp_inv = 0
	double Z;		//funzione di partizione, vale 0 prima del calcolo dei potenziali
} num;

typedef struct{ //la struttura arco serve a descrivere gli archi di un grafo, arco[i] contienne informazioni sull'i-esimo arco
	long int piede; 	//piede dell'arco, indicato con l'indice del vertice
	int testa;	//punta dell'arco, indicata con la posizione nella lista dei vicini del piede
	double potenziale;	//poteziale dell'arco
} arco;

long int vicino_aleatorio(long int k, num* nn_p, punto* pt);	//sorteggia un vicino di k, rinvia -1 per il cimitero, e incrementa il tempo universale
long int vicino_aleatorio_senza_uccisione(long int k, num* nn_p, punto* pt);	//sortg. un vic. di k, possib. k stesso e con tasso 0 per il cim., non tocca al tempo univ.
long int radice_attiva_aleatoria(num* nn_p);	//sorteggia uniformamente una radice attiva
long int radice_fredda_aleatoria(num* nn_p);	//sorteggia uniformamente una radice fredda
long int radice(long int i, punto** pt_p);		//rinvia la radice a cui i e` collegata
int congelare(long int k, num* nn_p, punto** pt_p);	//congela la radice k
int svegliare(long int k, num* nn_p, punto** pt_p);	//sveglia la radice k
int congelare_tutto(num* nn_p, punto** pt_p);		//congela tutto con l'incremento del tempo universale: si gira l'algo di Wilson con q infinito
int tutti_svegli_tempo_zero(num* nn_p, punto** pt_p); 	//si fa d'ogni punto un albero attivo e si mette il tempo a 0
int coalescenza(long int k, long int j, num* nn_p, punto** pt_p);	//attacca la radice attiva k in j, su di un albero distinto
int frammentazione(long int k, long int j, num* nn_p, punto** pt_p);	//sposta la radice k in j, radicata in k, e frammenta l'albero
double tempo_di_wilson(num* nn_p);		//converte il tempo universale in tempo utile a l'algo di Wilson
int	tutti_radici_da_sistemare(num* nn_p, punto** pt_p); 	//indica per ciasc. punto la radice come scon. (.rad = -1) e lo segna come radice da sistemare (.wilson = 2)
double wilson(num* nn_p, punto** pt_p); 	//gira l'algoritmo di Wilson semplice e rinvia il tempo associato (all'inizio si riazzera gli orlogi)
int sposta_radice(long int i, num* nn_p, punto** pt_p);	//sposta in i la radice dell'albero attivo che copre i
int archi_ordinati(arco* lista, int lunghezza); 	//ord. gli elem. della lista di lung. 'lunghezza' sec. i pot. d'arco e rinvia 0 se c'era lavoro da fare, 1 altrimenti
int kruskall(num* nn_p, punto** pt_p, arco** arc_p, int m);	//costr. lo stato fond., dato i pot. d'arco ordinati,  delle for. ric. con m alberi fred. e si azzerra il tempo
#endif
