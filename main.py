import sys
import pyvista as pv
from pyvistaqt.plotting import QtInteractor
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout,
                             QVBoxLayout, QFrame, QSlider, QLabel)
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Aircraft Designer")
        self.setGeometry(100, 100, 1400, 900)

        # Main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # --- Left Panel: Controls ---
        control_panel = QFrame()
        control_panel.setFrameShape(QFrame.Shape.StyledPanel)
        control_layout = QVBoxLayout(control_panel)
        main_layout.addWidget(control_panel, 1)

        # Wing Span Slider
        control_layout.addWidget(QLabel("Wing Span"))
        self.wing_span_slider = QSlider(Qt.Orientation.Horizontal)
        self.wing_span_slider.setRange(5, 30)
        self.wing_span_slider.setValue(12)
        self.wing_span_slider.valueChanged.connect(self.update_aircraft)
        control_layout.addWidget(self.wing_span_slider)

        # Wing Chord Slider
        control_layout.addWidget(QLabel("Wing Chord (Width)"))
        self.wing_chord_slider = QSlider(Qt.Orientation.Horizontal)
        self.wing_chord_slider.setRange(10, 50) # x 0.1
        self.wing_chord_slider.setValue(20)
        self.wing_chord_slider.valueChanged.connect(self.update_aircraft)
        control_layout.addWidget(self.wing_chord_slider)

        # Fuselage Length Slider
        control_layout.addWidget(QLabel("Fuselage Length"))
        self.fuselage_length_slider = QSlider(Qt.Orientation.Horizontal)
        self.fuselage_length_slider.setRange(8, 20)
        self.fuselage_length_slider.setValue(10)
        self.fuselage_length_slider.valueChanged.connect(self.update_aircraft)
        control_layout.addWidget(self.fuselage_length_slider)

        # Fuselage Radius Slider
        control_layout.addWidget(QLabel("Fuselage Radius"))
        self.fuselage_radius_slider = QSlider(Qt.Orientation.Horizontal)
        self.fuselage_radius_slider.setRange(3, 10) # x 0.1
        self.fuselage_radius_slider.setValue(5)
        self.fuselage_radius_slider.valueChanged.connect(self.update_aircraft)
        control_layout.addWidget(self.fuselage_radius_slider)

        # Tail Wing Span Slider
        control_layout.addWidget(QLabel("Tail Wing Span"))
        self.tail_wing_span_slider = QSlider(Qt.Orientation.Horizontal)
        self.tail_wing_span_slider.setRange(2, 10)
        self.tail_wing_span_slider.setValue(4)
        self.tail_wing_span_slider.valueChanged.connect(self.update_aircraft)
        control_layout.addWidget(self.tail_wing_span_slider)

        # Vertical Stabilizer Height Slider
        control_layout.addWidget(QLabel("Vertical Stabilizer Height"))
        self.stabilizer_height_slider = QSlider(Qt.Orientation.Horizontal)
        self.stabilizer_height_slider.setRange(1, 5)
        self.stabilizer_height_slider.setValue(2)
        self.stabilizer_height_slider.valueChanged.connect(self.update_aircraft)
        control_layout.addWidget(self.stabilizer_height_slider)

        control_layout.addStretch()

        # --- Right Panel: 3D Viewer ---
        self.plotter = QtInteractor(self)
        main_layout.addWidget(self.plotter.interactor, 3)

        # --- Initial Scene Setup ---
        self.setup_scene()
        self.update_aircraft()

    def setup_scene(self):
        """Sets up the initial plotter properties."""
        self.plotter.camera_position = 'xy'
        self.plotter.camera.azimuth = 45
        self.plotter.camera.elevation = 20
        self.plotter.reset_camera()
        # Add a light for better shading
        light = pv.Light(position=(0, 0, 10), light_type='scene light')
        self.plotter.add_light(light)

    def update_aircraft(self):
        """Clears the scene and redraws the aircraft with current slider values."""
        self.plotter.clear_actors()  # Clear previous aircraft parts

        # Get values from sliders
        wing_span = self.wing_span_slider.value()
        wing_chord = self.wing_chord_slider.value() / 10.0
        fuselage_length = self.fuselage_length_slider.value()
        fuselage_radius = self.fuselage_radius_slider.value() / 10.0
        tail_wing_span = self.tail_wing_span_slider.value()
        stabilizer_height = self.stabilizer_height_slider.value()

        # Define tail position based on fuselage length
        tail_pos_x = -fuselage_length / 2.0 + 0.5

        # Create airplane parts using parameters
        fuselage = pv.Cylinder(center=(0, 0, 0), direction=(1, 0, 0), radius=fuselage_radius, height=fuselage_length)
        wing = pv.Cube(center=(0, 0, 0), x_length=wing_chord, y_length=wing_span, z_length=wing_chord / 10.0)
        tail_wing = pv.Cube(center=(tail_pos_x, 0, fuselage_radius * 0.5), x_length=wing_chord / 2.0, y_length=tail_wing_span, z_length=wing_chord / 20.0)
        vertical_stabilizer = pv.Cube(center=(tail_pos_x, 0, fuselage_radius + stabilizer_height / 2.0), x_length=wing_chord / 2.0, y_length=wing_chord/10, z_length=stabilizer_height)

        # Add parts to the plotter
        self.plotter.add_mesh(fuselage, name="fuselage", color='silver', smooth_shading=True)
        self.plotter.add_mesh(wing, name="wing", color='silver', smooth_shading=True)
        self.plotter.add_mesh(tail_wing, name="tail_wing", color='silver', smooth_shading=True)
        self.plotter.add_mesh(vertical_stabilizer, name="stabilizer", color='red', smooth_shading=True)

        self.plotter.render()


if __name__ == '__main__':
    # NOTE: This application requires a desktop environment (like Windows, macOS, or Linux with X11/Wayland)
    # to run. It will not run in a headless environment.
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
