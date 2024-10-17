#!/usr/bin/env python3o

"""
Calcualates required mic. gain

See amplifier-amp5.webp
"""

import math


def calculation_profile_1():
    """
    Calculate parameters given a certain gain value
    """
    # Parameters
    delta_v_in = 1e-2  # Capsule mic. oscillation amplitude, [V]
    delta_v_out = 1.65  # Required output, [V]
    r_l = 1e3  # Resistor RE value, [ohm]. Let's just use some arbitrary value
    v_e = 1.65  # We need the mic output to oscillate around 1.65 [V], 'coz the MCU's VCC is 3.3V
    v_cc = 3.3
    v_ee = 25e-3

    print("Let:", '\n' + '\n'.join(map(lambda i: str(i[0]) + ' = ' + str(i[1]), locals().items())))

    # calc max current [A]
    i_max = (v_cc - v_e) / r_l
    # Quiescent current is .5 point on the load line, i.e. the same, but Voltage / 2. Simplify calculations
    i_q = i_max / 2
    print("Quiescent current:", i_q)

    gain = delta_v_out / delta_v_in
    print("gain", gain)
    # gain = -r_e / (r_ee + r_e), where r_e -- thermal resistance of the
    # transistor. In the datasheet for 2n2222, internal BE resistance is
    # r_ee = 25[mV] / i_e.
    # i_e is i_q, the current we let through the transistor.
    r_ee = v_ee / i_q
    print("Internal transistor BE impedance:", r_ee)
    r_e = r_l / gain - r_ee
    print("R_E resistor value:", r_e)


if __name__ == "__main__":
    calculation_profile_1()

