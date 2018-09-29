#include <24FJ48GA002.h>
#include "BL_Support.h"
#include "math.h"
#use delay(internal = 8 MHz, clock = 32000000)
#PIN_SELECT U1TX = PIN_B13
#PIN_SELECT U1RX = PIN_B12

#use rs232(UART1, baud = 9600, xmit = PIN_B13, rcv = PIN_B12)

#PIN_SELECT OC1 = PIN_B2  //DX02
#PIN_SELECT OC2 = PIN_B3  //DX03
#PIN_SELECT INT1 = PIN_B4  //DXI0  (PWM)
#PIN_SELECT INT2 = PIN_B5 //DXI1  (Encoder)
// #PIN_SELECT INT2 = PIN_B6			// Pin output is connected to DXI2


int percent_duty = 0;
unsigned int count = 0;
BOOLEAN run_direction = FALSE;
BOOLEAN toggle = FALSE;
float timer3time = 0;
float volt = 0;
int x;

#INT_EXT1
void INT_EXT_INPUT1(void) {
  toggle = !toggle;
}

// int convertToDUTY(float voltage) {
//   int duty = abs(voltage) * 100 / 12;
//   return duty;
// }

// int dutyPercentInput(int duty_percent){
//   int duty = abs(duty_percent);
//   if(duty > 100){
//     duty = 100;
//   }
//   return duty;
// }
//
// int getDirection(int duty_percent) {
//   int direction;
//   if (duty_percent > 0) {
//     direction = 0;
//   } else if (duty_percent < 0) {
//     direction = 1;
//   }
//   else{
//     direction = 2;
//   }
//   return direction;
// }

void Init_Interrupts() {
  enable_interrupts(INT_EXT1);
  ext_int_edge(1, H_TO_L); // Falling Edge
}

#INT_TIMER2
void TIMER2_isr() {
  if(count == 100){
    count = 0;
    if(percent_duty == 100||percent_duty == 0){
      run_direction = !run_direction;
    }
    if(run_direction == TRUE){//TRUE is +
      percent_duty += 10;
    }
    else{
      percent_duty -= 10;
    }
    // printf("duty = %d \n", percent_duty);
  }
  if(toggle == TRUE){//TRUE is LED3
    set_pwm_duty(1, 2000);
    set_pwm_duty(2, percent_duty*20);
  }
  else{
    set_pwm_duty(2, 2000);
    set_pwm_duty(1, percent_duty*20);
  }
  count++;
}

void Init_Timer2() {
  setup_timer2(TMR_INTERNAL | TMR_DIV_BY_8, 2000);//f = 2000Hz
  enable_interrupts(INT_TIMER2);
  setup_compare(1, COMPARE_PWM| COMPARE_TIMER2);
  setup_compare(2, COMPARE_PWM| COMPARE_TIMER2);
}

// void directional_drive(int direction, int driveduty) {
//   if (direction == 0) { // turn right
//     set_pwm_duty(1, 2 * driveduty);
//     set_pwm_duty(2, 0);
//   } else if (direction == 1) { // turn left
//     set_pwm_duty(1, 0);
//     set_pwm_duty(2, 2 * driveduty);
//   } else if (direction == 2) {//stop
//     set_pwm_duty(1, 0);
//     set_pwm_duty(2, 0);
//   }
// }


// #INT_TIMER3
// void TIMER3_ist() {
//   // volt = chirpSine(timer3time);
//
//   int duty = dutyPercentInput(percent_duty);
//   int dir = getDirection(percent_duty);
//   directional_drive(dir, duty);
//   // timer3time += 0.0001;
// }

// void Drivemotor() {
//   setup_timer3(TMR_INTERNAL | TMR_DIV_BY_8, 200); // Set frequency at 10 KHz
//   enable_interrupts(INT_TIMER3);
//   setup_compare(1, COMPARE_PWM | COMPARE_TIMER3);
//   setup_compare(2, COMPARE_PWM | COMPARE_TIMER3);
// }

void main() {
  // countPulse = 0;
  // timer3time = 0;
  disable_interrupts(GLOBAL);
  // Drivemotor();
  Init_Timer2();
  Init_Interrupts();
  enable_interrupts(GLOBAL);


  while (TRUE) {
  }
}
