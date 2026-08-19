# =========================================================
# === INICIO BLOQUE 1: LIBRERIAS Y VARIABLES DE FILAS =====
# =========================================================
import os
import json
import random
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty
from kivy.metrics import dp

class FilaTabla(BoxLayout):
    pos_num = StringProperty("01")
    equipo_name = StringProperty("Equipo")
    pts, pj = StringProperty("0"), StringProperty("0")
    g, e, p = StringProperty("0"), StringProperty("0"), StringProperty("0")
    gf, gc, dg = StringProperty("0"), StringProperty("0"), StringProperty("0")
    es_lider = BooleanProperty(False)
    es_descenso = BooleanProperty(False)

class FilaFixture(BoxLayout):
    local = StringProperty("LOCAL")
    marcador = StringProperty("vs")
    visitante = StringProperty("VISITANTE")
    estado = StringProperty("-")

class FilaPromedios(BoxLayout):
    pos_num = StringProperty("01")
    equipo_name = StringProperty("Equipo")
    pts_acum = StringProperty("0")
    pj_acum = StringProperty("0")
    promedio = StringProperty("0.000")
    es_descenso = BooleanProperty(False)
# =========================================================
# === FIN BLOQUE 1 ========================================
# =========================================================
# =========================================================
# === INICIO BLOQUE 2: DISENO KV DE FILAS DE POSICIONES ===
# =========================================================
Builder.load_string('''
<FilaTabla>:
    orientation: 'horizontal'
    size_hint_y: None
    height: dp(38)
    canvas.before:
        Color:
            rgba: (0.12, 0.43, 0.23, 0.4) if root.es_lider else ((0.7, 0.2, 0.2, 0.4) if root.es_descenso else (0.13, 0.16, 0.19, 1))
        Rectangle:
            pos: self.pos
            size: self.size
    Label:
        text: " " + root.pos_num + "." + root.equipo_name
        font_size: '13sp'
        halign: 'left'
        text_size: self.width, None
    Label:
        text: root.pts
        font_size: '13sp'
        bold: True
        size_hint_x: None
        width: dp(38)
    Label:
        text: root.pj
        font_size: '13sp'
        size_hint_x: None
        width: dp(28)
    Label:
        text: root.g
        font_size: '13sp'
        size_hint_x: None
        width: dp(28)
    Label:
        text: root.e
        font_size: '13sp'
        size_hint_x: None
        width: dp(28)
    Label:
        text: root.p
        font_size: '13sp'
        size_hint_x: None
        width: dp(28)
    Label:
        text: root.gf
        font_size: '13sp'
        size_hint_x: None
        width: dp(28)
    Label:
        text: root.gc
        font_size: '13sp'
        size_hint_x: None
        width: dp(28)
    Label:
        text: root.dg
        font_size: '13sp'
        size_hint_x: None
        width: dp(32)
''')
# =========================================================
# === FIN BLOQUE 2 ========================================
# =========================================================
# =========================================================
# === INICIO BLOQUE 3: DISENO KV FIXTURES Y PROMEDIOS =====
# =========================================================
Builder.load_string('''
<FilaFixture>:
    orientation: 'horizontal'
    size_hint_y: None
    height: dp(40)
    canvas.before:
        Color:
            rgba: (0.11, 0.14, 0.17, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    Label:
        text: root.local
        font_size: '13sp'
        bold: True
        halign: 'right'
        text_size: self.width, None
    Label:
        text: root.marcador
        font_size: '14sp'
        bold: True
        color: (0.12, 0.73, 0.44, 1) if root.estado == 'JUGADO' else (0.7, 0.7, 0.7, 1)
        size_hint_x: None
        width: dp(65)
        halign: 'center'
    Label:
        text: root.visitante
        font_size: '13sp'
        bold: True
        halign: 'left'
        text_size: self.width, None

<FilaPromedios>:
    orientation: 'horizontal'
    size_hint_y: None
    height: dp(38)
    canvas.before:
        Color:
            rgba: (0.7, 0.2, 0.2, 0.4) if root.es_descenso else (0.13, 0.16, 0.19, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    Label:
        text: " " + root.pos_num + "." + root.equipo_name
        font_size: '13sp'
        halign: 'left'
        text_size: self.width, None
    Label:
        text: root.pts_acum
        font_size: '13sp'
        size_hint_x: None
        width: dp(55)
    Label:
        text: root.pj_acum
        font_size: '13sp'
        size_hint_x: None
        width: dp(55)
    Label:
        text: root.promedio
        font_size: '13sp'
        bold: True
        size_hint_x: None
        width: dp(75)

<CustomButton@Button>:
    background_normal: ''
    background_color: (0.15, 0.18, 0.22, 1)
    color: (1, 1, 1, 1)
    font_size: '14sp'
    bold: True
    size_hint_y: None
    height: dp(48)
''')
# =========================================================
# === FIN BLOQUE 3 ========================================
# =========================================================
# =========================================================
# === INICIO BLOQUE 4: DISENO KV MENU E INICIO DE LIGAS ===
# =========================================================
Builder.load_string('''
<MainScreen>:
    canvas.before:
        Color:
            rgba: (0.07, 0.09, 0.11, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        orientation: 'vertical'
        padding: dp(12)
        spacing: dp(12)
        Label:
            text: 'CAMPEONATO A.F.A.'
            font_size: '22sp'
            bold: True
            color: (0.12, 0.73, 0.44, 1)
            size_hint_y: None
            height: dp(50)
        Label:
            text: 'Se detecto la base de datos de equipos. Selecciona una opcion:'
            font_size: '14sp'
            color: (0.7, 0.74, 0.8, 1)
            text_size: self.width, None
            halign: 'center'
            size_hint_y: None
            height: dp(40)
        Widget:
            size_hint_y: None
            height: dp(20)
        CustomButton:
            text: '1. Continuar Ultimo Partido'
            on_release: root.seleccionar_opcion('1')
        CustomButton:
            text: '2. Reiniciar Campeonato (Fecha 1)'
            on_release: root.seleccionar_opcion('2')
        CustomButton:
            text: '3. Borrar Todo y Cargar por Defecto'
            on_release: root.seleccionar_opcion('3')
            background_color: (0.7, 0.2, 0.2, 1)
        Widget:
''')
# =========================================================
# === FIN BLOQUE 4 ========================================
# =========================================================
# =========================================================
# === INICIO BLOQUE 5: DISENO KV DE PESTANAS Y PANTALLAS ==
# =========================================================
Builder.load_string('''
<LeagueScreen>:
    canvas.before:
        Color:
            rgba: (0.07, 0.09, 0.11, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(45)
            padding: [dp(10), dp(4)]
            spacing: dp(10)
            canvas.before:
                Color:
                    rgba: (0.11, 0.14, 0.17, 1)
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label:
                text: "CATEGORIA:"
                font_size: '14sp'
                bold: True
                size_hint_x: None
                width: dp(90)
                halign: 'left'
            Spinner:
                id: selector_categoria_spinner
                text: 'Primera A'
                values: ['Primera A', 'Primera B', 'Primera C', 'Primera D', 'Primera E']
                background_normal: ''
                background_color: (0.15, 0.18, 0.22, 1)
                color: (1, 1, 1, 1)
                bold: True
                font_size: '14sp'
                on_text: root.forzar_cambio_categoria(self.text)
            Label:
                text: root.fecha_titulo
                font_size: '13sp'
                halign: 'right'
                color: (0.95, 0.76, 0.2, 1)
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(35)
            Button:
                text: "POSICIONES Y FIXTURE"
                background_normal: ''
                background_color: (0.15, 0.18, 0.22, 1) if root.pestana_activa == 'tabla' else (0.09, 0.11, 0.13, 1)
                bold: True
                font_size: '12sp'
                on_release: root.cambiar_pestana('tabla')
            Button:
                text: "PROMEDIOS DESCENSO"
                background_normal: ''
                background_color: (0.15, 0.18, 0.22, 1) if root.pestana_activa == 'promedios' else (0.09, 0.11, 0.13, 1)
                bold: True
                font_size: '12sp'
                on_release: root.cambiar_pestana('promedios')

        BoxLayout:
            orientation: 'vertical'
            ScreenManager:
                id: league_sm
                Screen:
                    name: 'screen_tabla'
                    BoxLayout:
                        orientation: 'vertical'
                        padding: dp(4)
                        spacing: dp(4)
                        BoxLayout:
                            orientation: 'horizontal'
                            size_hint_y: None
                            height: dp(26)
                            canvas.before:
                                Color:
                                    rgba: (0.11, 0.14, 0.17, 1)
                                Rectangle:
                                    pos: self.pos
                                    size: self.size
                            Label:
                                text: ' Equipo'
                                font_size: '11sp'
                                bold: True
                                halign: 'left'
                                text_size: self.width, None
                            Label:
                                text: 'PTS'
                                font_size: '11sp'
                                bold: True
                                size_hint_x: None
                                width: dp(38)
                            Label:
                                text: 'PJ'
                                font_size: '11sp'
                                bold: True
                                size_hint_x: None
                                width: dp(28)
                            Label:
                                text: 'G'
                                font_size: '11sp'
                                bold: True
                                size_hint_x: None
                                width: dp(28)
                            Label:
                                text: 'E'
                                font_size: '11sp'
                                bold: True
                                size_hint_x: None
                                width: dp(28)
                            Label:
                                text: 'P'
                                font_size: '11sp'
                                bold: True
                                size_hint_x: None
                                width: dp(28)
                            Label:
                                text: 'GF'
                                font_size: '11sp'
                                bold: True
                                size_hint_x: None
                                width: dp(28)
                            Label:
                                text: 'GC'
                                font_size: '11sp'
                                bold: True
                                size_hint_x: None
                                width: dp(28)
                            Label:
                                text: 'DG'
                                font_size: '11sp'
                                bold: True
                                size_hint_x: None
                                width: dp(32)
                        ScrollView:
                            size_hint_y: 0.5
                            BoxLayout:
                                id: tabla_posiciones_container
                                orientation: 'vertical'
                                size_hint_y: None
                                height: self.minimum_height
                                spacing: dp(2)
                        BoxLayout:
                            orientation: 'horizontal'
                            size_hint_y: None
                            height: dp(24)
                            canvas.before:
                                Color:
                                    rgba: (0.09, 0.11, 0.13, 1)
                                Rectangle:
                                    pos: self.pos
                                    size: self.size
                            Label:
                                text: '📅 PARTIDOS DE LA FECHA'
                                font_size: '11sp'
                                bold: True
                                halign: 'left'
                                text_size: self.width, None
                                color: (0.12, 0.73, 0.44, 1)
                        ScrollView:
                            size_hint_y: 0.5
                            BoxLayout:
                                id: fixture_container
                                orientation: 'vertical'
                                size_hint_y: None
                                height: self.minimum_height
                                spacing: dp(3)

                Screen:
                    name: 'screen_promedios'
                    BoxLayout:
                        orientation: 'vertical'
                        BoxLayout:
                            orientation: 'horizontal'
                            size_hint_y: None
                            height: dp(26)
                            canvas.before:
                                Color:
                                    rgba: (0.11, 0.14, 0.17, 1)
                                Rectangle:
                                    pos: self.pos
                                    size: self.size
                            Label:
                                text: ' Equipo'
                                font_size: '12sp'
                                bold: True
                                halign: 'left'
                                text_size: self.width, None
                            Label:
                                text: 'PTS AC'
                                font_size: '11sp'
                                bold: True
                                size_hint_x: None
                                width: dp(55)
                            Label:
                                text: 'PJ AC'
                                font_size: '11sp'
                                bold: True
                                size_hint_x: None
                                width: dp(55)
                            Label:
                                text: 'PROMEDIO'
                                font_size: '11sp'
                                bold: True
                                size_hint_x: None
                                width: dp(75)
                        ScrollView:
                            BoxLayout:
                                id: promedios_container
                                orientation: 'vertical'
                                size_hint_y: None
                                height: self.minimum_height
                                spacing: dp(2)
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: dp(115)
            padding: dp(8)
            spacing: dp(4)
            canvas.before:
                Color:
                    rgba: (0.15, 0.18, 0.22, 1)
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label:
                text: root.partido_estado_info
                font_size: '12sp'
                bold: True
                color: (0.95, 0.76, 0.2, 1)
                size_hint_y: None
                height: dp(14)
            BoxLayout:
                orientation: 'horizontal'
                Label:
                    text: root.equipo_local
                    font_size: '15sp'
                    bold: True
                    halign: 'right'
                Label:
                    text: root.marcador_texto
                    font_size: '20sp'
                    bold: True
                    color: (0.12, 0.73, 0.44, 1)
                    size_hint_x: None
                    width: dp(70)
                    halign: 'center'
                Label:
                    text: root.equipo_visitante
                    font_size: '15sp'
                    bold: True
                    halign: 'left'
            Button:
                text: root.boton_accion_texto
                background_normal: ''
                background_color: (0.12, 0.73, 0.44, 1)
                color: (1, 1, 1, 1)
                bold: True
                size_hint_y: None
                height: dp(38)
                on_release: root.procesar_click_partido()
''')
# =========================================================
# === FIN BLOQUE 5 ========================================
# =========================================================
# =========================================================
# === INICIO BLOQUE 6: LOGICA DE PANTALLAS Y ENLACES ======
# =========================================================
CATEGORIAS = ['Primera A', 'Primera B', 'Primera C', 'Primera D', 'Primera E']
CATEGORIAS_JUEGO = list(reversed(CATEGORIAS))
ARCHIVO_PERMANENTE = 'Torneo_Datos.json'

