# Arch Mirrorlist Optimiser

This script reads your mirrorlist file, and times how long it takes to download a file.

It outputs a list of mirrors that successfully downloaded the file, in the order of download speed. This can then replace your mirrorlist file.

* ./sourcesoptimiser.py > ~/mirrorlist
* sudo cp ~/mirrorlist /etc/pacman.d/mirrorlist
* sudo pacman -Sc
* sudo pacman-key --refresh-keys
* sudo pacman -Syy
