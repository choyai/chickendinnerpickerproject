#include <24FJ48GA002.h>
#include "BL_Support.h"
#use delay (internal = 8MHz, clock = 32MHz)

#PIN_SELECT OC1 = PIN_B2

void main(){	
	disable_interrupts(GLOBAL);
	// ((32M/2)/256)/1Hz = 62500
	//set 1 Hz
	setup_timer2(TMR_INTERNAL | TMR_DIV_BY_256, 62500); 
	enable_interrupts(GLOBAL);	
	
	setup_compare(1, COMPARE_PWM | COMPARE_TIMER2);
	set_pwm_duty(1, 6250); //set duty 10% by (62500/10) = 6250
	//set_pwm_duty(1, 15625); //set duty 25% by (62500/25) = 15625
	//set_pwm_duty(1, 31250); //set duty 50% by (62500/10) = 31250
	//set_pwm_duty(1, 46875); //set duty 75% by (62500/10) = 46875
	//set_pwm_duty(1, 62500); //set duty 100% by (62500/10) = 62500	
		
	while(TRUE){
	}
}
