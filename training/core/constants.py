# -*- coding: utf-8 -*-
from collections import namedtuple

Area = namedtuple('Area', ['codename', 'name', 'code'])


class State:
    ATLANTIDA = Area(codename='atlantida', name='Atlántida', code='01')
    COLON = Area(codename='colon', name='Colón', code='02')
    COMAYAGUA = Area(codename='comayagua', name='Comayagua', code='03')
    COPAN = Area(codename='copan', name='Copán', code='04')
    CORTES = Area(codename='cortes', name='Cortés', code='05')
    CHOLUTECA = Area(codename='choluteca', name='Choluteca', code='06')
    EL_PARAISO = Area(codename='el_paraiso', name='El Paraíso', code='07')
    FRANCISCO_MORAZAN = Area(codename='francisco_morazan', name='Francisco Morazán', code='08')
    GRACIAS_A_DIOS = Area(codename='gracias_a_dios', name='Gracias a Dios', code='09')
    INTIBUCA = Area(codename='intibuca', name='Intibucá', code='10')
    ISLAS_DE_LA_BAHIA = Area(codename='islas_de_la_bahia', name='Islas de la Bahía', code='11')
    LA_PAZ = Area(codename='la_paz', name='La Paz', code='12')
    LEMPIRA = Area(codename='lempira', name='Lempira', code='13')
    OCOTEPEQUE = Area(codename='ocotepeque', name='Ocotepeque', code='14')
    OLANCHO = Area(codename='olancho', name='Olancho', code='15')
    SANTA_BARBARA = Area(codename='santa_barbara', name='Santa Bárbara', code='16')
    VALLE = Area(codename='valle', name='Valle', code='17')
    YORO = Area(codename='yoro', name='Yoro', code='18')

    CHOICES = (
        (ATLANTIDA.code, ATLANTIDA.name),
        (COLON.code, COLON.name),
        (COMAYAGUA.code, COMAYAGUA.name),
        (COPAN.code, COPAN.name),
        (CORTES.code, CORTES.name),
        (CHOLUTECA.code, CHOLUTECA.name),
        (EL_PARAISO.code, EL_PARAISO.name),
        (FRANCISCO_MORAZAN.code, FRANCISCO_MORAZAN.name),
        (GRACIAS_A_DIOS.code, GRACIAS_A_DIOS.name),
        (INTIBUCA.code, INTIBUCA.name),
        (ISLAS_DE_LA_BAHIA.code, ISLAS_DE_LA_BAHIA.name),
        (LA_PAZ.code, LA_PAZ.name),
        (LEMPIRA.code, LEMPIRA.name),
        (OCOTEPEQUE.code, OCOTEPEQUE.name),
        (OLANCHO.code, OLANCHO.name),
        (SANTA_BARBARA.code, SANTA_BARBARA.name),
        (VALLE.code, VALLE.name),
        (YORO.code, YORO.name)
    )
