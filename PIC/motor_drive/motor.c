#include <24FJ48GA002.h>
#include "BL_Support.h"
#use delay(internal = 8MHz, clock = 32MHz)
#PIN_SELECT OC1 = PIN_B2
#PIN_SELECT OC2 = PIN_B3
#PIN_SELECT INT1 = PIN_B4
#PIN_SELECT INT2 = PIN_B5
#PIN_SELECT U1RX = PIN_B12 // pin_b14
#PIN_SELECT U1TX = PIN_B13 // pin_b15
#use rs232(UART1, BAUD = 9600, XMIT = PIN_B13, RCV = PIN_B12)

// float chirpSignal(float time){
//   float val = sin((1*(time*time)+ PI/2.0)*Vin;
//   return val;
// }
// float time = 0;
long count = 0;
// BOOLEAN trig = FALSE;

// #INT_TIMER3
// void TIMER3_isr(void) {
  // if (trig) {
//     printf("%d \n\r", count);
  // }
// }

#INT_EXT1
void INT_EXT_INPUT1(void) {
  // if (trig) {
    if (input(PIN_B5)) {
      count++;
    } else {
      count--;
    }
    printf("(%d)\n", count);
  // }
}

#INT_EXT2
void INT_EXT_INPUT2(void) {
  // if (trig) {
    if (input(PIN_B4)) {
      count--;
    } else {
      count++;
    }
    printf("(%d)\n", count);
  // }
}

void main() {
  count = 0;
  disable_interrupts(GLOBAL);
  setup_timer2(TMR_INTERNAL | TMR_DIV_BY_256, 62500);
  enable_interrupts(INT_TIMER2);
  // setup_timer2(TMR_INTERNAL | TMR_DIV_BY_8 | TMR_32_BIT, 20000);
  // enable_interrupts(INT_TIMER3);
  enable_interrupts(INT_EXT1);
  ext_int_edge(1, H_TO_L);
  enable_interrupts(INT_EXT2);
  ext_int_edge(2, H_TO_L);

  enable_interrupts(GLOBAL);

  setup_compare(1, COMPARE_PWM | COMPARE_TIMER2);

  set_pwm_duty(1, 31250);

  while (TRUE) {
    // if(input(PIN_B6)){
      // count = 0;
      // trig = TRUE;
    // }
  }
}
