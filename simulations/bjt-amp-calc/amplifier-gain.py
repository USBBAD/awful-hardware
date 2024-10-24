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


def calc2():
    beta = 200
    v0 = 1.65
    gain = 100
    vcc = 3.3
    ic = 1e-3
    vc = 1.65
    v_be = 0.7
    print("Let:", '\n' + '\n'.join(map(lambda i: str(i[0]) + ' = ' + str(i[1]), locals().items())))
    print()
    exclude_locals = set(locals().keys())

    #rth = r1 * r2 / (r1 + r2)
    #print("if rth = (1 + beta) * re / 10, given re =", re, "by-the-book rth would be", (1 + beta) * re / 10)

    rc = vc / ic
    re = rc / gain
    ib = ic / beta
    ie = (1 + beta) * ib

    # voltage on R2
    v2 = v_be + ie * re
    v1 = vcc - v2
    ve = ie * re
    vth = v_be + ve
    r1 = vcc / vth

    lcs = {k: v for k, v in locals().items() if k not in exclude_locals and k not in {'exclude_locals', 'lcs'}}
    print("Result:", '\n' + '\n'.join(map(lambda i: str(i[0]) + ' = ' + str(i[1]), lcs.items())))


if __name__ == "__main__":
    calc2()

