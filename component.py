﻿# -*- coding: utf-8 -*-
# ======================================================================================================= #
#   
#   $Log: component.py,v $
#
#   Revision 3.0  2018/07/10 16:32:51  matteo
#   Il programma è ora compatibile con Python3, oltre che con Python2. 
#
#   Revision 2.1  2012/07/29 15:55:06  alice
#   Il programma è stato reso eseguibile, e dotato di opzioni dalla riga di
#   comando. Sono inoltre state implementate ulteriori dipendenze di parametri
#   dimensionali in modo da rendere il simulatore ancor più ridimensionabile
#   automaticamente sulla base di dimensione orizzontale e numero di I/O/AND.
#
#   Revision 2.0  2012/06/13 14:00:59  alice
#   Commenti adattati al metalinguaggio epytext, per la generazione automatica della
#   documentazione.
#   
#   Revision 1.5  2012/06/08 08:48:55  alice
#   Modificata l'acquisizione della libreria per una massima flessibilità;
#   aggiunti tutti i circuiti disponibili sul testo Tanenbaum e altri.
#   
#   Revision 1.4  2012/06/06 07:54:09  alice
#   Completata l'aggiunta di circuiti da libreria, con possibilità di numero
#   arbitrario di input e output, purché entro quelli del PLA
#   
#   Revision 1.3  2012/04/16 09:52:35  alice
#   Prima versione completa con pulsanti RUN e RESET
#   
#   Revision 1.2  2012/03/30 15:12:02  alice
#   Semplice sistemazione del codice e inserimento commenti, nessuna modifica
#   funzionale
#   
#   Revision 1.1.1.1  2012/02/29 16:41:00  alice
#   Programmable Logic Array simulator
#   
# ======================================================================================================= #

"""
Classi di tutti i componenti elettronici del simulatore.
@authors: Alice Plebe, Matteo Cavallaro
@version: 3.0
"""
from sys import version_info
if version_info[0]==2:
    from Tkinter    import Tk, Frame, Canvas
    from Tkinter    import Button
    from Tkinter    import ARC, HIDDEN, NORMAL, DISABLED
elif version_info[0]==3:
    from tkinter    import Tk, Frame, Canvas
    from tkinter    import Button
    from tkinter    import ARC, HIDDEN, NORMAL, DISABLED
from math       import pi, sin, cos, acos, asin, sqrt

class Component( object ):
    """
    Classe astratta di tutti i componenti circuitali nella loro forma grafica.

    Ogni sottoclasse va istanziata con primo argomento un oggetto di classe Pla.
    Tuti i valori geometrici sono trattati in coordinate normalizzate, e solo nel momento
    di chiamare le primitive grafiche sono trasformati in valori assoluti (pixel).

    Per tutti i componenti, Wire e pin di ingresso e uscita esclusi, viene validato l'attributo I{tags}
    di Tkinter con una stringa composta dal nome del componente e il suo numero progressivo.
    """
    __abstract  = True

        
class Port( Component ):
    """
    Classe delle porte logiche.

    Tutte le sottoclassi avranno un loro attributo di classe 'count' che contiene il numero di
    porte correntemente istanziate di quel tipo.
    Tutte le sottoclassi avranno un loro attributo di classe 'name' con il prefisso del rispettivo
    tipo di porta.

    @cvar size: grandezza complessiva di una porta
    @type size: dimensione normalizzata 0..1
    @cvar thick: spessore dei contorni di una porta
    @cvar color: colore dei bordi di una porta
    """

    size    = 0.04          # dimensione complessiva in coordinate normalizzate
    thick   = 1             # spessore dei contorni
    color   = 'black'       # colore dei bordi



# ======================================================================================================= #



