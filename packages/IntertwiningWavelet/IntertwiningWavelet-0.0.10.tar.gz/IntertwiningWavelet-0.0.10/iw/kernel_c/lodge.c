#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <time.h>
#include <string.h>  
#include "lodge.h"

int calcolare_potenziale(num* nn_p, punto** pt_p){
	long int i, v;	//vertici
	int j, k;	//indici di vicini
	int* fatto = NULL;	//fatto[i] rinvia 1 se il calcolo e` stato fatto per il vertice i, 0 senno`
	int fatti = 0;	//conta il numero di vertici per cui il calcolo e` stato fatto
	double pot_min = (double) 0;	//potenziale minimale aggiustato mentre si fanno i calcoli
	double pot_max = (double) 0;	//potenziale maximale aggiustato mentre si fanno i calcoli
	int giro_bianco = 1;	//vale 0 quando girando i vertici si e` potuto fare un nuovo calcolo utilizzando un vertice vicino per cui il calcolo era gia` stato fatto
	int reversibile = 1; 	//passa a zero appena si vede che la dinamica non e` reversibile

	fatto = malloc((*nn_p).n * sizeof(int));	//si inizializza la tabella fatto con dei zeri
	for(i = 0; i < (*nn_p).n; i++){
		fatto[i] = 0; }
	while (reversibile && (fatti < (*nn_p).n)) {	//si finisce quando i calcoli fatti sono quanti i vertici
		i = 0;
		while (fatto[i]) i++;	//si trova il primo vertice per cui il conto non e` stato fatto
		if (giro_bianco){	//si mette il potenziale a 0 se si e` fatto un giro bianco, quando non c'erano piu` vicini dei siti per cui il calcolo era stato fatto
			(*pt_p)[i].pot = 0;
			fatto[i] = 1;
			fatti++;
			i++; }
		giro_bianco = 1;	//e` un a priori che si correge appena si fa un nuovo conto
		while(i < (*nn_p).n){	//si percorre l'insiemme dei vertici (c'e` un i++ alla fine)
			if ((*pt_p)[i].tt == 0) {	//si mette 0 per un punto assorbente
				(*pt_p)[i].pot = 0;
				fatto[i] = 1;
				fatti++; }
			else{
				for(j = 0; (j < (*pt_p)[i].nv) && !(fatto[i]); j++){	//si cerca un vic. di i per cui il conto e` stato fatto (il conto per i stando da fare)
					if (fatto[v = ((*pt_p)[i].vic)[j]]){	//se si trova si chiama v quel vicino
						giro_bianco = 0;	//non e` quindi stato un giro bianco
						for(k = 0;  (k < (*pt_p)[v].nv) && !(((*pt_p)[v].vic)[k] == i); k++){} 	//si controlla que i e` un vicino di v
						if (k == (*pt_p)[v].nv) {	//se cosi` non e` si nega la reversibilita`
							reversibile = 0; }
						else{	//se i e` effetivamente un vicino di v si calcola il potenziale di i e si aggiusta massimi e minimi
							(*pt_p)[i].pot = (*pt_p)[v].pot - log(((*pt_p)[v].tass)[k]) + log(((*pt_p)[i].tass)[j]);
							if ((*pt_p)[i].pot < pot_min) pot_min = (*pt_p)[i].pot;
							if ((*pt_p)[i].pot > pot_max) pot_max = (*pt_p)[i].pot;
							fatto[i] = 1;
							fatti++; } } } }
			i++; } }
	free(fatto);

	i = 0; //si gira il grafo per controllare la reversibilita`
	while (reversibile && (i < (*nn_p).n)) {
		j = 0;
		while (reversibile && (j < (*pt_p)[i].nv)) {
			v = ((*pt_p)[i].vic)[j];
			k = 0;
			while ((k < (*pt_p)[v].nv) && (((*pt_p)[v].vic)[k] != i)) k++;
			if (k == (*pt_p)[v].nv) {
				reversibile = 0; }
			else {
				if (fabs((*pt_p)[i].pot - (*pt_p)[v].pot + log(((*pt_p)[v].tass)[k]) - log(((*pt_p)[i].tass)[j])) > EPSILON) reversibile = 0; }
			j++; }
		i++; }
			
	if (reversibile && (pot_min < pot_max)) {	//si spalma il potenziale tra 0 e 1, se possibile, senno` lo si mette tutto a 1
		(*nn_p).tmp_inv = pot_max - pot_min; 
		for(i = 0; i < (*nn_p).n; i++){
			(*pt_p)[i].pot = ((*pt_p)[i].pot - pot_min) / (pot_max - pot_min); } }
	else{
		(*nn_p).tmp_inv = (double) 0;
		if (reversibile) {
			for(i = 0; i < (*nn_p).n; i++) (*pt_p)[i].pot = (double) 1;
		}
		else {
			for(i = 0; i < (*nn_p).n; i++) (*pt_p)[i].pot = (double) -1; } }
	for(i = 0; i < (*nn_p).n; i++) {	//calcolo della funzione di partizione
		(*nn_p).Z += exp( - (*nn_p).tmp_inv * (*pt_p)[i].pot); }
	for(i =0; i < (*nn_p).n; i++) {	//calcolo delle masse
		(*pt_p)[i].massa = exp( -(*nn_p).tmp_inv * (*pt_p)[i].pot) / (*nn_p).Z ; }
	
	return EXIT_SUCCESS;
}


