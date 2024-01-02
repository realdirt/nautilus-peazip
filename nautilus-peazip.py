# PeaZip Nautilus Extension
#
# Place this script in ~/.local/share/nautilus-python/extensions/
# create the folders if they do not exist and make sure you have nautilus python installed

from gi.repository import Nautilus, GObject
from subprocess import call
from typing import List

def get_file_paths(files: List[Nautilus.FileInfo]) -> str:
    file_paths = ''
    for file in files:
        file_paths += '"' + file.get_location().get_path() + '" '
    return file_paths

class PeaZipExtension(GObject.GObject, Nautilus.MenuProvider):

    def peazip_call(self, menu: Nautilus.MenuItem, param: str, files: List[Nautilus.FileInfo]) -> None:
        call('flatpak run io.github.peazip.PeaZip ' + param + ' ' + get_file_paths(files) +'&', shell=True)
        pass

    def create_menu_entry(self, peazip_param: str, label: str, tip: str, files: List[Nautilus.FileInfo]):
        menu_item = Nautilus.MenuItem(name = 'PeaZipExtension::PeaZip' + label.replace(" ", ""), label = label, tip = tip)
        menu_item.connect('activate', self.peazip_call, peazip_param, files)
        return menu_item

    def get_file_items(self, files: List[Nautilus.FileInfo]) -> List[Nautilus.MenuItem]:
        peazip_topmenu = Nautilus.MenuItem(name = "PeaZipExtension::PeaZip", label = "PeaZip", tip = "Contains all PeaZip related entries")
        peazip_menu = Nautilus.Menu()
        peazip_topmenu.set_submenu(peazip_menu)

        # open
        peazip_menu.append_item(self.create_menu_entry('-ext2browse', 'Open archive', 'Open the selected archive(s)', files))

        # extraction
        peazip_menu.append_item(self.create_menu_entry('-ext2main', 'Extract archive', 'Open the "archive extraction" interface for the selected archive(s)', files))
        peazip_menu.append_item(self.create_menu_entry('-ext2here', 'Extract here', 'Extract the selected archive(s) to the current folder', files))
        peazip_menu.append_item(self.create_menu_entry('-ext2folder', 'Extract to folder smart', 'Extract the selected archive(s) to a new folder, but only if it contains more than one file', files))
        peazip_menu.append_item(self.create_menu_entry('-ext2newfolder', 'Extract to folder', 'Extract the selected archive(s) to a new folder', files))

        # test
        peazip_menu.append_item(self.create_menu_entry('-ext2test', 'Test archive', 'Test archive(s) content', files))

        # add
        peazip_menu.append_item(self.create_menu_entry('-add2archive', 'Add to archive', 'Add the selected file(s) to an archive', files))
        peazip_menu.append_item(self.create_menu_entry('-add2zip', 'Add to zip archive immediate', 'Add the selected file(s) to an zip archive immediately', files))

        return [peazip_topmenu]

    def get_background_items(self, current_folder: Nautilus.FileInfo) -> List[Nautilus.MenuItem]:
        return []