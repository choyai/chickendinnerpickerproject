#include <24FJ48GA002.h>
#include "BL_Support.h"
#use delay (internal = 8 MHz, clock = 32MHz)
#PIN_SELECT U1RX = PIN_B12 //PIN_B14 //
#PIN_SELECT U1TX = PIN_B13 //PIN_B15 //
#use rs232 (UART1, BAUD = 9600, XMIT = PIN_B13, RCV = PIN_B12)

#define DEVICE_ID   2

char array[20] = {};
char SM_id = 1;
int getPackage = 0;
// char* print_float(float data){
// 	int intDist = data / 1;
//     int dotDist = (((intDist>>15)*-2)+1) * ((data * 1000.0f) - (intDist * 1000));
//     char stringFloat[20];
//     sprintf(stringFloat, "%d.%d", intDist, dotDist);
//     return stringFloat;
// }
// void print_float(char* stringResult, float data){
// 	int intDist = data / 1;
//     int dotDist = (((intDist>>15)*-2)+1) * ((data * 1000.0f) - (intDist * 1000));
//     sprintf(stringResult, "%d.%d", intDist, dotDist);
// }
void SM_RxD(int c){
	if (SM_id <= 2){
		if (c == 255){
			SM_id++;
		}else{
			SM_id = 1;
		}
	}else{
		putc(c);
		SM_id = 1;
	}
	// }else if (SM_id <= 3){
	// 	if (c == DEVICE_ID){
	// 		SM_id++;
	// 	}
	// }else if (SM_id > 3){
	// 	array[SM_id - 4] = c;
	// 	SM_id++;
	// 	if (SM_id >= 8){
	// 		getPackage = 1;
	// 		SM_id = 1;
	// 	}
	// }
}
#INT_RDA               // receive data interrupt one time per one
void UART1_Isr() {
    int c = (int)getc();
		putc(c);
    // SM_RxD(c);
}
void main(){
	disable_interrupts(GLOBAL);

    clear_interrupt(INT_RDA);   // recommend style coding to confirm everything clear before use
    enable_interrupts(INT_RDA);

	enable_interrupts(GLOBAL);
    // printf("System Ready!\r\n");
	while(TRUE){
		if (getPackage >= 1){
			getPackage = 0;
			// for(int i = 0; i < 8; i++){
			// 	putc(array[i]);
			// }
			// float test;
			// memcpy(&test, array, sizeof(test));
			// printf("\nresult = %s, %s\n", print_float(test), print_float(test));
		}
	}
}
