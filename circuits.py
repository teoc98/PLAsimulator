﻿# -*- coding: utf-8 -*-
# ======================================================================================================= #
#
#   $Log: circuits.py,v $
#
#   Revision 3.3 2018/07/14  04:20:00  matteo
#	Aggiunti circuiti: moltiplicatore a 2 bit, riduttore 3-2, MLG, decoder 7 segmenti;
#	flip-flop tipo SR, tipo T e tipo JK; 
#
#  	Revision 3.1 2018/07/11  16:59:23  matteo
#   Aggiunto modello di circuito. Aggiunte funzioni generate_code e generate_obj
#	per creare circuti data una funzione logica. 
#
#   Revision 3.0  2018/07/10 16:32:51  matteo
#   Il programma è ora compatibile con Python3, oltre che con Python2. 
#
#   Revision 2.1  2012/07/29 15:55:06  alice
#   Il programma è stato reso eseguibile, e dotato di opzioni dalla riga di
#   comando. Sono inoltre state implementate ulteriori dipendenze di parametri
#   dimensionali in modo da rendere il simulatore ancor più371 ridimensionabile
#   automaticamente sulla base di dimensione orizzontale e numero di I/O/AND.
#
#   Revision 2.0  2012/06/13 14:00:59  alice
#   Commenti adattati al metalinguaggio epytext, per la generazione automatica della
#   documentazione.
#   
#   Revision 1.2  2012/06/08 08:48:55  alice
#   Modificata l'acquisizione della libreria per una massima flessibilità;
#   aggiunti tutti i circuiti disponibili sul testo Tanenbaum e altri.
#   
#   Revision 1.1  2012/06/06 07:54:09  alice
#   Completata l'aggiunta di circuiti da libreria, con possibilità di numero
#   arbitrario di input e output, purché entro quelli del PLA
#
# ======================================================================================================= #

"""
Libreria di circuiti predefiniti.
@authors: Alice Plebe, Matteo Cavallaro
@version: 3.0

@var circ_h: 1 bit half adder
@var circ_a: 1 bit full adder
@var circ_b: 2 bit adder
@var circ_mult2: 2 bit multiplicator
@var circ_mlg: multiple logic gate
@var circ_e: priority encoder
@var circ_m: multiplexer
@var circ_g: majority
@var circ_d: decoder
@var circ_s: shift register
@var circ_c: comparator
@var circ_r32: reductor 3-2
@var circ_bcd: decoder 7 segmenti
@var circ_sr: one step flip-flop sr
@var circ_t: one step flip-flop t
@var circ_jk: one step flip-flop jk
@var circ_compl1: 6-bit ones' complement
@var circ_pc: parity check
@var circ_crc3: crc-3-gsm
@var circ_compl2: 4-bit two' complement
@var circ_sqrt: 6 bit square root floor
@var circs: lista dei circuiti predefiniti disponibili nella libreria
"""

from __future__ import print_function
from numpy      import array, empty, zeros, ones
from itertools import product
import operator

class Circuit( object ):
    """
    Classe dei circuiti predefiniti.
    Ogni istanza di questa classe è composta dalle due matrici di connessione delle porte AND e OR
    del PLA, inizializzate tutte con nodi non connessi.

    @note: il numero di input, output, porte AND non deve superare quello del simulatore.

    @ivar n_inputs: numero di ingressi del circuito
    @ivar n_outputs: numero di uscite del circuito, equivalente al numero di porte OR presenti
    @ivar n_and: numero di porte AND del circuito
    @ivar and_matrix: matrice di connessione tra ingressi e porte AND
    @ivar or_matrix: matrice di connessione tra porte AND e porte OR
    @ivar description: il nome del circuito predefinito
    @ivar labels_i: denominazioni degli input del circuito
    @ivar labels_o: denominazioni degli output del circuito
    """
    
    n_inputs        = 0                     # numero di ingressi
    n_outputs       = 0                     # numero di uscite
    n_and           = 0                     # numero di porte AND

    and_matrix      = None                  # matrice di connessione tra ingressi e porte AND
    or_matrix       = None                  # matrice di connessione tra porte AND e OR

    description     = ''                    # nome del circuito
    labels_i        = []                    # labels assegnate agli input del circuito
    labels_o        = []                    # labels assegnate agli output del circuito

    def __init__( self, n_in, n_out, n_and ):
        """
        Istanzia un circuito predefinito.
        @param n_in: numero di input del circuito
        @param n_out: numero di output del circuito
        @param n_and: numero di porte AND del circuito
        """
        self.n_inputs       = n_in
        self.n_outputs      = n_out
        self.n_and          = n_and
        self.and_matrix     = zeros( ( self.n_and, 2 * self.n_inputs ), dtype=int )
        self.or_matrix      = zeros( ( self.n_and, self.n_outputs ), dtype=int )

    @staticmethod
    def generate_code(name, description, function, input_names, output_names):
        """
        Genera il codice necessario per creare un circuito data una funzione logica.
        Nota: questa funzione non genera una rete combinatoria minimale.
        @param name: nome della variabile
        @param description: nome del circuito
        @param function: funzione booleana da replicare
        @param input_names: denominazioni degli input del circuito
        @param output_names: denominazioni degli input del circuito
        """
        i=len(input_names)
        o=len(output_names)

        d={}
        for x in product([False, True], repeat=i):
            d[x]=function(*x)
            d[x]=tuple(filter(lambda k: k>=0, map(lambda k: k if d[x][k] else -1, range(o))))

        sd = sorted(d.items(), key=operator.itemgetter(1), reverse=True)
        ands=sum(map(lambda x: bool(x[1]), sd))

        print("# ", "-"*103, " #\n#\t", description, "\n# ", "-"*103, " #\n", sep="")
        print(name, "=Circuit( %d, %d, %d )" %(i, o, ands), sep="")
        print(name, ".description=", repr(description), sep="")
        print(name, ".labels_i=", repr(input_names), sep="")
        print(name, ".labels_o=", repr(output_names), sep="")
        print()

        for a in range(ands):
            for e in range(i):
                e=2*e+sd[a][0][e]
                print(name, ".and_matrix[", a, ",", e, "]=1", sep="")
        print()

        for a in range(ands):
            for e in sd[a][1]:
                print(name, ".or_matrix[", a, ",", e, "]=1", sep="")
        print()

    @staticmethod
    def generate_obj(description, function, input_names, output_names):
        """
        Genera un circuito data una funzione logica.
        Nota: questa funzione non genera una rete combinatoria minimale.
        @param description: nome del circuito
        @param function: funzione booleana da replicare
        @param input_names: denominazioni degli input del circuito
        @param output_names: denominazioni degli input del circuito
        """
        i=len(input_names)
        o=len(output_names)

        d={}
        for x in product([False, True], repeat=i):
            d[x]=function(*x)
            d[x]=tuple(filter(lambda k: k>=0, map(lambda k: k if d[x][k] else -1, range(o))))

        sd = sorted(d.items(), key=operator.itemgetter(1), reverse=True)
        ands=sum(map(lambda x: bool(x[1]), sd))

        self=Circuit(i, o, ands)
        self.description=description
        self.labels_i=input_names
        self.labels_o=output_names

        for a in range(ands):
            for e in range(i):
                e=2*e+sd[a][0][e]
                self.and_matrix[a, e,]=1

        for a in range(ands):
            for e in sd[a][1]:
                self.or_matrix[a, e]=1
        return self