class Not( Port ):
    """
    Classe della porta logica NOT.

    La porta viene disegnata in orientamento verticale con ingresso in alto, quindi con un triangolo
    equilatero al cui vertice è\ aggiunto un piccolo cerchio.

    @ivar count: numero di porte NOT correntemente istanziate
    @cvar name: prefisso della porta NOT
    @ivar y_not: coordinata verticale del centro della porta NOT
    @type y_not: dimensione normalizzata 0..1
    @cvar c_size: diametro del cerchio da cui è50 composta la porta NOT
    @type c_size: frazione della dimensione totale della porta
    @ivar tag: tag dell'oggetto grafico delineante la porta
    @type tag: Tkinter widget tag
    @ivar x: coordinata orizzontale del centro della porta
    @type x: dimensione normalizzata 0..1
    @ivar y_in: coordinata verticale del pin di ingresso della porta
    @type y_in: dimensione normalizzata 0..1
    @ivar y_out: coordinata verticale del pin di uscita della porta
    @type y_out: dimensione normalizzata 0..1
    """

    count       = 0
    name        = 'not_'
    y_not       = 0.        # altezza del centro della NOT
    c_size      = 0.2       # diametro del cerchio, come frazione della dimensione totale


    def __init__( self, pla, x ):
        """
        Istanzia una porta NOT.

        @param pla: il simulatore
        @type pla: Pla
        @param x: coordinata orizzontale del centro della porta
        @type x: dimensione normalizzata 0..1
        """
        self.tag    = self.name + str( Not.count )

        h           = self.size - self.c_size * self.size
        l           = 2 * h / sqrt( 3 )

        y0_nor      = self.y_not - l / 4
        x0_nor      = x  - l / 2

        y0          = pla.nor_to_abs( y0_nor )
        y1          = pla.nor_to_abs( y0_nor + h )
        y2          = pla.nor_to_abs( y0_nor + self.size )

        x0          = pla.nor_to_abs( x0_nor )
        x1          = pla.nor_to_abs( x0_nor + l )
        xc1         = pla.nor_to_abs( x - self.c_size * self.size / 2 )
        xc2         = pla.nor_to_abs( x + self.c_size * self.size / 2 )

        triang      = ( x1, y0, x0, y0, pla.nor_to_abs( x ), y1 )
        self.triang = pla.canvas.create_polygon(
                *triang,
                tags=self.tag,
                width=self.thick,
                outline=self.color,
                fill=''
        )

        circ        = ( xc1, y1, xc2, y2 )
        self.circ   = pla.canvas.create_oval(
                *circ,
                tags=self.tag,
                width=self.thick,
                outline=self.color,
                fill=''
        )

        self.x      = x
        self.y_in   = y0_nor
        self.y_out  = y0_nor + self.size

        Not.count   += 1



    def pin_in( self ):
        """
        Calcola le coordinate del punto di ingresso della porta.
        @return: coordinate normalizzate del punto di ingresso della porta
        """
        return ( self.x, self.y_in )


    def pin_out( self ):
        """
        Calcola le coordinate del punto di uscita della porta.
        @return: coordinate normalizzate del punto di uscita della porta
        """
        return ( self.x, self.y_out )



# ------------------------------------------------------------------------------------------------------- #



