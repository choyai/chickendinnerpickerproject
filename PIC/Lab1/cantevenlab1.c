#include <24FJ48GA002.h>
#include "BL_Support.h"
#include "math.h"
#use delay(internal = 8 MHz, clock = 32000000)
#PIN_SELECT U1TX = PIN_B13
#PIN_SELECT U1RX = PIN_B12

#use rs232(UART1, baud = 115200, xmit = PIN_B13, rcv = PIN_B12)

#PIN_SELECT OC1 = PIN_B2 // DX02
// #PIN_SELECT OC2 = PIN_B3 // DX03
// #PIN_SELECT OC3 = PIN_B4 // DXI0
// #PIN_SELECT INT1 = PIN_B5
// DXI1 We'll use this pin for toggling different duty cycles
// #PIN_SELECT INT2 = PIN_B6
// DXI2 We'll use this pin for toggling different frequencies

// set the default frequency, duty cycle
int frequency = 10;
int duty_percent = 50;


int desired_period = 6250;
int count = 0;
int duty = 0;
// #INT_EXT1
// void INT_EXT_INPUT1(void) {
//   // toggle the duty cycle between 10, 25, 50, 75, and 100%
//   if (duty_percent == 10) {
//     duty_percent = 25;
//   } else if (duty_percent == 100) {
//     duty_percent = 10;
//   } else {
//     duty_percent += 25;
//   }
// }
//
// #INT_EXT2
// void INT_EXT_INPUT2(void) {
//   // toggle frequency between 1, 10, 100, 1000, 10kHz
//   if (frequency == 10000) {
//     frequency = 1;
//   } else {
//     frequency = frequency * 10;
//   }
// }

// void Init_Interrupts() {
//   enable_interrupts(INT_EXT1);
//   ext_int_edge(1, L_TO_H);
//   // enable_interrupts(INT_EXT2);
//   // ext_int_edge(2, L_TO_H);
// }

#INT_TIMER2
void TIMER2_ist() {
  count++;
  if (count == 10) {
    printf("duty = %d\n", duty);
    printf("frequency = %d\n", frequency);
    printf("desired_period = %d\n", desired_period);
    count = 0;
  }
}
// void generatePWM() {
  // 32MHz Base Clock
  // 2 Internal Divisor
  // 256 Prescaler
  // to get desired frequency, use formula
  // f = base clock/(internal divisor * prescaler * desired clock cycle)
  // we need to determine the desired clock cycles to use for setup_timer()
  // so we get
  // desired clock cycles = base clock/(internal divisor * prescaler *
  // frequency)
  // We must also make sure that desired_period doesn't overflow
  // So we fix the prescaler to be 256
// }

void main() {
  disable_interrupts(GLOBAL);
  // generatePWM();
  desired_period = 62500/ frequency;
  setup_timer2(TMR_INTERNAL | TMR_DIV_BY_256, desired_period);
  enable_interrupts(INT_TIMER2);
  // Init_Interrupts();
  enable_interrupts(GLOBAL);
  setup_compare(1, COMPARE_PWM | COMPARE_TIMER2);
  // to get the value for set_pwm_duty, we need to use both desired_period
  // and duty_percent.
  // duty_percent = 100 * duty / desired_period
  // so duty = desired_period * duty_percent / 100
  duty = (desired_period / 100);
  duty = (duty * duty_percent);
  set_pwm_duty(1, duty);

  while (TRUE) {
  }
}