# ------------------------------------------------------------------------------------------------------- #
#	modello
# ------------------------------------------------------------------------------------------------------- #
##circ_x	                                = Circuit( n_inputs, n_outputs=n_porte_or, n_porte_and )
##circ_x.description                      = 'descrizione circuito'
##circ_x.labels_i                         = [ 'input 1', '...' ]
##circ_x.labels_o                         = [ 'output 1', '...' ]
##
##circ_x.and_matrix[ porta_and, input ]		= 1
##circ_x.or_matrix[ porta_and, porta_or=output ]		= 1
#aggiungere a circs

# ------------------------------------------------------------------------------------------------------- #
#	semisommatore
# ------------------------------------------------------------------------------------------------------- #
circ_h	                                = Circuit( 2, 2, 3 )
circ_h.description                      = '1 bit half adder'
circ_h.labels_i                         = [ 'A0', 'B0' ]
circ_h.labels_o                         = [ 'S', 'C' ]

circ_h.and_matrix[ 0, 1 : 3 ]		= 1
circ_h.and_matrix[ 1, : 5 : 3 ]		= 1
circ_h.and_matrix[ 2, 1 : 5 : 2 ]	= 1

circ_h.or_matrix[ : 2, 0 ]		= 1
circ_h.or_matrix[ 2, 1 ]		= 1


# ------------------------------------------------------------------------------------------------------- #
#	sommatore 1 bit
# ------------------------------------------------------------------------------------------------------- #
circ_a	                                = Circuit( 3, 2, 7 )
circ_a.description                      = '1 bit full adder'
circ_a.labels_i                         = [ 'A0', 'B0', 'C' ]
circ_a.labels_o                         = [ 'S', 'C' ]

circ_a.and_matrix[ 0, 1 : 3 ]		= 1
circ_a.and_matrix[ 0, 4 ]		= 1
circ_a.and_matrix[ 1, 0 ]		= 1
circ_a.and_matrix[ 1, 3 : 5 ]		= 1
circ_a.and_matrix[ 2, : 3 : 2 ]		= 1
circ_a.and_matrix[ 2, 5 ]		= 1
circ_a.and_matrix[ 3, 1 : : 2 ]		= 1
circ_a.and_matrix[ 4, 1 : 4 : 2 ]	= 1
circ_a.and_matrix[ 5, 3 : : 2 ]	        = 1
circ_a.and_matrix[ 6, 1 : : 4 ]	        = 1

circ_a.or_matrix[ : 4, 0 ]		= 1
circ_a.or_matrix[ 4 :, 1 ]		= 1


# ------------------------------------------------------------------------------------------------------- #
#	sommatore 2 bit
# ------------------------------------------------------------------------------------------------------- #
circ_b	                                = Circuit( 4, 3, 13 )
circ_b.description                      = '2 bit adder'
circ_b.labels_i                         = [ 'A1', 'B1', 'A0', 'B0' ]
circ_b.labels_o                         = [ 'S1', 'S0', 'C' ]

circ_b.and_matrix[ 0, 4 : : 2 ]         = 1
circ_b.and_matrix[ 0, : 4 : 3 ]         = 1
circ_b.and_matrix[ 1, 4 : : 2 ]         = 1
circ_b.and_matrix[ 1, 1 : 3 ]           = 1
circ_b.and_matrix[ 2, 5 : 7 ]           = 1
circ_b.and_matrix[ 2, : 4 : 3 ]         = 1
circ_b.and_matrix[ 3, 5 : 7 ]           = 1
circ_b.and_matrix[ 3, 1 : 3 ]           = 1
circ_b.and_matrix[ 4, 4 : : 3 ]         = 1
circ_b.and_matrix[ 4, : 4 : 3 ]         = 1
circ_b.and_matrix[ 5, 4 : : 3 ]         = 1
circ_b.and_matrix[ 5, 1 : 3 ]           = 1
circ_b.and_matrix[ 6, 5 : : 2 ]         = 1
circ_b.and_matrix[ 6, : 3 : 2 ]         = 1
circ_b.and_matrix[ 7, 1 : : 2 ]         = 1

circ_b.and_matrix[ 8, 4 : : 3 ]         = 1
circ_b.and_matrix[ 9, 5 : 7 ]	        = 1
circ_b.and_matrix[ 10, 1 : 4 : 2 ]	= 1
circ_b.and_matrix[ 11, 1 ]	        = 1
circ_b.and_matrix[ 11, 5 : : 2 ]	= 1
circ_b.and_matrix[ 12, 3 : : 2 ]	= 1

