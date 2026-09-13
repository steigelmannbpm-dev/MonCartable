# -*- coding: utf-8 -*-
from kivy.config import Config
try:
    import android
    IS_ANDROID = True
except ImportError:
    IS_ANDROID = False
    Config.set('graphics', 'width', '400')
    Config.set('graphics', 'height', '780')
    Config.set('graphics', 'resizable', False)

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle, RoundedRectangle
from datetime import datetime

BG=(0.08,0.07,0.15,1);VIOLET=(0.42,0.37,0.92,1);VIOLET_DARK=(0.25,0.25,0.45,1)
VIOLET_DAY=(0.35,0.35,0.70,1);BLANC=(1,1,1,1);GRIS_TEXTE=(0.9,0.9,0.9,1)
VIOLET_CLAIR=(0.75,0.75,1,1);VERT=(0.3,0.9,0.3,1)

MON_EMPLOI_DU_TEMPS = {
    'Lundi':    ['Sport','Arts','Francais','espagnol','Histoire-Geo'],
    'Mardi':    ['SvT','Histoire-Geo','Maths','Technologie','Sport'],
    'Mercredi': ['Maths','Anglais','Francais','physique chimie'],
    'Jeudi':    ['Francais','Technologie','Anglais','espagnol','Maths'],
    'Vendredi': ['Anglais','Musique','Francais','espagnol'],
}
MON_MATERIEL = {
    'Maths':           ['Cahier de maths','Livre de maths','Calculatrice','Regle + Equerre'],
    'Francais':        ['Classeur de francais','Livre de francais'],
    'Histoire-Geo':    ['Cahier histoire-geo','Livre histoire-geo'],
    'Sport':           ['Tenue de sport','Deodorant','Baskets'],
    'Anglais':         ['Cahier d anglais','Livre d anglais'],
    'physique chimie': ['Porte vue de physique chimie'],
    'Arts':            ['Crayons de couleur','Cahier d arts plastiques'],
    'Musique':         ['Cahier de musique'],
    'SvT':             ['Cahier de svt'],
    'Technologie':     ['Classeur de technologie'],
    'espagnol':        ['Cahier d espagnol'],
}

def fond_sombre(w):
    with w.canvas.before:
        Color(*BG); r=Rectangle(pos=w.pos,size=w.size)
    w.bind(pos=lambda s,v:setattr(r,'pos',v),size=lambda s,v:setattr(r,'size',v))

class EcranAccueil(Screen):
    def __init__(self,**kw):
        super().__init__(**kw); fond_sombre(self)
        lay=BoxLayout(orientation='vertical',padding=dp(25),spacing=dp(18))
        lay.add_widget(Widget(size_hint_y=None,height=dp(30)))
        lay.add_widget(Label(text='Mon Cartable',font_size=dp(34),bold=True,color=BLANC,size_hint_y=None,height=dp(55)))
        self.lbl=Label(text='Bonjour !',font_size=dp(18),color=(0.7,0.7,1,1),size_hint_y=None,height=dp(40))
        lay.add_widget(self.lbl)
        lay.add_widget(Widget(size_hint_y=None,height=dp(10)))
        b1=Button(text='Checklist du jour',font_size=dp(20),background_color=VIOLET,size_hint_y=None,height=dp(70))
        b1.bind(on_press=lambda x:setattr(self.manager,'current','checklist'))
        lay.add_widget(b1)
        b2=Button(text='Mon emploi du temps',font_size=dp(20),background_color=(0.35,0.30,0.85,1),size_hint_y=None,height=dp(70))
        b2.bind(on_press=lambda x:setattr(self.manager,'current','emploi'))
        lay.add_widget(b2)
        lay.add_widget(Widget())
        lay.add_widget(Label(text='Bonne journee !',font_size=dp(15),color=(0.5,0.5,0.8,1),size_hint_y=None,height=dp(40)))
        self.add_widget(lay)
    def on_enter(self):
        j=['Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche']
        n=datetime.now().weekday()
        self.lbl.text=('Aujourd hui : '+j[n]) if n<5 else 'C est le week-end !'

