#ifndef _LODGE_
#define _LODGE_
#include "cuore.h"
#define LMAX (1 << 10)	//lunghezza massimale delle righe di un file .g da cui leggere i pesi 
#define EPSILON (double) 1 / (double) (1 << 16) //serve a controllare l'ugualianze tra due double a meno di errori di approssimazione
#define OUTPUTFILE "./output.txt"
#define OUTPUTERRORFILE "./outputerrorfile.txt"

typedef struct{ 		//la struttra param descrive tutti i parametri
	int da_file;		//vale 1 se si vuole prendere il grafo da un file, 0 senno`
	char* grafo;		//nome del file da cui leggere il grafo (se cosi` si e` deciso di fare)
	long int m;		//numero di radici da raggiungere, vale 0 se non si vuole raggiungere nessun numero particolare
	double e;		//errore ammesso in multipli di sqrt(m)
	int fr;			//vale 1 se si vuole frammentare-ricompore lungo l'accopiamento delle foreste per q che va a zero, vale 0 senno`
	double q_min;	//valore minimo di q quando si fa scendere q lungo l'accompiamento : ha senso solo se (.fr == 1)
	double z;		//fatt. di mult. per costr. un altro grafo con tassi incamb. all'int. degli alb. e mult. per z tra alb. div., neg. per non costruire niente
	int stampa_foresta;	//vale 1 se si vuole stampare la foresta intera
	int raggiunto; 		//vale 1 dopo aver stampato cio` che era da stampare, 0 prima
	int ancora;		//vale 1 finche' si vuole far girare il programma, 0 dopo
	int scrivere;		//vale 1 quando si vuole scrivere nel terminale, dando inforamazioni sul stderr, vale 0 per un'esecuzione silenziosa
	int verboso;		//vale 1 se si vuole stampare le uscite nel stdin, 0 senno`
	int X;			//vale 1 se si vuole una versione grafica del programma, 0 altrimenti
	int immagini;		//numero di immagini al secondo -- rilevante per la visualizzazione grafica ma anche per decidere quando dare informazioni se (scrivere)
	int contatore;		//conta il numero di immagini mostrate dopo l'ultimo commento nello stderr -- rilevante quanto .immagini in modalita` non grafica
	double scadenza;	//limite da superare per il numero di battimenti di orologio per mostrare l'immagine succesiva -- rilevante quanto .immagini in modalita` non grafica
	int pausa;		//quantita` di millisecondi da aspettare prima di passare all'immagine successiva --  vale 0 in mod. non graf. ed e` allora rilevante quanto .immagini
	void* img_p;	//indirizzo dell'immagine che si mostra -- rilevante per la visualizzazione grafica
	char* nome;		//nome della finestra -- rilevante per la visualizzazione grafica
	int L;			//lunghezza orizzontale della finestra -- rilevante per la visualizzazione grafica
	int l;			//larghezza verticale della finestra -- rilevante per la visualizzazione grafica
	int soloradici;		//vale 1 se si vuole vedere le radici soltanto, 0 senno` -- rilevante per la visualizzazione grafica
	int bordo_si;		//vale 1 se si vuole vedere i bordi, 0 senno` -- rilevante per la visualizzazione grafica
	int ved_att;		//vale 1 se si vuole vedere gli alberi attivi, 0 senno` -- rilevante per la visualizzazione grafica
	int caric_manc;		//per caricamento mancato: vale 1 quando si aspetta la prossima configurazione tutta fredda per poter mostrarla -- rilevante per la vis. graf.
	int grandi_radici;	//fattore d'ingrandimento da 0 a 11 -- rilevante per la visualizzazione grafica
	int potenziale;		//vale 1 se si vuole utilizzare il potenziale per colorae gli alberi blu (i.e. freddi), 0 senno`
	int tasso_blu;		//vale 1 se si vuole utilizzare i tassi totali per colorare gli alberi blu, 0 senno` -- rilevante per la visualizzazione grafica
	int blu_unif;		//vale 1 se si vuole un blu uniforme invece del camaieu, 0 senno` -- rilevante per la visualizzazione grafica
	char* foto;		//nome del file in cui si vuole salvare l'immagine, vale NULL se non si vuole salvare niente -- rilevante per la visualizzazione grafica
	char foto_rad[100];	//nome senza estenzione del file in cui si vuole salvare l'immagine  -- rilevante per la visualizzazione grafica
	char foto_ext[100];	//estenzione del file in cui si vuole salvare l'immagine -- rilevante per la visualizzazione grafica
	int nb_foto;		//numero di immagini da salvare, rilevante se (.fr) soltanto -- rilevante per la visualizzazione grafica
	double q_foto;		//valore di q per il quale si deve salvare l'immagine succesiva, rilevante se (.fr) soltanto -- rilevante per la visualizzazione grafica
	double fdd;		//fattore di decimazione tra .q_foto successivi, rilevante se (.fr) soltanto  -- rilevante per la visualizzazione grafica
	int num_foto_fatte;	//numero di foto fate (previste) -- rilevante per la vis. graf.
	int num_istantanee;	//numero di foto istantanee prese (impreviste) -- rilevante per la vis. graf.
  int flag_outputfile;  // flag the output file name is informed
  char* outputfilename;   // name of the output file
  FILE* outputfile;  // output file *
  int flag_outputErrorfile;  // flag the output error file  name is informed
  char* outputErrorfilename; // name of the output error file
  FILE* outputErrorfile;  // output error file *
} param;

int acquisizione(int argc, char* argv[], num* nn_p, param* prm_p);
int inizializzazione_basica(num* nn_p, punto** pt_p, param* prm_p); //inizializza tutto cio` che non riguarda la parte grafica a meno del potenziale
int liberare_memoria(num* nn_p, punto** pt_p, param* prm_p);		
int scrivere_un_altro_grafo(num* nn_p, punto** pt_p, param* prm_p);	//si scrive un file di grafo ott. dal grafo orig. via mult. per z dei tassi tra vert. di alb. dist.;
int stampare_radici(num* nn_p, punto** pt_p, param* prm_p, double** obj1d); 
int stampare_foresta(num* nn_p, punto** pt_p, param* prm_p, double*** obj2d);
int pulire_terminale( param* prm_p);		//va a capo sul stderr per ridare una riga pulita quando si danno informazioni sullo stato del sistema via lo stderr, tipicamente nel terminale
int calcolare_potenziale(num* nn_p, punto** pt_p);
int dare_qualche_informazione(num* nn_p, param* prm_p); //scrive ogni tanto (circa una volta al secondo) qualche commento via lo stderr sullo stato del sistema
int dare_informazioni(num* nn_p, param* prm_p); //scrive un commento via lo stderr sullo stato del sistema
int grezza_acquisizione(int argc, char* argv[], num* nn_p, param* prm_p); //speciale per bruta_foresta : prm.X vale 0 e non ci sono i commenti legati alla grafica soltanto
int init_output(int n, double*** obj2d, double** obj1d, char* option, int index_re);
int determine_dimension(int n, int index_re, double*** obj2d, double** obj1d, int* dim1, int* dim2, char* option );
int free_output(int n, double** (*obj2d), double* (*obj1d), char* option, int index_re);
int createTable(int nbLin, int nbCol, double *** table);
#endif
