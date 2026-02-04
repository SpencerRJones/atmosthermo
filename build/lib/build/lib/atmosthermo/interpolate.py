import numpy as np
from scipy.interpolate import interp1d

def interpolate(var, old_hgt, new_hgt, kind='linear'):
    '''
    Interpolates `var` defined on `old_hgt` to `new_hgt`.

    kind = 'linear' or 'log' for interpolation of variables in log space.
    '''

    assert var.size == old_hgt.size

    var = np.asarray(var)
    old_hgt = np.asarray(old_hgt)
    new_hgt = np.asarray(new_hgt)

    if kind == 'log':
        interp_func = interp1d(old_hgt, np.log(var), bounds_error=False, fill_value='extrapolate')
        new_var = np.exp(interp_func(new_hgt))
    else:
        interp_func = interp1d(old_hgt, var, bounds_error=False, fill_value='extrapolate')
        new_var = interp_func(new_hgt)

    return new_var

#Below is old code that was unstable in some scenarios
#def interpolate(var, old_hgt, new_hgt, kind='linear'):
#
#    '''
#    Linear or logarithmic interpolation routine
#    for subdividing layers
#    '''
#
#    nlevs_new = new_hgt.size
#
#    new_var = np.zeros(nlevs_new, dtype='f')
#
#    j = 0
#
#    if kind == 'log':
#        var = np.log(var)
#
#    for i in range(nlevs_new):
#
#        ihgt = new_hgt[i]
#
#        if ihgt == 0.:
#            new_var[i] = var[0]
#            continue
#
#        if ihgt >= old_hgt[-1]:
#            new_var[i] = var[-1]
#            continue
#
#        j = np.where(ihgt < old_hgt)[0][0]
#
#        up_bound = old_hgt[j]
#        lo_bound = old_hgt[j-1]
#
#        #print(lo_bound, ihgt, up_bound, i,j, ihgt, old_hgt[j])
#
#        if ihgt == up_bound:
#            new_var[i] = var[j-1]
#            continue
#        if ihgt == lo_bound:
#            new_var[i] = var[j]
#            continue
#
#        w1 = 1./np.abs(ihgt - up_bound)
#        w2 = 1./np.abs(ihgt - lo_bound)
#        new_var[i] = ((var[j] * w1) + (var[j-1] * w2)) / (w1 + w2)
#
#    if kind == 'log':
#        new_var = np.exp(new_var)
#
#    return new_var
