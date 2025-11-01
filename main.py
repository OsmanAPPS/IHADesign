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

        # Wing Length Slider
        control_layout.addWidget(QLabel("Wing Length"))
        self.wing_slider = QSlider(Qt.Orientation.Horizontal)
        self.wing_slider.setRange(5, 25)
        self.wing_slider.setValue(12)
        self.wing_slider.valueChanged.connect(self.update_aircraft)
        control_layout.addWidget(self.wing_slider)

        # Fuselage Radius Slider
        control_layout.addWidget(QLabel("Fuselage Radius"))
        self.fuselage_slider = QSlider(Qt.Orientation.Horizontal)
        self.fuselage_slider.setRange(3, 10) # Using integers, will be divided by 10
        self.fuselage_slider.setValue(5)
        self.fuselage_slider.valueChanged.connect(self.update_aircraft)
        control_layout.addWidget(self.fuselage_slider)

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
        self.plotter.clear_actors() # Clear previous aircraft parts

        # Get values from sliders
        wing_length = self.wing_slider.value()
        fuselage_radius = self.fuselage_slider.value() / 10.0

        # Create airplane parts using parameters
        fuselage = pv.Cylinder(center=(0, 0, 0), direction=(1, 0, 0), radius=fuselage_radius, height=10)
        wing = pv.Cube(center=(0, 0, 0), x_length=0.2, y_length=wing_length, z_length=1)
        tail_wing = pv.Cube(center=(-4.5, 0, 0.5), x_length=0.1, y_length=wing_length / 3.0, z_length=0.5)
        vertical_stabilizer = pv.Cube(center=(-4.5, 0, 1), x_length=0.1, y_length=0.5, z_length=2)

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
