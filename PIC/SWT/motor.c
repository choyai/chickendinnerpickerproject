
#include <24FJ48GA002.h>
#fuses FRC_PLL
#use delay(clock = 32000000) // Real hardware requires 16MHz
#use rs232(baud = 57600, xmit = PIN_B14, rcv = PIN_B15)
#use fixed_io(b_outputs = PIN_B8, PIN_B9, PIN_B10, PIN_B11)
unsigned int swt_count = 100;
boolean swt_flag = FALSE;
typedef void (*SWTCallback)(void);
SWTCallback fp_ta = (void *)0;
void SystemTick(void) {
  if (swt_count > 0) {
    swt_count--;
    if (swt_count == 0) {
      swt_flag = TRUE;
    }
  }
}
#INT_TIMER1
void TIMER1_ISR() { SystemTick(); }
void SWTService(void) {
  if (swt_flag == TRUE) {
    swt_flag = FALSE;
    /* Runs the callback */
    if (fp_ta != (void *)0) {
      (*fp_ta)();
    }
  }
}
void task_a(void) { printf("\r\ntask_a"); }
void Init_Timer1() {
  setup_timer1(TMR_INTERNAL | TMR_DIV_BY_8, 2000);
  enable_interrupts(INT_TIMER1);
}
void main(void) {
  disable_interrupts(GLOBAL);
  Init_Timer1();
  enable_interrupts(GLOBAL);
  printf("\r\nApplication is running...");
  swt_count = 5000;
  fp_ta = &task_a;
  while (TRUE) {
    SWTService();
  }
}