int pulire_terminale( param* prm_p) {
     ;
	//fprintf((*prm_p).outputErrorfile, "\n");	//serve ad aver una riga pulita quando si scrive sul stderr

	return EXIT_SUCCESS;
}


int stampare_foresta(num *nn_p, punto** pt_p, param* prm_p, double** (*obj2d)) {
	long int i;	//radice generica
	long int rad;
    long int succ;
	for (i = 0; i < (*nn_p).n; i++) {
    rad = radice(i, pt_p);
    succ = (*pt_p)[i].succ;
    if((*prm_p).scrivere){
	//	fprintf((*prm_p).outputfile,"vertice %9ld    radice %9ld    successore %9ld", i, rad, succ);
	//	fprintf((*prm_p).outputfile,"                                              \n");
    ;}
    (*obj2d)[i][0] = i;
    (*obj2d)[i][1] = rad;
    (*obj2d)[i][2] = succ;
	}
	return EXIT_SUCCESS;
}

int stampare_radici(num* nn_p, punto** pt_p, param* prm_p, double** obj1d) {
	long int i;	//radice generica
  long int j = 0;

	for (i = 0; i < (*nn_p).n; i++){	//si percorre l'insieme dei vertici e si stampano vertice ascissa e ordinata se sono radici
		if (radice(i, pt_p) == i){
    //  if((*prm_p).scrivere){
			  //  fprintf((*prm_p).outputfile,"radice %9ld    ", i);
			//    if ((*prm_p).X)  //fprintf((*prm_p).outputfile,"ascissa %4d    ordinata %4d", (*pt_p)[i].x, (*pt_p)[i].y);	//si scrivono ascisse e ordinate solo nella versione grafica
			   // fprintf((*prm_p).outputfile,"                                                                     \n");
    //    }
      (*obj1d)[j] = i;
      j = j + 1;
		}
	}
	return EXIT_SUCCESS;
}

int scrivere_un_altro_grafo(num* nn_p, punto** pt_p, param* prm_p){ 
	long int i;	//i e` un vertice
	long int r;	//r la sua radice
	long int n = (*nn_p).n;	//per che sia piu` leggibile
	double z = (*prm_p).z;	//per che sia piu` leggibile
	int j;	//per percorrere i vicini di i

//	fprintf((*prm_p).outputfile,"# File di un grafo ottenuto da un altro grafo, dopo campionamento di una foresta,\n");
//	fprintf((*prm_p).outputfile,"# per multiplicazione per z = %lf dei tassi tra punti in alberi distinti.\n", z);
//	fprintf((*prm_p).outputfile,"#\n");
//	fprintf((*prm_p).outputfile,"numero_di_vertici %ld    ", (*nn_p).n);
	if ((*prm_p).X)// fprintf((*prm_p).outputfile,"lunghezza_della_finestra %d    altezza_della_finestra %d", (*prm_p).L, (*prm_p).l);	//si scriv. lung. e larg. solo nella versione grafica
//	fprintf((*prm_p).outputfile,"\n");
	
	for(i = 0; i < n; i++){	//i vertici saranno gli stessi
	//	fprintf((*prm_p).outputfile,"#\n");
	//	fprintf((*prm_p).outputfile,"vertice %9ld    numero_di_vicini %5d    ", i, (*pt_p)[i].nv);
		if ((*prm_p).X)// fprintf((*prm_p).outputfile,"ascissa %4d    ordinata %4d", (*pt_p)[i].x, (*pt_p)[i].y); //si scriv. lung. e larg. solo nella versione grafica
		//fprintf((*prm_p).outputfile,"\n");
		r = radice(i, pt_p);
		for(j = 0; j < (*pt_p)[i].nv; j++){	
			if (radice(((*pt_p)[i].vic)[j], pt_p) == r){	//si controlla per ciascun vicino di i se condivide con i la stessa radice r
			//	fprintf((*prm_p).outputfile,"vicino %9ld    tasso %E\n", ((*pt_p)[i].vic)[j], ((*pt_p)[i].tass)[j]);	//in quel caso il tasso e` lo stesso
			 // //W[i][((*pt_p)[i].vic)[j]] = (double)((*pt_p)[i].tass)[j];
      }
			else{	//nel caso contrario il tasso viene multiplicato per z
			//	fprintf((*prm_p).outputfile,"vicino %9ld    tasso %E\n", ((*pt_p)[i].vic)[j], z * ((*pt_p)[i].tass)[j]);
      //  //W[i][((*pt_p)[i].vic)[j]] =  (double) z * ((*pt_p)[i].tass)[j];
			}
		}
	}		
	return EXIT_SUCCESS;
}