circ_b.or_matrix[ : 8, 0 ]		= 1
circ_b.or_matrix[ 8 : 10, 1 ]		= 1
circ_b.or_matrix[ 10 :, 2 ]		= 1


# ------------------------------------------------------------------------------------------------------- #
#	priority encoder
# ------------------------------------------------------------------------------------------------------- #
circ_e	                                = Circuit( 4, 3, 7 )
circ_e.description                      = 'Priority encoder'
circ_e.labels_i                         = [ 'A3', 'A2', 'A1', 'A0' ]
circ_e.labels_o                         = [ 'B1', 'B0', 'V' ]

circ_e.and_matrix[ 0, : 3 : 2 ]	        = 1
circ_e.and_matrix[ 1, : 4 : 3 ]	        = 1
circ_e.and_matrix[ 2, : 5 : 4 ]	        = 1
circ_e.and_matrix[ 3, 1 ]		= 1
circ_e.and_matrix[ 4, 3 ]		= 1
circ_e.and_matrix[ 5, 5 ]		= 1
circ_e.and_matrix[ 6, 7 ]		= 1

circ_e.or_matrix[ 0, 0 ]		= 1
circ_e.or_matrix[ 1 : 3, 1 ]		= 1
circ_e.or_matrix[ 3 :, 2 ]		= 1


# ------------------------------------------------------------------------------------------------------- #
#	multiplexer
# ------------------------------------------------------------------------------------------------------- #
circ_m	                                = Circuit( 6, 1, 4 )
circ_m.description                      = 'Multiplexer'
circ_m.labels_i                         = [ 'A3', 'A2', 'A1', 'A0', 'C1', 'C0' ]
circ_m.labels_o                         = [ 'B' ]

circ_m.and_matrix[ 0, 1 ]		= 1
circ_m.and_matrix[ 1, 3 ]		= 1
circ_m.and_matrix[ 2, 5 ]		= 1
circ_m.and_matrix[ 3, 7 ]		= 1
circ_m.and_matrix[ 2 : 4, 8 ]		= 1
circ_m.and_matrix[ : 2, 9 ]		= 1
circ_m.and_matrix[ 1 : 4 : 2, 10 ]	= 1
circ_m.and_matrix[ : 3 : 2, 11 ]	= 1

circ_m.or_matrix[ : 4, 0 ]		= 1


# ------------------------------------------------------------------------------------------------------- #
#	maggioranza
# ------------------------------------------------------------------------------------------------------- #
circ_g                                  = Circuit( 3, 1, 4 )
circ_g.description                      = 'Majority'
circ_g.labels_i                         = [ 'A2', 'A1', 'A0' ]
circ_g.labels_o                         = [ 'B' ]

circ_g.and_matrix[ 0, 0 ]		= 1
circ_g.and_matrix[ 0, 3 : : 2 ]		= 1
circ_g.and_matrix[ 1, 1 : 3 ]		= 1
circ_g.and_matrix[ 1, 5 ]		= 1
circ_g.and_matrix[ 2, 1 ]		= 1
circ_g.and_matrix[ 2, 3 : 5 ]		= 1
circ_g.and_matrix[ 3, 1 : : 2 ]		= 1

circ_g.or_matrix[ : 4, 0 ]		= 1


# ------------------------------------------------------------------------------------------------------- #
#	decodificatore
# ------------------------------------------------------------------------------------------------------- #
circ_d	                                = Circuit( 3, 8, 8 )
circ_d.description                      = 'Decoder'
circ_d.labels_i                         = [ 'A2', 'A1', 'A0' ]
circ_d.labels_o                         = [ 'B7', 'B6', 'B5', 'B4', 'B3', 'B2', 'B1', 'B0' ]

circ_d.and_matrix[ : 4, 0 ]		= 1
circ_d.and_matrix[ 4 : 8, 1 ]		= 1
circ_d.and_matrix[ : 2, 2 ]		= 1
circ_d.and_matrix[ 4 : 6, 2 ]		= 1
circ_d.and_matrix[ 2 : 4, 3 ]		= 1
circ_d.and_matrix[ 6 : 8, 3 ]		= 1
circ_d.and_matrix[ : 7 : 2, 4 ]		= 1
circ_d.and_matrix[ 1 : 8 : 2, 5 ]	= 1

circ_d.or_matrix[ 0, 7 ]		= 1
circ_d.or_matrix[ 1, 6 ]		= 1
circ_d.or_matrix[ 2, 5 ]		= 1
circ_d.or_matrix[ 3, 4 ]		= 1
circ_d.or_matrix[ 4, 3 ]		= 1
circ_d.or_matrix[ 5, 2 ]		= 1
circ_d.or_matrix[ 6, 1 ]		= 1
circ_d.or_matrix[ 7, 0 ]		= 1


# ------------------------------------------------------------------------------------------------------- #
#	registro a scorrimento
# ------------------------------------------------------------------------------------------------------- #
circ_s	                                = Circuit( 6, 5, 8 )
circ_s.description                      = 'Shift register'
circ_s.labels_i                         = [ 'A4', 'A3', 'A2', 'A1', 'A0', 'C' ]
circ_s.labels_o                         = [ 'B4', 'B3', 'B2', 'B1', 'B0' ]

circ_s.and_matrix[ : : 2, 10 ]		= 1
circ_s.and_matrix[ 1 : : 2, 11 ]	= 1
circ_s.and_matrix[ -1 :, 1 ]		= 1
circ_s.and_matrix[ 5 : 7, 3 ]		= 1
circ_s.and_matrix[ 3 : 5, 5 ]		= 1
circ_s.and_matrix[ 1 : 3, 7 ]		= 1
circ_s.and_matrix[ 0, 9 ]		= 1

