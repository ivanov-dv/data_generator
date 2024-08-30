from utils.file_creator import FileCreator
from utils.generator import PersonGenerator
from utils.packer import PackerZip, Packer7z
from utils.terminal import Terminal

person_generator = PersonGenerator()
packer_zip = PackerZip()
packer_7z = Packer7z()
file_creator = FileCreator()

terminal = Terminal(person_generator=person_generator, packer_zip=packer_zip, packer_7z=packer_7z,
                    file_creator=file_creator)