int liberare_memoria(num* nn_p, punto** pt_p, param* prm_p){
	long int n = (*nn_p).n;	//per che sia piu` leggibile
	long int k;	//vertice generico
  fclose((*prm_p).outputErrorfile);
  if((*prm_p).scrivere){
      fclose((*prm_p).outputfile);
  }
	free((*nn_p).aa);
	free((*nn_p).af);
	free((*nn_p).rg);
	for (k = 0; k < n; k++){
		free((*pt_p)[k].vic);
		free((*pt_p)[k].tass);
		free((*pt_p)[k].somm_parz_tass);
	}
	free(*pt_p);

	return EXIT_SUCCESS;
}
	
int init_output(int n, double*** obj2d, double** obj1d, char* option, int index_re){
  int i, j;
  if (strcmp(option, "r") == 0){
      (*obj2d) = realloc((*obj2d), n *(index_re+1)*sizeof(double*));
      if ((*obj2d) == NULL){
        fprintf(stderr, "trouble in realloc memory");
        exit(EXIT_FAILURE);
        }
      double *table2 = (double*)malloc(sizeof(double)*3*n);
      for (i = 0  ; i < n; i++){
          (*obj2d)[i+n*index_re] = &table2[i *3];
          for (j = 0 ; j < 3 ; j++){
             (*obj2d)[i+n*index_re][j] = -1;
          }
       }
      }  
  else if ( strcmp(option,"z") ==0){
     createTable(n, n, obj2d);
  }
  else if ( strcmp(option, "j") == 0 || strcmp(option, "f")==0){ // cas j mj ou qj
     createTable(n, 3, obj2d );
  }
  else if ( strcmp(option, "m") == 0|| strcmp(option, "q") == 0){
     *obj1d = malloc(n * sizeof(double));   //cas m ou q sans j
     if ((*obj1d) == NULL){
       fprintf(stderr, "trouble in memory allocation");
       exit(EXIT_FAILURE);
       }
     for (i = 0 ; i < n ; i++){
        (*obj1d)[i]= -1;
     }
  }
  return EXIT_SUCCESS;
}


int createTable(int nbLin, int nbCol, double*** pt_table){
	*pt_table = (double **)malloc(sizeof(double*)*nbLin);
	double *table2;
	table2 = (double *)malloc(sizeof(double)*nbCol*nbLin);
	if (*pt_table == NULL){exit(EXIT_FAILURE);}
	if (table2== NULL){exit(EXIT_FAILURE);}
    int i, j;
	for( i = 0 ; i < nbLin ; i++){
		(*pt_table)[i] = &table2[i*nbCol];
    for( j = 0 ; j < nbCol; j++){
      (*pt_table)[i][j] = -1;
      }
	}
	return EXIT_SUCCESS;
}

int free_output(int n, double*** obj2d, double** obj1d, char* option,int index_re){
 int i;
 if(strcmp(option,"j") ==0|| strcmp(option,"z") ==0|| strcmp(option,"f") ==0){ // cas j mj ou qj
      for (i = 0; i < (index_re+1); i++){      
        free((*obj2d)[i*n]);
        (*obj2d)[i] = NULL;}
      free(*obj2d);
      (*obj2d) = NULL;
      }
  else if (strcmp(option,"m") ==0|| strcmp(option,"q") ==0){
      free ((*obj1d));
    (*obj1d)=NULL;
    }
  return EXIT_SUCCESS;
}