class Or( Port ):
    """
    Classe della porta logica OR.

    La porta viene disegnata in orientamento verticale con ingresso in alto, ed è composta mediante:
        - arco di cerchio con centro sull'asse, per la sua base
        - due linee verticali parallele
        - due archi di cerchio con centri sfasati rispetto all'asse, per la punta

    @ivar count: numero di porte OR correntemente istanziate
    @cvar name: prefisso della porta OR
    @ivar pla: il simulatore
    @type pla: Pla
    @ivar y_or: coordinata verticale del centro della porta OR
    @type y_or: dimensione normalizzata 0..1
    @cvar line_s: dimensione delle linee costituenti la porta
    @type line_s: frazione della dimensione totale della porta
    @cvar elong: rapporto tra lunghezza (verticale) e larghezza (orizzontale) della porta OR
    @cvar r_top: rapporto tra raggio dei cerchi usati per la punta e dimensione della porta
    @cvar r_bottom: rapporto tra raggio del cerchio usato per la base e dimensione della porta
    @cvar top_sharp: inverso dell'acutezza della punta
    @cvar adjust: fattore correttivo della dimensione della porta OR per equipararla alla porta AND
    @ivar tag: tag dell'oggetto grafico delineante la porta
    @type tag: Tkinter widget tag
    @ivar x: coordinata orizzontale del centro della porta
    @type x: dimensione normalizzata 0..1
    @ivar y_in: coordinata verticale del pin di ingresso della porta
    @type y_in: dimensione normalizzata 0..1
    @ivar y_out: coordinata verticale del pin di uscita della porta
    @type y_out: dimensione normalizzata 0..1
    """

    count       = 0
    name        = 'or_'
    y_or        = 0.        # altezza del centro della OR
    line_s      = 0.4       # dimensione delle linee, come frazione della dimensione totale
    elong       = 1.7       # rapporto tra lunghezza (verticale) e larghezza (orizzontale) delle porte
    r_top       = 0.5       # rapporto tra raggio dei cerchi usati per la punta e dimensione
    r_bottom    = 0.7       # rapporto tra raggio del cerchio usato per la base e dimensione
    top_sharp   = 0.2       # inverso dell'acutezza della punta
    adjust      = 1.4       # fattore correttivo della dimensione per equipararla alla AND
    pla         = None      # l'oggetto circuito


    def _rad_to_deg( self, ang ):
        """
        Funzione di ausilio per la conversione da radianti in gradi

        @param ang: angolo espresso in radianti
        @return: angolo espresso in gradi (interi)
        """
        return int( round( 180 * ang / pi ) )


    def draw_lines( self, xa_0, xa_2, ya_0, ya_2 ):
        """
        Traccia le linee verticali della porta

        Il metodo non restituisce nulla, inserisce gli oggetti widget
        nella lista self.lines

        @param xa_0: coordinata orizzontale della linea sinistra
        @param xa_0: coordinata orizzontale della linea destra
        @param ya_0: coordinata verticale del vertice superiore delle linee
        @param ya_2: coordinata verticale del vertice inferiore delle linee
        """

        x0          = self.pla.nor_to_abs( xa_0 )
        x1          = self.pla.nor_to_abs( self.x )
        x2          = self.pla.nor_to_abs( xa_2 )
        y0          = self.pla.nor_to_abs( ya_0 )
        y1          = self.pla.nor_to_abs( self.y_or )
        y2          = self.pla.nor_to_abs( ya_2 )

        line        = ( x0, y0, x0, y2 )
        l           = []
        self.lines.append( self.pla.canvas.create_line(
                *line,
                width=self.thick,
                tags=self.tag,
                fill=self.color )
        )
        line        = ( x2, y0, x2, y2 )
        self.lines.append( self.pla.canvas.create_line(
                *line,
                width=self.thick,
                tags=self.tag,
                fill=self.color )
        )



    def draw_bottom( self, ra, theta ):
        """
        Disegna l'arco per la base della porta

        Il metodo non restituisce nulla, inserisce gli oggetti widget
        nella lista self.arcs
        
        @param ra: raggio dell'arco
        @param theta: semiangolo del vertice superiore del triangolo isoscele su cui insiste l'arco
        """

        x1      = self.pla.nor_to_abs( self.x )
        r       = self.pla.nor_to_abs( ra )
        bx0     = x1 - r
        bx1     = x1 + r
        by1     = self.pla.nor_to_abs( self.y_in )
        bb      = ( bx0, by1 - 2 * r, bx1, by1 )
        t0      = self._rad_to_deg( 3 * pi / 2 - theta )
        t1      = self._rad_to_deg( 2 * theta )

        self.arcs.append( self.pla.canvas.create_arc(
                bb,
                start=t0,
                extent=t1,
                tags=self.tag,
                width=self.thick,
                fill=self.color,
                style=ARC )
        )



    def draw_top( self, xa_delta, ya_c, ra, theta, delta ):
        """
        Disegna i due archi per la punta della porta

        Il metodo non restituisce nulla, inserisce gli oggetti widget
        nella lista self.arcs
        
        @param xa_delta: offset tra il centro orizzontale della porta, e i centri delle circonferenze
        @param ya_c: coordinata verticale dei centri delle circonferenze
        @param ra: raggio degli archi
        @param theta: angolo formato tra il segmento che congiunge il vertice inferiore della linea
        sinistra (che è anche vertice superiore dell'arco sinistro) con il centro
        della circonferenza per l'arco sinsitro, e l'asse orizzontale
        @param delta: angolo formato tra il segmento che congiunge il vertice inferiore degli archi
        con il centro della circonferenza per l'arco sinsitro, e l'asse verticale
        """

        y0      = self.pla.nor_to_abs( ya_c - ra )
        y1      = self.pla.nor_to_abs( ya_c + ra )
        r       = self.pla.nor_to_abs( ra )
        alfa    = pi / 2 - theta - delta

        xc      = self.pla.nor_to_abs( self.x + xa_delta )
        bb      = ( xc - r, y0, xc + r, y1 )
        t0      = self._rad_to_deg(  pi + theta )
        t1      = self._rad_to_deg( alfa )

        self.arcs.append( self.pla.canvas.create_arc(
                bb,
                start=t0,
                extent=t1,
                tags=self.tag,
                width=self.thick,
                fill=self.color,
                style=ARC )
        )

        xc      = self.pla.nor_to_abs( self.x - xa_delta )
        bb      = ( xc - r, y0, xc + r, y1 )
        t0      = self._rad_to_deg( 3 * pi / 2 + delta )
        self.arcs.append( self.pla.canvas.create_arc(
                bb,
                start=t0,
                extent=t1,
                tags=self.tag,
                width=self.thick,
                fill=self.color,
                style=ARC )
        )



    def __init__( self, pla, x ):
        """
        Istanzia una porta OR.

        @param pla: il simulatore
        @type pla: Pla
        @param x: coordinata orizzontale del centro della porta
        @type x: dimensione normalizzata 0..1
        """
        self.x      = x
        self.tag    = self.name + str( Or.count )
        self.lines  = []
        self.arcs   = []
        self.pla    = pla

        self.size   *= self.adjust
        half_w      = 0.5 * self.size / self.elong
        half_h      = 0.5 * self.size
        xa_0        = x - half_w
        xa_2        = x + half_w
        ya_0        = self.y_or - half_h
        ya_2        = ya_0 + self.line_s * self.size

        ra          = self.r_bottom * self.size
        theta       = asin( half_w / ra )
        h_top       = ra * cos( theta )
        self.y_in   = ya_0 + ( ra - h_top )
        self.y_out  = ya_0 + self.size / self.adjust


        self.draw_lines( xa_0, xa_2, ya_0, ya_2 )
        self.draw_bottom( ra, theta )

        ra          = self.r_top * self.size
        ya_delta    = self.top_sharp * self.size
        ya_c        = ya_2 - ya_delta
        theta       = asin( ya_delta / ra )
        xa_delta    = ra * cos( theta ) - half_w
        delta       = asin( xa_delta / ra )

        self.draw_top( xa_delta, ya_c, ra, theta, delta )

        Or.count  += 1



    def pin_in( self ):
        """
        Calcola le coordinate del punto di ingresso della porta.
        @return: coordinate normalizzate del punto di ingresso della porta
        """
        return ( self.x, self.y_in )


    def pin_out( self ):
        """
        Calcola le coordinate del punto di uscita della porta.
        @return: coordinate normalizzate del punto di uscita della porta
        """
        return ( self.x, self.y_out )



