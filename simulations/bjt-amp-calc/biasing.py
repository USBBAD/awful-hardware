# https://www.youtube.com/watch?v=9325TKD4dfY

import copy

try:
    # BJT parameters
    v_ce_sat = 0.7 # CE on saturation
    ve_t = 26e-3 # thermal voltage
    hfe = 300 # BJT's beta
    vbe = 1.2 # Voltage drop "base-emitter"

    # Subject area parameters
    vcc = 3.3
    a = -10 # gain
    ic = 1e-3
    vce = vcc / 2

    # quiescent point
    i_sat = ic * 2

    re_t = ve_t  / ic # "Thermal" resistance
    rc = -a * re_t # Rc
    re = (vcc - v_ce_sat) / i_sat - rc
    assert(re > 0)

    # Choose R2
    # r2 <= hfe * re / 10
    # to prevent current from flowing into base
    # round r2 to 10ks
    r2_bound = hfe * re / 10
    precision = 1e4 # round to 10k
    r2 = r2_bound - (r2_bound % precision)
    assert (r2 > 0)

    # Calculate R1
    ve = ic * re # ie ~= ic
    assert(ve > 0)
    v2 = ve + vbe # V on R2
    assert(v2 > 0)
    v1 = vcc - v2
    # v1 / v2 = r1 / r2 => r1 = v1 * r2 / v2
    r1 = v1 * r2 / v2

    c = copy.copy(locals())
    for k, v in c.items():
        if not k.startswith('_'):
            print(f'{k}="{v}"')
except Exception as e:
    c = copy.copy(locals())
    for k, v in c.items():
        if not k.startswith('_'):
            print(f'{k}="{v}"')
    raise e