int determine_dimension(int n, int index_re, double*** obj2d, double** obj1d, int* dim1, int* dim2, char* option ){
  int i ;
  if (strcmp(option,"j") == 0 || strcmp(option,"f") == 0){
      for (i=0 ; i <  n*(index_re+1); i++){
         if ((*obj2d)[i][0] == -1){
            *dim1 = i;
            *dim2 = 3;
            break;}
         
      }

      if (i == n * (index_re + 1) ){*dim1 = n*(index_re+1); *dim2=3;}
  }
   else if (strcmp(option,"m") ==0 ||strcmp(option,"q") ==0){
      for (i =0 ; i < n ; i++){
        if ((*obj1d)[i] == -1){
            *dim1 = i;
            *dim2 = 1;
            break;}      
      }
      if (i == n){*dim1 = n; *dim2=1;}
    }
  return EXIT_SUCCESS;
}
int inizializzazione_basica(num* nn_p, punto** pt_p, param* prm_p){
	long int i, j; 	//vertici generici e anche acissa e ordinata per costruire un grafo torico
	long int k, k1;	//vertici generici
	int kk;	//per girare i vicini di k o k1
	char riga[LMAX];	//ciascuna riga di un eventuale file di grafo
	FILE* grafo_p = NULL;	//puntatore al file di grafo
	int l, L;	//larghezza e lunghezza di un grafo torico
	long int n;	//per il numero di vertici

	srand48((long int) time(NULL));	//per inizializare il seme del generatore di numeri pseudo aleatori
  //(*prm_p).outputErrorfile = fopen((*prm_p).outputErrorfilename, "w");
 // if ((*prm_p).outputErrorfile == NULL) {
 //   fprintf(stderr, "errror in the output error file...\n");
	//	exit(EXIT_FAILURE);
  //}
//  if((*prm_p).scrivere){
 // (*prm_p).outputfile =  fopen((*prm_p).outputfilename, "w");
  //  if ((*prm_p).outputfile == NULL) {
  //  fprintf(stderr, "errror in the output file...\n");
	//	exit(EXIT_FAILURE);
 // }
//  }
	if ((*prm_p).da_file) {	//se si vuole legere il grafo da un file
		grafo_p = fopen((*prm_p).grafo, "r");	//si apre il file
		if (grafo_p == NULL){	//si controlla che sia ben aperto
			fprintf(stderr, "Non e` stato possibile aprire il file del grafo...\n");
			exit(EXIT_FAILURE);
		}	
		do{	//si cerca la prima riga che non comincia con '#'
			if (fgets(riga, LMAX, grafo_p)==0){
        fprintf(stderr, "fget function failure \n");}
		} while(riga[0] == '#');
		if (3 == sscanf(riga, "%*s %ld %*s %d %*s %d", &n, &L, &l)){	//si prendono il numero di nodi assieme alle lunghezza e larghezza della finestra
			(*prm_p).L = L;
			(*prm_p).l = l;
		}
		else (*prm_p).X = 0;
	}
	else{	//nel caso in cui si costruisce un grafo torico
		l = (*prm_p).l;
		L = (*prm_p).L;
		n = L * l;
	}

	(*nn_p).n = n;
	(*nn_p).ttm = (double) 0; 	//si parte con 0 per il tasso totale massimale e si corregge percorando i tassi puntuali
	(*nn_p).aa = malloc(n * sizeof(long int));	//ci sarrano al massimo n alberi attivi
	(*nn_p).af = malloc(n * sizeof(long int));	//ci sarrano al massimo n alberi freddi
	(*nn_p).rg = malloc(n * sizeof(long int));	//ci sarrano al massimo n alberi
	(*nn_p).na = 0;	//si fara` crescere vertice per vertice, aggiugendo ogni volta il numero di vicini
	*pt_p = malloc(n * sizeof(punto));	//ci sono n vertici
	if((*prm_p).da_file){	//se c'e` un file da leggere
		for(k = 0; k < n; k++){	//tante volte quanto sono i vertici
			do{	//si cerca la successiva riga a non cominciare con '#'
				if(fgets(riga, LMAX, grafo_p)==0){fprintf(stderr, "fget function failure \n");}
			} while(riga[0] == '#');
			sscanf(riga, "%*s %ld", &k1);	//si legge il nome k1 del vertice
			sscanf(riga, "%*s %*d %*s %d %*s %d %*s %d", &((*pt_p)[k1].nv), &((*pt_p)[k1].x), &((*pt_p)[k1].y)); //si leg. num. vert. asc. e ord.
			(*nn_p).na += (*pt_p)[k1].nv;
			(*pt_p)[k1].vic = malloc((*pt_p)[k1].nv * sizeof(long int));	//si riserva lo spazio per la tabella dei vicini
			(*pt_p)[k1].tass = malloc((*pt_p)[k1].nv * sizeof(double));	//anche per quella dei tassi
			(*pt_p)[k1].somm_parz_tass = malloc((*pt_p)[k1].nv * sizeof(double));	//anche per le somme parziali 
			for(j = 0; j < (*pt_p)[k1].nv; j++){ 	//tante volte quanto sono i vicini
				do{	//si cerca la successiva riga che non comincia con '#'
					if (fgets(riga, LMAX, grafo_p)==0){fprintf(stderr, "fget function failure \n");}
				} while(riga[0] == '#');
				sscanf(riga, "%*s %ld %*s %lE", &(((*pt_p)[k1].vic)[j]), &(((*pt_p)[k1].tass)[j]));	//si piglia vicino e tasso
			}
			(*pt_p)[k1].tt = 0;	//si parte da zero per il tasso totale per poi sommare tutti i tassi
			for(kk = 0; kk < (*pt_p)[k1].nv; kk++) (*pt_p)[k1].tt = ((*pt_p)[k1].somm_parz_tass)[kk] = (*pt_p)[k1].tt + ((*pt_p)[k1].tass)[kk];
			if ((*pt_p)[k1].tt > (*nn_p).ttm) (*nn_p).ttm = (*pt_p)[k1].tt;	//si paragona con il tasso totale massimale per eventualmente agiustarlo

		}
		fclose(grafo_p);	//e si chiude il file del grafo
	}
	else{	//caso del grafo torico
		k = 0;
		for (i = 0; i < l; i++){
			for (j = 0; j < L; j++){
				(*pt_p)[k].x = i;	//i e` l'ascissa del vertice k = i * l + j
				(*pt_p)[k].y = j;	//j la sua ordinata
				(*pt_p)[k].nv = 4;	//ogni vertice a 4 vertici
				(*nn_p).na += (*pt_p)[k].nv;
				(*pt_p)[k].vic = malloc(4 * sizeof(long int));
				((*pt_p)[k].vic)[0] = (k + L) % n;
				if (j == L - 1) ((*pt_p)[k].vic)[1] = k + 1 - L;
				else ((*pt_p)[k].vic)[1] = k + 1;
				((*pt_p)[k].vic)[2] = (k - L + n) % n;
				if (j == 0) ((*pt_p)[k].vic)[3] = k + L - 1;
				else ((*pt_p)[k].vic)[3] = k - 1;
				(*pt_p)[k].tass = malloc(4 * sizeof(double));
				(*pt_p)[k].somm_parz_tass = malloc(4 * sizeof(double));
				((*pt_p)[k].tass)[3] = (double)1;
				((*pt_p)[k].tass)[2] = (double)1;
				((*pt_p)[k].tass)[1] = (double)1;
				((*pt_p)[k].tass)[0] = (double)1;
				(*pt_p)[k].tt = 0;	//si parte da zero per il tasso totale per poi sommare tutti i tassi
				for(kk = 0; kk < (*pt_p)[k].nv; kk++) (*pt_p)[k].tt = ((*pt_p)[k].somm_parz_tass)[kk] = (*pt_p)[k].tt + ((*pt_p)[k].tass)[kk];
				if ((*pt_p)[k].tt > (*nn_p).ttm) (*nn_p).ttm = (*pt_p)[k].tt;	//si paragona con il tasso totale massimale per eventualmente agiustarlo
				k++;
			}
		}
	}

	if (!(*prm_p).X){
		(*prm_p).pausa = 0;		//non ci sono pause in modalita` non grafica
		(*prm_p).nome = NULL;	//non servira dare un nome ad una finestra
		(*prm_p).img_p = NULL; 	//non ci sara` nessun immagine da creare
		(*prm_p).foto = NULL; 	//non ci sara` nessuna foto da salvare
	}
		
	(*prm_p).scadenza = (double) CLOCKS_PER_SEC * ((double) 1 / (double) (*prm_p).immagini  - (*prm_p).pausa / (double) 1000);	//le pause fermano il conto dei tics
	(*prm_p).contatore = 0;	//ancora non si e` fatto vedere niente
	(*prm_p).ancora = 1;	//si vuole far girare il programma
	(*prm_p).raggiunto = 0;	//ancora non si e` provato a stampare niente

	if ((*prm_p).m) (*nn_p).q = (*nn_p).ttm;	//si parte con il tasso totale massimale per q se c'e` un numero bersaglio di radici

	(*nn_p).tmp_inv = (double) -1;
	(*nn_p).Z = (double) 0;

	return EXIT_SUCCESS;
}


