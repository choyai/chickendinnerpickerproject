#include <24FJ48GA002.h>
#include "BL_Support.h"
#use delay (internal = 8MHz, clock = 32MHz)
#PIN_SELECT U1TX = PIN_B13
#PIN_SELECT U1RX = PIN_B12
#use rs232(UART1, baud = 115200, xmit = PIN_B13, rcv = PIN_B12)

#PIN_SELECT OC1 = PIN_B2
#PIN_SELECT INT1 = PIN_B5 //DXI1  (Encoder)
#PIN_SELECT INT2 = PIN_B6

double frequency(double f){
	double frequency;
	//set frequency by ((32M/2)/8)/frequency = clock
	if (f == 1){
		frequency = (((32000000/2)/256)/f);
	}
	else if(f >= 2 && f <= 10000){
		frequency = (((32000000/2)/8)/f);
	}
	return frequency;
}


int duty_cycle( int f, int d){
	//set duty cycle by (clock*duty)/100 = duty input
	unsigned int duty_cycle;
	duty_cycle = (int)((frequency(f)/100)*d);
	printf("duty cycle: %d", duty_cycle);
	printf("frequency: %d", (int)frequency(f));
	return duty_cycle;
}

void PWM( int f, int d){
	if (f == 1){
		disable_interrupts(GLOBAL);
		setup_timer2(TMR_INTERNAL | TMR_DIV_BY_256,(int)frequency(f));
		enable_interrupts(GLOBAL);
		setup_compare(1, COMPARE_PWM | COMPARE_TIMER2);
		set_pwm_duty(1, duty_cycle(f,d));
	}
	else if(f >= 2 && f <= 10000){
		disable_interrupts(GLOBAL);
		setup_timer2(TMR_INTERNAL | TMR_DIV_BY_8,(int)frequency(f));
		enable_interrupts(GLOBAL);
		setup_compare(1, COMPARE_PWM | COMPARE_TIMER2);
		set_pwm_duty(1, duty_cycle(f,d));
	}
}

void main(){	;
	//set pwm(frequency,duty cycle)
	int f = 10000;
	int d = 10;
	PWM(10000,10);
	while(TRUE){
		if(input(PIN_B6) == 0){
			if(d == 100){
				d = 0;
			}
			else{
				d += 5;
			}
			PWM(f, d);
		}
		if(input(PIN_B5) == 0){
			if(f == 10000){
				f = 1;
			}
			else{
				f *= 10;
			}
			PWM(f, d);
		}
	}
}