# ------------------------------------------------------------------------------------------------------- #



class And( Port ):
    """
    Classe della porta logica AND.

    La porta viene disegnata in orientamento orizzontale con ingresso a sinistra, ed è composta mediante:
        - poligonale con due linee orizzontali parallele e una verticale
        - arco di cerchio con centro sull'asse, per la sua parte anteriore

    @ivar count: numero di porte AND correntemente istanziate
    @cvar name: prefisso della porta AND
    @ivar x_and: coordinata orizzontale del centro della porta AND
    @type x_and: dimensione normalizzata 0..1
    @cvar line_s: dimensione delle linee costituenti la porta
    @type line_s: frazione della dimensione totale della porta
    @ivar status: stato logico della porta
    @ivar locked: variabile indicante se la porta è inattiva
    @type locked: boolean
    @ivar text: area di testo dove viene visualizzato lo I{status} della porta
    @type text: Tkinter.Canvas object ID
    @ivar tag: tag dell'oggetto grafico delineante la porta
    @type tag: Tkinter widget tag
    @ivar y: coordinata verticale del centro della porta
    @type y: dimensione normalizzata 0..1
    @ivar x_in: coordinata orizzontale del pin di ingresso della porta
    @type x_in: dimensione normalizzata 0..1
    @ivar x_out: coordinata orizzontale del pin di uscita della porta
    @type x_out: dimensione normalizzata 0..1
    """

    count   = 0
    name    = 'and_'
    x_and   = 0.            # posizione orizzontale del centro della AND
    line_s  = 0.6           # dimensione delle linee, come frazione della dimensione totale
    status  = 0             # stato logico della porta
    locked  = False         # indicante se la porta e` inattiva
    text    = None          # area di testo dove viene visualizzato lo status


    def __init__( self, pla, y ):
        """
        Istanzia una porta AND.

        @param pla: il simulatore
        @type pla: Pla
        @param y: coordinata verticale del centro della porta
        @type y: dimensione normalizzata 0..1
        """
        cv          = pla.canvas

        self.y      = y
        self.x_in   = self.x_and - 0.5 * self.size
        self.x_out  = self.x_and + 0.5 * self.size

        x0          = pla.nor_to_abs( self.x_in )
        x1          = x0 + pla.nor_to_abs( self.line_s * self.size )

        r           = ( 1 - self.line_s ) * self.size

        y0          = pla.nor_to_abs( y - r )
        y1          = pla.nor_to_abs( y + r )

        t           = self.name + str( And.count )
        self.tag    = t

        lines       = ( x1, y0, x0, y0, x0, y1, x1, y1 )
        self.lines  = cv.create_line(
                *lines,
                width=self.thick,
                tags=t,
                fill=self.color
        )

        r_abs       = pla.nor_to_abs( r )

        bb          = ( x1 - r_abs, y0, x1 + r_abs, y1 )
        self.arc    = pla.canvas.create_arc(
                bb,
                start=270,
                extent=180,
                tags=t,
                width=self.thick,
                fill=self.color,
                style=ARC
        )

        self.text   = pla.canvas.create_text(
                pla.nor_to_abs( self.x_and ),
                pla.nor_to_abs( self.y ),
                state=HIDDEN,
                text='0'
        )

        And.count  += 1



    def value( self, pla, status ):
        """
        Aggiorna I{status} e I{text} della porta in base al valore indicato.

        @param pla: il simulatore
        @type pla: Pla
        @param status: nuovo stato logico della porta
        """
        if self.locked:
            return
        t   = 1 if status   else 0
        pla.canvas.itemconfigure( self.text, text=str( t ) )
        pla.canvas.itemconfigure( self.text, state=NORMAL )
        self.status = status


    def disable( self, pla ):
        """
        Disattiva una porta AND.

        @param pla: il simulatore
        @type pla: Pla
        """
        self.locked = True
        pla.canvas.itemconfigure( self.text, text='0' )
        pla.canvas.itemconfigure( self.text, state=HIDDEN )

    def reset( self, pla ):
        """
        Resetta una porta AND al suo stato iniziale.

        @param pla: il simulatore
        @type pla: Pla
        """
        self.locked = False
        pla.canvas.itemconfigure( self.text, text='0' )
        pla.canvas.itemconfigure( self.text, state=HIDDEN )
        self.status = 0



    def pin_in( self ):
        """
        Calcola le coordinate del punto di entrata della porta.
        @return: coordinate normalizzate del punto di entrata della porta
        """
        return ( self.x_in, self.y )


    def pin_out( self ):
        """
        Calcola le coordinate del punto di uscita della porta.
        @return: coordinate normalizzate del punto di uscita della porta
        """
        return ( self.x_out, self.y )