circ_s.or_matrix[ 6, 0 ]		= 1
circ_s.or_matrix[ 4 : : 3, 1 ]		= 1
circ_s.or_matrix[ 2 : : 3, 2 ]		= 1
circ_s.or_matrix[ : 4 : 3, 3 ]		= 1
circ_s.or_matrix[ 1, 4 ]		= 1



# ------------------------------------------------------------------------------------------------------- #
#	comparatore
# ------------------------------------------------------------------------------------------------------- #
circ_c	                                = Circuit( 4, 3, 10 )
circ_c.description                      = 'Comparator'
circ_c.labels_i                         = [ 'A1', 'B1', 'A0', 'B0' ]
circ_c.labels_o                         = [ 'B>A', 'A>B', 'A=B' ]

circ_c.and_matrix[ 0, 1 : 4 : 2 ]	= 1
circ_c.and_matrix[ 0, 4 : : 3 ]		= 1
circ_c.and_matrix[ 1, : 3 : 2 ]		= 1
circ_c.and_matrix[ 1, 4 : : 3 ]		= 1
circ_c.and_matrix[ 2, : 4 : 3 ]		= 1
circ_c.and_matrix[ 3, 1 : 4 : 2 ]	= 1
circ_c.and_matrix[ 3, 5 : 7 ]		= 1
circ_c.and_matrix[ 4, : 3 : 2 ]		= 1
circ_c.and_matrix[ 4, 5 : 7 ]		= 1
circ_c.and_matrix[ 5, 1 : 3 ]		= 1
circ_c.and_matrix[ 6, 1 : 4 : 2 ]	= 1
circ_c.and_matrix[ 6, 5 : : 2 ]		= 1
circ_c.and_matrix[ 7, 1 : 4 : 2 ]	= 1
circ_c.and_matrix[ 7, 4 : : 2 ]		= 1
circ_c.and_matrix[ 8, : 3 : 2 ]		= 1
circ_c.and_matrix[ 8, 5 : : 2 ]		= 1
circ_c.and_matrix[ 9, : 3 : 2 ]		= 1
circ_c.and_matrix[ 9, 4 : : 2 ]		= 1

circ_c.or_matrix[ : 3, 0 ]		= 1
circ_c.or_matrix[ 3 : 6, 1 ]		= 1
circ_c.or_matrix[ 6 :, 2 ]		= 1

# ------------------------------------------------------------------------------------------------------- #
#	gate logico multiplo
# ------------------------------------------------------------------------------------------------------- #
circ_mlg	                                = Circuit( 2, 6, 10 )
circ_mlg.description                      = 'Multiple Logic Gate'
circ_mlg.labels_i                         = [ 'A','B' ]
circ_mlg.labels_o                         = [ 'AND','OR','NAND','NOR','XOR','EQ']

circ_mlg.and_matrix[ 0, 1:4:2 ]		= 1
circ_mlg.and_matrix[ 1, 1 ]		= 1
circ_mlg.and_matrix[ 2, 3 ]		= 1
circ_mlg.and_matrix[ 3, 0 ]		= 1
circ_mlg.and_matrix[ 4, 2 ]		= 1
circ_mlg.and_matrix[ 5, 0:3:2 ]		= 1
circ_mlg.and_matrix[ 6, 0 ]		= 1
circ_mlg.and_matrix[ 6, 3 ]		= 1
circ_mlg.and_matrix[ 7, 1 ]		= 1
circ_mlg.and_matrix[ 7, 2 ]		= 1
circ_mlg.and_matrix[ 8, 0:4:2 ]		= 1
circ_mlg.and_matrix[ 9, 1:4:2 ]		= 1

circ_mlg.or_matrix[ 0, 0 ]		= 1
circ_mlg.or_matrix[ 1:3, 1 ]		= 1
circ_mlg.or_matrix[ 3:5, 2 ]		= 1
circ_mlg.or_matrix[ 5, 3 ]		= 1
circ_mlg.or_matrix[ 6:8, 4 ]		= 1
circ_mlg.or_matrix[ 8:10, 5 ]		= 1

# ------------------------------------------------------------------------------------------------------- #
#	2 bit multiplicator
# ------------------------------------------------------------------------------------------------------- #

circ_mult2=Circuit( 4, 4, 9 )
circ_mult2.description='2 bit multiplicator'
circ_mult2.labels_i=['A1', 'B1', 'A0', 'B0']
circ_mult2.labels_o=['S3', 'S2', 'S1', 'S0']

circ_mult2.and_matrix[0,0]=1
circ_mult2.and_matrix[0,2]=1
circ_mult2.and_matrix[0,5]=1
circ_mult2.and_matrix[0,7]=1
circ_mult2.and_matrix[1,0]=1
circ_mult2.and_matrix[1,3]=1
circ_mult2.and_matrix[1,5]=1
circ_mult2.and_matrix[1,7]=1
circ_mult2.and_matrix[2,1]=1
circ_mult2.and_matrix[2,2]=1
circ_mult2.and_matrix[2,5]=1
circ_mult2.and_matrix[2,7]=1
circ_mult2.and_matrix[3,0]=1
circ_mult2.and_matrix[3,3]=1
circ_mult2.and_matrix[3,5]=1
circ_mult2.and_matrix[3,6]=1
circ_mult2.and_matrix[4,1]=1
circ_mult2.and_matrix[4,2]=1
circ_mult2.and_matrix[4,4]=1
circ_mult2.and_matrix[4,7]=1
circ_mult2.and_matrix[5,1]=1
circ_mult2.and_matrix[5,3]=1
circ_mult2.and_matrix[5,4]=1
circ_mult2.and_matrix[5,7]=1
circ_mult2.and_matrix[6,1]=1
circ_mult2.and_matrix[6,3]=1
circ_mult2.and_matrix[6,5]=1
circ_mult2.and_matrix[6,6]=1
circ_mult2.and_matrix[7,1]=1
circ_mult2.and_matrix[7,3]=1
circ_mult2.and_matrix[7,4]=1
circ_mult2.and_matrix[7,6]=1
circ_mult2.and_matrix[8,1]=1
circ_mult2.and_matrix[8,3]=1
circ_mult2.and_matrix[8,5]=1
circ_mult2.and_matrix[8,7]=1

