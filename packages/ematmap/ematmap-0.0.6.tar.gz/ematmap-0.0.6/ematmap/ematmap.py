import efuntool.efuntool as eftl


def _get_fo(x,y,**kwargs):
    map_func = eftl.dflt_kwargs("map_func",lambda ele:ele,**kwargs)
    other_args = eftl.dflt_kwargs("other_args",[],**kwargs)
    map_func_mat = eftl.dflt_kwargs("map_func_mat",None,**kwargs)
    other_args_mat = eftl.dflt_kwargs("other_args_mat",None,**kwargs)
    if(map_func_mat == None):
        pass
    else:
        map_func = map_func_mat[x][y]
    if(other_args_mat == None):
        pass
    else:
        other_args = other_args_mat[x][y]
    return((map_func,other_args))


@eftl.deepcopy_wrapper
def _map(func):
    def wrapper(m,**kwargs):
        lngth = len(m)
        for x in range(lngth):
            layer = m[x]
            llen = len(layer)
            for y in range(llen):
                map_func,other_args = _get_fo(x,y,**kwargs)
                m[x][y] = func({
                    "f":map_func,
                    "x":x,
                    "y":y,
                    "o":other_args,
                    "m":m
                })
        return(m)
    return(wrapper)


@_map
def mapf(d):
    m = d['m']
    map_func = d['f']
    other_args = d['o']
    x = d['x']
    y = d['y']
    v = m[x][y]
    ele = map_func(*other_args)
    return(ele)



@_map
def mapx(d):
    m = d['m']
    map_func = d['f']
    other_args = d['o']
    x = d['x']
    y = d['y']
    v = m[x][y]
    ele = map_func(x,*other_args)
    return(ele)



@_map
def mapy(d):
    m = d['m']
    map_func = d['f']
    other_args = d['o']
    x = d['x']
    y = d['y']
    v = m[x][y]
    ele = map_func(y,*other_args)
    return(ele)



@_map
def mapv(d):
    m = d['m']
    map_func = d['f']
    other_args = d['o']
    x = d['x']
    y = d['y']
    v = m[x][y]
    ele = map_func(v,*other_args)
    return(ele)



@_map
def mapo(d):
    m = d['m']
    map_func = d['f']
    other_args = d['o']
    x = d['x']
    y = d['y']
    v = m[x][y]
    ele = map_func(*other_args)
    return(ele)



@_map
def mapfx(d):
    m = d['m']
    map_func = d['f']
    other_args = d['o']
    x = d['x']
    y = d['y']
    v = m[x][y]
    ele = map_func(x,*other_args)
    return(ele)



@_map
def mapfy(d):
    m = d['m']
    map_func = d['f']
    other_args = d['o']
    x = d['x']
    y = d['y']
    v = m[x][y]
    ele = map_func(y,*other_args)
    return(ele)



@_map
def mapfv(d):
    m = d['m']
    map_func = d['f']
    other_args = d['o']
    x = d['x']
    y = d['y']
    v = m[x][y]
    ele = map_func(v,*other_args)
    return(ele)



@_map
def mapfo(d):
    m = d['m']
    map_func = d['f']
    other_args = d['o']
    x = d['x']
    y = d['y']
    v = m[x][y]
    ele = map_func(o,*other_args)
    return(ele)



@_map
def mapxy(d):
    m = d['m']
    map_func = d['f']
    other_args = d['o']
    x = d['x']
    y = d['y']
    v = m[x][y]
    ele = map_func(x,y,*other_args)
    return(ele)



@_map
def mapxv(d):
    m = d['m']
    map_func = d['f']
    other_args = d['o']
    x = d['x']
    y = d['y']
    v = m[x][y]
    ele = map_func(x,v,*other_args)
    return(ele)



@_map
def mapxo(d):
    m = d['m']
    map_func = d['f']
    other_args = d['o']
    x = d['x']
    y = d['y']
    v = m[x][y]
    ele = map_func(x,*other_args)
    return(ele)



@_map
def mapyv(d):
    m = d['m']
    map_func = d['f']
    other_args = d['o']
    x = d['x']
    y = d['y']
    v = m[x][y]
    ele = map_func(y,v,*other_args)
    return(ele)



@_map
def mapyo(d):
    m = d['m']
    map_func = d['f']
    other_args = d['o']
    x = d['x']
    y = d['y']
    v = m[x][y]
    ele = map_func(y,*other_args)
    return(ele)



@_map
def mapvo(d):
    m = d['m']
    map_func = d['f']
    other_args = d['o']
    x = d['x']
    y = d['y']
    v = m[x][y]
    ele = map_func(v,*other_args)
    return(ele)



@_map
def mapfxy(d):
    m = d['m']
    map_func = d['f']
    other_args = d['o']
    x = d['x']
    y = d['y']
    v = m[x][y]
    ele = map_func(x,y,*other_args)
    return(ele)



