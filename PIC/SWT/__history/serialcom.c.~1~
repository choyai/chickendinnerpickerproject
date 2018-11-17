#include <24FJ48GA002.h>
#include "BL_Support.h"
#use delay(internal = 8 MHz, clock = 32MHz)

#PIN_SELECT U1RX = PIN_B12 // PIN_B14 //
#PIN_SELECT U1TX = PIN_B13 // PIN_B15 //
#use rs232(UART1, BAUD = 9600, XMIT = PIN_B13, RCV = PIN_B12)

#PIN_SELECT INT1 = PIN_B5
#PIN_SELECT INT2 = PIN_B6


#define DEVICE_ID 2

long count = 0;
long direction = 0;
char array[20] = {};
char SM_id = 0;
int getPackage = 0;
char command_ID;
int posi = 0;
// char* print_float(float data){
// 	long intDist = data / 1;
//     long dotDist = (((intDist>>31)*-2)+1) * ((data * 1000.0f) - (intDist *
//     1000));
//     char stringFloat[20];
//     sprintf(stringFloat, "%d.%d", intDist, dotDist);
//     return stringFloat;
// }
// void print_float(char* stringResult, float data){
// 	long intDist = data / 1;
//     long dotDist = (((intDist>>31)*-2)+1) * ((data * 1000.0f) - (intDist *
//     1000));
//     sprintf(stringResult, "%d.%d", intDist, dotDist);
// }

//Encoder Interrupts

//


// Communication Routines

void SM_RxD(int c) {
  if (getPackage == 0) {
    if (SM_id < 2) {
      if (c == 255) {
        array[SM_id] = c;
        SM_id++;
      } else {
        SM_id = 0;
      }
    } else if (SM_id == 2) {
      array[SM_id] = c;
      command_ID = c;
      SM_id++;
    } else if (SM_id > 2) {
      array[SM_id] = c;
      if (SM_id >= 8) {
        getPackage = 1;
        SM_id = 0;
      } else {
        SM_id++;
      }
    }
  }
}

#INT_RDA // receive data interrupt one time per one
void UART1_Isr() {
  int c = getc();
  // putc(c);
  SM_RxD(c);
}

// COMMANDS//
void setHome() {
  printf("done");
  getPackage = 0;
}

void setPosAB() {
  printf("done");
  getPackage = 0;
}

void setPosZ() {
  printf("done");
  getPackage = 0;
}

void gripClose(){
  printf("done");
  getPackage = 0;
}

void gripOpen(){
  printf("done");
  getPackage = 0;
}

void gripRotate(){
  printf("done");
  getPackage = 0;
}

int sumCheck() {
  int sum = 0;
  int checksum = array[8];
  for (int i = 0; i < 7; i++) {
    sum = sum + array[i];
  }
  if (sum == checksum) {
    return 1;
  } else {
    return 0;
  }
}

//
void main() {
  disable_interrupts(GLOBAL);

  clear_interrupt(
      INT_RDA); // recommend style coding to confirm everything clear before use
  enable_interrupts(INT_RDA);

  enable_interrupts(GLOBAL);
  // printf("System Ready!\r\n");
  while (TRUE) {
    if (getPackage >= 1) {
      int received = sumCheck();
      if (!received) {
        printf("resend");
        getPackage = 0;
      } else {
        switch (array[2]) {
        case 0:
          setHome();
          break;
        case 1:
          setPosAB();
          break;
        case 2:
          setPosZ();
          break;
        case 3:
          gripClose();
          break;
        case 4:
          gripOpen();
          break;
        case 5:
          gripRotate();
          break;
        default:
          printf("resend");
          getPackage = 0;
          break;
        }
      }
    }
  }
}
