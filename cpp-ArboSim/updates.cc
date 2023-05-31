#include "updates.h"
#include<cmath>
#include<fstream>
#include<iostream>
#include<random>
using std::vector;

void dif(double t, vector<double>& y0,vector<double>& dy,vector<double>& yf0,vector<double>& dyf)
{
        // std::cout<<"I am in here in updates.cc and in time loop\t"<<y0.size()<<"\n"<<std::endl;

  int j,i,k,l,Nm; 
  int Nodes=GLOBAL.Nodes;
  int sM=GLOBAL.sM,sid=GLOBAL.sid;
//====================================================Host natural history===========================================================//

//------------Primary Susceptibles----------//

for(i=1;i<=Nodes;i++)
   {
  GLOBAL.lamM1=0;GLOBAL.lamH1=0;
   for(j=1;j<=Nodes;j++)
      {
       GLOBAL.NH=y0[3*Nodes+j]+y0[4*Nodes+j]+y0[5*Nodes+j]+y0[6*Nodes+j];
       GLOBAL.lamM1+=GLOBAL.b*GLOBAL.bet1*GLOBAL.adjMatrixB[i][j]*y0[5*Nodes+j]*y0[i]/GLOBAL.NH;
       GLOBAL.lamH1+=GLOBAL.b*GLOBAL.bet2*GLOBAL.adjMatrixA[i][j]*y0[j+2*Nodes]*y0[3*Nodes+i]/GLOBAL.NH;
 // GLOBAL.lamM1=GLOBAL.bet1*GLOBAL.b*y0[5*Nodes+j]*y0[i]/GLOBAL.NH;
   //    GLOBAL.lamH1=GLOBAL.bet2*GLOBAL.b*y0[j+2*Nodes]*y0[3*Nodes+i]/GLOBAL.NH;
      }
Nm=y0[i]+y0[Nodes+i]+y0[2*Nodes+i];
GLOBAL.NH=y0[3*Nodes+i]+y0[4*Nodes+i]+y0[5*Nodes+i]+y0[6*Nodes+i];

     dy[i]=GLOBAL.PIM[i]-GLOBAL.lamM1-GLOBAL.muM[i]*y0[i];//Susceptible Mostquitoes
     dy[Nodes+i]=GLOBAL.lamM1-(GLOBAL.sigM+GLOBAL.muM[i])*y0[Nodes+i];//Exposed Mosquitoes
     dy[2*Nodes+i]=GLOBAL.sigM*y0[Nodes+i]-GLOBAL.muM[i]*y0[2*Nodes+i];//Infectious Mosquitoes

     dy[3*Nodes+i]=GLOBAL.PIH[i]-GLOBAL.lamH1-GLOBAL.muH*y0[3*Nodes+i];//Susceptible Humans
     dy[4*Nodes+i]=GLOBAL.lamH1-(GLOBAL.sigH+GLOBAL.muH)*y0[4*Nodes+i];//Exposed Humans
     dy[5*Nodes+i]=GLOBAL.sigH*y0[4*Nodes+i]-(GLOBAL.gam+GLOBAL.muH)*y0[5*Nodes+i];//Infectious Humans
     dy[6*Nodes+i]=GLOBAL.gam*y0[5*Nodes+i]-GLOBAL.muH*y0[6*Nodes+i];//Recovered Humans
   }





// for(i=1;i<=sM;i++)
// {l=i*sid;
//      dyf[l+1]=0;//x1
//     dyf[l+2]= 0;
 
// }




}

// void rk4(double t, vector<double>& y0, vector<double>& yf0, vector<double>& dy0, vector<double>& dyf0, double h, vector<double>& y1, vector<double>& yf1, void dif(double, vector<double>&, vector<double>&, vector<double>&, vector<double>&)) {
//     int n = GLOBAL.N;//y0.size();
//     int n1 = GLOBAL.sN;//yf0.size();
//     double h2 = h / 2.0;
//     vector<double> wk1(n+1, 0.0);
//     vector<double> wk2(n+1, 0.0);
//     vector<double> wkf1(n1+1, 0.0);
//     vector<double> wkf2(n1+1, 0.0);

//     for(int i = 1; i <= n; ++i) {
//         y1[i] = h2 * dy0[i];
//         wk1[i] = y0[i] + y1[i];
//     }