circ_mult2.or_matrix[0,3]=1
circ_mult2.or_matrix[1,2]=1
circ_mult2.or_matrix[1,3]=1
circ_mult2.or_matrix[2,2]=1
circ_mult2.or_matrix[2,3]=1
circ_mult2.or_matrix[3,2]=1
circ_mult2.or_matrix[4,2]=1
circ_mult2.or_matrix[5,1]=1
circ_mult2.or_matrix[5,2]=1
circ_mult2.or_matrix[6,1]=1
circ_mult2.or_matrix[6,2]=1
circ_mult2.or_matrix[7,1]=1
circ_mult2.or_matrix[8,0]=1
circ_mult2.or_matrix[8,3]=1

# ------------------------------------------------------------------------------------------------------- #
#	Reductor 3-2
# ------------------------------------------------------------------------------------------------------- #

circ_r32=Circuit( 3, 2, 7 )
circ_r32.description='Reductor 3-2'
circ_r32.labels_i=['A', 'B', 'C']
circ_r32.labels_o=['S', 'C']

circ_r32.and_matrix[0,0]=1
circ_r32.and_matrix[0,3]=1
circ_r32.and_matrix[0,5]=1
circ_r32.and_matrix[1,1]=1
circ_r32.and_matrix[1,2]=1
circ_r32.and_matrix[1,5]=1
circ_r32.and_matrix[2,1]=1
circ_r32.and_matrix[2,3]=1
circ_r32.and_matrix[2,4]=1
circ_r32.and_matrix[3,1]=1
circ_r32.and_matrix[3,3]=1
circ_r32.and_matrix[3,5]=1
circ_r32.and_matrix[4,0]=1
circ_r32.and_matrix[4,2]=1
circ_r32.and_matrix[4,5]=1
circ_r32.and_matrix[5,0]=1
circ_r32.and_matrix[5,3]=1
circ_r32.and_matrix[5,4]=1
circ_r32.and_matrix[6,1]=1
circ_r32.and_matrix[6,2]=1
circ_r32.and_matrix[6,4]=1

circ_r32.or_matrix[0,1]=1
circ_r32.or_matrix[1,1]=1
circ_r32.or_matrix[2,1]=1
circ_r32.or_matrix[3,0]=1
circ_r32.or_matrix[3,1]=1
circ_r32.or_matrix[4,0]=1
circ_r32.or_matrix[5,0]=1
circ_r32.or_matrix[6,0]=1

# ------------------------------------------------------------------------------------------------------- #
#	Decoder 4 bit - 7 segment
# ------------------------------------------------------------------------------------------------------- #

circ_bcd=Circuit( 4, 7, 16 )
circ_bcd.description='Decoder 4 bit - 7 segment'
circ_bcd.labels_i=['A3', 'A2', 'A1', 'A0']
circ_bcd.labels_o=['a', 'b', 'c', 'd', 'e', 'f', 'g']

circ_bcd.and_matrix[0,0]=1
circ_bcd.and_matrix[0,2]=1
circ_bcd.and_matrix[0,4]=1
circ_bcd.and_matrix[0,6]=1
circ_bcd.and_matrix[1,0]=1
circ_bcd.and_matrix[1,2]=1
circ_bcd.and_matrix[1,4]=1
circ_bcd.and_matrix[1,7]=1
circ_bcd.and_matrix[2,0]=1
circ_bcd.and_matrix[2,2]=1
circ_bcd.and_matrix[2,5]=1
circ_bcd.and_matrix[2,6]=1
circ_bcd.and_matrix[3,0]=1
circ_bcd.and_matrix[3,2]=1
circ_bcd.and_matrix[3,5]=1
circ_bcd.and_matrix[3,7]=1
circ_bcd.and_matrix[4,0]=1
circ_bcd.and_matrix[4,3]=1
circ_bcd.and_matrix[4,4]=1
circ_bcd.and_matrix[4,6]=1
circ_bcd.and_matrix[5,0]=1
circ_bcd.and_matrix[5,3]=1
circ_bcd.and_matrix[5,4]=1
circ_bcd.and_matrix[5,7]=1
circ_bcd.and_matrix[6,0]=1
circ_bcd.and_matrix[6,3]=1
circ_bcd.and_matrix[6,5]=1
circ_bcd.and_matrix[6,6]=1
circ_bcd.and_matrix[7,0]=1
circ_bcd.and_matrix[7,3]=1
circ_bcd.and_matrix[7,5]=1
circ_bcd.and_matrix[7,7]=1
circ_bcd.and_matrix[8,1]=1
circ_bcd.and_matrix[8,2]=1
circ_bcd.and_matrix[8,4]=1
circ_bcd.and_matrix[8,6]=1
circ_bcd.and_matrix[9,1]=1
circ_bcd.and_matrix[9,2]=1
circ_bcd.and_matrix[9,4]=1
circ_bcd.and_matrix[9,7]=1
circ_bcd.and_matrix[10,1]=1
circ_bcd.and_matrix[10,2]=1
circ_bcd.and_matrix[10,5]=1
circ_bcd.and_matrix[10,6]=1
circ_bcd.and_matrix[11,1]=1
circ_bcd.and_matrix[11,2]=1
circ_bcd.and_matrix[11,5]=1
circ_bcd.and_matrix[11,7]=1
circ_bcd.and_matrix[12,1]=1
circ_bcd.and_matrix[12,3]=1
circ_bcd.and_matrix[12,4]=1
circ_bcd.and_matrix[12,6]=1
circ_bcd.and_matrix[13,1]=1
circ_bcd.and_matrix[13,3]=1
circ_bcd.and_matrix[13,4]=1
circ_bcd.and_matrix[13,7]=1
circ_bcd.and_matrix[14,1]=1
circ_bcd.and_matrix[14,3]=1
circ_bcd.and_matrix[14,5]=1
circ_bcd.and_matrix[14,6]=1
circ_bcd.and_matrix[15,1]=1
circ_bcd.and_matrix[15,3]=1
circ_bcd.and_matrix[15,5]=1
circ_bcd.and_matrix[15,7]=1

