import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import random

try:
    QT = 4
    import PyQt4.QtGui as QtG
    import PyQt4.QtCore as QtCore
    from PyQt4.QtGui import QFontMetrics
    import matplotlib.backends.backend_qt4agg as plt_qtbackend
except ImportError:
    QT = 5
    import PyQt5.QtWidgets as QtG
    from PyQt5.QtGui import QFontMetrics
    import PyQt5.QtCore as QtCore
    import matplotlib.backends.backend_qt5agg as plt_qtbackend


from cryolo import imagereader, CoordsIO
from . import boxmanager_toolbar
from . import MyRectangle
import argparse

argparser = argparse.ArgumentParser(
    description="Train and validate crYOLO on any dataset",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)

argparser.add_argument("-i", "--image_dir", help="Path to image directory.")

argparser.add_argument("-b", "--box_dir", help="Path to box directory.")


class MainWindow(QtG.QMainWindow):
    def __init__(self, font, images_path=None, boxes_path=None, parent=None):

        super(MainWindow, self).__init__(parent)
        # SETUP QT
        self.font = font
        self.setWindowTitle("Box manager")
        central_widget = QtG.QWidget(self)

        self.setCentralWidget(central_widget)

        # Center on screen
        resolution = QtG.QDesktopWidget().screenGeometry()
        self.move(
            (resolution.width() / 2) - (self.frameSize().width() / 2),
            (resolution.height() / 2) - (self.frameSize().height() / 2),
        )

        # Setup Menu
        close_action = QtG.QAction("Close", self)
        close_action.setShortcut("Ctrl+Q")
        close_action.setStatusTip("Leave the app")
        close_action.triggered.connect(self.close_boxmanager)

        open_image_folder = QtG.QAction("Open image folder", self)
        open_image_folder.triggered.connect(self.open_image_folder)

        import_box_folder = QtG.QAction("Import box files", self)
        import_box_folder.triggered.connect(self.load_box_files)

        write_box_files = QtG.QAction("Write box files", self)
        write_box_files.triggered.connect(self.write_box_files)

        self.mainMenu = self.menuBar()
        self.fileMenu = self.mainMenu.addMenu("&File")
        self.fileMenu.addAction(open_image_folder)
        self.fileMenu.addAction(import_box_folder)
        self.fileMenu.addAction(write_box_files)
        self.fileMenu.addAction(close_action)
        self.image_folder = ""

        # Setup tree
        self.layout = QtG.QGridLayout(central_widget)
        self.setMenuBar(self.mainMenu)

        self.tree = QtG.QTreeWidget(self)
        self.tree.setHeaderHidden(True)
        self.layout.addWidget(self.tree, 0, 0, 1, 3)
        self.tree.currentItemChanged.connect(self._event_image_changed)

        # Box size setup
        self.boxsize = 200
        self.boxsize_label = QtG.QLabel()
        self.boxsize_label.setText("Box size: ")
        self.layout.addWidget(self.boxsize_label, 1, 0)

        self.boxsize_line = QtG.QLineEdit()
        self.boxsize_line.setText(str(self.boxsize))
        self.layout.addWidget(self.boxsize_line, 1, 1)

        self.button_set_box_size = QtG.QPushButton("Set")
        self.button_set_box_size.clicked.connect(self.box_size_changed)
        self.layout.addWidget(self.button_set_box_size, 1, 2)

        # Confidence threshold setup
        self.current_conf_thresh = 0.3
        self.conf_thresh_label = QtG.QLabel()
        self.conf_thresh_label.setText("Confidence threshold: ")
        self.layout.addWidget(self.conf_thresh_label, 2, 0)
        self.conf_thresh_label.setEnabled(False)
        self.conf_thresh_slide = QtG.QSlider(QtCore.Qt.Horizontal)
        #self.conf_thresh_line.setText(str(self.current_conf_thresh))
        self.conf_thresh_slide.setMinimum(0)
        self.conf_thresh_slide.setMaximum(100)
        self.conf_thresh_slide.setValue(30)
        self.conf_thresh_slide.valueChanged.connect(self.conf_thresh_changed)
        self.conf_thresh_slide.setTickPosition(QtG.QSlider.TicksBelow)
        self.conf_thresh_slide.setTickInterval(1)
        self.conf_thresh_slide.setEnabled(False)
        self.layout.addWidget(self.conf_thresh_slide, 2, 1)

        self.conf_thresh_line = QtG.QLineEdit()
        self.conf_thresh_line.setText("0.3")
        self.conf_thresh_line.textChanged.connect(self.conf_thresh_label_changed)
        self.conf_thresh_line.setEnabled(False)
        self.layout.addWidget(self.conf_thresh_line, 2, 2)

        #self.button_set_conf_thresh = QtG.QPushButton("Set")
        #self.button_set_conf_thresh.clicked.connect(self.conf_thresh_changed)
        #self.layout.addWidget(self.button_set_conf_thresh, 2, 2)

        # Show image selection
        self.show()
        # self.open_image_folder()
        self.box_dictionary = {}

        self.plot = None
        self.fig = None
        self.ax = None

        self.moving_box = None

        self.zoom_update = False
        self.doresizing = False
        self.current_image_path = None
        self.background_current = None
        self.unsaved_changes = False
        self.is_cbox = False
        self.toggle = False

        if images_path:
            self._open_image_folder(images_path)
            if boxes_path:
                self._import_boxes(box_dir=boxes_path, keep=False)

    def close_boxmanager(self):
        if self.unsaved_changes:
            msg = "All loaded boxes are discarded. Are you sure?"
            reply = QtG.QMessageBox.question(
                self, "Message", msg, QtG.QMessageBox.Yes, QtG.QMessageBox.Cancel
            )

            if reply == QtG.QMessageBox.Cancel:
                return
        self.close()

    def _event_image_changed(self, root_tree_item):

        if (
            root_tree_item is not None
            and root_tree_item.childCount() == 0
            and self.current_image_path is not None
        ):
            self.current_tree_item = root_tree_item
            filename = root_tree_item.text(0)
            pure_filename = os.path.splitext(os.path.basename(self.current_image_path))[0]

            if pure_filename in self.box_dictionary:
                self.rectangles = self.box_dictionary[pure_filename]
                self.delete_all_patches(self.rectangles)
            else:
                self.rectangles = []

            self.current_image_path = os.path.join(self.image_folder, str(filename))
            self.fig.canvas.set_window_title(os.path.basename(self.current_image_path))
            img = self.read_image(self.current_image_path)
            self.im.set_data(img)
            self.fig.canvas.draw()
            self.background_current = self.fig.canvas.copy_from_bbox(self.ax.bbox)
            self.background_orig = self.fig.canvas.copy_from_bbox(self.ax.bbox)
            self.update_boxes_on_current_image()

    def conf_thresh_label_changed(self):
        try:
            new_value = float(self.conf_thresh_line.text())
            if new_value > 1.0 or new_value < 0:
                return
        except ValueError:
            return
        self.current_conf_thresh = new_value
        self.conf_thresh_slide.setValue(new_value * 100)

    def conf_thresh_changed(self):
        try:
            self.current_conf_thresh = float(self.conf_thresh_slide.value()) / 100
        except ValueError:
            return
        try:
            if np.abs(float(self.conf_thresh_line.text())-self.current_conf_thresh) >= 0.01:
                self.conf_thresh_line.setText(""+str(self.current_conf_thresh))
        except ValueError:
            self.conf_thresh_line.setText("" + str(self.current_conf_thresh))

        self.update_boxes_on_current_image()
        self.fig.canvas.restore_region(self.background_current)
        self._draw_all_boxes()
        self.unsaved_changes = True

    def box_size_changed(self):
        try:
            self.boxsize = int(self.boxsize_line.text())
        except ValueError:
            return

        if self.boxsize > 0:
            for _, rectangles in self.box_dictionary.items():
                for rect in rectangles:
                    height_diff = self.boxsize - rect.get_height()
                    width_diff = self.boxsize - rect.get_width()
                    newy = rect.get_y() - height_diff / 2
                    newx = rect.get_x() - width_diff / 2
                    rect.set_height(self.boxsize)
                    rect.set_width(self.boxsize)
                    rect.set_xy((newx, newy))

            self.update_boxes_on_current_image()
            self.fig.canvas.restore_region(self.background_current)
            self._draw_all_boxes()
            self.unsaved_changes = True

    def delte_all_boxes(self):
        for _, rectangles in self.box_dictionary.items():
            self.delete_all_patches(rectangles)

        self.rectangles = []
        self.box_dictionary = {}
        self.update_boxes_on_current_image()
        if self.background_current is not None:
            self.fig.canvas.restore_region(self.background_current)

    def update_boxes_on_current_image(self):
        if self.current_image_path is None:
            return
        pure_filename = os.path.splitext(os.path.basename(self.current_image_path))[0]
        if pure_filename in self.box_dictionary:
            self.rectangles = self.box_dictionary[pure_filename]
            self.delete_all_patches(self.rectangles)
            self.draw_all_patches(self.rectangles)
            self._draw_all_boxes()

    def delete_all_patches(self, rects):
        for box in rects:
            box.set_visible(False)
            if box.is_figure_set():
                box.remove()

    def write_box_files(self):
        """
        Write all files
        :return: None
        """
        box_dir = str(
            QtG.QFileDialog.getExistingDirectory(self, "Select Box Directory")
        )
        if box_dir == "":
            return

        # Remove untitled from path if untitled not exists
        if box_dir[-8] == "untitled" and os.path.isdir(box_dir):
            box_dir = box_dir[:-8]

        if box_dir == "":
            return
        num_writtin_part = 0
        for filename, rectangles in self.box_dictionary.items():
            box_filename = filename + ".box"
            box_file_path = os.path.join(box_dir, box_filename)
            if self.is_cbox:
                rectangles = [box for box in rectangles if box.confidence>self.current_conf_thresh]
            num_writtin_part = num_writtin_part + len(rectangles)
            CoordsIO.write_boxfile_manager(box_file_path, rectangles)
            self.unsaved_changes = False
        print(num_writtin_part,"particles written.")

    def load_box_files(self):
        self.is_cbox = False
        keep = False
        if self.unsaved_changes:
            msg = "There are unsaved changes. Are you sure?"
            reply = QtG.QMessageBox.question(
                self, "Message", msg, QtG.QMessageBox.Yes, QtG.QMessageBox.Cancel
            )

            if reply == QtG.QMessageBox.Cancel:
                return

        if len(self.box_dictionary) > 0:
            msg = "Keep old boxes loaded and show the new ones in a different color?"
            reply = QtG.QMessageBox.question(
                self, "Message", msg, QtG.QMessageBox.Yes, QtG.QMessageBox.No
            )

            if reply == QtG.QMessageBox.Yes:
                keep = True

        if keep == False:
            self.delte_all_boxes()

        if self.plot is not None:
            box_dir = str(
                QtG.QFileDialog.getExistingDirectory(self, "Select Box Directory")
            )

            if box_dir == "":
                return

            self._import_boxes(box_dir, keep)
        else:
            errmsg = QtG.QErrorMessage(self)
            errmsg.showMessage("Please open an image folder first")

    def _import_boxes(self, box_dir, keep=False):
        self.setWindowTitle("Box manager (Showing: " + box_dir + ")")
        box_imported = 0
        onlyfiles = [
            f
            for f in os.listdir(box_dir)
            if os.path.isfile(os.path.join(box_dir, f)) and not f.startswith(".")
        ]
        colors = ["b", "g", "r", "c", "m", "y", "k", "w"]
        if keep == False:
            rand_color = "r"
        else:
            rand_color = random.choice(colors)
            while rand_color == "r":
                rand_color = random.choice(colors)
        star_dialog_was_shown = False
        for file in onlyfiles:
            if file.endswith(".box") or file.endswith(".txt") or file.endswith(".star") or file.endswith(".cbox"):
                path = os.path.join(box_dir, file)
                is_helicon = CoordsIO.is_eman1_helicon(path)
                is_eman1_startend = CoordsIO.is_eman1_filament_start_end(path)
                is_star_startend = False
                if file.endswith(".star") and star_dialog_was_shown == False:
                    msg = "Are the star files containing filament coordinates (start/end)?"
                    reply = QtG.QMessageBox.question(
                        self, "Message", msg, QtG.QMessageBox.Yes, QtG.QMessageBox.No
                    )
                    if reply == QtG.QMessageBox.Yes:
                        is_star_startend = True
                    star_dialog_was_shown = True

                if is_helicon or is_eman1_startend or is_star_startend:
                    rects = []
                    identifier = file[:-4]
                    if is_helicon:
                        filaments = CoordsIO.read_eman1_helicon(path)
                    elif is_eman1_startend:
                        filaments = CoordsIO.read_eman1_filament_start_end(path)
                    elif is_star_startend:
                        filaments = CoordsIO.read_star_filament_file(path=path, box_width=100)
                        identifier = file[:-5]
                    for fil in filaments:
                        rand_color = random.choice(colors)
                        for box in fil.boxes:
                            x_ll = int(box.x)
                            y_ll = int(box.y)
                            width = int(box.w)
                            height = int(box.h)
                            self.boxsize = box.w
                            rect = MyRectangle.MyRectangle(
                                (x_ll, y_ll),
                                width,
                                height,
                                linewidth=1,
                                edgecolor=rand_color,
                                facecolor="none",
                            )
                            rect.set_confidence(1)
                            rects.append(rect)
                            box_imported = box_imported + 1
                    self.box_dictionary[identifier] = rects
                else:
                    if os.stat(path).st_size != 0:
                        self.conf_thresh_line.setEnabled(False)
                        self.conf_thresh_slide.setEnabled(False)
                        self.conf_thresh_label.setEnabled(False)

                        self.is_cbox = False
                        if path.endswith(".box"):
                            boxes = CoordsIO.read_eman1_boxfile(path)
                            dict_entry_name = file[:-4]
                        if path.endswith(".star"):
                            boxes = CoordsIO.read_star_file(path, 100)
                            dict_entry_name = file[:-5]
                        if path.endswith(".cbox"):
                            boxes = CoordsIO.read_cbox_boxfile(path)
                            dict_entry_name = file[:-5]
                            self.is_cbox = True
                            self.conf_thresh_line.setEnabled(True)
                            self.conf_thresh_slide.setEnabled(True)
                            self.conf_thresh_label.setEnabled(True)

                        rects = []
                        xscale = yscale = 1
                        #np.random.seed(5)
                        for box in boxes:
                            #if np.random.rand()>0.8:
                            x_ll = int(box.x * xscale)
                            y_ll = int(box.y * yscale)
                            #if x_ll > (197 - 10) and x_ll < (197 + 10) and y_ll > (
                            #        225 - 10) and y_ll < (225 + 10):
                            width = int(box.w * xscale)
                            height = int(box.h * yscale)
                            self.boxsize = width
                            rect = MyRectangle.MyRectangle(
                                (x_ll, y_ll),
                                width,
                                height,
                                linewidth=1,
                                edgecolor=rand_color,
                                facecolor="none",
                            )
                            if self.is_cbox:
                                rect.set_confidence(box.c)
                            else:
                                rect.set_confidence(1)
                            rects.append(rect)
                            box_imported = box_imported + 1
                        if dict_entry_name in self.box_dictionary:
                            self.box_dictionary[dict_entry_name].extend(rects)
                        else:
                            self.box_dictionary[dict_entry_name] = rects

        self.update_boxes_on_current_image()
        self.boxsize_line.setText(str(self.boxsize))
        print("Total imported particles: ", box_imported)

    def is_helicon_with_particle_coords(self, path):
        with open(path) as f:
            first_line = f.readline()
            f.close()
        return "#micrograph" in first_line

    def is_eman1_helicion(self, path):
        try:
            box_lines = np.atleast_2d(np.genfromtxt(path))
            if len(box_lines) < 2:
                return False
            return (
                len(box_lines[0]) == 5 and box_lines[0][4] == -1 and box_lines[1][4] == -2
            )
        except ValueError:
            return False

    def getEquidistantRectangles(
        self, x_start, y_start, x_end, y_end, width, parts, edgecolor
    ):
        points = zip(
            np.linspace(x_start, x_end, parts + 1, endpoint=False),
            np.linspace(y_start, y_end, parts + 1, endpoint=False),
        )
        new_rectangles = []
        w = width
        h = width

        for point in points:
            rect = MyRectangle.MyRectangle(
                (point[0], point[1]),
                w,
                h,
                linewidth=1,
                edgecolor=edgecolor,
                facecolor="none",
            )
            rect.set_confidence(1)
            new_rectangles.append(rect)
        return new_rectangles

    def draw_all_patches(self, rect):
        for box in rect:
            if box.confidence > self.current_conf_thresh:
                box.set_visible(True)
                if box not in self.ax.patches:
                    self.ax.add_patch(box)

    def read_image(self, path):
        if path.endswith(("jpg", "jpeg", "png")):
            img = imagereader.image_read(path)
            img = np.flip(img, 0)
            return img
        if path.endswith(("tif", "tiff")):
            ret = imagereader.image_read(path)
            if not np.issubdtype(ret.dtype, np.float32):
                ret = ret.astype(np.float32)
            ret = np.flip(ret, 0)
            mean = np.mean(ret)
            sd = np.std(ret)
            ret = (ret - mean) / sd
            ret[ret > 3] = 3
            ret[ret < -3] = -3
            return ret
        if path.endswith(("mrc","mrcs")):
            ret = imagereader.image_read(path)
            ret = np.flip(ret, 0)
            mean = np.mean(ret)
            sd = np.std(ret)
            ret = (ret - mean) / sd
            ret[ret > 2] = 2
            ret[ret < -2] = -2

            return ret
        return None

    def open_image_folder(self):
        """
        Let the user choose the image folder and adds it to the ImageFolder-Tree
        :return: none
        """
        selected_folder = str(
            QtG.QFileDialog.getExistingDirectory(self, "Select Image Directory")
        )

        if selected_folder == "":
            return

        if self.unsaved_changes:
            msg = "All loaded boxes are discarded. Are you sure?"
            reply = QtG.QMessageBox.question(
                self, "Message", msg, QtG.QMessageBox.Yes, QtG.QMessageBox.Cancel
            )

            if reply == QtG.QMessageBox.Cancel:
                return

        self.current_image_path = None
        self._open_image_folder(selected_folder)

    def _open_image_folder(self, path):
        """
        Reads the image folder, setup the folder daemon and signals
        :param path: Path to image folder
        """
        self.image_folder = path
        if path != "":
            root = QtG.QTreeWidgetItem([str(path)])
            self.tree.clear()
            if self.plot is not None:
                self.plot.close()
            self.rectangles = []
            self.box_dictionary = {}
            self.tree.addTopLevelItem(root)
            fm = QFontMetrics(self.font)
            w = fm.width(path)
            self.tree.setMinimumWidth(w + 150)

            onlyfiles = [
                f
                for f in sorted(os.listdir(path))
                if os.path.isfile(os.path.join(path, f))
            ]
            onlyfiles = [i for i in onlyfiles if not i.startswith(".")]
            contains_valid_file = False

            for file in onlyfiles:
                if file.endswith((".jpg", ".jpeg", ".png", ".mrc", ".mrcs",".tif", ".tiff")):
                    # if imagereader.is_single_channel(os.path.join(path, file)):
                    next_item = QtG.QTreeWidgetItem([file])
                    root.addChild(next_item)
                    contains_valid_file = True

            if contains_valid_file:
                root.setExpanded(True)
                # Show first image
                self.current_image_path = os.path.join(
                    self.image_folder, str(root.child(0).text(0))
                )
                self.current_tree_item = root.child(0)
                im = self.read_image(self.current_image_path)

                self.rectangles = []
                # Create figure and axes

                self.fig, self.ax = plt.subplots(1)

                self.ax.xaxis.set_visible(False)
                self.ax.yaxis.set_visible(False)

                self.fig.tight_layout()
                self.fig.canvas.set_window_title(
                    os.path.basename(self.current_image_path)
                )

                # Display the image
                self.im = self.ax.imshow(
                    im, origin="lower", cmap="gray", interpolation="Hanning"
                )  #

                self.plot = QtG.QDialog(self)
                self.plot.canvas = plt_qtbackend.FigureCanvasQTAgg(self.fig)
                self.plot.canvas.mpl_connect("button_press_event", self.onclick)
                self.plot.canvas.mpl_connect("key_press_event", self.myKeyPressEvent)
                self.plot.canvas.setFocusPolicy(QtCore.Qt.ClickFocus)
                self.plot.canvas.setFocus()
                self.plot.canvas.mpl_connect("button_release_event", self.onrelease)
                self.plot.canvas.mpl_connect("motion_notify_event", self.onmove)
                self.plot.canvas.mpl_connect("resize_event", self.onresize)
                self.plot.canvas.mpl_connect("draw_event", self.ondraw)
                self.plot.toolbar = boxmanager_toolbar.Boxmanager_Toolbar(
                    self.plot.canvas, self.plot, self.fig, self.ax, self
                )  # plt_qtbackend.NavigationToolbar2QT(self.plot.canvas, self.plot)
                layout = QtG.QVBoxLayout()
                layout.addWidget(self.plot.toolbar)
                layout.addWidget(self.plot.canvas)
                self.plot.setLayout(layout)
                self.plot.canvas.draw()
                self.plot.show()
                self.background_current = self.fig.canvas.copy_from_bbox(self.ax.bbox)
                self.background_orig = self.fig.canvas.copy_from_bbox(self.ax.bbox)

    def myKeyPressEvent(self, event):
        if event.name == "key_press_event" and event.key == "h":
            pure_filename = os.path.basename(self.current_image_path)[:-4]
            if pure_filename in self.box_dictionary:
                rects = self.box_dictionary[pure_filename]
                if self.toggle:
                    self.draw_all_patches(rects)
                    self.fig.canvas.draw()
                    self.toggle = False
                else:
                    self.delete_all_patches(rects)
                    self.fig.canvas.draw()
                    self.toggle = True

    def ondraw(self, event):
        if self.zoom_update:
            self.zoom_update = False
            self.background_current = self.fig.canvas.copy_from_bbox(self.ax.bbox)
            self.draw_all_patches(self.rectangles)
            self._draw_all_boxes()

    def onresize(self, event):
        self.delete_all_patches(self.rectangles)
        self.fig.canvas.draw()
        self.background_current = self.fig.canvas.copy_from_bbox(self.ax.bbox)
        self.background_orig = self.fig.canvas.copy_from_bbox(self.ax.bbox)
        self.draw_all_patches(self.rectangles)

    def onmove(self, event):
        if event.inaxes != self.ax:
            return
        if event.button == 1:
            if self.moving_box is not None:
                x = event.xdata - self.moving_box.get_width() / 2
                y = event.ydata - self.moving_box.get_width() / 2
                self.boxsize = self.moving_box.get_width()  # Update the current boxsize
                self.moving_box.set_x(x)
                self.moving_box.set_y(y)

                self.fig.canvas.restore_region(self.background_current)

                ## draw all boxes again
                self._draw_all_boxes()

    def onrelease(self, event):
        self.moving_box = None

    def onclick(self, event):
        if self.plot.toolbar._active is not None:
            return

        modifiers = QtG.QApplication.keyboardModifiers()
        if event.xdata < 0 or event.ydata < 0:
            return
        pure_filename = os.path.splitext(os.path.basename(self.current_image_path))[0]

        if pure_filename in self.box_dictionary:
            self.rectangles = self.box_dictionary[pure_filename]
        else:
            self.rectangles = []
            self.box_dictionary[pure_filename] = self.rectangles

        if (
            modifiers == QtCore.Qt.ControlModifier
            or modifiers == QtCore.Qt.MetaModifier
        ):
            # Delete box
            box = self.get_corresponding_box(
                event.xdata - self.boxsize / 2,
                event.ydata - self.boxsize / 2,
                self.rectangles,
            )

            if box is not None:
                self.delete_box(box)
        else:
            self.moving_box = self.get_corresponding_box(
                event.xdata - self.boxsize / 2,
                event.ydata - self.boxsize / 2,
                self.rectangles,
            )
            if self.moving_box is None:

                # Delete lower confidence box if available
                box = self.get_corresponding_box(
                    event.xdata - self.boxsize / 2,
                    event.ydata - self.boxsize / 2,
                    self.rectangles, get_low=True
                )

                if box is not None:
                    self.rectangles.remove(box)

                # Create new box

                xy = (event.xdata - self.boxsize / 2, event.ydata - self.boxsize / 2)
                rect = MyRectangle.MyRectangle(
                    xy,
                    self.boxsize,
                    self.boxsize,
                    linewidth=1,
                    edgecolor="r",
                    facecolor="none",
                )
                rect.set_confidence(1)
                self.moving_box = rect
                self.rectangles.append(rect)
                # Add the patch to the Axes
                self.ax.add_patch(rect)
                self.ax.draw_artist(rect)

                self.fig.canvas.blit(self.ax.bbox)
                self.unsaved_changes = True
                # self.fig.canvas.draw()

    def delete_box(self, box):
        box.remove()
        del self.rectangles[self.rectangles.index(box)]
        self.fig.canvas.restore_region(self.background_current)
        self._draw_all_boxes()
        self.unsaved_changes = True
    def _draw_all_boxes(self):
        for box in self.rectangles:
            self.ax.draw_artist(box)
        self.fig.canvas.blit(self.ax.bbox)

    def get_corresponding_box(self, x, y, rectangles, get_low = False):
        a = np.array([x, y])

        for box in rectangles:
            b = np.array(box.xy)
            dist = np.linalg.norm(a - b)
            if get_low:
                if dist < self.boxsize / 2 and box.confidence < self.current_conf_thresh:
                    return box
            else:
                if dist < self.boxsize / 2 and box.confidence > self.current_conf_thresh:
                    return box
        return None

    def get_number_visible_boxes(self, rectangles):
        i = 0
        for box in rectangles:
            if box.is_figure_set():
                i = i + 1
        return i


def run(args=None):
    app = QtG.QApplication(sys.argv)
    args = argparser.parse_args()
    image_dir = args.image_dir
    box_dir = args.box_dir
    gui = MainWindow(app.font(), images_path=image_dir, boxes_path=box_dir)
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
