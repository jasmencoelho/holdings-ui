import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QPushButton, QMessageBox
from PyQt5.QtWidgets import QFileDialog, QLabel
from PyQt5.QtWidgets import QProgressBar
from db_handler import get_geodata_group, get_basemap_for_region
from image_generator import save_plot
from ppt_generator import build_ppt_for_regions

class RegionSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Country/Region Selector")
        self.setGeometry(100, 100, 400, 450)

        self.selected_output_folder = None

        layout = QVBoxLayout()

        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.MultiSelection)

        self.populate_regions()

        self.folder_label = QLabel("No folder selected.")
        self.folder_button = QPushButton("Choose Output Folder")
        self.folder_button.clicked.connect(self.choose_output_folder)

        self.generate_button = QPushButton("Generate Report")
        
        self.generate_button.clicked.connect(self.get_selection)
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        layout.addWidget(self.list_widget)
        layout.addWidget(self.folder_button)
        layout.addWidget(self.folder_label)
        layout.addWidget(self.generate_button)
        self.setLayout(layout)

    def choose_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.selected_output_folder = folder
            self.folder_label.setText(f"Selected: {folder}")
        else:
            self.folder_label.setText("No folder selected.")

       def get_selection(self):
        from PyQt5.QtWidgets import QApplication
        import os

        selected = [item.text() for item in self.list_widget.selectedItems()]
        if not selected:
            QMessageBox.warning(self, "No Selection", "Please select at least one region.")
            return

        if not self.selected_output_folder:
            QMessageBox.warning(self, "No Output Folder", "Please choose an output folder.")
            return

        try:
            region_images = {}

            # Initialize progress bar
            total_steps = len(selected) * 3  # 3 layers per region
            step = 0
            self.progress_bar.setValue(0)

            for region in selected:
                gdf_dict = get_geodata_group(region)
                basemap = get_basemap_for_region(region)
                img_paths = []

                for tag, gdf in gdf_dict.items():
                    if gdf.empty or basemap.empty:
                        continue

                    path = save_plot(gdf, region, tag, basemap, out_dir=self.selected_output_folder)
                    img_paths.append(path)

                    # Update progress bar
                    step += 1
                    progress = int((step / total_steps) * 100)
                    self.progress_bar.setValue(progress)
                    QApplication.processEvents()  # keeps the UI from freezing

                if img_paths:
                    region_images[region] = img_paths

            if region_images:
                ppt_path = os.path.join(self.selected_output_folder, "output.pptx")
                build_ppt_for_regions(region_images, out_path=ppt_path)

                self.progress_bar.setValue(100)
                QMessageBox.information(self, "Done", f"Slides and images saved to:\n{self.selected_output_folder}")
            else:
                QMessageBox.warning(self, "No Data", "No valid plots generated for selected regions.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate report:\n{str(e)}")
            self.progress_bar.setValue(0)
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegionSelector()
    window.show()
    sys.exit(app.exec_())