class MainScreen(Screen):
    def seleccionar_opcion(self, opcion):
        app = App.get_running_app()
        if opcion == '1': app.cargar_todo()
        elif opcion == '2': app.cargar_equipos_solo(); app.resetear_campeonato_a_fecha_1()
        elif opcion == '3': app.configurar_valores_defecto(); app.resetear_campeonato_a_fecha_1()
        app.root.current = 'league'
        app.league_screen.cat_seleccionada_nombre = 'Primera A'
        app.league_screen.actualizar_pantalla()

class LeagueScreen(Screen):
    categoria_titulo = StringProperty('CATEGORIA')
    fecha_titulo = StringProperty('FECHA 1')
    equipo_local = StringProperty('LOCAL')
    equipo_visitante = StringProperty('VISITANTE')
    marcador_texto = StringProperty('vs')
    boton_accion_texto = StringProperty('SIMULAR 90 MINUTOS')
    partido_estado_info = StringProperty('PARTIDO EN CURSO')
    pestana_activa = StringProperty('tabla')
    cat_seleccionada_nombre = StringProperty('Primera A')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fixtures = {}
        self.resultados_goleada = {}
        self.estado_partido = 'PREVIO'
        self.g_loc, self.g_vis = 0, 0

    def forzar_cambio_categoria(self, nombre_cat):
        self.cat_seleccionada_nombre = nombre_cat
        self.actualizar_pantalla()

    def cambiar_pestana(self, nombre):
        self.pestana_activa = nombre
        if nombre == 'tabla': self.ids.league_sm.current = 'screen_tabla'
        else: self.ids.league_sm.current = 'screen_promedios'
