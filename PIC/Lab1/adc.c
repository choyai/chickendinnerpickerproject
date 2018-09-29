#include <24FJ48GA002.h>
#device ADC=10
#include "BL_Support.h"

#use delay (internal = 8 MHz, clock = 32MHz)
#PIN_SELECT U1RX = PIN_B12 //PIN_B14 //
#PIN_SELECT U1TX = PIN_B13 //PIN_B15 //
#use rs232 (UART1, BAUD = 9600, XMIT = PIN_B13, RCV = PIN_B12)

int adc_data;

void init_adc(){
	setup_adc_ports(sAN3, VSS_VDD);
	setup_adc(ADC_CLOCK);
	set_adc_channel(3);
	delay_us(10);
}
void main(){
	init_adc();
	adc_data = 0;
	while(TRUE){
		adc_data = read_adc();
		printf("AN3: %d\r\n", read_adc());
		delay_ms(500);
	}
}