# ======================================================================================================= #



class Fuse( Component ):
    """
    Classe dei fusibili.

    Vengono considerate più categorie di fusibili, pertanto il nome di un tipo di fusibile è
    composto dall'attributo I{name}, più un suffisso specificato come argomento, ed è conservato
    nell'attributo I{category}.

    @ivar count: numero di fusibili correntemente istanziati per ogni categoria
    @cvar name: prefisso del fusibile
    @ivar status: stato del fusibile (è I{False} quando esso risulta interrotto)
    @type status: boolean
    @ivar category: nome completo del fusibile, comprendente il suffisso della categoria a cui appartiene
    @cvar size: grandezza complessiva di un fusibile
    @type size: dimensione normalizzata 0..1
    @cvar thick: spessore dei contorni di un fusibile
    @cvar color: colore dei bordi di un fusibile
    @ivar tag: tag dell'oggetto grafico delineante la porta
    @type tag: Tkinter widget tag
    @ivar y: coordinata verticale del centro del fusibile
    @type y: dimensione normalizzata 0..1
    @ivar x_in: coordinata orizzontale del pin di ingresso del fusibile
    @type x_in: dimensione normalizzata 0..1
    @ivar x_out: coordinata orizzontale del pin di uscita del fusibile
    @type x_out: dimensione normalizzata 0..1
    """

    count       = {}        # conteggio totale dei fusibili per ogni loro categoria
    name        = 'fuse_'
    category    = ''        # nome completo del componente
    status      = True      # False quando il fusibile e` interrotto
    size        = 0.009     # dimensione complessiva in coordinate normalizzate
    thick       = 1         # spessore dei contorni
    color       = 'black'   # colore dei bordi


    def __init__( self, pla, x, y, suffix='' ):
        """
        Istanzia un fusibile.

        @param pla: il simulatore
        @type pla: Pla
        @param x: coordinata orizzontale del centro del fusibile
        @type x: dimensione normalizzata 0..1
        @param y: coordinata verticale del centro del fusibile
        @type y: dimensione normalizzata 0..1
        @param suffix: suffisso indicante la categoria di appartenenza del fusibile
        """
        self.category   = self.name + suffix
        self.center     = ( x, y )

        if self.category not in Fuse.count.keys():
            Fuse.count[ self.category ] = 0

        self.tag        = self.category + str( Fuse.count[ self.category ] )

        r           = 0.5 * self.size

        x0          = pla.nor_to_abs( x - r )
        x1          = pla.nor_to_abs( x + r )
        y0          = pla.nor_to_abs( y - r )
        y1          = pla.nor_to_abs( y + r )

        self.circ   = ( x0, y0, x1, y1 )
        self._fuse_on( pla )

        self.y      = y
        self.x_in   = x - r
        self.x_out  = x + r

        Fuse.count[ self.category ] += 1



    def _fuse_on( self, pla ):
        """
        Modifica l'aspetto visivo del fusibile in modo da mostrarlo collegato.

        @param pla: il simulatore
        @type pla: Pla
        """
        self.blob   = pla.canvas.create_oval(
            *self.circ,
            tags=self.tag,
            width=self.thick,
            outline=self.color,
            fill=self.color
        )


    def _fuse_off( self, pla ):
        """
        Modifica l'aspetto visivo del fusibile in modo da mostrarlo interrotto.

        @param pla: il simulatore
        @type pla: Pla
        """
        self.blob   = pla.canvas.create_arc(
            self.circ,
            start=0,
            extent=180,
            tags=self.tag,
            width=self.thick,
            fill=self.color,
            style=ARC
        )


    def toggle( self, pla ):
        """
        Scambia lo stato attuale del fusibile.

        @param pla: il simulatore
        @type pla: Pla
        """
        pla.canvas.delete( self.tag )
        if self.status:
            self._fuse_off( pla )
            self.status = False
        else:
            self._fuse_on( pla )
            self.status = True


    def deset( self, pla ):
        """
        Setta lo stato scollegato a un fusibile.

        @param pla: il simulatore
        @type pla: Pla
        """
        if self.status:
            pla.canvas.delete( self.tag )
            self._fuse_off( pla )
            self.status = False

    def reset( self, pla ):
        """
        Resetta lo stato collegato a un fusibile.

        @param pla: il simulatore
        @type pla: Pla
        """
        if not self.status:
            self._fuse_on( pla )
            self.status = True


    def pin_in( self ):
        """
        Calcola le coordinate del pin a ovest del fusibile.
        @return: coordinate normalizzate del pin a ovest del fusibile
        """
        return ( self.x_in, self.y )


    def pin_out( self ):
        """
        Calcola le coordinate del pin a est del fusibile.
        @return: coordinate normalizzate del pin a est del fusibile
        """
        return ( self.x_out, self.y )



