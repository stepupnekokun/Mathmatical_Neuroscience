#include <stdio.h>
#include <stdlib.h> 
#include <math.h> 
#include <unistd.h>

#define IN_SIGNAL 1
#define SIGMA 5.0
#define NEURON 30
#define N_LEARNING 1000

FILE *gp;

double x[IN_SIGNAL];
double m[NEURON][IN_SIGNAL];


void init_ref_vec(){
    int i,j;
    for(i=0; i<NEURON; i++){
        for(j=0; j<IN_SIGNAL; j++){
        m[i][j] = (rand()+0.5 )/(RAND_MAX+1 );
        }
    }
}

void generate_a_input(){
    int i;
    for(i=0; i<IN_SIGNAL; i++){
        x[i] = (rand()+0.5 )/(RAND_MAX+1 );
    }
}

//入力値と参照ベクトルとのベクトルの距離が最小値ニューロンのインデックスを取ってくる
int winner_takes_all(){
    int i,j;
    int c = 0;
    double d = 0.0, dmin;

    for(j=0; j<IN_SIGNAL; j++){
    d += (x[j] - m[0][j])*(x[j] - m[0][j]);
    }
    dmin = d;

    for(i=1; i<NEURON; i++){
        d = 0.0;
        for(j=0; j<IN_SIGNAL; j++){
            d += (x[j] - m[i][j])*(x[j] - m[i][j]);
        }
        if ( d < dmin ){
            dmin = d;
            c = i; 
        }
    }
    return c;
}

//learning dynamics
//すべての参照ベクトルを更新
//近傍学習
void learning(int c){

  int i,j;
  double h;
  double alpha = 0.01;

  for(i=0; i<NEURON; i++){
      h = -(c-i)*(c-i)/(2.0*SIGMA*SIGMA);
      h = exp(h);
      for(j=0; j<IN_SIGNAL; j++){
          m[i][j] = m[i][j] + alpha*(x[j]-m[i][j])*h;
      }
  }

}


int main (int argc, char *argv[] ){

    int i,j,x;
    int c;

    srand(123);
    gp = popen("gnuplot -persist","w");
    // fprintf(gp, "set terminal gif animate optimize delay 10 size 400,400\n");
    // fprintf(gp, "set output '1demention_s%lf.gif'\n",SIGMA);
    fprintf(gp, "set style data linespoints\n");//線ができる
    fprintf(gp, "set xlabel \"neural fields\"\n");
    fprintf(gp,"set xrange[0:1]\n");
    fprintf(gp, "set yrange[0:1]\n");
    fprintf(gp, "set border 5\n"); 
    fprintf(gp, "set x2tics 0,0.2,1\n");
    fprintf(gp, "set noxtics\n");
    fprintf(gp, "set noytics\n");
    fprintf(gp, "set nokey\n");
    fflush(gp);

    init_ref_vec();
    for(i=0; i<N_LEARNING; i++){
        generate_a_input();
        c = winner_takes_all();
        fprintf(gp, "set title 't = %d sigma =%lf neuron = %d'\n",i+1,SIGMA,NEURON);
        fprintf(gp, "plot '-'\n");
        for(j=0; j<NEURON; j++){
            for(x=0; x<IN_SIGNAL; x++){
                fprintf(gp, "%lf\t%lf\n",m[j][x],0.99);
                fprintf(gp, "%lf\t%lf\n", (double)j/(double)NEURON+0.01,0.01);
                fprintf(gp,"\n"); 
            }                                
        }
        fprintf(gp, "e\n");
        fflush(gp);
        // usleep(1000); 
        learning(c);
    }  
    pclose(gp);
    return 0;

}
