#include <vector>
#include <algorithm>
#include <map>
#include <string>
#include "models.h"
#include "initializers.h"
#include "updates.h"
#include "simulator.h"
#include "outputs.h"
#include <iomanip>


using std::vector;
using std::string;



plot_data_struct run_simulation(){

GLOBAL.id=GLOBAL.Nodes*7; 
GLOBAL.sid=GLOBAL.Nodes*2;
GLOBAL.M=1;
GLOBAL.sM=1; 
GLOBAL.N=(GLOBAL.M+1)*GLOBAL.id;
GLOBAL.sN=(GLOBAL.sM+1)*GLOBAL.sid;
GLOBAL.A.resize(GLOBAL.Nodes*GLOBAL.Nodes+1);
GLOBAL.B.resize(GLOBAL.Nodes*GLOBAL.Nodes+1);

GLOBAL.adjMatrixA.resize(GLOBAL.Nodes+1);
GLOBAL.adjMatrixB.resize(GLOBAL.Nodes+1);

for (int i = 1; i <=GLOBAL.Nodes; ++i) {
    GLOBAL.adjMatrixA[i].resize(GLOBAL.Nodes+1);
    GLOBAL.adjMatrixB[i].resize(GLOBAL.Nodes+1);

}
   generateHumanNetwork(GLOBAL.networktypeH);//generates GLOBAL.adjMatrixA
   generateMosquitoNetwork(GLOBAL.networktypeM);// generates GLOBAL.adjMatrixB


        // std::cout<<"I am in here in simulator.cc and in time loop\t"<<adjMatrix.size()<<"\n"<<std::endl;

  vector<double> y0(GLOBAL.Nodes*GLOBAL.N+1, 0);
  vector<double> dy(GLOBAL.Nodes*GLOBAL.N+1, 0);
  
  vector<double> yf0(GLOBAL.Nodes*GLOBAL.sN+1, 0);
  vector<double> dyf(GLOBAL.Nodes*GLOBAL.sN+1, 0);
  

  vector<double> y1(GLOBAL.Nodes*GLOBAL.N+1, 0);
  vector<double> yf1(GLOBAL.Nodes*GLOBAL.sN+1, 0);



//GLOBAL.networktype=0, 1, 2 for small world, random and scale free networks

plot_data_struct plot_data;


GLOBAL.ntrans=10000;
GLOBAL.h=0.001;

GLOBAL.degA.resize(GLOBAL.Nodes+1, 0.0);
GLOBAL.degB.resize(GLOBAL.Nodes+1, 0.0);
// GLOBAL.A.resize(GLOBAL.Nodes+1, 0.0);
// GLOBAL.B.resize(GLOBAL.Nodes+1, 0.0);
GLOBAL.R0.resize(GLOBAL.Nodes+1, 0.0);
GLOBAL.I.resize(GLOBAL.Nodes+1, 0.0);
GLOBAL.muM.resize(GLOBAL.Nodes+1, 0.0);
GLOBAL.Qv.resize(GLOBAL.Nodes+1, 0.0);
GLOBAL.PIM.resize(GLOBAL.Nodes+1, 0.0);
GLOBAL.PIH.resize(GLOBAL.Nodes+1, 0.0);

plot_data.nums["csvContent"] = {};
plot_data.nums["csvContent"].reserve((int(GLOBAL.NUM_DAYS)) * GLOBAL.Nodes);

std::string logging1 = "Time_step,total_new_infections,Exposed,Infected,Recovered" ;
std::vector<std::string> logger1;
logger1.push_back(logging1);


int N=GLOBAL.Nodes*GLOBAL.id;
double t=0,h=GLOBAL.h;
std::cout<<GLOBAL.NUM_DAYS<<"\t"<<GLOBAL.bet1<<std::endl;

init_states(y0);
        std::cout<<"I am in here in simulator.cc before time loop\t"<<y0.size()<<"\n"<<std::endl;

// for (int i=1;i<=GLOBAL.N;i++){
// std::cout<<"writing states\t"<<y0[i]<<"\t"<<i<<std::endl;
// }
GLOBAL.SIM_STEPS_PER_DAY=int(1/h);
GLOBAL.SIM_STEPS=GLOBAL.NUM_DAYS*GLOBAL.SIM_STEPS_PER_DAY;
t=GLOBAL.START_DAY/GLOBAL.SIM_STEPS_PER_DAY;
for(count_type time_step=GLOBAL.START_DAY/GLOBAL.SIM_STEPS_PER_DAY;time_step<=GLOBAL.SIM_STEPS;time_step++)
     {
      // std::cout<<"time step\t"<<time_step<<std::endl;

      t=t+h;
      int new_day=time_step%GLOBAL.SIM_STEPS_PER_DAY,day=time_step/GLOBAL.SIM_STEPS_PER_DAY;

     dif(t,y0,dy,yf0,dyf);

     rk4(t, y0, yf0, dy,dyf, h, y1,yf1, dif);

           //-----Writing outputs from the simulator-----//
      double num_new_symptomatic=0,exposed=0,recovered=0,infected=0;
      if(new_day==0)
      {
            for (int c = 1; c <= GLOBAL.Nodes; ++c){
                  //let row = [time_step/SIM_STEPS_PER_DAY,c,temp_stats[0],temp_stats[1],temp_stats[2],temp_stats[3],temp_stats[4]].join(",");
                  plot_data.nums["csvContent"].push_back({count_type(day), {c*1.0,GLOBAL.sigH*y0[4*GLOBAL.Nodes+c]}});
                  num_new_symptomatic+=GLOBAL.sigH*y0[4*GLOBAL.Nodes+c];
                  exposed+=y0[4*GLOBAL.Nodes+c];
                  infected+=y0[5*GLOBAL.Nodes+c];
                  recovered+=y0[6*GLOBAL.Nodes+c];
            }
            logging1 = std::to_string(count_type(day))+","+std::to_string(num_new_symptomatic)+","+std::to_string(exposed)+","+std::to_string(infected)+","+std::to_string(recovered);

            logger1.push_back(logging1);
      }
     for(int i=1;i<=N;i++)
      {
      y0[i]=y1[i];
      }
              // std::cout<<"I am in here in simulator.cc and in time loop\t"<<y0.size()<<"\t"<<t<<"\t"<<time_step<<"\n"<<std::endl;

/*if(t>1000)
{
for(i=1;i<=Nodes;i++)
   {
    if(sp.deg[i]>Nc)
{
    sp.muM[i]=sp.muV/sp.cc;
}
   }
}*/
      //gs(yf0,sid,sM,sN,sum);
      //gs(y0,id,M,N,ssum);
      //gs(yf0,sid,sM,sN,sum);
      //gs(y0,id,M,N,ssum);
      // double num_new_symptomatic=0,exposed=0,recovered=0,infected=0;
      // if(new_day==0)
      // {
      //       for (int c = 1; c <= GLOBAL.Nodes; ++c){
      //             //let row = [time_step/SIM_STEPS_PER_DAY,c,temp_stats[0],temp_stats[1],temp_stats[2],temp_stats[3],temp_stats[4]].join(",");
      //             plot_data.nums["csvContent"].push_back({count_type(day), {c*1.0,GLOBAL.sigH*y0[4*GLOBAL.Nodes+c]}});
      //             num_new_symptomatic+=GLOBAL.sigH*y0[4*GLOBAL.Nodes+c];
      //             exposed+=y0[4*GLOBAL.Nodes+c];
      //             infected+=y0[5*GLOBAL.Nodes+c];
      //             recovered+=y0[6*GLOBAL.Nodes+c];
      //       }
      //       logging1 = std::to_string(count_type(day))+","+std::to_string(num_new_symptomatic)+","+std::to_string(exposed)+","+std::to_string(infected)+","+std::to_string(recovered);

      //       logger1.push_back(logging1);
      // }
// if(int(time_step*h)==time_step*h){
// logging1 = std::to_string(time_step)+","+std::to_string(num_new_symptomatic);

// logger1.push_back(logging1);
// }

}
plot_data.logger1 = logger1;

return plot_data;

}

