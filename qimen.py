G='甲乙丙丁戊己庚辛壬癸';Z='子丑寅卯辰巳午未申酉戌亥';Y='戊己庚辛壬癸丁丙乙';RING=[1,8,3,4,9,2,7,6]
ST={1:'天蓬',8:'天任',3:'天冲',4:'天辅',9:'天英',2:'天芮',7:'天柱',6:'天心'}
DO={1:'休',8:'生',3:'伤',4:'杜',9:'景',2:'死',7:'惊',6:'开'}
def rotating(sign,ju,hour):
    earth={((ju-1+sign*i)%9)+1:s for i,s in enumerate(Y)}
    hi=next(i for i in range(60) if G[i%10]+Z[i%12]==hour);xg=Y[hi//10]
    cp=next(p for p,s in earth.items() if s==xg);origin=2 if cp==5 else cp
    hs=xg if hour[0]=='甲' else hour[0];raw=next(p for p,s in earth.items() if s==hs);target=2 if raw==5 else raw
    sh=(RING.index(target)-RING.index(origin))%8
    sky={RING[(RING.index(p)+sh)%8]:[earth[p]]+([earth[5]] if p==2 else []) for p in RING}
    stars={RING[(RING.index(p)+sh)%8]:[ST[p]]+(['天禽'] if p==2 else []) for p in RING}
    draw=(cp-1+sign*(hi%10))%9+1;dest=2 if draw==5 else draw
    ds=(RING.index(dest)-RING.index(origin))%8
    doors={RING[(RING.index(p)+ds)%8]:DO[p] for p in RING}
    gods={RING[(RING.index(target)+sign*i)%8]:s for i,s in enumerate(['值符','腾蛇','太阴','六合','白虎','玄武','九地','九天'])}
    return dict(earth=earth,sky=sky,stars=stars,doors=doors,gods=gods,chief_from_numeric=cp,chief_from_projected=origin,chief_to=target,chief_door=DO[origin],chief_door_to=dest,chief_star='天禽' if cp==5 else ST[cp],xun_index=hi//10*10,hour_index=hi,xun_hidden=xg)