int acquisizione(int argc, char* argv[], num* nn_p, param* prm_p){

	int i;	//per girare argv
	int ndefL = 1;	//ndef sta per 'non definito', si danno cosi` a priori per fissare opzioni per difetto
	int ndefl = 1;
	int ndefq = 1;
	int ndefa = 1;
	int ndefc = 1;
	int ndefnome = 1;

	(*nn_p).q = (double)1 / (double)(1 << 9);

	(*prm_p).L = (*prm_p).l = 1 << 9;
	(*prm_p).m = (double) 0;
	(*prm_p).e = (double) 2;
	(*prm_p).soloradici = 0;
	(*prm_p).bordo_si = 0;
	(*prm_p).immagini = 12;
	(*prm_p).fr = 0;
	(*prm_p).q_min = 0;
	(*prm_p).ved_att = 1;
	(*prm_p).scrivere = 1;
	(*prm_p).pausa = 1;
	(*prm_p).verboso = 0;
	(*prm_p).grandi_radici = 0;
	(*prm_p).da_file = 0;
	(*prm_p).potenziale = 0;
	(*prm_p).tasso_blu = 0;
	(*prm_p).blu_unif = 0;
	(*prm_p).z = (double) -1;
	(*prm_p).foto = NULL;
	(*prm_p).nb_foto = 8;
	(*prm_p).fdd = (double) 2;
	(*prm_p).X = 1;
	(*prm_p).stampa_foresta = 0;

	for (i = 1; i < argc; i++){
		if (argv[i][0] == '-'){
			switch(argv[i][1]){
				case 'l':
					sscanf(argv[++i], "%d", &((*prm_p).l));
					ndefl = 0;
					if (ndefL) (*prm_p).L = (*prm_p).l;
					break;
				case 'L':
					sscanf(argv[++i], "%d", &((*prm_p).L));
					ndefL = 0;
					if (ndefl) (*prm_p).l = (int) floor(2 * (*prm_p).L / (1 + sqrt(5)));
					break;
				case 'q':
					sscanf(argv[++i], "%lf", &((*nn_p).q));
					ndefq = 0;
					break;
				case 's':
					(*prm_p).scrivere = 0;
					break;
				case 'r':
					(*prm_p).soloradici = 1;
					break;
				case 'c':
					(*prm_p).bordo_si = 1;
					ndefc = 0;
					break;
				case 'i':
					sscanf(argv[++i], "%d", &((*prm_p).immagini));
					break; 
				case 'f':
					(*prm_p).fr = 1;
					(*prm_p).m = 0;
					if(ndefa) (*prm_p).ved_att = 0;
					if(ndefc) (*prm_p).bordo_si = 1;
					if(ndefq) (*nn_p).q = -1;
					break;
				case 'k':
					sscanf(argv[++i], "%lf", &((*prm_p).q_min));
					break;
				case 'a':
					(*prm_p).ved_att = 1;
					ndefa = 0;
					break;
				case 'b':
					(*prm_p).ved_att = 0;
					(*prm_p).bordo_si = 0;
					ndefa = 0;
					ndefc = 0;
					break;
				case 'p':
					sscanf(argv[++i], "%d", &((*prm_p).pausa));
					break;
				case 'v':
					(*prm_p).verboso = 1;
					if (ndefc) (*prm_p).bordo_si = 0;
					break;
				case 'm':
					sscanf(argv[++i], "%ld", &((*prm_p).m));
					(*prm_p).fr = 0;
					if(ndefc) (*prm_p).bordo_si = 0;
					if (ndefa) (*prm_p).ved_att = 0;
					break;
				case 'e':
					sscanf(argv[++i], "%lf", &((*prm_p).e));
					break;
				case 'g':
					(*prm_p).grandi_radici = 1;
					sscanf(argv[++i], "%d", &((*prm_p).grandi_radici));
					break;
				case 'w':
					(*prm_p).da_file = 1;
					(*prm_p).grafo = argv[++i];
					break;
				case 't':
					(*prm_p).tasso_blu = 1;
					break;
				case 'u':
					(*prm_p).blu_unif = 1;
					break;
				case 'z':
					sscanf(argv[++i], "%lf", &((*prm_p).z));
					(*prm_p).verboso = 1;	
					break;
				case 'V':
					(*prm_p).potenziale = 1;
					break;
				case 'o':
					(*prm_p).foto = argv[++i];
					if (!(*prm_p).X){
						//fprintf((*prm_p).outputErrorfile, "Non si possono prendere foto senza visualizzazione...\n");
						exit(EXIT_FAILURE);
					}
					break;
				case 'n':
					sscanf(argv[++i], "%d", &((*prm_p).nb_foto));
					break;
				case 'd':
					sscanf(argv[++i], "%lf", &((*prm_p).fdd));
					break;
				case 'y':
					(*prm_p).X = 0;
					(*prm_p).verboso = 1;
					(*prm_p).foto = NULL;
					break;
				case 'j':
					(*prm_p).stampa_foresta = 1;
					(*prm_p).verboso = 1;
					break;
				default:
					fprintf(stderr, "Uso: %s [-l larghezza] [-L lunghezza] [-q tasso_di_raffredamento] ", argv[0]);
					fprintf(stderr, "[-f] [-k q_minimale] [-m radici] [-e errore] [-r] [-c] [-a] [-b] [-V] [-t] [-u] [-g ingrandimento] [-v] [-s] [-j]");
					fprintf(stderr, "[-o nome_file.extensione] [-n numero_di_immagini_da_salvare] [-d fattore_di_decimazione] ");
					fprintf(stderr, "[-p pausa] [-i immagini_per_secondo] [-y]");
					fprintf(stderr, "[-w grafo] [-z fattore_di_multiplicazione_dei_tassi_tra_alberi_diversi] [nome]\n");
					fprintf(stderr, "-l : per specificare la larghezza verticale della finestra,\n");
					fprintf(stderr, "-L : per specificare la lunghezza orizontale della finestra,\n");
					fprintf(stderr, "-q : per specificare il tasso di raffredamento,\n");
					fprintf(stderr, "-f : per frammentare ed innestare col decrescere di q,\n");
					fprintf(stderr, "-k : per specificare il piu` piccolo tasso di raffredamento ");
					fprintf(stderr, "sotto il quale non si dovra` scendere lungo l'accoppiamento,\n");
					fprintf(stderr, "-m : per il numero m di radici che si vuole raggiungere,\n");
					fprintf(stderr, "-e : per l'errore ammesso in multipli della radice quadrata di m,\n");
					fprintf(stderr, "-r : per colorare negli alberi le radici soltanto (pigiando 'r' si puo` cambiare in corso di esecuzione),\n");
					fprintf(stderr, "-c : per imporre di mostrare i contorni degli alberi ");
					fprintf(stderr, "(pigiando 'c' si puo` cambiare in corso di esecuzione),\n");
					fprintf(stderr, "-a : per imporre di vedere gli alberi attivi (pigiando 'a' si puo` cambiare in corso di esecuzione),\n");
					fprintf(stderr, "-b : per imporre di non vedere contorni ne alberi attivi a meno della foresta seminale iniziale,\n");
					fprintf(stderr, "-V : per colorare i punti degli alberi freddi in funzione del potenziale d'equilibrio nel caso reversibile ");
					fprintf(stderr, "(pigiando 'V' si puo` cambiare in corso di esecuzione),\n");	
					fprintf(stderr, "-t : per colorare i punti degli alberi freddi in funzione del loro tasso di salto ");
					fprintf(stderr, "(pigiando 't' si puo` cambiare in corso di esecuzione),\n");	
					fprintf(stderr, "-u : per uniformizzare i colori,\n");
					fprintf(stderr, "-g : per ingrandire le radici 'ingrandimento' volte, ");
					fprintf(stderr, "con 'ingrandimento' un numero da 0 a 11 (pigiando 'g' si puo` cambiare in corso di esecuzione),\n");
					fprintf(stderr, "-v : per stampare le varie uscite nel terminale (sullo stdout),\n");
					fprintf(stderr, "-s : per non scrivere commenti nel terminale (via lo (*prm_p).outputErrorfile),\n");
					fprintf(stderr, "-j : per stampare la foresta,\n");
					fprintf(stderr, "-o : per dare il nome di un file in cui salvare l'immagine (pigiando 'o' si puo` anche fare una foto),\n");
					fprintf(stderr, "-n : numero di immagi da salvare ");
					fprintf(stderr, "(rilevante solanto con -f, i files saranno denominati 'nome_file_numero.q_valore.estensione'),\n");
					fprintf(stderr, "-d : per specificare la quantita` per la quale dividere q tra due immagini salvate successivi,\n");
					fprintf(stderr, "-p : per aspettare 'pausa' millisecondi dopo ciascun immagine (pigiando '+' o '_'");
					fprintf(stderr, " si puo` aumentare o abbassare in corso di esecuzione),\n");
					fprintf(stderr, "-i : per specificare il numero di immagini al secondo (pigiando '=' o '-' si puo` aumentare ");
					fprintf(stderr, "o abbassare in corso di esecuzione),\n") ;
					fprintf(stderr, "-y : per una versione senza immagini del programma,\n");
					fprintf(stderr, "-w : per specificare un file da cui leggere il grafo,\n");
					fprintf(stderr, "-z : per specificare un fattore di multiplicazione dei tassi tra vertici di alberi disitinti nel costruire ");
					fprintf(stderr, "un altro grafo,\n");
					fprintf(stderr, "nome : per battezzare la finestra.\n");
					exit(EXIT_FAILURE);
			}
		} 
		else{
			if (ndefnome) (*prm_p).nome = argv[i];
			ndefnome = 0;	
		}
	}
	if (ndefnome) (*prm_p).nome = "Foresta";
	if ((*prm_p).da_file == 0) (*prm_p).grafo = NULL;

	return EXIT_SUCCESS;
}