circ_bcd.or_matrix[0,0]=1
circ_bcd.or_matrix[0,1]=1
circ_bcd.or_matrix[0,2]=1
circ_bcd.or_matrix[0,3]=1
circ_bcd.or_matrix[0,4]=1
circ_bcd.or_matrix[0,5]=1
circ_bcd.or_matrix[1,1]=1
circ_bcd.or_matrix[1,2]=1
circ_bcd.or_matrix[2,0]=1
circ_bcd.or_matrix[2,1]=1
circ_bcd.or_matrix[2,3]=1
circ_bcd.or_matrix[2,4]=1
circ_bcd.or_matrix[2,6]=1
circ_bcd.or_matrix[3,0]=1
circ_bcd.or_matrix[3,1]=1
circ_bcd.or_matrix[3,2]=1
circ_bcd.or_matrix[3,3]=1
circ_bcd.or_matrix[3,6]=1
circ_bcd.or_matrix[4,1]=1
circ_bcd.or_matrix[4,2]=1
circ_bcd.or_matrix[4,5]=1
circ_bcd.or_matrix[4,6]=1
circ_bcd.or_matrix[5,0]=1
circ_bcd.or_matrix[5,2]=1
circ_bcd.or_matrix[5,3]=1
circ_bcd.or_matrix[5,5]=1
circ_bcd.or_matrix[5,6]=1
circ_bcd.or_matrix[6,0]=1
circ_bcd.or_matrix[6,2]=1
circ_bcd.or_matrix[6,3]=1
circ_bcd.or_matrix[6,4]=1
circ_bcd.or_matrix[6,5]=1
circ_bcd.or_matrix[6,6]=1
circ_bcd.or_matrix[7,0]=1
circ_bcd.or_matrix[7,1]=1
circ_bcd.or_matrix[7,2]=1
circ_bcd.or_matrix[8,0]=1
circ_bcd.or_matrix[8,1]=1
circ_bcd.or_matrix[8,2]=1
circ_bcd.or_matrix[8,3]=1
circ_bcd.or_matrix[8,4]=1
circ_bcd.or_matrix[8,5]=1
circ_bcd.or_matrix[8,6]=1
circ_bcd.or_matrix[9,0]=1
circ_bcd.or_matrix[9,1]=1
circ_bcd.or_matrix[9,2]=1
circ_bcd.or_matrix[9,3]=1
circ_bcd.or_matrix[9,5]=1
circ_bcd.or_matrix[9,6]=1
circ_bcd.or_matrix[10,0]=1
circ_bcd.or_matrix[10,1]=1
circ_bcd.or_matrix[10,2]=1
circ_bcd.or_matrix[10,4]=1
circ_bcd.or_matrix[10,5]=1
circ_bcd.or_matrix[10,6]=1
circ_bcd.or_matrix[11,2]=1
circ_bcd.or_matrix[11,3]=1
circ_bcd.or_matrix[11,4]=1
circ_bcd.or_matrix[11,5]=1
circ_bcd.or_matrix[11,6]=1
circ_bcd.or_matrix[12,0]=1
circ_bcd.or_matrix[12,3]=1
circ_bcd.or_matrix[12,4]=1
circ_bcd.or_matrix[12,5]=1
circ_bcd.or_matrix[13,1]=1
circ_bcd.or_matrix[13,2]=1
circ_bcd.or_matrix[13,3]=1
circ_bcd.or_matrix[13,4]=1
circ_bcd.or_matrix[13,6]=1
circ_bcd.or_matrix[14,0]=1
circ_bcd.or_matrix[14,3]=1
circ_bcd.or_matrix[14,4]=1
circ_bcd.or_matrix[14,5]=1
circ_bcd.or_matrix[14,6]=1
circ_bcd.or_matrix[15,0]=1
circ_bcd.or_matrix[15,4]=1
circ_bcd.or_matrix[15,5]=1
circ_bcd.or_matrix[15,6]=1

# ------------------------------------------------------------------------------------------------------- #
#	One step flip-flop SR
# ------------------------------------------------------------------------------------------------------- #
circ_sr=Circuit( 4, 2, 5 )
circ_sr.description='One step flip-flop SR'
circ_sr.labels_i=['S','R','Q(t)','¬Q(t)']
circ_sr.labels_o=['Q(t+1)','¬Q(t+1)']

circ_sr.and_matrix[0,1:3]=1
circ_sr.and_matrix[1,0:4:3]=1
circ_sr.and_matrix[2,0:3:2]=1
circ_sr.and_matrix[2,5]=1
circ_sr.and_matrix[3,0:3:2]=1
circ_sr.and_matrix[3,7]=1

circ_sr.or_matrix[0:3:2,0]=1
circ_sr.or_matrix[1:4:2,1]=1

# ------------------------------------------------------------------------------------------------------- #
#	One step Flip-flop T
# ------------------------------------------------------------------------------------------------------- #
circ_t=Circuit( 2, 2, 5 )
circ_t.description='One step flip-flop T'
circ_t.labels_i=['T','Q(t)']
circ_t.labels_o=['Q(t+1)','¬Q(t+1)']

circ_t.and_matrix[0,0:4:3]=1
circ_t.and_matrix[1,1:3]=1
circ_t.and_matrix[2,1:4:2]=1
circ_t.and_matrix[3,0:3:2]=1

circ_t.or_matrix[0:2,0]=1
circ_t.or_matrix[2:4,1]=1

