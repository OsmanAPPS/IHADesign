import sys
import numpy as np
import pyvista as pv
from pyvistaqt.plotting import QtInteractor
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout,
                             QVBoxLayout, QFrame, QLabel, QScrollArea, QDoubleSpinBox)
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Aircraft Designer - Bugfix & SpinBox UI")
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
        self._create_spinbox(control_layout, "Fuselage Length", 10, 50, 25, 0.5)
        self._create_spinbox(control_layout, "Fuselage Radius", 0.5, 3, 1.2, 0.1)
        self._create_spinbox(control_layout, "Nose Cone Ratio", 0.01, 0.5, 0.25, 0.01)
        self._create_spinbox(control_layout, "Tail Cone Ratio", 0.01, 0.5, 0.2, 0.01)
        self._add_header(control_layout, "Cockpit")
        self._create_spinbox(control_layout, "Cockpit Position", 0, 1, 0.8, 0.01)
        self._create_spinbox(control_layout, "Cockpit Length", 0.5, 5, 2.5, 0.1)
        self._create_spinbox(control_layout, "Cockpit Height", 0.2, 2, 0.9, 0.1)
        self._add_header(control_layout, "Main Wings")
        self._create_spinbox(control_layout, "Wing Position", 0.1, 0.9, 0.45, 0.01)
        self._create_spinbox(control_layout, "Wing Span", 10, 80, 28, 1)
        self._create_spinbox(control_layout, "Wing Sweep", 0, 60, 35, 1)
        self._create_spinbox(control_layout, "Wing Chord Root", 1, 10, 4.5, 0.1)
        self._create_spinbox(control_layout, "Wing Taper Ratio", 0.1, 1, 0.4, 0.01)
        self._create_spinbox(control_layout, "Wing Dihedral", -10, 20, 6, 1)
        self._add_header(control_layout, "Engines")
        self._create_spinbox(control_layout, "Engine Count", 2, 4, 2, 2)
        self._create_spinbox(control_layout, "Engine H-Position", 0.2, 0.8, 0.35, 0.01)
        self._create_spinbox(control_layout, "Engine V-Position", -2, 2, -0.8, 0.1)
        self._create_spinbox(control_layout, "Engine Size", 0.5, 4, 1.8, 0.1)
        self._add_header(control_layout, "Horizontal Stabilizer")
        self._create_spinbox(control_layout, "H-Stab Span", 4, 25, 12, 0.5)
        self._create_spinbox(control_layout, "H-Stab Sweep", 0, 60, 40, 1)
        self._create_spinbox(control_layout, "H-Stab Chord Root", 0.5, 5, 2.5, 0.1)
        self._create_spinbox(control_layout, "H-Stab Taper Ratio", 0.1, 1, 0.5, 0.01)
        self._add_header(control_layout, "Vertical Stabilizer")
        self._create_spinbox(control_layout, "V-Stab Height", 2, 12, 6, 0.5)
        self._create_spinbox(control_layout, "V-Stab Sweep", 0, 60, 45, 1)
        self._create_spinbox(control_layout, "V-Stab Chord Root", 0.5, 6, 3.0, 0.1)
        self._create_spinbox(control_layout, "V-Stab Taper Ratio", 0.1, 1, 0.4, 0.01)
        control_layout.addStretch()

        self.plotter = QtInteractor(self)
        main_layout.addWidget(self.plotter.interactor, 4)

        self.setup_scene()
        self.update_aircraft()

    def _add_header(self, layout, name):
        label = QLabel(name)
        label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(label)

    def _create_spinbox(self, layout, name, min_val, max_val, start_val, step):
        layout.addWidget(QLabel(name))
        spinbox = QDoubleSpinBox()
        spinbox.setRange(min_val, max_val)
        spinbox.setValue(start_val)
        spinbox.setSingleStep(step)
        spinbox.setObjectName(name)
        spinbox.valueChanged.connect(self.update_aircraft)
        layout.addWidget(spinbox)
        return spinbox

    def setup_scene(self):
        self.plotter.camera_position = 'xy'
        self.plotter.camera.elevation = 15
        self.plotter.camera.azimuth = 30
        self.plotter.camera.zoom(1.2)
        light = pv.Light(position=(10, 10, 10), intensity=1.5)
        self.plotter.add_light(light)
        self.plotter.background_color = 'white'

    def create_fuselage(self, params):
        length = params["Fuselage Length"]
        radius = params["Fuselage Radius"]
        nose_ratio = params["Nose Cone Ratio"]
        tail_ratio = params["Tail Cone Ratio"]
        nose_len = length * nose_ratio
        tail_len = length * tail_ratio
        main_body_len = length - nose_len - tail_len
        x_nose_end = length / 2
        x_nose_start = x_nose_end - nose_len
        x_tail_start = -length / 2
        x_tail_end = x_tail_start + tail_len
        main_body_center_x = x_tail_end + (main_body_len / 2)
        main_body = pv.Cylinder(center=(main_body_center_x, 0, 0), direction=(1, 0, 0), radius=radius, height=main_body_len)
        nose_cone = pv.Cone(center=(x_nose_start + nose_len / 2, 0, 0), direction=(1, 0, 0), radius=radius, height=nose_len)
        tail_cone = pv.Cone(center=(x_tail_start + tail_len / 2, 0, 0), direction=(-1, 0, 0), radius=radius, height=tail_len)
        cockpit_pos = params["Cockpit Position"]
        cockpit_len = params["Cockpit Length"]
        cockpit_height = params["Cockpit Height"]
        cockpit_x_start = x_tail_end + (cockpit_pos * main_body_len)
        cockpit_center = (cockpit_x_start, 0, radius * 0.7)
        cockpit_cyl = pv.Cylinder(center=cockpit_center, direction=(1,0,0), radius=cockpit_height, height=cockpit_len)
        s1 = pv.Sphere(radius=cockpit_height, center=(cockpit_center[0] - cockpit_len/2, cockpit_center[1], cockpit_center[2]))
        s2 = pv.Sphere(radius=cockpit_height, center=(cockpit_center[0] + cockpit_len/2, cockpit_center[1], cockpit_center[2]))
        cockpit = cockpit_cyl + s1 + s2
        return main_body + nose_cone + tail_cone + cockpit

    def create_wings(self, params):
        span = params["Wing Span"]
        chord_root = params["Wing Chord Root"]
        taper_ratio = params["Wing Taper Ratio"]
        sweep = params["Wing Sweep"]
        dihedral = params["Wing Dihedral"]
        position = params["Wing Position"]
        fuselage_radius = params["Fuselage Radius"]
        fuselage_length = params["Fuselage Length"]
        chord_tip = chord_root * taper_ratio
        half_span = span / 2
        wing_center_x = -fuselage_length / 2 + (position * fuselage_length)
        root_front = wing_center_x + chord_root / 2
        root_back = wing_center_x - chord_root / 2
        tip_x_offset = half_span * np.tan(np.deg2rad(sweep))
        tip_z_offset = half_span * np.tan(np.deg2rad(dihedral))
        tip_front = root_front - tip_x_offset
        tip_back = (root_back - tip_x_offset) + (chord_root - chord_tip)
        points = np.array([
            [root_back, fuselage_radius, 0], [root_front, fuselage_radius, 0],
            [tip_back, half_span, tip_z_offset], [tip_front, half_span, tip_z_offset],
            [root_back, -fuselage_radius, 0], [root_front, -fuselage_radius, 0],
            [tip_back, -half_span, tip_z_offset], [tip_front, -half_span, tip_z_offset],
        ])
        right_wing = pv.PolyData([points[0], points[1], points[3], points[2]]).extrude([0,0,chord_root/20], capping=True)
        left_wing = pv.PolyData([points[4], points[5], points[7], points[6]]).extrude([0,0,chord_root/20], capping=True)
        return right_wing + left_wing

    def create_engines(self, params):
        count = int(params["Engine Count"])
        h_pos = params["Engine H-Position"]
        v_pos = params["Engine V-Position"]
        size = params["Engine Size"]
        wing_span = params["Wing Span"]
        wing_center_x = -params["Fuselage Length"] / 2 + (params["Wing Position"] * params["Fuselage Length"])
        engine_y = (wing_span / 2) * h_pos
        engine_z = v_pos
        engine_len = size * 2
        engine_rad = size
        engines = pv.MultiBlock()
        engines.append(pv.Cylinder(center=(wing_center_x, engine_y, engine_z), direction=(1,0,0), radius=engine_rad, height=engine_len))
        engines.append(pv.Cylinder(center=(wing_center_x, -engine_y, engine_z), direction=(1,0,0), radius=engine_rad, height=engine_len))
        if count == 4:
            engines.append(pv.Cylinder(center=(wing_center_x, engine_y * 1.5, engine_z), direction=(1,0,0), radius=engine_rad, height=engine_len))
            engines.append(pv.Cylinder(center=(wing_center_x, -engine_y * 1.5, engine_z), direction=(1,0,0), radius=engine_rad, height=engine_len))
        return engines

    def create_horizontal_stabilizer(self, params):
        span = params["H-Stab Span"]
        chord_root = params["H-Stab Chord Root"]
        taper_ratio = params["H-Stab Taper Ratio"]
        sweep = params["H-Stab Sweep"]
        fuselage_radius_at_tail = params["Fuselage Radius"] * 0.5
        tail_pos_x = -params["Fuselage Length"] / 2 + (params["Fuselage Length"] * params["Tail Cone Ratio"])
        chord_tip = chord_root * taper_ratio
        half_span = span / 2
        tip_x_offset = half_span * np.tan(np.deg2rad(sweep))
        root_front = tail_pos_x + chord_root / 2
        root_back = tail_pos_x - chord_root / 2
        tip_front = root_front - tip_x_offset
        tip_back = (root_back - tip_x_offset) + (chord_root - chord_tip)
        points = np.array([
            [root_back, fuselage_radius_at_tail, 0], [root_front, fuselage_radius_at_tail, 0],
            [tip_back, half_span, 0], [tip_front, half_span, 0],
            [root_back, -fuselage_radius_at_tail, 0], [root_front, -fuselage_radius_at_tail, 0],
            [tip_back, -half_span, 0], [tip_front, -half_span, 0]
        ])
        right_stab = pv.PolyData([points[0], points[1], points[3], points[2]]).extrude([0,0,chord_root/20], capping=True)
        left_stab = pv.PolyData([points[4], points[5], points[7], points[6]]).extrude([0,0,chord_root/20], capping=True)
        return right_stab + left_stab

    def create_vertical_stabilizer(self, params):
        height = params["V-Stab Height"]
        chord_root = params["V-Stab Chord Root"]
        taper_ratio = params["V-Stab Taper Ratio"]
        sweep = params["V-Stab Sweep"]
        fuselage_radius_at_tail = params["Fuselage Radius"] * 0.7
        tail_pos_x = -params["Fuselage Length"] / 2 + (params["Fuselage Length"] * params["Tail Cone Ratio"])
        chord_tip = chord_root * taper_ratio
        tip_x_offset = height * np.tan(np.deg2rad(sweep))
        root_back = tail_pos_x - chord_root / 2
        root_front = tail_pos_x + chord_root / 2
        tip_back = (root_back - tip_x_offset) + (chord_root - chord_tip)
        tip_front = root_front - tip_x_offset
        points = np.array([
            [root_back, 0, fuselage_radius_at_tail],
            [root_front, 0, fuselage_radius_at_tail],
            [tip_back, 0, fuselage_radius_at_tail + height],
            [tip_front, 0, fuselage_radius_at_tail + height]
        ])
        return pv.PolyData(points).extrude([0, chord_root/20, 0], capping=True)

    def update_aircraft(self):
        self.plotter.clear()
        params = {}
        for spinbox in self.findChildren(QDoubleSpinBox):
            params[spinbox.objectName()] = spinbox.value()

        fuselage_mesh = self.create_fuselage(params)
        wings_mesh = self.create_wings(params)
        h_stab_mesh = self.create_horizontal_stabilizer(params)
        v_stab_mesh = self.create_vertical_stabilizer(params)
        engines_mesh = self.create_engines(params)

        self.plotter.add_mesh(fuselage_mesh, color='#c0c0c0', smooth_shading=True, specular=1.0, specular_power=15)
        self.plotter.add_mesh(wings_mesh, color='#c0c0c0', smooth_shading=True, specular=1.0, specular_power=15)
        self.plotter.add_mesh(h_stab_mesh, color='#c0c0c0', smooth_shading=True, specular=1.0, specular_power=15)
        self.plotter.add_mesh(v_stab_mesh, color='#ad1b02', smooth_shading=True, specular=1.0, specular_power=15)
        self.plotter.add_mesh(engines_mesh, color='#404040', smooth_shading=True)

        self.plotter.render()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
