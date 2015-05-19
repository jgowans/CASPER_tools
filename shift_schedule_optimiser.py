#!/usr/bin/env python

import logging

class ShiftSheduleOptimiser:
    def __init__(self, shift_reg, fft_stages, overflow_reg, fpga, re_sync=None, logger=logging.getLogger()):
        """ Create a Shift Schedule Optimiser instance.

        Parameters:
        shift_reg_name : string
            Name of register which controlls shifting
        fft_stages : int
            The number of stages INSIDE the FFT block.
            This is typicall two less than the number of FFT points. 
        overflow_reg : string
            name of register which has its bit0 checked for overflow
        fpga : corr.katcp_wrapper.FgpaClient
            Interface to the FPGA
        re_sync : function, optional
            function to call for re-sync. If None, a re-sync will not be done
        logger : logger
        """
        logging.basicConfig()
        self.shift_reg = shift_reg
        self.fft_stages = fft_stages
        self.overflow_reg = overflow_reg
        self.fpga = fpga
        self.re_sync = re_sync
        self.logger = logger

    def find_optimal(self):
        # set all bits to 1
        self.optimal = 2**(self.fft_stages) - 1
        self.write_shift(self.optimal)
        # itteratively try to clear bits
        for bit_idx in range(self.fft_stages - 1, -1, -1):  # range: [9, 8, 7, ..., 1, 0]
            self.optimal &= ~(1 << bit_idx)  # clear this bit
            self.write_shift(self.optimal)
            if (self.check_overflow()):  
                # oh no! That was bad. Set the bit back to 1
                self.optimal |= (1 << bit_idx)


    def write_shift(self, shift_val):
        """ Sets the shift schedule to a value passed in and
        re-syncs if possible
        """
        self.fpga.write_int(self.shift_reg, shift_val)
        loggin.debug("Shift value set to: {n}".format(n = shift_val))
        if self.re_sync != None:
            self.logger.debug("Doing a re-sync")
            self.re_sync()
        time.sleep(1)  # delay to allow effect to manifest.

    def check_overflow(self):
        """ Returns true if overflow has happened
        """
        # select lsb from overflow reg
        overflow_val = self.fpga.read_uint(self.overflow_reg) & 0x1
        if overflow_val != 0:
            self.logger.debug("Overflow flag is SET")
            return True
        self.logger.debug("Overflow flag is CLEAR")
        return False
        


