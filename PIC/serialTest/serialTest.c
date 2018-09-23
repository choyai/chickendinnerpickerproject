#include <24FJ48GA002.h>
#include "BL_Support.h"
//#fuses FRC_PLL
#use delay (internal = 8 MHz, clock = 32000000)
#PIN_SELECT U1RX = PIN_B12
#PIN_SELECT U1TX = PIN_B13

#use rs232(UART1, BAUD = 9600, PARITY = N, STOP = 1, XMIT = PIN_B13, RCV = PIN_B12)

//#use fixed_io(b_outputs = PIN_B4, PIN_B5, PIN_B6, PIN_B7)

//int led_data = 0;
int main(){
	//set_tris_b(0xFF0F);
	while(TRUE){
		//output_b((led_data<<4));
    putc('1');
		//led_data += 1;
		delay_ms(100);
	}
	return (0);
}