# =========================================================
# === FIN BLOQUE 6 ========================================
# =========================================================
# =========================================================
# === INICIO BLOQUE 7: METODOS DE DIBUJO DE TABLAS Y FIX ==
# =========================================================
    def actualizar_pantalla(self):
        app = App.get_running_app(); cat = self.cat_seleccionada_nombre
        self.categoria_titulo = f'{cat.upper()}'; self.fecha_titulo = f'FECHA {app.fecha_actual + 1}/10 (ANO {app.ano_actual})'
        if not self.fixtures or cat not in self.fixtures: self.fixtures = {c: app.generar_fixture_oficial(app.equipos[c]) for c in CATEGORIAS}
        partidos_fecha = self.fixtures[cat][app.fecha_actual]; cat_juego_real = CATEGORIAS_JUEGO[app.cat_idx_actual]; partidos_juego_real = self.fixtures[cat_juego_real][app.fecha_actual]
        if app.partido_idx_actual < len(partidos_juego_real):
            loc, vis = partidos_juego_real[app.partido_idx_actual]; self.equipo_local, self.equipo_visitante = loc.upper(), vis.upper()
            self.partido_estado_info = f' JUGANDO EN VIVO: {cat_juego_real.upper()} - PARTIDO {app.partido_idx_actual + 1}/{len(partidos_juego_real)}'
            if self.estado_partido == 'PREVIO': self.marcador_texto, self.boton_accion_texto = 'vs', 'SIMULAR 90 MINUTOS'
        else:
            self.equipo_local, self.equipo_visitante, self.marcador_texto = 'FIN FECHA', 'FIN FECHA', '-'
            self.partido_estado_info = f'🏁 CONCLUIDO: {cat_juego_real.upper()} JUGO TODA LA FECHA'; self.boton_accion_texto = 'AVANZAR CATEGORIA / PROXIMA FECHA'
        self.dibujar_tabla_posiciones(cat); self.dibujar_fixture_pestana(cat, app.fecha_actual, partidos_fecha); self.dibujar_tabla_promedios(cat)

    def dibujar_tabla_posiciones(self, cat):
        app = App.get_running_app(); container = self.ids.tabla_posiciones_container; container.clear_widgets()
        eqs = app.equipos[cat]; t = app.tablas_ano[cat]
        for e in eqs:
            t[e]['PTS'] = (t[e]['L_G'] + t[e]['V_G']) * 3 + (t[e]['L_E'] + t[e]['V_E']) * 1
            t[e]['G_TOTAL'] = t[e]['L_G'] + t[e]['V_G']; t[e]['E_TOTAL'] = t[e]['L_E'] + t[e]['V_E']; t[e]['P_TOTAL'] = t[e]['L_P'] + t[e]['V_P']
        tabla_anual = sorted(eqs, key=lambda x: (t[x]['PTS'], t[x]['GF']-t[x]['GC'], t[x]['GF']), reverse=True)
        container.height = len(tabla_anual) * dp(40)
        for pos, e in enumerate(tabla_anual, 1):
            dg = t[e]['GF'] - t[e]['GC']; dg_str = f'+{dg}' if dg > 0 else f'{dg}'
            # Condición corregida: No hay descenso si la categoría actual es la 'Primera E'
            es_ultimo_anual = (pos == len(tabla_anual)) and (cat != 'Primera E')
            container.add_widget(FilaTabla(pos_num=f"{pos:02d}", equipo_name=e.upper(), pts=str(t[e]['PTS']), pj=str(t[e]['PJ']), g=str(t[e]['G_TOTAL']), e=str(t[e]['E_TOTAL']), p=str(t[e]['P_TOTAL']), gf=str(t[e]['GF']), gc=str(t[e]['GC']), dg=dg_str, es_lider=(pos == 1), es_descenso=es_ultimo_anual))

    def dibujar_fixture_pestana(self, cat, num_fecha, partidos):
        app = App.get_running_app(); container = self.ids.fixture_container; container.clear_widgets(); key_base = f"{cat}_{num_fecha}_"
        container.height = len(partidos) * dp(42)
        for idx, (loc, vis) in enumerate(partidos):
            key = f"{key_base}{idx}"
            if key in self.resultados_goleada: txt_marcador, est = self.resultados_goleada[key], "JUGADO"
            else:
                txt_marcador, est = "vs", "PREVIO"
                if idx == app.partido_idx_actual and cat == CATEGORIAS_JUEGO[app.cat_idx_actual]: txt_marcador = f"({self.marcador_texto})" if self.estado_partido == "JUGADO" else "EN VIVO"
            container.add_widget(FilaFixture(local=loc.upper(), marcador=txt_marcador, visitante=vis.upper(), estado=est))

    def dibujar_tabla_promedios(self, cat):
        app = App.get_running_app(); container = self.ids.promedios_container; container.clear_widgets()
        eqs = app.equipos[cat]; t_hist = app.historial_puntos[cat]; t_actual = app.tablas_ano[cat]; datos_promedios = []
        for e in eqs:
            pts_acum = t_hist.get(e, {}).get('PTS', 0) + t_actual[e]['PTS']; pj_acum = t_hist.get(e, {}).get('PJ', 0) + t_actual[e]['PJ']
            prom = float(pts_acum) / float(pj_acum) if pj_acum > 0 else 0.000
            datos_promedios.append({'equipo': e, 'pts': pts_acum, 'pj': pj_acum, 'prom': prom})
        tabla_prom = sorted(datos_promedios, key=lambda x: (x['prom'], x['pts']), reverse=True)
        container.height = len(tabla_prom) * dp(40)
        for pos, item in enumerate(tabla_prom, 1): 
            # Condición corregida: Tampoco hay descenso en promedios si es 'Primera E'
            es_ultimo_promedio = (pos == len(tabla_prom)) and (cat != 'Primera E')
            container.add_widget(FilaPromedios(pos_num=f"{pos:02d}", equipo_name=item['equipo'].upper(), pts_acum=str(item['pts']), pj_acum=str(item['pj']), promedio=f"{item['prom']:.3f}", es_descenso=es_ultimo_promedio))
