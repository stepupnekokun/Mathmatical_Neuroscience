#include <stdio.h>
#include <stdlib.h> 
#include <math.h> 
#include <unistd.h>

#define IN_SIGNAL 2
#define NEURON_X 10
#define NEURON_Y 10
#define NEURON_LEARN 150
#define SUB_NEURON_LEARN 100

FILE *gp;

double x[IN_SIGNAL];
double m[NEURON_X][NEURON_Y][IN_SIGNAL];
double SIGMA = 0.8;
double ALPHA = 0.2;

void init_ref_vec();
void generate_a_input();
void winner_takes_all();

int main (int argc, char *argv[] ){

    int i,j,k;
    int c;
    double m1;

    srand(123);
    gp = popen("gnuplot -persist","w");
    // fprintf(gp, "set terminal gif animate optimize delay 10 size 400,400\n");
    // fprintf(gp, "set output 'triangle_s%lf_a%lf.gif'\n",SIGMA,ALPHA);
    fprintf(gp, "set size ratio 1\n");
    fprintf(gp, "set style data linespoints\n");//線ができる
    fprintf(gp, "set xlabel \"Neural Fields\"\n");
    fprintf(gp,"set xrange[0:1]\n");
    fprintf(gp, "set yrange[0:1]\n");
    fprintf(gp, "set border 5\n");
    fflush(gp);

    init_ref_vec();
    for(i=0; i<1; i++){
        
        fprintf(gp, "set title 't = %d/%d sigma =%lf alpha = %lf'\n",i*SUB_NEURON_LEARN+100, NEURON_LEARN*SUB_NEURON_LEARN,SIGMA,ALPHA);
        fprintf(gp, "plot '-' linestyle 5\n");
        fflush(gp);

        //書き込み回数を減らし、処理を軽くする
        for(c=0; c<SUB_NEURON_LEARN; c++){
            generate_a_input();
            winner_takes_all();
        }

        for(j=0; j<NEURON_X; j++){
            for(k=0; k<NEURON_Y; k++){
                fprintf(gp, "%lf\t%lf\n",m[j][k][0],m[j][k][1]);
            }
            fprintf(gp,"\n");                                
        }
        for(k=0; k<NEURON_X; k++){
            for(j=0; j<NEURON_Y; j++){
                fprintf(gp, "%lf\t%lf\n",m[j][k][0],m[j][k][1]);

            }
            fprintf(gp,"\n");                                
        }
        
        fprintf(gp, "e\n");               
        fflush(gp);
        usleep(100000); 
    }
    
    pclose(gp);
    return 0;

}

void init_ref_vec(){
    int i,j,k;
    double m1;

    for(i=0; i<NEURON_X; i++){
        for(j=0; j<NEURON_Y; j++){
            for(k=0; k<IN_SIGNAL; k++){
                m[i][j][k] = (rand()+0.5 )/(RAND_MAX+1 );
            }
            if(m[i][j][0]<=0.5){
                m1=2*m[i][j][0];
            }else{
                m1=-2*m[i][j][0]+2;
            }
            if(m[i][j][1]>m1){
                j -= 1;
            }
        }
    }
  
}

void generate_a_input(){
    int i;
    double m1;

    for(i=0; i<IN_SIGNAL; i++){
        x[i] = (rand()+0.5 )/(RAND_MAX+1 );
    }
    if(x[0]<=0.5){
        m1=2*x[0];
    }else{
        m1=-2*x[0]+2;
    }
    if(x[1]>m1){
        generate_a_input();
    }
}

//入力値と参照ベクトルとのベクトルの距離が最小値ニューロンのインデックスを取ってくる
void winner_takes_all(){
    int i,j,k;
    int minx = 0,miny = 0;
    double d = 0.0, dmin;
    int norm;
    double h;
    double m1;

    for(k=0; k<IN_SIGNAL; k++){
    d += (x[k] - m[0][0][k])*(x[k] - m[0][0][k]);
    }
    dmin = d;

    for(i=1; i<NEURON_X; i++){
        for(j=0; j<NEURON_Y; j++){
            d = 0.0;
            for(k=0; k<IN_SIGNAL; k++){
                d += (x[k] - m[i][j][k])*(x[k] - m[i][j][k]);
            }
            if ( d < dmin ){
            dmin = d;
            minx = i;
            miny = j; 
            }
        }
        
    }
    
    for(i=0; i<NEURON_X; i++){
      for (j=0; j<NEURON_Y; j++){
            norm = (minx-i)*(minx-i)+(miny-j)*(miny-j);
            h = -((double)norm)/(2.0*SIGMA*SIGMA);
            h = exp(h);  
            for(k=0; k<IN_SIGNAL; k++){
                m[i][j][k] = m[i][j][k] + ALPHA*(x[k]-m[i][j][k])*h;
            }
            
        }
    }
}
