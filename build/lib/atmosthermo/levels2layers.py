import numpy as np

def levels2layers(data, lev_dim, method='linear'):

    '''
    Creates layered data from level data. Layer values are either
    standard or logarithmic mean value of level values.

    -------------------------------------- level 2

    layer variable = mean of level values

    -------------------------------------- level 1

    Inputs:
        data      | array of any shape
        lev_dim   | dimension of level variable
        method    | 'linear' or 'log' to specify type of mean to
                    take
    Outputs:
        lyrdata   | array of original shape except for level dim,
                    which is nlayers = nlevs - 1.
    '''

    dims = data.shape

    nlevs = dims[lev_dim]
    nlyrs = nlevs - 1

    shape = np.array(dims)
    shape[lev_dim] = shape[lev_dim] - 1

    lyrdata = np.zeros(shape, dtype=data.dtype)
    stackeddata = lyrdata[np.newaxis,:]
    stackeddata = np.concat((stackeddata,stackeddata), axis=0)

    stackeddata[0,:] = np.take(data, range(nlyrs), axis=lev_dim)
    stackeddata[1,:] = np.take(data, range(1,nlevs), axis=lev_dim)

    if method == 'linear':
        lyrdata = np.mean(stackeddata, axis=0)
    elif method == 'log':
        close = np.isclose(stackeddata[0], stackeddata[1], rtol=1e-6, atol=1e-6)
        lyrdata[close]  = stackeddata[0,close]
        lyrdata[~close] = ((stackeddata[0,~close]-stackeddata[1,~close]) / 
                           (np.log(stackeddata[0,~close])-np.log(stackeddata[1,~close])))

    return lyrdata
