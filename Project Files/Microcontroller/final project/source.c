#include "NU32.h"
#define ARRAYSIZE 10000

static volatile unsigned int i = 0;
static volatile unsigned int reset = 0;
static volatile unsigned int done_populating = 0;
static volatile unsigned int populate_notes = 1;
static volatile unsigned int actual_array_size = 0;
static volatile unsigned int notes[ARRAYSIZE] = {};
static volatile unsigned int times[ARRAYSIZE] = {};

void __ISR(_UART_3_VECTOR, IPL6SRS) UartISR(void) {
  IFS1bits.U3RXIF = 0;

  unsigned int data = 0;
  data = (data | U3RXREG) << 8;
  data = (data | U3RXREG) << 8;
  data = (data | U3RXREG) << 8;
  data = data | U3RXREG;

  if (data == 0xFFFFFFFF) {
    done_populating = 1;
    i = 0;
  }
  else if (data == 0xFFFFFFFE) {
    populate_notes = 0;
    actual_array_size = i;
    i = 0;
  }
  else if (data == 0xFFFFFFFD) {
    T2CONbits.ON = !T2CONbits.ON;
  }
  else if (data == 0xFFFFFFFC) {
    reset = 1;
  }
  else if (populate_notes) {
    notes[i++] = data;
  }
  else {
    times[i++] = data;
  }
}

int main(void) {
  NU32_Startup();

  TRISBCLR = 0xFFFF;
  TRISCCLR = 0xFFFF;
  TRISDCLR = 0xFFFF;
  TRISECLR = 0xFFFF;
  TRISFCLR = 0xFFFF;
  LATBCLR = 0xFFFF;
  LATCCLR = 0xFFFF;
  LATDCLR = 0xFFFF;
  LATECLR = 0xFFFF;
  LATFCLR = 0xFFFF;

  __builtin_disable_interrupts();
  U3STAbits.URXISEL = 1;
  IFS1bits.U3RXIF = 0;
  IPC7bits.U3IP = 6;
  IEC1bits.U3RXIE = 1;

  T2CONbits.T32 = 1;
  T2CONbits.TCKPS = 7;
  T2CONbits.ON = 1;
  __builtin_enable_interrupts();

  int j = 0;

  loop:
    NU32_LED2 = 1;
    while (!done_populating) {
      ;
    }
    NU32_LED2 = 0;

    reset = 0;
    TMR2 = 0;
    T2CONbits.ON = 1;

    while (1) {
      if (TMR2 > times[i]) {
        LATBSET = (0x0FFF & (notes[i] >> 16)) | ((notes[i] << 10) & 0xF000);
        LATCSET = notes[i] << 7;
        LATDSET = notes[i] >> 8;
        LATESET = notes[i] >> 24;
        LATFSET = notes[i] << 4;

        for (j = 0; j < 500000; j++) {
          _nop();
        }

        LATBCLR = 0xFFFF;
        LATCCLR = 0xFFFF;
        LATDCLR = 0xFFFF;
        LATECLR = 0xFFFF;
        LATFCLR = 0xFFFF;

        if ((++i == actual_array_size) || (reset)) {
          if (!reset) {
            U3TXREG = 0xFF;
          }
          i = 0;
          done_populating = 0;
          populate_notes = 1;
          goto loop;
        }
      }

      else if (reset) {
        i = 0;
        done_populating = 0;
        populate_notes = 1;
        goto loop;
      }
    }
}