# ------------------------------------------------------------------------------------------------------- #
#	One step flip-flop JK
# ------------------------------------------------------------------------------------------------------- #
circ_jk=Circuit( 3, 2, 5 )
circ_jk.description='One step flip-flop JK'
circ_jk.labels_i=['J', 'K','Q(t)']
circ_jk.labels_o=['Q(t+1)','¬Q(t+1)']

circ_jk.and_matrix[0,0:3:2]=1
circ_jk.and_matrix[0,5]=1
circ_jk.and_matrix[1,1:3]=1
circ_jk.and_matrix[2,0:3:2]=1
circ_jk.and_matrix[2,4]=1
circ_jk.and_matrix[3,0:4:3]=1

circ_jk.or_matrix[0:2,0]=1
circ_jk.or_matrix[2:4,1]=1

# ------------------------------------------------------------------------------------------------------- #
#	6-bit ones' complement
# ------------------------------------------------------------------------------------------------------- #
circ_compl1=Circuit( 6, 6, 6 )
circ_compl1.description='6-bit ones\' complement'
circ_compl1.labels_i=['A5','A4','A3','A2','A1','A0']
circ_compl1.labels_o=['B5','B4','B3','B2','B1','B0']

circ_compl1.and_matrix[0,0]=1
circ_compl1.and_matrix[1,2]=1
circ_compl1.and_matrix[2,4]=1
circ_compl1.and_matrix[3,6]=1
circ_compl1.and_matrix[4,8]=1
circ_compl1.and_matrix[5,10]=1

circ_compl1.or_matrix[0,0]=1
circ_compl1.or_matrix[1,1]=1
circ_compl1.or_matrix[2,2]=1
circ_compl1.or_matrix[3,3]=1
circ_compl1.or_matrix[4,4]=1
circ_compl1.or_matrix[5,5]=1

# ------------------------------------------------------------------------------------------------------- #
#	Parity check
# ------------------------------------------------------------------------------------------------------- #
circ_pc=Circuit( 4, 1, 8 )
circ_pc.description='Parity check (CRC-1)'
circ_pc.labels_i=['A3','A2','A1','A0']
circ_pc.labels_o=['C']

circ_pc.and_matrix[0,0]=1
circ_pc.and_matrix[0,2]=1
circ_pc.and_matrix[0,4]=1
circ_pc.and_matrix[0,7]=1
circ_pc.and_matrix[1,0]=1
circ_pc.and_matrix[1,2]=1
circ_pc.and_matrix[1,5]=1
circ_pc.and_matrix[1,6]=1
circ_pc.and_matrix[2,0]=1
circ_pc.and_matrix[2,3]=1
circ_pc.and_matrix[2,4]=1
circ_pc.and_matrix[2,6]=1
circ_pc.and_matrix[3,1]=1
circ_pc.and_matrix[3,2]=1
circ_pc.and_matrix[3,4]=1
circ_pc.and_matrix[3,6]=1
circ_pc.and_matrix[4,1]=1
circ_pc.and_matrix[4,3]=1
circ_pc.and_matrix[4,5]=1
circ_pc.and_matrix[4,6]=1
circ_pc.and_matrix[5,1]=1
circ_pc.and_matrix[5,3]=1
circ_pc.and_matrix[5,4]=1
circ_pc.and_matrix[5,7]=1
circ_pc.and_matrix[6,1]=1
circ_pc.and_matrix[6,2]=1
circ_pc.and_matrix[6,5]=1
circ_pc.and_matrix[6,7]=1
circ_pc.and_matrix[7,0]=1
circ_pc.and_matrix[7,3]=1
circ_pc.and_matrix[7,5]=1
circ_pc.and_matrix[7,7]=1

circ_pc.or_matrix[0:8,0]=1

# ------------------------------------------------------------------------------------------------------- #
#	CRC-3-GSM
# ------------------------------------------------------------------------------------------------------- #
circ_crc3=Circuit( 4, 3, 14 )
circ_crc3.description='CRC-3-GSM'
circ_crc3.labels_i=['A3','A2','A1','A0']
circ_crc3.labels_o=['C2','C1','C0']

circ_crc3.and_matrix[0,0]=1
circ_crc3.and_matrix[0,2]=1
circ_crc3.and_matrix[0,4]=1
circ_crc3.and_matrix[0,7]=1
circ_crc3.and_matrix[1,0]=1
circ_crc3.and_matrix[1,2]=1
circ_crc3.and_matrix[1,5]=1
circ_crc3.and_matrix[1,6]=1
circ_crc3.and_matrix[2,0]=1
circ_crc3.and_matrix[2,2]=1
circ_crc3.and_matrix[2,5]=1
circ_crc3.and_matrix[2,7]=1
circ_crc3.and_matrix[3,0]=1
circ_crc3.and_matrix[3,3]=1
circ_crc3.and_matrix[3,4]=1
circ_crc3.and_matrix[3,6]=1
circ_crc3.and_matrix[4,0]=1
circ_crc3.and_matrix[4,3]=1
circ_crc3.and_matrix[4,4]=1
circ_crc3.and_matrix[4,7]=1
circ_crc3.and_matrix[5,0]=1
circ_crc3.and_matrix[5,3]=1
circ_crc3.and_matrix[5,5]=1
circ_crc3.and_matrix[5,6]=1
circ_crc3.and_matrix[6,0]=1
circ_crc3.and_matrix[6,3]=1
circ_crc3.and_matrix[6,5]=1
circ_crc3.and_matrix[6,7]=1
circ_crc3.and_matrix[7,1]=1
circ_crc3.and_matrix[7,2]=1
circ_crc3.and_matrix[7,4]=1
circ_crc3.and_matrix[7,6]=1
circ_crc3.and_matrix[8,1]=1
circ_crc3.and_matrix[8,2]=1
circ_crc3.and_matrix[8,4]=1
circ_crc3.and_matrix[8,7]=1
circ_crc3.and_matrix[9,1]=1
circ_crc3.and_matrix[9,2]=1
circ_crc3.and_matrix[9,5]=1
circ_crc3.and_matrix[9,6]=1
circ_crc3.and_matrix[10,1]=1
circ_crc3.and_matrix[10,3]=1
circ_crc3.and_matrix[10,4]=1
circ_crc3.and_matrix[10,6]=1
circ_crc3.and_matrix[11,1]=1
circ_crc3.and_matrix[11,3]=1
circ_crc3.and_matrix[11,4]=1
circ_crc3.and_matrix[11,7]=1
circ_crc3.and_matrix[12,1]=1
circ_crc3.and_matrix[12,3]=1
circ_crc3.and_matrix[12,5]=1
circ_crc3.and_matrix[12,6]=1
circ_crc3.and_matrix[13,1]=1
circ_crc3.and_matrix[13,3]=1
circ_crc3.and_matrix[13,5]=1
circ_crc3.and_matrix[13,7]=1