# =========================================================
# === FIN BLOQUE 7 ========================================
# =========================================================
# =========================================================
# === INICIO BLOQUE 8: MOTOR LOGICO GENERAL Y APP RUN ====
# =========================================================
    def procesar_click_partido(self):
        app = App.get_running_app(); cat = CATEGORIAS_JUEGO[app.cat_idx_actual]; partidos_fecha = self.fixtures[cat][app.fecha_actual]
        if app.partido_idx_actual < len(partidos_fecha):
            if self.estado_partido == 'PREVIO':
                self.g_loc, self.g_vis = random.randint(0, 4), random.randint(0, 4)
                self.marcador_texto, self.boton_accion_texto, self.estado_partido = f"{self.g_loc} - {self.g_vis}", "GUARDAR Y CONTINUAR", 'JUGADO'
                self.actualizar_pantalla()
            else:
                loc, vis = partidos_fecha[app.partido_idx_actual]; key = f"{self.cat_seleccionada_nombre}_{app.fecha_actual}_{app.partido_idx_actual}"; self.resultados_goleada[key] = f"{self.g_loc} - {self.g_vis}"
                t = app.tablas_ano[cat]; t[loc]['PJ'] += 1; t[loc]['GF'] += self.g_loc; t[loc]['GC'] += self.g_vis; t[vis]['PJ'] += 1; t[vis]['GF'] += self.g_vis; t[vis]['GC'] += self.g_loc
                if self.g_loc > self.g_vis: t[loc]['L_G'] += 1; t[vis]['V_P'] += 1
                elif self.g_loc < self.g_vis: t[vis]['V_G'] += 1; t[loc]['L_P'] += 1
                else: t[loc]['L_E'] += 1; t[vis]['V_E'] += 1
                app.partido_idx_actual, self.estado_partido = app.partido_idx_actual + 1, 'PREVIO'
                app.guardar_todo(); self.actualizar_pantalla()
        else:
            app.partido_idx_actual, app.cat_idx_actual = 0, app.cat_idx_actual + 1
            if app.cat_idx_actual >= len(CATEGORIAS_JUEGO):
                app.cat_idx_actual, app.fecha_actual = 0, app.fecha_actual + 1; self.resultados_goleada.clear()
            
            if app.fecha_actual >= 10:
                app.fecha_actual = 0; app.ano_actual += 1
                
                # 1. Guardamos los puntos en el historial acumulado antes de limpiar las tablas anuales
                for c in CATEGORIAS:
                    for e in app.equipos[c]:
                        app.historial_puntos[c][e]['PTS'] += app.tablas_ano[c][e]['PTS']
                        app.historial_puntos[c][e]['PJ'] += app.tablas_ano[c][e]['PJ']

                # 2. Calcular ascensos (tabla anual) y descensos (tabla de promedios acumulados)
                nuevos_equipos = {c: [] for c in CATEGORIAS}
                ascendidos = {}  # Guardará quién sube de cada categoría
                descendidos = {} # Guardará quién baja de cada categoría

                for c in CATEGORIAS:
                    eqs = app.equipos[c]
                    t = app.tablas_ano[c]
                    # Orden para saber el campeón / posible ascenso
                    tabla_anual = sorted(eqs, key=lambda x: (t[x]['PTS'], t[x]['GF']-t[x]['GC'], t[x]['GF']), reverse=True)
                    
                    # Orden para promedios (el último desciende)
                    datos_prom = []
                    for e in eqs:
                        pts_ac = app.historial_puntos[c][e]['PTS']
                        pj_ac = app.historial_puntos[c][e]['PJ']
                        prom = float(pts_ac) / float(pj_ac) if pj_ac > 0 else 0.0
                        datos_prom.append({'equipo': e, 'prom': prom, 'pts': pts_ac})
                    tabla_prom = sorted(datos_prom, key=lambda x: (x['prom'], x['pts']), reverse=True)

                    # Asignamos quién debería subir y bajar si las reglas de la categoría lo permiten
                    if c != 'Primera A':
                        ascendidos[c] = tabla_anual[0]   # El 1ro de la tabla anual sube
                    if c != 'Primera E':
                        descendidos[c] = tabla_prom[-1]['equipo'] # El último del promedio baja
                # 3. Reacomodar los equipos en sus nuevas ligas basándose en las restricciones
                for idx, c in enumerate(CATEGORIAS):
                    for e in app.equipos[c]:
                        # Si el equipo ascendió, va a la categoría superior
                        if c in ascendidos and e == ascendidos[c]:
                            cat_superior = CATEGORIAS[idx - 1]
                            nuevos_equipos[cat_superior].append(e)
                        # Si el equipo descendió, va a la categoría inferior
                        elif c in descendidos and e == descendidos[c]:
                            cat_inferior = CATEGORIAS[idx + 1]
                            nuevos_equipos[cat_inferior].append(e)
                        # Si se mantiene en su categoría
                        else:
                            nuevos_equipos[c].append(e)

                app.equipos = nuevos_equipos
                app.resetear_campeonato_a_fecha_1()
            
            app.guardar_todo(); self.actualizar_pantalla()

