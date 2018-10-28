#include <24FJ48GA002.h>
#include "BL_Support.h"
#use delay (internal = 8 MHz, clock = 32MHz)

#define limitSw_x PIN_B7 //PIN_B7// 
#PIN_SELECT U1RX = PIN_B13 //PIN_B14 //
#PIN_SELECT U1TX = PIN_B12 //PIN_B15 //
#use rs232 (UART1, BAUD = 9600, XMIT = PIN_B13, RCV = PIN_B12)
#PIN_SELECT OC1 = PIN_B2         // Pin output is connected to DX02  
#PIN_SELECT OC2 = PIN_B3         // Pin output is connected to DX03
#PIN_SELECT OC3 = PIN_B4         // Pin output is connected to DXI0  (PWM)
#PIN_SELECT INT1 = PIN_B6    

long count = 0;
long direction = 0;
long posi = 0;

void Motor(int u){
   if (u > 100)u = 100;
   if (u < -100)u = -100;
   if(u>0){
      output_bit(PIN_B2,0);
      output_bit(PIN_B3,1);
      direction = 0;
      set_pwm_duty(3, (int)(2 * u));
   }
   else if(u<0) {
      output_bit(PIN_B2,1);
      output_bit(PIN_B3,0);
      direction = 1;
      set_pwm_duty(3, (int)(2 * -u));
   }else{
      output_bit(PIN_B2,1);
      output_bit(PIN_B3,1);      
      set_pwm_duty(3, (int)(100));   
      delay_ms(100);
   }
}
#INT_EXT1
void INT_EXT_INPUT1(void) {
   if(input(PIN_B6)==1){
      count++;
   }else{
      count--;
   }
}

void Init_Interrupts() {
   enable_interrupts( INT_EXT1 );
   ext_int_edge( 1, L_TO_H ); // Rising Edge
}

void Set_position(int post){
   int error = post - count;
   int Kp = 1;
   if (error > 5){
      Motor(error*Kp);
	  posi = (((count*2*5*22)/7)/768)+((((count*2*5*22*2)/7)/768)/5) ;
	  printf("Position : %d\n",posi);	
   }
   else{
      Motor(0);
      delay_ms(500);
      //printf("count: %d\n",count);
	  posi = (((count*2*5*22)/7)/768)+((((count*2*5*22*2)/7)/768)/5) ;
	  printf("Position : %d\n",posi);
   }
}

void main(){
   Init_Interrupts();
   enable_interrupts(GLOBAL);
   setup_timer3(TMR_INTERNAL | TMR_DIV_BY_8, 200);               
   setup_compare(3, COMPARE_PWM | COMPARE_TIMER3);
   set_pwm_duty(3,0);
  while(input(limitSw_x)==1){ //not found limit switch
		Motor(-50); //back until can found limit switch(lm_switch == 1)
	}
	Motor(0); //if found limit motor. motor is stop
	delay_ms(100);
	count = 0; //set count 

   while(TRUE){
		//printf("limit : %d\n",input(PIN_B7));
		//delay_ms(50);
		posi = (((count*2*5*22)/7)/768)+((((count*2*5*22*2)/7)/768)/5) ;
	  	printf("Position : %d\n",posi);
        Set_position(1500); //forword 
   }
}