//     for(int i = 1; i <= n1; ++i) {
//         yf1[i] = h2 * dyf0[i];
//         wkf1[i] = yf0[i] + yf1[i];
//     }

//     double t1 = t + h2;
//     dif(t1, wk1, wk2, wkf1, wkf2);

//     for(int i = 1; i <= n; ++i) {
//         y1[i] = y1[i] + h * wk2[i];
//         wk1[i] = y0[i] + h2 * wk2[i];
//     }

//     for(int i = 1; i <= n1; ++i) {
//         yf1[i] = yf1[i] + h * wkf2[i];
//         wkf1[i] = yf0[i] + h2 * wkf2[i];
//     }

//     dif(t1, wk1, wk2, wkf1, wkf2);

//     for(int i = 1; i <= n; ++i) {
//         y1[i] = y1[i] + h * wk2[i];
//         wk1[i] = y0[i] + h * wk2[i];
//     }

//     for(int i = 1; i <= n1; ++i) {
//         yf1[i] = yf1[i] + h * wkf2[i];
//         wkf1[i] = yf0[i] + h * wkf2[i];
//     }

//     t1 = t + h;
//     dif(t1, wk1, wk2, wkf1, wkf2);

//     for(int i = 1; i <= n; ++i) {
//         y1[i] = y0[i] + (y1[i] + h2 * wk2[i]) / 3.0;
//     }

//     for(int i = 1; i <= n1; ++i) {
//         yf1[i] = yf0[i] + (yf1[i] + h2 * wkf2[i]) / 3.0;
//     }

//      return;
// }

void rk4(double t, vector<double>& y0, vector<double>& yf0, vector<double>& dy0, vector<double>& dyf0, double h, vector<double>& y1, vector<double>& yf1, void dif(double, vector<double>&, vector<double>&, vector<double>&, vector<double>&)) {
    int n = GLOBAL.N;
    int n1 = GLOBAL.sN;
    double h2 = h/2.0;
    // vector<double> wk1(n+1), wk2(n+1), wkf1(n1+1), wkf2(n1+1);
        vector<double> wk1, wk2, wkf1, wkf2;
        wk1.reserve(n+1);
        wk2.reserve(n+1);
        wkf1.reserve(n1+1);
        wkf2.reserve(n1+1);

    wk1.clear();
    wk2.clear();
    wkf1.clear();
    wkf2.clear();
    for (int i=1; i<=n; i++) {
        y1[i] = h2 * dy0[i];
        wk1[i] = y0[i] + y1[i];
    }
    
    for (int i=1; i<=n1; i++) {
        yf1[i] = h2 * dyf0[i];
        wkf1[i] = yf0[i] + yf1[i];
    }
    
    double t1 = t + h2;
    dif(t1, wk1, wk2, wkf1, wkf2);
    
    for (int i=1; i<=n; i++) {
        y1[i] = y1[i] + h * wk2[i];
        wk1[i] = y0[i] + h2 * wk2[i];
    }
    
    for (int i=1; i<=n1; i++) {
        yf1[i] = yf1[i] + h * wkf2[i];
        wkf1[i] = yf0[i] + h2 * wkf2[i];
    }
    
    dif(t1, wk1, wk2, wkf1, wkf2);
    
    for (int i=1; i<=n; i++) {
        y1[i] = y1[i] + h * wk2[i];
        wk1[i] = y0[i] + h * wk2[i];
    }
    
    for (int i=1; i<=n1; i++) {
        yf1[i] = yf1[i] + h * wkf2[i];
        wkf1[i] = yf0[i] + h * wkf2[i];
    }
    
    t1 = t + h;
    dif(t1, wk1, wk2, wkf1, wkf2);
    
    for (int i=1; i<=n; i++) {
        y1[i] = y0[i] + (y1[i] + h2 * wk2[i]) / 3.0;
    }
    
    for (int i=1; i<=n1; i++) {
        yf1[i] = yf0[i] + (yf1[i] + h2 * wkf2[i]) / 3.0;
    }
    wk1.clear();
    wk2.clear();
    wkf1.clear();
    wkf2.clear();
    return;
}

// void rk4(double t, double *y0, double *yf0,double *dy0, double *dyf0, double h, double *y1,double *yf1,void dif(double , double *, double *,double *, double *))
// {
    
