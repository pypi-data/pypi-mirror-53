import os.path
import sys
import re

from AnyQt.QtWidgets import QFileDialog, QGridLayout, QMessageBox

from Orange.data.table import Table
from Orange.data.io import TabReader, CSVReader, PickleReader, ExcelReader
from Orange.widgets import gui, widget
from Orange.widgets.settings import Setting
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.widget import Input


class OWSave(widget.OWWidget):
    name = "Save Data"
    description = "Save data to an output file."
    icon = "icons/Save.svg"
    category = "Data"
    keywords = []

    settings_version = 2

    writers = [TabReader, CSVReader, PickleReader, ExcelReader]
    filters = {
        **{f"{w.DESCRIPTION} (*{w.EXTENSIONS[0]})": w
           for w in writers},
        **{f"Compressed {w.DESCRIPTION} (*{w.EXTENSIONS[0]}.gz)": w
           for w in writers if w.SUPPORT_COMPRESSED}
    }
    userhome = os.path.expanduser(f"~{os.sep}")

    class Inputs:
        data = Input("Data", Table)

    class Error(widget.OWWidget.Error):
        unsupported_sparse = widget.Msg("Use Pickle format for sparse data.")
        no_file_name = widget.Msg("File name is not set.")
        general_error = widget.Msg("{}")

    want_main_area = False
    resizing_enabled = False

    last_dir = Setting("")
    filter = Setting(next(iter(filters)))
    filename = Setting("", schema_only=True)
    add_type_annotations = Setting(True)
    auto_save = Setting(False)

    def __init__(self):
        super().__init__()
        self.data = None

        grid = QGridLayout()
        gui.widgetBox(self.controlArea, orientation=grid)
        grid.addWidget(
            gui.checkBox(
                None, self, "add_type_annotations",
                "Add type annotations to header",
                tooltip=
                "Some formats (Tab-delimited, Comma-separated) can include \n"
                "additional information about variables types in header rows.",
                callback=self._update_messages),
            0, 0, 1, 2)
        grid.setRowMinimumHeight(1, 8)
        grid.addWidget(
            gui.checkBox(
                None, self, "auto_save", "Autosave when receiving new data",
                callback=self._update_messages),
            2, 0, 1, 2)
        grid.setRowMinimumHeight(3, 8)
        self.bt_save = gui.button(None, self, "Save", callback=self.save_file)
        grid.addWidget(self.bt_save, 4, 0)
        grid.addWidget(
            gui.button(None, self, "Save as ...", callback=self.save_file_as),
            4, 1)

        self.adjustSize()
        self._update_messages()

    @property
    def writer(self):
        return self.filters[self.filter]

    @Inputs.data
    def dataset(self, data):
        self.Error.clear()
        self.data = data
        self._update_status()
        self._update_messages()
        if self.auto_save and self.filename:
            self.save_file()

    def save_file(self):
        if not self.filename:
            self.save_file_as()
            return

        self.Error.general_error.clear()
        if self.data is None \
                or not self.filename \
                or (self.data.is_sparse()
                        and not self.writer.SUPPORT_SPARSE_DATA):
            return
        try:
            self.writer.write(
                self.filename, self.data, self.add_type_annotations)
        except IOError as err_value:
            self.Error.general_error(str(err_value))

    def save_file_as(self):
        filename, selected_filter = self.get_save_filename()
        if not filename:
            return
        self.filename = filename
        self.filter = selected_filter
        self.last_dir = os.path.split(self.filename)[0]
        self.bt_save.setText(f"Save as {os.path.split(filename)[1]}")
        self._update_messages()
        self.save_file()

    def _update_messages(self):
        self.Error.no_file_name(
            shown=not self.filename and self.auto_save)
        self.Error.unsupported_sparse(
            shown=self.data is not None and self.data.is_sparse()
            and self.filename and not self.writer.SUPPORT_SPARSE_DATA)

    def _update_status(self):
        if self.data is None:
            self.info.set_input_summary(self.info.NoInput)
        else:
            self.info.set_input_summary(
                str(len(self.data)),
                f"Data set {self.data.name or '(no name)'} "
                f"with {len(self.data)} instances")

    def send_report(self):
        self.report_data_brief(self.data)
        writer = self.writer
        noyes = ["No", "Yes"]
        self.report_items((
            ("File name", self.filename or "not set"),
            ("Format", writer.DESCRIPTION),
            ("Type annotations",
             writer.OPTIONAL_TYPE_ANNOTATIONS
             and noyes[self.add_type_annotations])
        ))

    @classmethod
    def migrate_settings(cls, settings, version=0):
        def migrate_to_version_2():
            # Set the default; change later if possible
            settings.pop("compression", None)
            settings["filter"] = next(iter(cls.filters))
            filetype = settings.pop("filetype", None)
            if filetype is None:
                return

            ext = cls._extension_from_filter(filetype)
            if settings.pop("compress", False):
                for afilter in cls.filters:
                    if ext + ".gz" in afilter:
                        settings["filter"] = afilter
                        return
                # If not found, uncompressed may have been erroneously set
                # for a writer that didn't support if (such as .xlsx), so
                # fall through to uncompressed
            for afilter in cls.filters:
                if ext in afilter:
                    settings["filter"] = afilter
                    return

        if version < 2:
            migrate_to_version_2()

    def _initial_start_dir(self):
        if self.filename and os.path.exists(os.path.split(self.filename)[0]):
            return self.filename
        else:
            data_name = getattr(self.data, 'name', '')
            if data_name:
                data_name += self.writer.EXTENSIONS[0]
            return os.path.join(self.last_dir or self.userhome, data_name)

    @staticmethod
    def _replace_extension(filename, extension):
        """
        Remove all extensions that appear in any filter.

        Double extensions are broken in different weird ways across all systems,
        including omitting some, like turning iris.tab.gz to iris.gz. This
        function removes anything that can appear anywhere.
        """
        known_extensions = set()
        for filt in OWSave.filters:
            known_extensions |= \
                set(OWSave._extension_from_filter(filt).split("."))
        known_extensions.remove("")
        while True:
            base, ext = os.path.splitext(filename)
            if ext[1:] not in known_extensions:
                break
            filename = base
        return filename + extension

    @staticmethod
    def _extension_from_filter(selected_filter):
        return re.search(r".*\(\*?(\..*)\)$", selected_filter).group(1)

    def _valid_filters(self):
        if self.data is None or not self.data.is_sparse():
            return self.filters
        else:
            return {filt: writer for filt, writer in self.filters.items()
                    if writer.SUPPORT_SPARSE_DATA}

    def _default_valid_filter(self):
        if self.data is None or not self.data.is_sparse() \
                or self.filters[self.filter].SUPPORT_SPARSE_DATA:
            return self.filter
        for filt, writer in self.filters.items():
            if writer.SUPPORT_SPARSE_DATA:
                return filt
        # This shouldn't happen and it will trigger an error in tests
        return None   # pragma: no cover

    # As of Qt 5.9, QFileDialog.setDefaultSuffix does not support double
    # suffixes, not even in non-native dialogs. We handle each OS separately.
    if sys.platform in ("darwin", "win32"):
        # macOS and Windows native dialogs do not correctly handle double
        # extensions. We thus don't pass any suffixes to the dialog and add
        # the correct suffix after closing the dialog and only then check
        # if the file exists and ask whether to override.
        # It is a bit confusing that the user does not see the final name in the
        # dialog, but I see no better solution.
        def get_save_filename(self):  # pragma: no cover
            if sys.platform == "darwin":
                def remove_star(filt):
                    return filt.replace(" (*.", " (.")
            else:
                def remove_star(filt):
                    return filt

            no_ext_filters = {remove_star(f): f for f in self._valid_filters()}
            filename = self._initial_start_dir()
            while True:
                dlg = QFileDialog(
                    None, "Save File", filename, ";;".join(no_ext_filters))
                dlg.setAcceptMode(dlg.AcceptSave)
                dlg.selectNameFilter(remove_star(self._default_valid_filter()))
                dlg.setOption(QFileDialog.DontConfirmOverwrite)
                if dlg.exec() == QFileDialog.Rejected:
                    return "", ""
                filename = dlg.selectedFiles()[0]
                selected_filter = no_ext_filters[dlg.selectedNameFilter()]
                filename = self._replace_extension(
                    filename, self._extension_from_filter(selected_filter))
                if not os.path.exists(filename) or QMessageBox.question(
                        self, "Overwrite file?",
                        f"File {os.path.split(filename)[1]} already exists.\n"
                        "Overwrite?") == QMessageBox.Yes:
                    return filename, selected_filter

    else:  # Linux and any unknown platforms
        # Qt does not use a native dialog on Linux, so we can connect to
        # filterSelected and to overload selectFile to change the extension
        # while the dialog is open.
        # For unknown platforms (which?), we also use the non-native dialog to
        # be sure we know what happens.
        class SaveFileDialog(QFileDialog):
            # pylint: disable=protected-access
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.suffix = ""
                self.setAcceptMode(QFileDialog.AcceptSave)
                self.setOption(QFileDialog.DontUseNativeDialog)
                self.filterSelected.connect(self.updateDefaultExtension)

            def selectNameFilter(self, selected_filter):
                super().selectNameFilter(selected_filter)
                self.updateDefaultExtension(selected_filter)

            def updateDefaultExtension(self, selected_filter):
                self.suffix = OWSave._extension_from_filter(selected_filter)
                files = self.selectedFiles()
                if files and not os.path.isdir(files[0]):
                    self.selectFile(files[0])

            def selectFile(self, filename):
                filename = OWSave._replace_extension(filename, self.suffix)
                super().selectFile(filename)

        def get_save_filename(self):
            dlg = self.SaveFileDialog(
                None, "Save File", self._initial_start_dir(),
                ";;".join(self._valid_filters()))
            dlg.selectNameFilter(self._default_valid_filter())
            if dlg.exec() == QFileDialog.Rejected:
                return "", ""
            else:
                return dlg.selectedFiles()[0], dlg.selectedNameFilter()


if __name__ == "__main__":  # pragma: no cover
    WidgetPreview(OWSave).run(Table("iris"))