@_map
def mapfxv(d):
    m = d['m']
    map_func = d['f']
    other_args = d['o']
    x = d['x']
    y = d['y']
    v = m[x][y]
    ele = map_func(x,v,*other_args)
    return(ele)



@_map
def mapfxo(d):
    m = d['m']
    map_func = d['f']
    other_args = d['o']
    x = d['x']
    y = d['y']
    v = m[x][y]
    ele = map_func(x,o,*other_args)
    return(ele)



@_map
def mapfyv(d):
    m = d['m']
    map_func = d['f']
    other_args = d['o']
    x = d['x']
    y = d['y']
    v = m[x][y]
    ele = map_func(y,v,*other_args)
    return(ele)



@_map
def mapfyo(d):
    m = d['m']
    map_func = d['f']
    other_args = d['o']
    x = d['x']
    y = d['y']
    v = m[x][y]
    ele = map_func(y,o,*other_args)
    return(ele)



@_map
def mapfvo(d):
    m = d['m']
    map_func = d['f']
    other_args = d['o']
    x = d['x']
    y = d['y']
    v = m[x][y]
    ele = map_func(v,o,*other_args)
    return(ele)



@_map
def mapxyv(d):
    m = d['m']
    map_func = d['f']
    other_args = d['o']
    x = d['x']
    y = d['y']
    v = m[x][y]
    ele = map_func(x,y,v,*other_args)
    return(ele)



@_map
def mapxyo(d):
    m = d['m']
    map_func = d['f']
    other_args = d['o']
    x = d['x']
    y = d['y']
    v = m[x][y]
    ele = map_func(x,y,*other_args)
    return(ele)



@_map
def mapxvo(d):
    m = d['m']
    map_func = d['f']
    other_args = d['o']
    x = d['x']
    y = d['y']
    v = m[x][y]
    ele = map_func(x,v,*other_args)
    return(ele)



@_map
def mapyvo(d):
    m = d['m']
    map_func = d['f']
    other_args = d['o']
    x = d['x']
    y = d['y']
    v = m[x][y]
    ele = map_func(y,v,*other_args)
    return(ele)



@_map
def mapfxyv(d):
    m = d['m']
    map_func = d['f']
    other_args = d['o']
    x = d['x']
    y = d['y']
    v = m[x][y]
    ele = map_func(x,y,v,*other_args)
    return(ele)



@_map
def mapfxyo(d):
    m = d['m']
    map_func = d['f']
    other_args = d['o']
    x = d['x']
    y = d['y']
    v = m[x][y]
    ele = map_func(x,y,o,*other_args)
    return(ele)



@_map
def mapfxvo(d):
    m = d['m']
    map_func = d['f']
    other_args = d['o']
    x = d['x']
    y = d['y']
    v = m[x][y]
    ele = map_func(x,v,o,*other_args)
    return(ele)



@_map
def mapfyvo(d):
    m = d['m']
    map_func = d['f']
    other_args = d['o']
    x = d['x']
    y = d['y']
    v = m[x][y]
    ele = map_func(y,v,o,*other_args)
    return(ele)



@_map
def mapxyvo(d):
    m = d['m']
    map_func = d['f']
    other_args = d['o']
    x = d['x']
    y = d['y']
    v = m[x][y]
    ele = map_func(x,y,v,*other_args)
    return(ele)



@_map
def mapfxyvo(d):
    m = d['m']
    map_func = d['f']
    other_args = d['o']
    x = d['x']
    y = d['y']
    v = m[x][y]
    ele = map_func(x,y,v,o,*other_args)
    return(ele)


#################

#ox orig_x
#oy orig_y

#rcrdize         recordize

def rcrdize(m):
    map_func = lambda x,y,v:{"_ox":x,"_oy":y,"_v":v}
    nm = mapxyv(m,map_func=map_func)
    return(nm)

def unrcrdize_x(nm):
    map_func = lambda v:v["_ox"]
    om = mapv(nm,map_func=map_func)
    return(om)

def unrcrdize_y(nm):
    map_func = lambda v:v["_oy"]
    om = mapv(nm,map_func=map_func)
    return(om)

def unrcrdize_v(nm):
    map_func = lambda v:v["_v"]
    om = mapv(nm,map_func=map_func)
    return(om)


def rcrdize_wrapper(f):
    '''
        the data is already wrapped as 
        {
            "_ox":ox,
            "_oy":oy,
            "_v":ov
        }
        so the old map_func  should be wrapped
    '''
    def wrapper(*args,**kwargs):
        mode = dflt_kwargs("mode","v",**kwargs)
        mode = ''.join(list(filter(lambda ele:(ele in "xyv"),mode)))
        which = mode.index("v")
        v = args[which]
        nv = v["_v"]
        ox = v["_ox"]
        oy = v["_oy"]
        args[which] = nv
        nv = f(*args)
        return({
            "_ox":ox,
            "_oy":oy,
            "_v":nv
        })