# ======================================================================================================= #



class Wire( Component ):
    """
    Classe dei fili di collegamento

    Un filo viene inizializzata specificando gli oggetti di classe Component di partenza e di arrivo del
    collegamento, e con l'argomento opzionale I{placement} se il collegamento deve essere al pin
    del Component oppure al suo centro.

    @cvar thick: spessore della linea del filo di collegamento
    @cvar color: colore della linea del filo di collegamento
    """

    thick   = 1             # spessore della linea
    color   = 'black'       # colore della linea

    
    def __init__( self, pla, c_from, c_to, placement=( 'pin', 'pin' ) ):
        """
        Istanzia un filo di collegamento.

        @param pla: il simulatore
        @type pla: Pla
        @param c_from: componente collegato alla partenza del filo
        @type c_from: Component
        @param c_to: componente collegato all'arrivo del filo
        @type c_to: Component
        @param placement: indica se il collegamento va effettuato al pin del componente (default),
        o al suo centro
        """
        if placement[ 0 ] == 'pin':
            x0  = pla.nor_to_abs( c_from.pin_out()[ 0 ] )
            y0  = pla.nor_to_abs( c_from.pin_out()[ 1 ] )
        else:
            x0  = pla.nor_to_abs( c_from.center[ 0 ] )
            y0  = pla.nor_to_abs( c_from.center[ 1 ] )
        if placement[ 1 ] == 'pin':
            x1  = pla.nor_to_abs( c_to.pin_in()[ 0 ] )
            y1  = pla.nor_to_abs( c_to.pin_in()[ 1 ] )
        else:
            x1  = pla.nor_to_abs( c_to.center[ 0 ] )
            y1  = pla.nor_to_abs( c_to.center[ 1 ] )

        pla.canvas.create_line( x0, y0, x1, y1, width=self.thick, fill=self.color )



# ======================================================================================================= #