//     int i,n,n1;
//     double h2,t1;
//     double *wk1, *wk2,*wkf1,*wkf2;
// n=GLOBAL.N;
// n1=GLOBAL.sN;
//     h2=h/2.;
//     wk1=(double *) calloc(n+1, sizeof(double));
//     wk2=(double *) calloc(n+1, sizeof(double));
//     wkf1=(double *) calloc(n1+1, sizeof(double));
//     wkf2=(double *) calloc(n1+1, sizeof(double));
//     for(i=1; i<=n; ++i) {
//         y1[i]=h2*dy0[i];
// /*    y_0+0.5k_1 */
//         wk1[i]=y0[i]+y1[i];
//     }
// for(i=1; i<=n1; ++i) {
//         yf1[i]=h2*dyf0[i];
// /*    y_0+0.5k_1 */
//         wkf1[i]=yf0[i]+yf1[i];
//     }

//     t1=t+h2;
// //dif(sp,id,sid,M,sM,N,sN,t,y0,dy,yf0,dyf);
//     dif(t1,wk1,wk2,wkf1,wkf2);
//     for(i=1; i<=n; ++i) {
//         y1[i]=y1[i]+h*wk2[i];
// /*    y_0+0.5k_2 */
//         wk1[i]=y0[i]+h2*wk2[i];
//     }
// for(i=1; i<=n1; ++i) {
//         yf1[i]=yf1[i]+h*wkf2[i];
// /*    y_0+0.5k_2 */
//         wkf1[i]=yf0[i]+h2*wkf2[i];
//     }
// dif(t1,wk1,wk2,wkf1,wkf2);
// //    dif(sp,t1,wk1,wk2);
//     for(i=1; i<=n; ++i) {
//         y1[i]=y1[i]+h*wk2[i];
// /*    y_0+k_3 */
//         wk1[i]=y0[i]+h*wk2[i];
//     }
// for(i=1; i<=n1; ++i) {
//         yf1[i]=yf1[i]+h*wkf2[i];
// /*    y_0+k_3 */
//         wkf1[i]=yf0[i]+h*wkf2[i];
//     }
//     t1=t+h;
//     dif(t1,wk1,wk2,wkf1,wkf2);
//     for(i=1; i<=n; ++i)  y1[i]=y0[i]+(y1[i]+h2*wk2[i])/3.0;
//     for(i=1; i<=n1; ++i)  yf1[i]=yf0[i]+(yf1[i]+h2*wkf2[i])/3.0;
//     free(wk2); free(wk1);free(wkf2); free(wkf1);
//     return;
// }


void gs(vector<double> &y,int sid,int sM,int N,vector<double> &sum)
{
  double a[sM+1];
  double bnorm;
  int ii,itt,it,iii;

  for(ii=1;ii<=sM;ii++){
    a[ii]=0.0;
  }

  for(itt=1;itt<=sM;itt++){
    bnorm=0.0;
    if(itt==1){
      for(it=1;it<=sid;it++){
    bnorm=bnorm+pow(y[it+sid],2.0);
      }
      for(it=1;it<=sid;it++){
    y[it+sid]=y[it+sid]/sqrt(bnorm);
      }
      sum[itt]=sum[itt]+0.5*log(bnorm);
      bnorm=0.0;
    }
    else{
      for(iii=1;iii<=(itt-1);iii++){
    a[iii]=0.0;
    for(it=1;it<=sid;it++){
      a[iii]=a[iii]+y[it+iii*sid]*y[it+itt*sid];
    }
    for(it=1;it<=sid;it++){
      y[it+itt*sid]=y[it+itt*sid]-a[iii]*y[it+iii*sid];
        }
      }
      for(it=1;it<=sid;it++){
    bnorm=bnorm+pow(y[it+itt*sid],2.0);
      }
      for(it=1;it<=sid;it++){
    y[it+itt*sid]=y[it+itt*sid]/sqrt(bnorm);
      }
      sum[itt]=sum[itt]+0.5*log(bnorm);
      bnorm=0.0;
    }}}




// casualty_stats get_infected_community( std::vector<double> & y){
//   count_type symptomatic = 0;
//   count_type  infected_age_group_1 = 0;
//   const auto SIZE = GLOBAL.Nodes; 

//   for (count_type i=0; i<SIZE; ++i){

//   }
// }

