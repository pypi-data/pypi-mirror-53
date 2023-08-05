import elist.elist as elel

def get_all_easciis():
    return(elel.join(elel.mapv(elel.init_range(0,256,1),chr),''))

def is_valid_attr_init_char(ch):
    '''
        this is a little trick
    '''
    class tst():
        pass
    t = tst()
    cds = "t."+ch+"=0"
    try:
        cd = compile(cds,'','exec')
        exec(cd)
    except Exception as err:
        return(False)
    else:
        return(True)


def is_valid_attr_noninit_char(ch):
    '''
        this is a little trick
    '''
    class tst():
        pass
    t = tst()
    cds = "t._"+ch+"=0"
    try:
        cd = compile(cds,'','exec')
        exec(cd)
        cds = "t._"+ch
        cd = compile(cds,'','exec')
        exec(cd)
    except:
        return(False)
    else:
        return(True)

def get_all_valid_attr_init_char(s):
    chs = elel.cond_select_values_all(s,cond_func=is_valid_attr_init_char)
    return(elel.join(chs,''))

def get_all_valid_attr_noninit_char(s):
    chs = elel.cond_select_values_all(s,cond_func=is_valid_attr_noninit_char)
    try:
        chs.remove("\t")
        chs.remove(" ")
        chs.remove("\x0c")
    except:
        pass
    else:
        pass
    rslt = elel.join(chs,'')
    return(rslt)





eascii = get_all_easciis()
ascii_valid_attrname_init_char = get_all_valid_attr_init_char(eascii)
ascii_valid_attrname_noninit_char = get_all_valid_attr_noninit_char(eascii)

greece_chname = ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta', 'iota', 'kappa', 'lambda', 'mu', 'nu', 'xi', 'omicron', 'pi', 'rho', 'sigma', 'tau', 'upsilon', 'phi', 'chi', 'psi', 'omega']
greece_lowerch = 'αβγδεζηθικλμνξοπρστυφχψω'
greece_lowerch_ord = [945, 946, 947, 948, 949, 950, 951, 952, 953, 954, 955, 956, 957, 958, 959, 960, 961, 963, 964, 965, 966, 967, 968, 969]
greece_upperch = 'ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ'
greece_upperch_ord = [913, 914, 915, 916, 917, 918, 919, 920, 921, 922, 923, 924, 925, 926, 927, 928, 929, 931, 932, 933, 934, 935, 936, 937]


greece_name2ch = {'alpha': 'α', 'beta': 'β', 'gamma': 'γ', 'delta': 'δ', 'epsilon': 'ε', 'zeta': 'ζ', 'eta': 'η', 'theta': 'θ', 'iota': 'ι', 'kappa': 'κ', 'lambda': 'λ', 'mu': 'μ', 'nu': 'ν', 'xi': 'ξ', 'omicron': 'ο', 'pi': 'π', 'rho': 'ρ', 'sigma': 'σ', 'tau': 'τ', 'upsilon': 'υ', 'phi': 'φ', 'chi': 'χ', 'psi': 'ψ', 'omega': 'ω'}


greech_ch2name = {'α': 'alpha', 'β': 'beta', 'γ': 'gamma', 'δ': 'delta', 'ε': 'epsilon', 'ζ': 'zeta', 'η': 'eta', 'θ': 'theta', 'ι': 'iota', 'κ': 'kappa', 'λ': 'lambda', 'μ': 'mu', 'ν': 'nu', 'ξ': 'xi', 'ο': 'omicron', 'π': 'pi', 'ρ': 'rho', 'σ': 'sigma', 'τ': 'tau', 'υ': 'upsilon', 'φ': 'phi', 'χ': 'chi', 'ψ': 'psi', 'ω': 'omega'}


greece_md = {'alpha': 'α', 'beta': 'β', 'gamma': 'γ', 'delta': 'δ', 'epsilon': 'ε', 'zeta': 'ζ', 'eta': 'η', 'theta': 'θ', 'iota': 'ι', 'kappa': 'κ', 'lambda': 'λ', 'mu': 'μ', 'nu': 'ν', 'xi': 'ξ', 'omicron': 'ο', 'pi': 'π', 'rho': 'ρ', 'sigma': 'σ', 'tau': 'τ', 'upsilon': 'υ', 'phi': 'φ', 'chi': 'χ', 'psi': 'ψ', 'omega': 'ω', 'α': 'alpha', 'β': 'beta', 'γ': 'gamma', 'δ': 'delta', 'ε': 'epsilon', 'ζ': 'zeta', 'η': 'eta', 'θ': 'theta', 'ι': 'iota', 'κ': 'kappa', 'λ': 'lambda', 'μ': 'mu', 'ν': 'nu', 'ξ': 'xi', 'ο': 'omicron', 'π': 'pi', 'ρ': 'rho', 'σ': 'sigma', 'τ': 'tau', 'υ': 'upsilon', 'φ': 'phi', 'χ': 'chi', 'ψ': 'psi', 'ω': 'omega'}