class InPin( Component ):
    """
    Classe dei pin di ingresso del PLA realizzati mediante pulsanti.

    La classe comprende nell'attributo I{var} un oggetto Tkinter.IntVar, utile per propagare nel
    programma lo stato dei pin di ingresso.

    Al costruttore Button è assegnato l'argomento I{command} al metodo I{toggle}, che crea la gestione
    dell'evento del mouse che clicca sul pulsante, senza necessità di un'esplicita chiamata
    canvas.bind()

    @ivar x: coordinata orizzontale del centro del pin di input
    @type x: dimensione normalizzata 0..1
    @ivar y_in: coordinata verticale del centro del pin di input
    @type y_in: dimensione normalizzata 0..1
    @ivar y_lab: fattore di posizionamento della label nella finestra
    @type y_lab: pixel
    @ivar label: area di testo dove viene visualizzata l'etichetta dell'input
    @type label: Tkinter.Canvas object ID
    @ivar v: valore dello stato logico del pin
    @type v: Tkinter.IntVar
    """

    y_in    = 0.            # altezza del centro del pin
    label   = None          # testo dove viene visualizzata l'etichetta dell'input
    y_lab   = 540.          # fattore di posizionamento della label nella finestra


    def __init__( self, pla, x, v ):
        """
        Istanzia un pin di ingresso.

        @param pla: il simulatore
        @type pla: Pla
        @param x: coordinata orizzontale del punto di uscita del pin
        @param v: valore dello stato logico del pin
        @type v: Tkinter.IntVar
        """
        self.var    = v
        self.x      = x
        x0          = pla.nor_to_abs( x )
        y0          = pla.nor_to_abs( self.y_in )
        self.button = Button(
                        pla.root,
                        height=1,
                        width=2,
                        textvariable=v,
                        disabledforeground='#f0f0f0',   # non funziona!
                        command=self.toggle
        ) 
        b           = pla.canvas.create_window(
                x0,
                y0,
                window=self.button
        )
        yd  = pla.grid_delta * self.y_lab / pla.size[ 1 ]
        self.label  = pla.canvas.create_text(
                x0,
                y0 - pla.nor_to_abs( yd ),
                text=''
        )
    

    def set_label( self, pla, t ):
        """
        Setta l'etichetta dell'input con la stringa passata come parametro.

        @param pla: il simulatore
        @type pla: Pla
        @param t: stringa della nuova etichetta dell'input
        """
        pla.canvas.itemconfigure( self.label, text=t )


    def reset_label( self, pla ):
        """
        Resetta l'etichetta dell'input a stringa vuota.

        @param pla: il simulatore
        @type pla: Pla
        """
        pla.canvas.itemconfigure( self.label, text='' )


    def toggle( self ):
        """
        Scambia lo stato logico del pin
        """
        if self.var.get():
            self.var.set( 0 )
        else:
            self.var.set( 1 )


    def enable( self ):
        """
        Abilita il pin.
        """
        self.var.set( 0 )
        self.button.configure( state=NORMAL )
	

    def disable( self ):
        """
        Disabilita il pin.
        """
        self.var.set( 0 )
        self.button.configure( state=DISABLED )


    def reset( self, pla ):
        """
        Resetta il pin di input al suo stato iniziale.

        @param pla: il simulatore
        @type pla: Pla
        """
        self.var.set( 0 )
        self.button.configure( state=NORMAL )
        self.reset_label( pla )




    def wire_not( self, pla, c_not ):
        """
        Funzione ausiliaria per disegnare il collegamento tra pin di ingresso del PLA e gli
        ingressi delle porte NOT.

        @param pla: il simulatore
        @type pla: Pla
        @param c_not: porta logica NOT
        @type c_not: Component.Not
        """

        xc, yc	= c_not.pin_in()

        x0	= pla.nor_to_abs( self.x )
        y0	= pla.nor_to_abs( self.y_in + pla.grid_delta )
        x1	= pla.nor_to_abs( xc )
        y1	= y0
        x2	= x1
        y2	= pla.nor_to_abs( yc )

        pla.canvas.create_line( x0, y0, x1, y1, x2, y2, width=Wire.thick, fill=Wire.color )
    	
    	
    def pin_out( self ):
        """
        Calcola le coordinate del punto di uscita del pin.
        @return: coordinate normalizzate del punto di uscita del pin
        """
        return ( self.x, self.y_in )



# ======================================================================================================= #



