#include <24FJ48GA002.h>
#include "BL_Support.h"
#use delay (internal = 8 MHz, clock = 32MHz)

#PIN_SELECT OC1 = PIN_B2

#INT_TIMER2
void TIMER2_ist(){
}
void main(){


	disable_interrupts(GLOBAL);
	// (for 1 Hz)setup_timer2(TMR_INTERNAL |TMR_DIV_BY_256, 62500); // freq=32M/2/8/6250
	// (for 100Hz)setup_timer2(TMR_INTERNAL |TMR_DIV_BY_8, 20000);
	//(for 1KHz)setup_timer2(TMR_INTERNAL |TMR_DIV_BY_8, 2000);
	//(for 10 kHz)
	setup_timer2(TMR_INTERNAL |TMR_DIV_BY_8, 200);
	enable_interrupts(INT_TIMER2);
	enable_interrupts(GLOBAL);

	setup_compare(1, COMPARE_PWM | COMPARE_TIMER2);
	set_pwm_duty(1,200); //6000/6250 *100

	while(TRUE){
	}
}
