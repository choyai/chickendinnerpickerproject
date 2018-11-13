#include <24FJ48GA002.h>
#include "BL_Support.h"
#use delay(internal = 8 MHz, clock = 32MHz)

#define DEVICE_ID 2
#PIN_SELECT U1RX = PIN_B13 //PIN_B14 //
#PIN_SELECT U1TX = PIN_B12 //PIN_B15 //
#use rs232 (UART1, BAUD = 9600, XMIT = PIN_B13, RCV = PIN_B12)
#PIN_SELECT OC1 = PIN_B2         // Pin output is connected to DX02
#PIN_SELECT OC2 = PIN_B3         // Pin output is connected to DX03
#PIN_SELECT OC3 = PIN_B4         // Pin output is connected to DXI0  (PWM)
#PIN_SELECT INT1 = PIN_B6
#define limitSw_x PIN_B7 				 //PIN_B7

long count = 0;
long direction = 0;
char array[20] = {};
char SM_id = 0;
int getPackage = 0;
char command_ID;
int posi = 0;
// char* print_float(float data){
// 	int intDist = data / 1;
//     int dotDist = (((intDist>>15)*-2)+1) * ((data * 1000.0f) - (intDist *
//     1000));
//     char stringFloat[20];
//     sprintf(stringFloat, "%d.%d", intDist, dotDist);
//     return stringFloat;
// }
// void print_float(char* stringResult, float data){
// 	int intDist = data / 1;
//     int dotDist = (((intDist>>15)*-2)+1) * ((data * 1000.0f) - (intDist *
//     1000));
//     sprintf(stringResult, "%d.%d", intDist, dotDist);
// }

// Communication Routines//

void SM_RxD(int c) {
  if (getPackage == 0) {
    if (SM_id < 2) {
      if (c == 255) {
        array[SM_id] = c;
        SM_id++;
      } else {
        SM_id = 0;
      }
    } else if (SM_id == 2) {
      array[SM_id] = c;
      command_ID = c;
      SM_id++;
    } else if (SM_id > 2) {
      array[SM_id] = c;
      if (SM_id >= 8) {
        getPackage = 1;
        SM_id = 0;
      } else {
        SM_id++;
      }
    }
  }
}
#INT_RDA
void UART1_Isr() {
	int c = getc();
	putc(c);
	SM_RxD(c);
}
/***/

//PID Control//
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

//motor driver

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
/***/

//COMMANDS//
void setHome(){
	printf("done");
	getPackage = 0;

}

void setPosXY(){
	printf("done");
	getPackage = 0;
}

void setPosZ(){
	printf("done");
	getPackage = 0;
}

int sumCheck() {
	int sum = 0;
	int checksum = array[8];
	for(int i = 0; i < 7; i++){
		sum = sum + array[i];
	}
	if(sum == checksum){
		return 1;
	}
	else{
		return 0;
	}
}


void main() {

  disable_interrupts(GLOBAL);
  clear_interrupt(
      INT_RDA); // recommend style coding to confirm everything clear before use
  enable_interrupts(INT_RDA);
	Init_Interrupts();
	setup_timer3(TMR_INTERNAL | TMR_DIV_BY_8, 200);
	setup_compare(3, COMPARE_PWM | COMPARE_TIMER3);
	set_pwm_duty(3,0);
  enable_interrupts(GLOBAL);

	printf("System Ready!\r\n");

  while (TRUE) {
    if (getPackage >= 1) {
      int received = sumCheck();
      if (!received) {
				printf("resend");
        getPackage = 0;
      }
			else{
				switch (array[2]) {
					case 0:
						setHome();
						break;
					case 1:
						setPosXY();
						break;
					case 2:
						setPosZ();
						break;
					default:
						printf("resend");
						getPackage = 0;
						break;
				}
			}
      // float test;
      // memcpy(&test, array, sizeof(test));
      // printf("\nresult = %s, %s\n", print_float(test), print_float(test));
    }
  }
}
