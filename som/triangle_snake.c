// init_refが永遠と-1をし続ける
#include <stdio.h>
#include <stdlib.h> 
#include <math.h> 
#include <unistd.h>
#include <time.h>

#define IN_SIGNAL 2
#define NEURON 64
#define NEURON_LEARN 250
#define SUB_NEURON_LEARN 100

FILE *gp;

double x[IN_SIGNAL];
double m[NEURON][IN_SIGNAL];
double SIGMA = 0.8;
double ALPHA = 0.2;

void init_ref_vec();
void generate_a_input();
void winner_takes_all();

int main (int argc, char *argv[] ){

    int i,j,k;
    int c;
    double m1;

    srand((unsigned)time(NULL));
    gp = popen("gnuplot ","w");
    // fprintf(gp, "set terminal gif animate optimize delay 10 size 400,400\n");
    // fprintf(gp, "set output 'triangle_s%lf_a%lf.gif'\n",SIGMA,ALPHA);
    fprintf(gp, "set size ratio 1\n");
    fprintf(gp, "set style data linespoints\n");//線ができる
    fprintf(gp, "set xlabel \"Neural Fields\"\n");
    fprintf(gp,"set xrange[-1:1]\n");
    fprintf(gp, "set yrange[-1:1]\n");
    fprintf(gp, "set border 5\n");
    fflush(gp);

    
    init_ref_vec();
    
    for(i=0; i<NEURON_LEARN; i++){
        fprintf(gp, "set title 't = %d/%d sigma =%lf alpha = %lf'\n",i*SUB_NEURON_LEARN+100, NEURON_LEARN*SUB_NEURON_LEARN,SIGMA,ALPHA);
        fprintf(gp, "plot '-' linestyle 5 pointsize 2 linewidth 2\n");
        fprintf(gp,"%d\t%d\n",-1,-1);
        fprintf(gp,"%d\t%d\n",0,1);
        fprintf(gp,"%d\t%d\n",1,-1);
        fprintf(gp,"\n");
        fflush(gp);

        //書き込み回数を減らし、処理を軽くする
        for(c=0; c<SUB_NEURON_LEARN; c++){
            generate_a_input();
            winner_takes_all();
        }

        
        for(j=0; j<NEURON; j++){
            fprintf(gp, "%lf\t%lf\n",m[j][0],m[j][1]);
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

    for(i=0; i<NEURON; i++){
        for(j=0;j<IN_SIGNAL;j++){
            // m[i][j] = (double)(rand()-(RAND_MAX/2))/(RAND_MAX/2)*0.01;
            m[i][j] = (double)(rand()-RAND_MAX)/RAND_MAX*0.01;

        }
        if(m[i][0]<=0){
            m1=2*m[i][0]+1;
        }else{
            m1=-2*m[i][0]+1;
        }
        if(-1>m[i][1] || m[i][1]>m1){
            i -= 1;
        }
    }
  
}

// 入力を三角形上の座標をとるように設定した
void generate_a_input(){
    int i;
    double m1;

    for(i=0; i<IN_SIGNAL; i++){
        x[i] = (double)(rand()-(RAND_MAX/2))/(RAND_MAX/2);
        // x[i] = (double)(rand()-RAND_MAX)/RAND_MAX;
    }
    // x[1] = (double)(rand()-(RAND_MAX/2))/(RAND_MAX/2);
    // if(rand()-(RAND_MAX/2)>0.5){
    //     x[0]=(x[1]-1)/2;
    // }else{
    //     x[0]=(-x[1]+1)/2;
    // }
    if(x[0]<=0){
        m1=2*x[0]+1;
    }else{
        m1=-2*x[0]+1;
    }
    if(-1>x[1] || x[1]>m1){
        generate_a_input();
    }
    if(x[1]!=-1){
        x[1]=m1;
    }
    
}

//入力値と参照ベクトルとのベクトルの距離が最小値ニューロンのインデックスを取ってくる
void winner_takes_all(){
    int i,j;
    int min = 0;
    double d = 0.0, dmin;
    int norm;
    double h;
    double m1;

    for(i=0; i<IN_SIGNAL; i++){
    d += (x[i] - m[0][i])*(x[i] - m[0][i]);
    }
    dmin = d;

    for(i=1; i<NEURON; i++){
        for(j=0; j<IN_SIGNAL; j++){
            d = 0.0;
            d += (x[j] - m[i][j])*(x[j] - m[i][j]);
            if ( d < dmin ){
            dmin = d;
            min = i;
            }
        }
    }


    for(i=0; i<NEURON; i++){ 
        norm = (min-i)*(min-i);
        h = -((double)norm)/(2.0*SIGMA*SIGMA);
        h = exp(h);
        // for(j=0; j<IN_SIGNAL; j++){
        //     m[i][j] = m[i][j] + ALPHA*(x[j]-m[i][j])*h;
        // }
        m[i][0] = m[i][0] + ALPHA*(x[0]-m[i][0])*h;
        m[i][1] = m[i][1] + ALPHA*(x[1]-m[i][1])*h;
    }


}