int grezza_acquisizione(int argc, char* argv[], num* nn_p, param* prm_p){
	int i;	//per girare argv
	int ndefL = 1;	//ndef sta per 'non definito', si danno cosi` a priori per fissare opzioni per difetto
	int ndefl = 1;
	int ndefq = 1;
	(*nn_p).q = (double)1 / (double)(1 << 9);

	(*prm_p).L = (*prm_p).l = 1 << 9;
	(*prm_p).m = (double) 0;
	(*prm_p).e = (double) 2;
	(*prm_p).immagini = 12;	//ha senso per il ritmo dei commenti da dare via lo (*prm_p).outputErrorfile
	(*prm_p).fr = 0;
	(*prm_p).q_min = 0;
	(*prm_p).scrivere = 0;
	(*prm_p).pausa = 0;
	(*prm_p).verboso = 1;
	(*prm_p).da_file = 0;
	(*prm_p).z = (double) -1;
	(*prm_p).X = 0;
	(*prm_p).stampa_foresta = 0;
  (*prm_p).flag_outputfile = 0;
  (*prm_p).outputfilename = OUTPUTFILE;
  (*prm_p).flag_outputErrorfile = 0;
  (*prm_p).outputErrorfilename = OUTPUTERRORFILE;
	for (i = 0; i < argc; i++){
		if (argv[i][0] == '-'){
		switch(argv[i][1]){
		   case 'l':
			   (*prm_p).l = atoi(argv[++i]);
			   ndefl = 0;
			   if (ndefL) (*prm_p).L = (*prm_p).l;
			   break;
		   case 'L':
			   (*prm_p).L =  atoi(argv[++i]);
		   case 'q':
			   (*nn_p).q = atof(argv[++i]);
			   ndefq = 0;
			   break;
			case 's':
				(*prm_p).scrivere = 1;
				break;
			case 'f':
				(*prm_p).fr = 1;
			    (*prm_p).m = 0;
			    if(ndefq) (*nn_p).q = -1;
			    break;
			case 'k':
				(*prm_p).q_min = atof(argv[++i]);
				break;
            case 'm':
            	(*prm_p).m = atoi(argv[++i]);
            	(*prm_p).fr = 0;
            	break;
			case 'e':
				(*prm_p).e = atof(argv[++i]);
				break;
			case 'w':
				(*prm_p).da_file = 1;
				(*prm_p).grafo = argv[++i];
				break;
			case 'z':
				(*prm_p).z = atof(argv[++i]);
				(*prm_p).verboso = 1;
				break;
			case 'j':
				(*prm_p).stampa_foresta = 1;
				(*prm_p).verboso = 1;
				break;
		}
		} 
    else if (argv[i][0] == '>'){
       (*prm_p).flag_outputfile = 1;
       (*prm_p).outputfilename = argv[++i];
       (*prm_p).scrivere = 1;
    }   
    else if (argv[i][0] == '2' && argv[i][1] == '>' ){ 
      (*prm_p).flag_outputErrorfile = 1;
      (*prm_p).outputErrorfilename = argv[++i];   
      }
    }
	if ((*prm_p).da_file == 0) (*prm_p).grafo = NULL;

	return EXIT_SUCCESS;
}


int dare_qualche_informazione(num* nn_p, param* prm_p){ //scrive qualche commento via lo stderr sullo stato del sistema

	(*prm_p).contatore++;
	if ((*prm_p).contatore >= (*prm_p).immagini){	//si da qualche informazione sul stderr ogni secondo circa
		(*prm_p).contatore = 0;
		//dare_informazioni(nn_p, prm_p);
	}
	
	return EXIT_SUCCESS;
}


int dare_informazioni(num* nn_p, param* prm_p){ //scrive qualche commento via lo stderr sullo stato del sistema

	if((*prm_p).scrivere){;
	//	fflush((*prm_p).outputfile);
	//	fprintf((*prm_p).outputErrorfile, "   Radici fredde: %ld, attive: %ld, q: %.3e. ", (*nn_p).f, (*nn_p).a, (*nn_p).q);
	//	fprintf((*prm_p).outputErrorfile, "Tempo di Wilson * q: %g.     \r", (*nn_p).q * tempo_di_wilson(nn_p));
	//	fflush((*prm_p).outputErrorfile);
	}
	
	return EXIT_SUCCESS;
}