class TorneoApp(App):
    def build(self):
        self.equipos, self.tablas_ano, self.historial_puntos, self.fecha_actual, self.cat_idx_actual, self.partido_idx_actual, self.ano_actual = {c: [] for c in CATEGORIAS}, {}, {c: {} for c in CATEGORIAS}, 0, 0, 0, 1
        sm = ScreenManager(); self.main_screen = MainScreen(name='main'); self.league_screen = LeagueScreen(name='league'); sm.add_widget(self.main_screen); sm.add_widget(self.league_screen)
        if os.path.exists(ARCHIVO_PERMANENTE): sm.current = 'main'
        else: self.configurar_valores_defecto(); self.resetear_campeonato_a_fecha_1(); sm.current = 'league'; self.league_screen.actualizar_pantalla()
        return sm
    def configurar_valores_defecto(self):
        self.equipos = {
            'Primera A': ['River Plate', 'Boca Jrs', 'Independiente', 'Racing Club', 'San Lorenzo'],
            'Primera B': ['Independiente Rivadavia', 'Gimnasia y Esg.Mza.', "Newell's O.B.", 'Rosario Central', 'Velez Sarfield'],
            'Primera C': ['Estudiantes LP.', 'Gimnasia y Esg.', 'Ferro Carril Oeste', 'Gimnasia y Esg.Jujuy', 'Huracan'],
            'Primera D': ['Godoy Cruz', 'Deportivo Maipú', 'San Martin SJ.', 'San Martin de Tuc.', 'Atl. Tucumán'],
            'Primera E': ['San Martin Mza.', 'Huracan LH.', 'Gutierrez SC.', 'Chacarita', 'Olimpo BB.']
        }
    def resetear_campeonato_a_fecha_1(self):
        self.fecha_actual, self.cat_idx_actual, self.partido_idx_actual, self.tablas_ano = 0, 0, 0, {}
        for cat in CATEGORIAS:
            self.tablas_ano[cat] = {}
            if cat not in self.historial_puntos or not self.historial_puntos[cat]: self.historial_puntos[cat] = {}
            for eq in self.equipos[cat]:
                self.tablas_ano[cat][eq] = {'PTS': 0, 'PJ': 0, 'GF': 0, 'GC': 0, 'L_G': 0, 'L_E': 0, 'L_P': 0, 'V_G': 0, 'V_E': 0, 'V_P': 0}
                if eq not in self.historial_puntos[cat]: self.historial_puntos[cat][eq] = {'PTS': random.randint(35, 55), 'PJ': 38}
        self.guardar_todo()
    def guardar_todo(self):
        datos = {'equipos': self.equipos, 'tablas_ano': self.tablas_ano, 'historial_puntos': self.historial_puntos, 'fecha_actual': self.fecha_actual, 'cat_idx_actual': self.cat_idx_actual, 'partido_idx_actual': self.partido_idx_actual, 'ano_actual': self.ano_actual}
        with open(ARCHIVO_PERMANENTE, 'w', encoding='utf-8') as f: json.dump(datos, f, ensure_ascii=False, indent=4)
    def cargar_todo(self):
        with open(ARCHIVO_PERMANENTE, 'r', encoding='utf-8') as f: datos = json.load(f)
        self.equipos, self.tablas_ano, self.historial_puntos, self.fecha_actual, self.cat_idx_actual, self.partido_idx_actual, self.ano_actual = datos['equipos'], datos['tablas_ano'], datos.get('historial_puntos', {c: {} for c in CATEGORIAS}), datos['fecha_actual'], datos['cat_idx_actual'], datos['partido_idx_actual'], datos.get('ano_actual', 1)
    def cargar_equipos_solo(self):
        if os.path.exists(ARCHIVO_PERMANENTE):
            with open(ARCHIVO_PERMANENTE, 'r', encoding='utf-8') as f: datos = json.load(f); self.equipos = datos['equipos']
    def generar_fixture_oficial(self, equipos):
        eqs = list(equipos); n = len(eqs); fechas_ida = []
        for f in range(n - 1):
            partidos_fecha = []
            for i in range(n // 2): partidos_fecha.append((eqs[i], eqs[n - 1 - i]))
            fechas_ida.append(partidos_fecha); eqs = [eqs] + [eqs[-1]] + eqs[1:-1]
        fechas_vuelta = []
        for f_ida in fechas_ida:
            partidos_vuelta = []
            for l, v in f_ida: partidos_vuelta.append((v, l))
            fechas_vuelta.append(partidos_vuelta)
        return fechas_ida + fechas_vuelta

if __name__ == '__main__':
    TorneoApp().run()
# =========================================================
# === FIN BLOQUE 8 ========================================
# =========================================================
