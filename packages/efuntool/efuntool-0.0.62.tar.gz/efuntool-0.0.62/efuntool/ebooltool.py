import efuntool.efuntool as eftl
import dtable.dtable as dtdt
import itertools
import elist.elist as elel
#1-1 
#1-2
def blnot(p,*args):
    count = args[0] if(len(args)==0) else 1
    cond = not(p) if( (count%2) == 1) else p
    return(cond)

def identity(o0,o1):
    cond0 = (type(o0) == type(o1))
    cond1 = (o0 == o1)
    return((cond0 and cond1))

def is_zero_len(value):
    try:
        rslt = (len(value)==0)
    except:
        return(False)
    else:
        return(rslt)


def is_fls(value,*args):
    if(len(args)==0 or args[0] == []):
        rslt = True if(identity(value,0) or identity(value,False) or (value == None) or is_zero_len(value) ) else False
        return(rslt)
    else:
        flses = args[0]
        for i in range(len(flses)):
            if(identity(value,flses[i])):
                return(True)
            else:
                pass
        return(False)


def bland(*args,**kwargs):
    base = eftl.dflt_kwargs('base',True,**kwargs)
    flses = eftl.dflt_kwargs('flses',[],**kwargs)
    for i in range(len(args)):
        cond = False if(is_fls(args[i],flses)) else True
        base = (base and cond)
    return(base)


def blor(*args,**kwargs):
    base = eftl.dflt_kwargs('base',False,**kwargs)
    flses = eftl.dflt_kwargs('flses',[],**kwargs)
    for i in range(len(args)):
        cond = False if(is_fls(args[i],flses)) else True
        base = (base or cond)
    return(base)


def bland_rtrn_last(*args,**kwargs):
    base = eftl.dflt_kwargs('base',True,**kwargs)
    flses = eftl.dflt_kwargs('flses',[],**kwargs)
    for i in range(len(args)):
        cond = False if(is_fls(args[i],flses)) else True
        if(cond):
            base = args[i]
        else:
            return(False)
    return(base)


def blor_rtrn_first(*args,**kwargs):
    base = eftl.dflt_kwargs('base',False,**kwargs)
    flses = eftl.dflt_kwargs('flses',[],**kwargs)
    for i in range(len(args)):
        cond = False if(is_fls(args[i],flses)) else True
        if(cond):
            base = args[i]
            break
        else:
            pass
    return(base)


def scond(p,q):
    return(not(p) or q)

def dcond(p,q):
    return(scond(p,q) and scond(q,p))

def blxor(p,q):
    return(not(dcond(p,q)))

#1-3
#1-4
#1-5
#ifnt           ifnot


def product(l,repeat=2,**kwargs):
    st = eftl.dflt_kwargs("sort",False,**kwargs) 
    rslt = itertools.product(l,repeat=repeat)
    rslt = list(rslt)
    rslt = elel.mapv(rslt,list,[])
    rslt = elel.mapv(rslt,sorted,[]) if(st) else rslt
    return(rslt)




def permutate(l,repeat=2,**kwargs):
    st = eftl.dflt_kwargs("sort",False,**kwargs)
    rslt = [each for each in itertools.permutations(l,repeat)]
    rslt = list(rslt)
    rslt = elel.mapv(rslt,list,[])
    rslt = elel.mapv(rslt,sorted,[]) if(st) else rslt
    return(rslt)

def permutate_all(l,*args,**kwargs):
    '''
        >>> permutate_all(['a','b','c'])
        [[], ['a'], ['b'], ['c'], ['a', 'b'], ['a', 'c'], ['a', 'b'], ['b', 'c'], ['a', 'c'], ['b', 'c'], ['a', 'b', 'c'], ['a', 'b', 'c'], ['a', 'b', 'c'], ['a', 'b', 'c'], ['a', 'b', 'c'], ['a', 'b', 'c']]
        >>>
    '''
    lngth = (len(l)+1) if (len(args)==0) else args[0]
    rslt = []
    for i in range(lngth):
        tmp = permutate(l,repeat=i,**kwargs)
        rslt.extend(tmp)
    return(rslt)



