#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include "cuore.h"
#include "lodge.h"


//int rforest_cfunc(int argcSuite, char** argvSuite, double* out, int* pt_size1, int* pt_size2)
int rforest_internal(num* nn_p, punto** pt_p,param* prm_p, double** pt_out, int* pt_size1, int* pt_size2 )
{
  long int j, k;	//vertici generici
  double nuova_partenza; 	//segna il numero di tics prima di mostrare un immagine : serve per sapere quando l'immagine succesiva deve essere mostrata
  double unif_alla_uno_su_num_rad_fredde;	//v. a. con quella distr., utilizzata lungo il proc. di coal. e framm. col decresc. di q
  int inputparam = 0;
  int ind, i, ii;
  long int index_f = 0;
  int index_realloc = 0;
  char* a;
  double* output1d = NULL;  // output 1D
  double** output2d = NULL;  // output 2D
  //punto * pt ;
  //param prm;
  //num nn;
  char* option;
  double* out;
  int dimension1, dimension2;
  dimension1 = 0;
  dimension2 = 0;
  // (*prm_p).outputfilename = OUTPUTFILE;
  // (*prm_p).outputErrorfilename = OUTPUTERRORFILE;
  // (*prm_p).outputErrorfile = fopen((*prm_p).outputErrorfilename, "w");
  // if ((*prm_p).outputErrorfile == NULL) {
  //  fprintf(stderr, "errror in the output error file...\n");
 //		exit(EXIT_FAILURE);
  // }
  //(*prm_p).scrivere = 0;
  //pt = *pt_p;
  //nn = *nn_p;
  //prm = *prm_p;
  // grezza_acquisizione(argcSuite+inputparam, entry, &nn, prm_p);
  // inizializzazione_basica(&nn, &pt, prm_p);
  tutti_svegli_tempo_zero(nn_p, pt_p);
  nuova_partenza = (double) clock();

    // cas f
  if ((*prm_p).fr) {

    option = "f";
    init_output((*nn_p).n, &output2d, &output1d, option, 0);
    }
  // cas m
  else if ((*prm_p).m) {

    if((*prm_p).stampa_foresta){
      option = "j";
      init_output((*nn_p).n, &output2d, &output1d, option, 0);
      }
    else {

      option = "m";
      init_output((*nn_p).n, &output2d, &output1d, option, 0);
      }
    }
  // cas q
  else if (!((*prm_p).fr) && !((*prm_p).m)){
    if((*prm_p).stampa_foresta){

      option = "j";
      init_output((*nn_p).n, &output2d,&output1d,option, 0);
      }
    else {

      option = "q";
      init_output((*nn_p).n, &output2d,&output1d,option, 0);
      }
  }
  else {

      option = "q";
      init_output((*nn_p).n, &output2d,&output1d,option, 0);
    }
	while((*prm_p).ancora){	//si gira il programma finche' arrivi l'ordine di uscire "(*prm_p).ancora = 0"
	//	fprintf(stderr," q value %e ",(*nn_p).q);
	//	fprintf(stderr," a value %d ",(*nn_p).a);

		if((*nn_p).q < 0) congelare_tutto(nn_p, pt_p);	//q < 0 sta per q infinito
		if((*nn_p).a > 0){	//se c'e` una radice attiva si sposta una radice aleatoria k in un suo vicino j (possibilmente il cimetero)
			k = radice_attiva_aleatoria(nn_p);
			j = vicino_aleatorio(k, nn_p, *pt_p);
			if(j < 0){
				congelare(k, nn_p, pt_p);
			}
			else{
				if(radice(j, pt_p) != k) coalescenza(k, j, nn_p, pt_p);
				else if(j != k) frammentazione(k, j, nn_p, pt_p);
			}
		}
		else{	//se tutt'e` freddo prima si controlla se non si stava aspettando una nuova immagine mostrabile poi si agisce al variare delle opzioni
			if((*prm_p).fr){//fprintf(stderr,"fr ");	//caso di frammentazzioni e ricomposizioni
				unif_alla_uno_su_num_rad_fredde = exp(log(drand48()) / (*nn_p).f);
				if ((*nn_p).q >= 0) {		//q infinito va trattato a parte
					if (((*prm_p).verboso) && !((*prm_p).raggiunto)){	//si stampano eventualmente q, il numero delle radici e il tempo di Wilson
						double cal = (*nn_p).q * tempo_di_wilson(nn_p);
           // if((*prm_p).scrivere){
             //   fprintf((*prm_p).outputfile,"q %8e  m %9ld  q*tw %8e", (*nn_p).q, (*nn_p).f, cal);
				//		    fprintf((*prm_p).outputfile,"                                                     \n");
            //}
            // case f increase memory if > n * index_realloc
            if (index_f >= (*nn_p).n * (index_realloc+1)) {
              index_realloc ++;
              init_output((*nn_p).n, &output2d, &output1d,"r", index_realloc);
              }
          //  fprintf(stderr,"ecriture output2 %e ", (*nn_p).q);
          //  fprintf(stderr,"ecriture output2 %d ", (*nn_p).f);
            output2d[index_f][0] = (*nn_p).q;
            output2d[index_f][1] = (*nn_p).f;
            output2d[index_f][2] = cal;
            index_f++;
					}	//e si fa decrescere q :
					(*nn_p).q = (*nn_p).q * (*nn_p).ttm * unif_alla_uno_su_num_rad_fredde / ((*nn_p).ttm + (*nn_p).q * ((double) 1 - unif_alla_uno_su_num_rad_fredde));
				}
				else (*nn_p).q = (*nn_p).ttm * unif_alla_uno_su_num_rad_fredde / ((double) 1 - unif_alla_uno_su_num_rad_fredde);
				if ((*nn_p).q < (*prm_p).q_min) { //se il prossimo salto sta al di la` del q minimo non c'è niente da muovere e si deve porre q = q_min
					(*nn_p).q = (*prm_p).q_min;
					(*prm_p).raggiunto = 1;      //non ci sara` piu` niente da stampare
					(*prm_p).ancora = 0;}  		//ci si puo` andare
				else {  //prima del q minimo c'e` qualcuno da svegliare
					k = radice_fredda_aleatoria(nn_p);	//si sceglie una radice k per svegliarla e spostarla
					svegliare(k, nn_p, pt_p);
					j = vicino_aleatorio_senza_uccisione(k, nn_p, *pt_p);
					if(radice(j, pt_p) != k) coalescenza(k, j, nn_p, pt_p);
					else if(j != k) frammentazione(k, j, nn_p, pt_p);}
			}
			if((*prm_p).m){	//caso di un numero bersaglio di radici
				if (((*prm_p).scrivere) && !((*prm_p).raggiunto)){	//se ancora non abbiamo stampato le radici ottenute (col numero giusto), si informa su q, m e il tempo
				//	fprintf((*prm_p).outputErrorfile,"q %8e  m %9ld  q*tw %8e", (*nn_p).q, (*nn_p).f, (*nn_p).q * tempo_di_wilson(nn_p));
				//	fprintf((*prm_p).outputErrorfile, "                                                     \n");
				;}
				if (((*nn_p).f < (*prm_p).m - (*prm_p).e * sqrt((*prm_p).m)) || ((*nn_p).f) > (*prm_p).m + (*prm_p).e * sqrt((*prm_p).m)){	//se m non sta nella finestra giusta
					(*nn_p).q *= (*prm_p).m / (double) (*nn_p).f;	//si prende un nuovo q e si ricommincia da capo
					tutti_svegli_tempo_zero(nn_p, pt_p);
				}
				else{	//se m sta nella finestra giusta
					if (((*prm_p).verboso) && !((*prm_p).raggiunto)){	//si stampa se non e` gia` stato fatto
						if ((*prm_p).z < 0) {
							if ((*prm_p).stampa_foresta) {
                stampare_foresta(nn_p, pt_p, prm_p, &output2d);	 //si stampa la foresta
                // case mj
                }
							else {
                // case m
                stampare_radici(nn_p, pt_p, prm_p, &output1d);	//o le radici
              }
						}
						else {
              // case z do not
              scrivere_un_altro_grafo(nn_p, pt_p, prm_p);	//o un altro grafo (m +z)
              }
					}
					(*prm_p).raggiunto = 1;	//comunque a quel punto l'obbiettivo e` stato raggiunto
					dare_informazioni(nn_p, prm_p);
					(*prm_p).ancora = 0;	//in modalita` non grafica è tutto finito
				}
			}
      // fin du cas m
			if (!((*prm_p).fr) && !((*prm_p).m) && !((*prm_p).raggiunto)){ 	//nel caso standard (q dato) c'e` da fare qualcosa solo se l'obbiettivo ancora non e` stato raggiunto
				if  ((*prm_p).verboso){	//forse c'e` da dare la foresta, le radici oppure un'altro grafo
					if ((*prm_p).z < 0) {
						if ((*prm_p).stampa_foresta) {
              stampare_foresta(nn_p, pt_p, prm_p,  &output2d);
              //cas q option j
              }
						else {
              stampare_radici(nn_p, pt_p, prm_p, &output1d);
              //cas q

            }
					}
					else scrivere_un_altro_grafo(nn_p, pt_p, prm_p); // cas z à supprimer (q +z)
				}
				(*prm_p).raggiunto = 1;	//e a quel punto si e` finito
				dare_informazioni(nn_p, prm_p);
				(*prm_p).ancora = 0;	//in modalita` non grafica ci si puo` anche andare..
			}
		}
		if ((double) clock() - nuova_partenza > (*prm_p).scadenza){	//magari c'e` una nuova immagine da mostrare o informazioni da dare
			nuova_partenza = (double) clock();
			dare_qualche_informazione(nn_p, prm_p);
		}
	}

  determine_dimension((*nn_p).n, index_realloc, &output2d, &output1d, &dimension1, &dimension2, option);

  out =  (double *)malloc(sizeof(double)*dimension2*dimension1);
  *pt_size1 = dimension1;
  *pt_size2 = dimension2;
  *pt_out = out;
  if ((out) == NULL){
      fprintf(stderr, "trouble in realloc memory");
      exit(EXIT_FAILURE);
      }


  for (i = 0; i < dimension1; i++){
        for (ii = 0; ii < dimension2; ii++){
           if (strcmp(option, "j") == 0|| strcmp(option, "z") == 0|| strcmp(option, "f") == 0){// cas j mj ou qj
                   out[ii+dimension2*i] =  output2d[i][ii];}
            else if (strcmp(option, "m") == 0 || strcmp(option, "q") == 0){
                   out[ii+dimension2*i] =  output1d[i];}
        }
  }
 // if ((*prm_p).scrivere) pulire_terminale( prm_p);

  free_output((*nn_p).n, &output2d, &output1d, option, index_realloc);

 // fclose((*prm_p).outputErrorfile);

//  if((*prm_p).scrivere){

//      fclose((*prm_p).outputfile);

//  }
 // fprintf(stderr, "apres fermeture rforst");
  //liberare_memoria(nn_p, &pt, prm_p);
  return EXIT_SUCCESS;
}
