import sys
import numpy as np
import pyvista as pv
from pyvistaqt.plotting import QtInteractor
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout,
                             QVBoxLayout, QFrame, QSlider, QLabel, QScrollArea)
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Aircraft Designer - Hyper Detailed")
        self.setGeometry(50, 50, 1800, 1200)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        control_panel = QFrame()
        scroll_area.setWidget(control_panel)
        control_layout = QVBoxLayout(control_panel)
        main_layout.addWidget(scroll_area, 1)

        self._add_header(control_layout, "Fuselage")
        self._create_slider(control_layout, "Fuselage Length", 10, 50, 25)
        self._create_slider(control_layout, "Fuselage Radius", 5, 20, 10, 10.0)
        self._create_slider(control_layout, "Nose Cone Ratio", 1, 40, 20, 100.0)
        self._create_slider(control_layout, "Tail Cone Ratio", 1, 40, 15, 100.0)
        self._add_header(control_layout, "Cockpit")
        self._create_slider(control_layout, "Cockpit Position", 0, 80, 70, 100.0)
        self._create_slider(control_layout, "Cockpit Length", 5, 25, 15, 10.0)
        self._create_slider(control_layout, "Cockpit Height", 2, 15, 8, 10.0)
        self._add_header(control_layout, "Main Wings")
        self._create_slider(control_layout, "Wing Position", 10, 90, 50, 100.0)
        self._create_slider(control_layout, "Wing Span", 10, 60, 30)
        self._create_slider(control_layout, "Wing Sweep", 0, 60, 30)
        self._create_slider(control_layout, "Wing Chord Root", 10, 80, 40, 10.0)
        self._create_slider(control_layout, "Wing Taper Ratio", 10, 100, 50, 100.0)
        self._create_slider(control_layout, "Wing Dihedral", -10, 30, 5)
        self._add_header(control_layout, "Engines")
        self._create_slider(control_layout, "Engine Count", 2, 4, 2, 2)
        self._create_slider(control_layout, "Engine H-Position", 20, 80, 40, 100.0)
        self._create_slider(control_layout, "Engine V-Position", -10, 10, -5, 10.0)
        self._create_slider(control_layout, "Engine Size", 5, 30, 15, 10.0)
        self._add_header(control_layout, "Horizontal Stabilizer")
        self._create_slider(control_layout, "H-Stab Span", 4, 20, 10)
        self._create_slider(control_layout, "H-Stab Sweep", 0, 60, 35)
        self._create_slider(control_layout, "H-Stab Chord Root", 5, 40, 20, 10.0)
        self._create_slider(control_layout, "H-Stab Taper Ratio", 10, 100, 60, 100.0)
        self._add_header(control_layout, "Vertical Stabilizer")
        self._create_slider(control_layout, "V-Stab Height", 2, 15, 8)
        self._create_slider(control_layout, "V-Stab Sweep", 0, 60, 40)
        self._create_slider(control_layout, "V-Stab Chord Root", 5, 40, 25, 10.0)
        self._create_slider(control_layout, "V-Stab Taper Ratio", 10, 100, 50, 100.0)
        control_layout.addStretch()

        self.plotter = QtInteractor(self)
        main_layout.addWidget(self.plotter.interactor, 4)

        self.setup_scene()
        self.update_aircraft()

    def _add_header(self, layout, name):
        label = QLabel(name)
        label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(label)

    def _create_slider(self, layout, name, min_val, max_val, start_val, factor=1.0):
        layout.addWidget(QLabel(name))
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(start_val)
        slider.setObjectName(name)
        slider.valueChanged.connect(self.update_aircraft)
        layout.addWidget(slider)
        setattr(slider, 'factor', factor)
        return slider

    def setup_scene(self):
        self.plotter.camera_position = 'iso'
        self.plotter.camera.zoom(1.5)
        light = pv.Light(position=(10, 10, 10), intensity=1.5)
        self.plotter.add_light(light)
        self.plotter.background_color = 'white'

    def create_wings(self, params):
        span = params.get("Wing Span", 30)
        chord_root = params.get("Wing Chord Root", 4.0)
        taper_ratio = params.get("Wing Taper Ratio", 0.5)
        sweep = params.get("Wing Sweep", 30)
        dihedral = params.get("Wing Dihedral", 5)
        position = params.get("Wing Position", 0.5)
        fuselage_radius = params.get("Fuselage Radius", 1.0)
        fuselage_length = params.get("Fuselage Length", 25)
        chord_tip = chord_root * taper_ratio
        half_span = span / 2
        root_front = (position * fuselage_length - fuselage_length/2) + chord_root / 2
        root_back = root_front - chord_root
        tip_x_offset = half_span * np.tan(np.deg2rad(sweep))
        tip_z_offset = half_span * np.tan(np.deg2rad(dihedral))
        tip_front = root_front - tip_x_offset
        tip_back = tip_front - chord_tip
        points = np.array([
            [root_back, fuselage_radius, 0], [root_front, fuselage_radius, 0],
            [tip_back, half_span, tip_z_offset], [tip_front, half_span, tip_z_offset],
            [root_back, -fuselage_radius, 0], [root_front, -fuselage_radius, 0],
            [tip_back, -half_span, tip_z_offset], [tip_front, -half_span, tip_z_offset],
        ])
        right_wing = pv.PolyData([points[0], points[1], points[3], points[2]]).extrude([0,0,chord_root/20], capping=True)
        left_wing = pv.PolyData([points[4], points[5], points[7], points[6]]).extrude([0,0,chord_root/20], capping=True)
        return right_wing + left_wing

    def create_fuselage(self, params):
        length = params.get("Fuselage Length", 25)
        radius = params.get("Fuselage Radius", 1.0)
        nose_ratio = params.get("Nose Cone Ratio", 0.2)
        tail_ratio = params.get("Tail Cone Ratio", 0.15)
        nose_len = length * nose_ratio
        tail_len = length * tail_ratio
        main_body_len = length - nose_len - tail_len
        main_body = pv.Cylinder(center=(tail_len/2 - nose_len/2, 0, 0), direction=(1, 0, 0), radius=radius, height=main_body_len)
        nose_cone = pv.Cone(center=(main_body_len/2 + tail_len/2 - nose_len/2, 0, 0), direction=(1, 0, 0), radius=radius, height=nose_len)
        tail_cone = pv.Cone(center=(-main_body_len/2 + tail_len/2 - nose_len/2, 0, 0), direction=(-1, 0, 0), radius=radius, height=tail_len)
        cockpit_pos = params.get("Cockpit Position", 0.7)
        cockpit_len = params.get("Cockpit Length", 1.5)
        cockpit_height = params.get("Cockpit Height", 0.8)
        cockpit_center_x = (cockpit_pos * main_body_len) - (main_body_len/2)
        cockpit_center = (cockpit_center_x, 0, radius * 0.7)
        cockpit_cyl = pv.Cylinder(center=cockpit_center, direction=(1,0,0), radius=cockpit_height, height=cockpit_len)
        s1 = pv.Sphere(radius=cockpit_height, center=(cockpit_center[0] - cockpit_len/2, cockpit_center[1], cockpit_center[2]))
        s2 = pv.Sphere(radius=cockpit_height, center=(cockpit_center[0] + cockpit_len/2, cockpit_center[1], cockpit_center[2]))
        cockpit = cockpit_cyl + s1 + s2
        return main_body + nose_cone + tail_cone + cockpit

    def create_horizontal_stabilizer(self, params):
        span = params.get("H-Stab Span", 10)
        chord_root = params.get("H-Stab Chord Root", 2.0)
        taper_ratio = params.get("H-Stab Taper Ratio", 0.6)
        sweep = params.get("H-Stab Sweep", 35)
        fuselage_radius = params.get("Fuselage Radius", 1.0) * 0.7
        tail_pos_x = -params.get("Fuselage Length", 25) / 2
        chord_tip = chord_root * taper_ratio
        half_span = span / 2
        tip_x_offset = half_span * np.tan(np.deg2rad(sweep))
        points = np.array([
            [tail_pos_x - chord_root/2, fuselage_radius, 0], [tail_pos_x + chord_root/2, fuselage_radius, 0],
            [tail_pos_x - chord_root/2 - tip_x_offset, half_span, 0], [tail_pos_x + chord_root/2 - tip_x_offset - (chord_tip - chord_root), half_span, 0],
            [tail_pos_x - chord_root/2, -fuselage_radius, 0], [tail_pos_x + chord_root/2, -fuselage_radius, 0],
            [tail_pos_x - chord_root/2 - tip_x_offset, -half_span, 0], [tail_pos_x + chord_root/2 - tip_x_offset - (chord_tip - chord_root), -half_span, 0]
        ])
        right_stab = pv.PolyData([points[0], points[1], points[3], points[2]]).extrude([0,0,chord_root/20], capping=True)
        left_stab = pv.PolyData([points[4], points[5], points[7], points[6]]).extrude([0,0,chord_root/20], capping=True)
        return right_stab + left_stab

    def create_vertical_stabilizer(self, params):
        height = params.get("V-Stab Height", 8)
        chord_root = params.get("V-Stab Chord Root", 2.5)
        taper_ratio = params.get("V-Stab Taper Ratio", 0.5)
        sweep = params.get("V-Stab Sweep", 40)
        fuselage_radius = params.get("Fuselage Radius", 1.0)
        tail_pos_x = -params.get("Fuselage Length", 25) / 2
        chord_tip = chord_root * taper_ratio
        tip_x_offset = height * np.tan(np.deg2rad(sweep))
        points = np.array([
            [tail_pos_x - chord_root/2, 0, fuselage_radius],
            [tail_pos_x + chord_root/2, 0, fuselage_radius],
            [tail_pos_x - chord_root/2 - tip_x_offset, 0, fuselage_radius + height],
            [tail_pos_x + chord_root/2 - tip_x_offset - (chord_tip - chord_root), 0, fuselage_radius + height]
        ])
        return pv.PolyData(points).extrude([0, chord_root/20, 0], capping=True)

    def create_engines(self, params):
        count = int(params.get("Engine Count", 2))
        h_pos = params.get("Engine H-Position", 0.4)
        v_pos = params.get("Engine V-Position", -0.5)
        size = params.get("Engine Size", 1.5)
        wing_span = params.get("Wing Span", 30)
        engine_y = (wing_span / 2) * h_pos
        engine_z = v_pos
        engine_len = size * 2
        engine_rad = size
        engines = pv.MultiBlock()
        engines.append(pv.Cylinder(center=(0, engine_y, engine_z), direction=(1,0,0), radius=engine_rad, height=engine_len))
        engines.append(pv.Cylinder(center=(0, -engine_y, engine_z), direction=(1,0,0), radius=engine_rad, height=engine_len))
        if count == 4:
            engines.append(pv.Cylinder(center=(0, engine_y * 0.5, engine_z), direction=(1,0,0), radius=engine_rad*0.8, height=engine_len*0.8))
            engines.append(pv.Cylinder(center=(0, -engine_y * 0.5, engine_z), direction=(1,0,0), radius=engine_rad*0.8, height=engine_len*0.8))
        return engines

    def update_aircraft(self):
        self.plotter.clear()
        params = {}
        for slider in self.findChildren(QSlider):
            params[slider.objectName()] = slider.value() / getattr(slider, 'factor', 1.0)

        wings_mesh = self.create_wings(params)
        fuselage_mesh = self.create_fuselage(params)
        h_stab_mesh = self.create_horizontal_stabilizer(params)
        v_stab_mesh = self.create_vertical_stabilizer(params)
        engines_mesh = self.create_engines(params)

        self.plotter.add_mesh(wings_mesh, color='#c0c0c0', smooth_shading=True, specular=1.0, specular_power=15)
        self.plotter.add_mesh(fuselage_mesh, color='#c0c0c0', smooth_shading=True, specular=1.0, specular_power=15)
        self.plotter.add_mesh(h_stab_mesh, color='#c0c0c0', smooth_shading=True, specular=1.0, specular_power=15)
        self.plotter.add_mesh(v_stab_mesh, color='#ad1b02', smooth_shading=True, specular=1.0, specular_power=15)
        self.plotter.add_mesh(engines_mesh, color='#404040', smooth_shading=True)

        self.plotter.render()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