class EcranChecklist(Screen):
    def __init__(self,**kw):
        super().__init__(**kw); fond_sombre(self); self.jour_actuel='Lundi'
        main=BoxLayout(orientation='vertical',padding=dp(15),spacing=dp(8))
        top=BoxLayout(size_hint_y=None,height=dp(55),spacing=dp(10))
        br=Button(text='< Retour',size_hint_x=None,width=dp(110),background_color=VIOLET_DARK,font_size=dp(16))
        br.bind(on_press=lambda x:setattr(self.manager,'current','accueil'))
        top.add_widget(br); top.add_widget(Label(text='Checklist',font_size=dp(24),bold=True,color=BLANC))
        main.add_widget(top)
        gj=GridLayout(cols=5,size_hint_y=None,height=dp(45),spacing=dp(4))
        for c,l in [('Lun','Lundi'),('Mar','Mardi'),('Mer','Mercredi'),('Jeu','Jeudi'),('Ven','Vendredi')]:
            b=Button(text=c,background_color=VIOLET_DAY)
            b.bind(on_press=lambda x,j=l:self.changer_jour(j)); gj.add_widget(b)
        main.add_widget(gj)
        self.lbl_t=Label(text='',font_size=dp(20),bold=True,color=(0.75,0.8,1,1),size_hint_y=None,height=dp(38))
        main.add_widget(self.lbl_t)
        sc=ScrollView(); self.gr=GridLayout(cols=1,spacing=dp(5),size_hint_y=None,padding=dp(5))
        self.gr.bind(minimum_height=self.gr.setter('height')); sc.add_widget(self.gr); main.add_widget(sc)
        self.add_widget(main)
    def on_enter(self):
        j=['Lundi','Mardi','Mercredi','Jeudi','Vendredi']
        n=datetime.now().weekday(); self.changer_jour(j[n] if n<5 else 'Lundi')
    def changer_jour(self,jour):
        self.jour_actuel=jour; self.lbl_t.text='Materiel pour '+jour; self.afficher_liste()
    def afficher_liste(self):
        self.gr.clear_widgets()
        if self.jour_actuel not in MON_EMPLOI_DU_TEMPS: return
        for mat in MON_EMPLOI_DU_TEMPS[self.jour_actuel]:
            self.gr.add_widget(Label(text='[b]'+mat+'[/b]',markup=True,font_size='18sp',color=VIOLET_CLAIR,size_hint_y=None,height='40dp',halign='left',text_size=(Window.width-40,None)))
            if mat in MON_MATERIEL:
                for item in MON_MATERIEL[mat]:
                    lg=BoxLayout(orientation='horizontal',size_hint_y=None,height='44dp',spacing='10dp')
                    cb=CheckBox(size_hint=(None,None),size=('44dp','44dp'),color=(0.6,0.6,1,1))
                    lb=Label(text=item,font_size='16sp',color=GRIS_TEXTE,halign='left',text_size=(Window.width-80,None))
                    cb.mon_label=lb; cb.bind(active=self.cocher); lg.add_widget(cb); lg.add_widget(lb); self.gr.add_widget(lg)
    def cocher(self,cb,v): cb.mon_label.color=VERT if v else GRIS_TEXTE

class EcranEmploiDuTemps(Screen):
    def __init__(self,**kw):
        super().__init__(**kw); fond_sombre(self); self._ok=False
        main=BoxLayout(orientation='vertical',padding=dp(15),spacing=dp(8))
        top=BoxLayout(size_hint_y=None,height=dp(55),spacing=dp(10))
        br=Button(text='< Retour',size_hint_x=None,width=dp(110),background_color=VIOLET_DARK,font_size=dp(16))
        br.bind(on_press=lambda x:setattr(self.manager,'current','accueil'))
        top.add_widget(br); top.add_widget(Label(text='Emploi du temps',font_size=dp(22),bold=True,color=BLANC))
        main.add_widget(top)
        sc=ScrollView(); self.gr=GridLayout(cols=1,spacing=dp(10),size_hint_y=None,padding=dp(5))
        self.gr.bind(minimum_height=self.gr.setter('height')); sc.add_widget(self.gr); main.add_widget(sc)
        self.add_widget(main)
    def on_enter(self):
        if self._ok: return
        self._ok=True
        for jour,mats in MON_EMPLOI_DU_TEMPS.items():
            h=len(mats)*dp(30)+dp(60)
            box=BoxLayout(orientation='vertical',size_hint_y=None,height=h,padding=dp(12),spacing=dp(4))
            with box.canvas.before:
                Color(0.18,0.16,0.32,1); rect=RoundedRectangle(pos=box.pos,size=box.size,radius=[12])
            box._rect=rect
            box.bind(pos=lambda w,v:setattr(w._rect,'pos',v),size=lambda w,v:setattr(w._rect,'size',v))
            box.add_widget(Label(text='[b]'+jour+'[/b]',markup=True,font_size='18sp',color=(0.8,0.8,1,1),size_hint_y=None,height='36dp'))
            for mat in mats:
                box.add_widget(Label(text='  - '+mat,font_size='16sp',color=GRIS_TEXTE,size_hint_y=None,height='28dp',halign='left',text_size=(Window.width-50,None)))
            self.gr.add_widget(box)

class CartableApp(App):
    def build(self):
        self.title='Mon Cartable'
        sm=ScreenManager()
        sm.add_widget(EcranAccueil(name='accueil'))
        sm.add_widget(EcranChecklist(name='checklist'))
        sm.add_widget(EcranEmploiDuTemps(name='emploi'))
        return sm

if __name__=='__main__': CartableApp().run()