def combinate(l,repeat=2,**kwargs):
    st = eftl.dflt_kwargs("sort",False,**kwargs)
    rslt = [each for each in itertools.combinations(l,repeat)]
    rslt = list(rslt)
    rslt = elel.mapv(rslt,list,[])
    rslt = elel.mapv(rslt,sorted,[]) if(st) else rslt
    return(rslt)

def combinate_all(l,*args,**kwargs):
    '''
        >>> combinate_all(['a','b','c'])
        [[], ['a'], ['b'], ['c'], ['a', 'b'], ['a', 'c'], ['b', 'c'], ['a', 'b', 'c']]
        >>>
    '''
    lngth = (len(l)+1) if (len(args)==0) else args[0]
    rslt = []
    for i in range(lngth):
        tmp = combinate(l,repeat=i,**kwargs)
        rslt.extend(tmp)
    return(rslt)



def creat_tru_fls_mat(cnl,*args):
    rl = eftl.optional_arg([True,False],*args)
    count = len(cnl)
    m = product(rl,count)
    return(m)


def creat_tru_fls_dtb(cnl,*args):
    '''
        >>> cnl
        ['A', 'B', 'C']
        >>>
        >>> parr(creat_tru_fls_dtb(cnl))
        {'A': True, 'B': True, 'C': True, '@RSLT@': None}
        {'A': False, 'B': True, 'C': True, '@RSLT@': None}
        {'A': False, 'B': True, 'C': True, '@RSLT@': None}
        {'A': False, 'B': False, 'C': True, '@RSLT@': None}
        {'A': False, 'B': True, 'C': True, '@RSLT@': None}
        {'A': False, 'B': False, 'C': True, '@RSLT@': None}
        {'A': False, 'B': False, 'C': True, '@RSLT@': None}
        {'A': False, 'B': False, 'C': False, '@RSLT@': None}
        >>>
    '''
    dtb = dtdt.init_dtb(creat_tru_fls_mat(cnl),cnl)
    dtb = dtdt.add_col(dtb,"@RSLT@",elel.init(len(dtb),None))
    return(dtb)

    
# v          or
# ^          and
# ->         if P then Q else true 
# <-         if Q then P else true
# <->
# P=>Q       P->Q always true  求出真值表 然后选取结果 全是true的行
# P<=Q       Q->P always true  
# P<=>Q      


###################################
# 1-6

#if          if  
#ifnt        if-not
#thenfls     then-false
#thentru     then-true
#elfls       else-false
#eltru       else-true

#notp        notp
#notq        notq


def if_p_then_q_else_true(p,q):
    '''
        p->q
        not(p) or q
        或(非p)
        条件
    '''
    return(scond(p,q))

def notp_or_q(p,q):
    return(scond(p,q))

def parrowq(p,q):
    return(scond(p,q))

def if_p_then_q_else_notq(p,q):
    '''
        p<->q
        notporq_and_pornotq
        与(或(非p),或(非q))
        双向条件
    '''
    return(dcond(p,q))

def notporq_and_pornotq(p,q):
    return(dcond(p,q))



####
def if_p_then_notq_else_q(p,q):
    '''
        p^q
        pandnotq_or_notpandq
        异或
        not_dcond
        否定双向条件
    '''
    return(not(dcond(p,q)))

def pandnotq_or_notpandq(p,q):
    return(not(dcond(p,q)))

def not_dcond(p,q):
    return(not(dcond(p,q)))

####

def if_p_then_notq_else_false(p,q):
    '''
        非p-或-非 not(or(not(p),q))
        p_and_notq
        not_scond
        条件否定
    '''
    return(p and not(q))

def p_and_notq(p,q):
    return(p and not(q))

def not_scond(p,q):
    return(not(scond(p,q)))

####################################

def if_p_then_notq_else_true(p,q):
    '''
        与-非 not(and(p,q))
        notp_or_notq
        not_pandq
    '''
    return(not(p) or not(q))

def notp_or_notq(p,q):
    return(not(p) or not(q))

def not_pandq(p,q):
    return(not(p and q))

#####################################

def if_p_then_false_else_notq(p,q):
    '''
        或-非 not(or(p,q))
        notp_and_notq
    '''
    return(not(p) and not(q))

def notp_and_notq(p,q):
    return(not(p) and not(q))

def not_porq(p,q):
    return(not(p or q))





#######################################