circ_crc3.or_matrix[0,1:3]=1
circ_crc3.or_matrix[1,0:2]=1
circ_crc3.or_matrix[2,0:3:2]=1
circ_crc3.or_matrix[3,0:3]=1
circ_crc3.or_matrix[4,0]=1
circ_crc3.or_matrix[5,2]=1
circ_crc3.or_matrix[6,1]=1
circ_crc3.or_matrix[7,0:3:2]=1
circ_crc3.or_matrix[8,0:2]=1
circ_crc3.or_matrix[9,1:3]=1
circ_crc3.or_matrix[10,1]=1
circ_crc3.or_matrix[11,2]=1
circ_crc3.or_matrix[12,0]=1
circ_crc3.or_matrix[13,0:3]=1

# ------------------------------------------------------------------------------------------------------- #
#	4-bit twos' complement
# ------------------------------------------------------------------------------------------------------- #
circ_compl2=Circuit( 4, 4, 13 )
circ_compl2.description='4-bit twos\' complement'
circ_compl2.labels_i=['A3','A2','A1','A0']
circ_compl2.labels_o=['B3','B2','B1','B0']

circ_compl2.and_matrix[0,0]=1
circ_compl2.and_matrix[0,3]=1
circ_compl2.and_matrix[1,0]=1
circ_compl2.and_matrix[1,5]=1
circ_compl2.and_matrix[2,0]=1
circ_compl2.and_matrix[2,7]=1
circ_compl2.and_matrix[3,1]=1
circ_compl2.and_matrix[3,2:7:2]=1
circ_compl2.and_matrix[4,2]=1
circ_compl2.and_matrix[4,5]=1
circ_compl2.and_matrix[5,2]=1
circ_compl2.and_matrix[5,7]=1
circ_compl2.and_matrix[6,3]=1
circ_compl2.and_matrix[6,4]=1
circ_compl2.and_matrix[6,6]=1
circ_compl2.and_matrix[7,5]=1
circ_compl2.and_matrix[7,6]=1
circ_compl2.and_matrix[8,4]=1
circ_compl2.and_matrix[8,7]=1
circ_compl2.and_matrix[9,7]=1

circ_compl2.or_matrix[0:4,0]=1
circ_compl2.or_matrix[4:7,1]=1
circ_compl2.or_matrix[7:9,2]=1
circ_compl2.or_matrix[9,3]=1

# ------------------------------------------------------------------------------------------------------- #
#	6 bit square root floor
# ------------------------------------------------------------------------------------------------------- #
circ_sqrt=Circuit( 6, 3, 16 )
circ_sqrt.description='6 bit square root floor'
circ_sqrt.labels_i=['A5','A4','A3','A2','A1','A0']
circ_sqrt.labels_o=['B2','B1','B0']

circ_sqrt.and_matrix[0,1]=1
circ_sqrt.and_matrix[1,3]=1
circ_sqrt.and_matrix[2,2]=1
circ_sqrt.and_matrix[2,5]=1
circ_sqrt.and_matrix[3,2]=1
circ_sqrt.and_matrix[3,7]=1
circ_sqrt.and_matrix[4,1:4:2]=1
circ_sqrt.and_matrix[5,0:8:2]=1
circ_sqrt.and_matrix[5,9]=1
circ_sqrt.and_matrix[6,0:8:2]=1
circ_sqrt.and_matrix[6,11]=1
circ_sqrt.and_matrix[7,0]=1
circ_sqrt.and_matrix[7,5]=1
circ_sqrt.and_matrix[7,7]=1
circ_sqrt.and_matrix[8,0]=1
circ_sqrt.and_matrix[8,5]=1
circ_sqrt.and_matrix[8,9]=1
circ_sqrt.and_matrix[9,0]=1
circ_sqrt.and_matrix[9,5]=1
circ_sqrt.and_matrix[9,11]=1
circ_sqrt.and_matrix[10,1:4:2]=1
circ_sqrt.and_matrix[10,5]=1
circ_sqrt.and_matrix[11,1:4:2]=1
circ_sqrt.and_matrix[11,7]=1
circ_sqrt.and_matrix[12,1:4:2]=1
circ_sqrt.and_matrix[12,9]=1
circ_sqrt.and_matrix[13,1:4:2]=1
circ_sqrt.and_matrix[13,11]=1
circ_sqrt.and_matrix[14,1]=1
circ_sqrt.and_matrix[14,2:8:2]=1

circ_sqrt.or_matrix[0:2,0]=1
circ_sqrt.or_matrix[2:5,1]=1
circ_sqrt.or_matrix[5:15,2]=1

# lista di tutti i circuiti
circs   = [ circ_h, circ_a, circ_b, circ_compl1, circ_compl2, circ_mult2, circ_sqrt, circ_r32, circ_mlg, circ_e, circ_s, circ_d, circ_bcd, circ_m, circ_g, circ_c, circ_sr , circ_t, circ_jk, circ_pc, circ_crc3]