class OutPin( Component ):
    """
    Classe dei pin di uscita del PLA.

    Il pin viene rappresentato da due cerchi concentrici.

    @param x: coordinata orizzontale del punto di uscita del pin
    @ivar y_in: coordinata verticale del centro del pin di output
    @type y_in: dimensione normalizzata 0..1
    @cvar size: grandezza complessiva di un pin
    @type size: dimensione normalizzata 0..1
    @cvar thick: spessore dei contorni di un fusibile
    @cvar color: colore dei bordi di un fusibile
    @ivar locked: variabile indicante se il pin è inattivo
    @type locked: boolean
    @ivar text: area di testo dove viene visualizzato lo stato del pin
    @type text: Tkinter.Canvas object ID
    @ivar label: area di testo dove viene visualizzata l'etichetta dell'output
    @type label: Tkinter.Canvas object ID
    """
    y_in    = 0.                # coordinata verticale del centro del pin di output
    size    = Port.size         # grandezza complessiva di un pin
    thick   = 1                 #
    color   = 'black'           #
    locked  = False             # indica se il pin e` inattivo
    text    = None              # testo dove viene visualizzato lo stato del pin
    label   = None              # testo dove viene visualizzata l'etichetta


    def __init__( self, pla, x ):
        """
        Istanzia un pin di ingresso.

        @param pla: il simulatore
        @type pla: Pla
        @param x: coordinata orizzontale del punto di uscita del pin
        @type x: dimensione normalizzata 0..1
        """
        r           = 0.5 * self.size
        r1          = 0.8 * r
        self.x	    = x
        
        self.y      = self.y_in + r

        x0          = pla.nor_to_abs( x - r )
        x1          = pla.nor_to_abs( x + r )
        y0          = pla.nor_to_abs( self.y - r )
        y1          = pla.nor_to_abs( self.y + r )

        circ	    = ( x0, y0, x1, y1 )

        self.circ   = pla.canvas.create_oval(
                *circ,
                width=self.thick,
                outline=self.color,
                fill=''
        )
        

        x0          = pla.nor_to_abs( x - r1 )
        x1          = pla.nor_to_abs( x + r1 )
        y0          = pla.nor_to_abs( self.y - r1 )
        y1          = pla.nor_to_abs( self.y + r1 )

        circ1	    = ( x0, y0, x1, y1 )

        self.circ1  = pla.canvas.create_oval(
                *circ1,
                width=self.thick,
                outline=self.color,
                fill=''
        )

        self.text   = pla.canvas.create_text(
                pla.nor_to_abs( self.x ),
                pla.nor_to_abs( self.y ),
                state=HIDDEN,
                text='0'
        )
        self.label  = pla.canvas.create_text(
                pla.nor_to_abs( self.x ),
                y0 + pla.nor_to_abs( 1.3 * pla.grid_delta ),
                text=''
        )


    def set_label( self, pla, t ):
        """
        Setta l'etichetta dell'output con la stringa passata come parametro.

        @param pla: il simulatore
        @type pla: Pla
        @param t: stringa della nuova etichetta del pin
        """
        pla.canvas.itemconfigure( self.label, text=t )


    def reset_label( self, pla ):
        """
        Resetta l'etichetta dell'output a stringa vuota.

        @param pla: il simulatore
        @type pla: Pla
        """
        pla.canvas.itemconfigure( self.label, text='' )


    def value( self, pla, status ):
        """
        Aggiorna I{text} del pin in base al valore di stato indicato.

        @param pla: il simulatore
        @type pla: Pla
        @param status: nuovo stato logico della porta
        """
        if self.locked:
            return
        t   = 1 if status else 0
        pla.canvas.itemconfigure( self.text, text=str( t ) )
        pla.canvas.itemconfigure( self.text, state=NORMAL )


    def disable( self, pla ):
        """
        Disabilita il pin.

        @param pla: il simulatore
        @type pla: Pla
        """
        self.locked = True
        pla.canvas.itemconfigure( self.text, text='0' )
        pla.canvas.itemconfigure( self.text, state=HIDDEN )


    def reset( self, pla ):
        """
        Resetta il pin di output al suo stato iniziale.

        @param pla: il simulatore
        @type pla: Pla
        """
        self.locked = False
        pla.canvas.itemconfigure( self.text, text='0' )
        pla.canvas.itemconfigure( self.text, state=HIDDEN )
        self.reset_label( pla )


    def pin_in( self ):
        """
        Calcola le coordinate del punto di entrata del pin.
        @return: coordinate normalizzate del punto di entrata del pin
        """
        return ( self.x, self.y_in )
