#include <24FJ48GA002.h>
#include "BL_Support.h"
#include "math.h"
#use delay (internal = 8 MHz, clock = 32MHz)

#PIN_SELECT U1RX = PIN_B13 
#PIN_SELECT U1TX = PIN_B12 

#use rs232 (UART1, BAUD = 9600, XMIT = PIN_B13, RCV = PIN_B12)

#define limitSw_x PIN_B8        //
#define limitSw_y PIN_A2        //   
#define limitSw_z PIN_A4        // 
#define Motor_Bp PIN_B10        // Pin output is connected to DXI0  (PWM)
#define Motor_Br PIN_B2         // Pin output is connected to DX02
#define Motor_Bl PIN_B3         // Pin output is connected to DX03
#define Motor_Ap PIN_B4         // Pin output is connected to DX03
#define Motor_Ar PIN_A0         // Pin output is connected to DX03
#define Motor_Al PIN_A1         // Pin output is connected to DX03
#define Motor_Zp PIN_B14        // Pin output is connected to DX03
#define Motor_Zr PIN_B15        // Pin output is connected to DX03
#define Motor_Zl PIN_B9         // Pin output is connected to DX03
#define Encode_A PIN_B7         // Pin output is connected to DX03
#define Encode_B PIN_B6         // Pin output is connected to DX03
#define Encode_Z PIN_B5         // Pin output is connected to DX03
#define servo_r PIN_B0          // servo 270 
#define servo_l PIN_B1          // servo 180

#PIN_SELECT OC1 = Motor_Bp       
#PIN_SELECT OC2 = Motor_Ap     
#PIN_SELECT OC3 = Motor_Zp      
#PIN_SELECT OC4 = servo_r       
#PIN_SELECT OC5 = servo_l       
#PIN_SELECT INT1 = Encode_B    
#PIN_SELECT INT2 = Encode_Z    
 
long count_a = 0;
long count_b = 0;
long count_z = 0;
long direction = 0;
long posi = 0;
float K_Pz = 0.6;
float K_Iz = 0.01;
//float K_Dz = 0.5;
//float K_Pa = 0.6;
//float K_Ia = 0.01;
//float K_Da = 0.5;
//float K_Pb = 0.6;
//float K_Ib = 0.01;
//float K_Db = 0.5;
int s = 0;
int p = 0;
int desired_value = 512;

void Motor_z(int u){
   if (u > 100)u = 100;
   if (u < -100)u = -100;
   if(u>0){
      output_bit(Motor_Zr,0);
      output_bit(Motor_Zl,1);
      direction = 0;
      set_pwm_duty(3, (int)(2 * u));
   }
   else if(u<0) {
      output_bit(Motor_Zr,1);
      output_bit(Motor_Zl,0);
      direction = 1;
      set_pwm_duty(3, (int)(2 * -u));
   }else{
      output_bit(Motor_Zr,1);
      output_bit(Motor_Zl,1);      
      set_pwm_duty(3, (int)(100));   
      delay_ms(100);
   }
}

void Motor_A(int u){
   if (u > 100)u = 100;
   if (u < -100)u = -100;
   if(u>0){
      output_bit(Motor_Ar,1);
      output_bit(Motor_Al,0);
      direction = 0;
      set_pwm_duty(2, (int)(2 * u));
   }
   else if(u<0) {
      output_bit(Motor_Ar,0);
      output_bit(Motor_Al,1);
      direction = 1;
      set_pwm_duty(2, (int)(2 * -u));
   }else{
      output_bit(Motor_Ar,1);
      output_bit(Motor_Al,1);      
      set_pwm_duty(2, (int)(100));   
      delay_ms(100);
   }
}

void Motor_B(int u){
   if (u > 100)u = 100;
   if (u < -100)u = -100;
   if(u>0){
      output_bit(Motor_Br,1);
      output_bit(Motor_Bl,0);
      direction = 0;
      set_pwm_duty(1, (int)(2 * u));
   }
   else if(u<0) {
      output_bit(Motor_Br,0);
      output_bit(Motor_Bl,1);
      direction = 1;
      set_pwm_duty(1, (int)(2 * -u));
   }else{
      output_bit(Motor_Br,1);
      output_bit(Motor_Bl,1);      
      set_pwm_duty(1, (int)(100));   
      delay_ms(100);
   }
}

#INT_EXT0
void INT_EXT_INPUT0(void) {
      count_a++;
}

#INT_EXT1
void INT_EXT_INPUT1(void) {
      count_b++;
}

#INT_EXT2
void INT_EXT_INPUT2(void) {
      count_z++;
}

void Init_Interrupts() {
	enable_interrupts( INT_EXT0 );
    ext_int_edge( 0, L_TO_H ); // Rising Edge
	enable_interrupts( INT_EXT1 );
    ext_int_edge( 1, L_TO_H ); // Rising Edge	
	enable_interrupts( INT_EXT2 );
    ext_int_edge( 2, L_TO_H ); // Rising Edge
}

void Set_position_z(int post){
   int e = post - count_z;
   if (e > 5){
      Motor_z(K_Pz * e + K_Iz * s + K_Iz * (e - p));
	  posi = (((count_z*2*5*22)/7)/768);
	  printf("Position : %d\n",posi);	
   }
   else{
      Motor_z(0);
      delay_ms(500);
      //printf("count: %d\n",count);
	  posi = (((count_z*2*5*22)/7)/768);
	  printf("Position : %d\n",posi);
   }
}

void Set_Home(void){
	setup_compare(3, COMPARE_PWM | COMPARE_TIMER3);
    setup_compare(2, COMPARE_PWM | COMPARE_TIMER3);
	setup_compare(1, COMPARE_PWM | COMPARE_TIMER3);
	set_pwm_duty(3,0);
	set_pwm_duty(2,0);
    set_pwm_duty(1,0);
	do{
		Motor_z(-100);	
	}while(input(limitSw_z)==1);
	Motor_z(0);
	do{
		Motor_a(-100);
		Motor_b(-100);	
	}while(input(limitSw_x)==1);
	Motor_a(0);
	Motor_b(0);	
	do{
		Motor_a(100);
		Motor_b(-100);		
	}while(input(limitSw_y)==1);
	Motor_a(0);
	Motor_b(0);			
}

void Grip_Open(void){
	setup_compare(5, COMPARE_PWM | COMPARE_TIMER2);
    set_pwm_duty(5, 4800);
}

void Grip_Close(void){
	setup_compare(5, COMPARE_PWM | COMPARE_TIMER2);
    set_pwm_duty(5, 1600);
}

/*void(){
	
}*/

void main(){
    Init_Interrupts();
    enable_interrupts(GLOBAL);
    setup_timer3(TMR_INTERNAL | TMR_DIV_BY_8, 200);
	setup_timer2(TMR_INTERNAL | TMR_DIV_BY_8, 8000);
	setup_timer1(TMR_INTERNAL | TMR_DIV_BY_8, 6666);               
	//Set_Home();
	Grip_Open();
	delay_ms(1000);
	Grip_Close();
	
   while(TRUE){
		//posi = (((count*2*5*22)/7)/768)+((((count*2*5*22*2)/7)/768)/5) ;
	  	//printf("\nPosition : %d\n",posi);
		//printf("limit : %d\n",input(PIN_B7));
		//printf("count : %d\n",count);
		//delay_ms(50);
        //Set_position(1700); //forword 
   }
}