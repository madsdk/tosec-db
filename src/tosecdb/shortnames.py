def get_platform_short_name(full_name: str) -> str | None:
    """
    Extracts the short name of a platform from its full TOSEC name.
    """
    if "C64" in full_name:
        return "Commodore 64"
    if "C16" in full_name:
        return "Commodore 16"
    if "VIC20" in full_name:
        return "Commodore VIC20"
    if "C128" in full_name:
        return "Commodore 128"
    if "PET" in full_name:
        return "Commodore PET"
    if "CD32" in full_name:
        return "Commodore CD32"
    if "CDTV" in full_name:
        return "Commodore CDTV"
    if "Amiga" in full_name:
        return "Commodore Amiga"
    if "CPC" in full_name:
        return "Amstrad CPC"
    if "Atari 2600" in full_name:
        return "Atari 2600"
    if "Atari 5200" in full_name:
        return "Atari 5200"
    if "Atari 7800" in full_name:
        return "Atari 7800"
    if "Atari Lynx" in full_name:
        return "Atari Lynx"
    if "Atari Jaguar" in full_name:
        return "Atari Jaguar"
    if "Atari ST" in full_name:
        return "Atari ST"
    if "Atari 8bit" in full_name:
        return "Atari 8bit"
    if "Apple III" in full_name:
        return "Apple III"
    if "Apple IIGS" in full_name:
        return "Apple IIGS"
    if "Apple II" in full_name:
        return "Apple II"
    if "Apple Macintosh" in full_name:
        return "Apple Macintosh"
    if "ZX Spectrum" in full_name:
        return "Sinclair ZX Spectrum"
    if "ZX80" in full_name:
        return "Sinclair ZX80"
    if "ZX81" in full_name:
        return "Sinclair ZX81"
    if "TRS-80 Color Computer" in full_name:
        return "TRS-80 CoCo"
    if "TRS-80 Model I" in full_name:
        return "TRS-80 Model I"
    if "TRS-80 Model III" in full_name:
        return "TRS-80 Model III"
    if "TRS-80 Model 4" in full_name:
        return "TRS-80 Model 4"
    if "TI-99 4A" in full_name:
        return "TI-99/4A"
    if "X68000" in full_name:
        return "Sharp X68000"
    if "Sega Mega Drive" in full_name:
        return "Sega Mega Drive"
    if "Master System" in full_name:
        return "Sega Master System"
    if "Game Gear" in full_name:
        return "Sega Game Gear"
    if "Sega 32X" in full_name:
        return "Sega 32X"
    if "Neo-Geo Pocket Color" in full_name:
        return "Neo-Geo Pocket Color"
    if "Neo-Geo Pocket" in full_name:
        return "Neo-Geo Pocket"
    if "Neo-Geo CD" in full_name:
        return "Neo-Geo CD"
    if "Neo-Geo" in full_name:
        return "Neo-Geo"
    if "Nintendo Virtual Boy" in full_name:
        return "Nintendo Virtual Boy"
    if "Nintendo Super Famicom" in full_name:
        return "SNES"
    if "Nintendo Famicom Disk System" in full_name:
        return "Famicom Disk System"
    if "Nintendo Famicom" in full_name:
        return "NES"
    if "Nintendo Game Boy Color" in full_name:
        return "Game Boy Color"
    if "Nintendo Game Boy Advance" in full_name:
        return "Game Boy Advance"
    if "Nintendo Game Boy" in full_name:
        return "Game Boy"
    if "Nintendo 64DD" in full_name:
        return "Nintendo 64DD"
    if "Nintendo 64" in full_name:
        return "Nintendo 64"
    if "Commander X16" in full_name:
        return "Commander X16"
    if "Acorn Archimedes" in full_name:
        return "Acorn Archimedes"
    if "Acorn Atom" in full_name:
        return "Acorn Atom"
    if "Acorn BBC" in full_name:
        return "Acorn BBC"
    if "Acorn Electron" in full_name:
        return "Acorn Electron"
    if "Applied Technology MicroBee" in full_name:
        return "MicroBee"
    if "Arduboy" in full_name:
        return "Arduboy"
    if "Bally Professional Arcade" in full_name:
        return "Bally"
    if "Bandai Gundam" in full_name:
        return "Bandai Gundam"
    if "Brother WP-230B, 330MDS & 335B" in full_name:
        return "Brother WP-230B/330MDS/335B"
    if "Cambridge Computer Z88" in full_name:
        return "Cambridge Z88"
    if "Camputers Lynx" in full_name:
        return "Camputers Lynx"
    if "Casio FP-1000 & FP-1100" in full_name:
        return "Casio FP-1000/1100"
    if "Casio Loopy" in full_name:
        return "Casio Loopy"
    if "Coleco ColecoVision ADAM" in full_name:
        return "Coleco ADAM"
    if "DEC PDP-1 " in full_name:
        return "DEC PDP-1"
    if "DEC PDP-11" in full_name:
        return "DEC PDP-11"
    if "DEC PDP-8" in full_name:
        return "DEC PDP-8"
    if "Dragon Data Dragon" in full_name:
        return "Dragon 32"
    if "EACA EG2000 Colour Genie" in full_name:
        return "EACA EG2000"
    if "Elektronska Industrija Nis PECOM 32 & 64" in full_name:
        return "PECOM 32/64"
    if "Enterprise 64 & 128" in full_name:
        return "Enterprise 64/128"
    if "Exelvision EXL100" in full_name:
        return "Exelvision EXL100"
    if "Exelvision Exeltel" in full_name:
        return "Exelvision Exeltel"
    if "Exidy Sorcerer" in full_name:
        return "Exidy Sorcerer"
    if "Fujitsu FM Towns" in full_name:
        return "FM Towns"
    if "Fujitsu FM-7" in full_name:
        return "FM-7"
    if "Fujitsu FM77-AV" in full_name:
        return "FM77-AV"
    if "Galaksija" in full_name:
        return "Galaksija"
    if "Game Park GP32" in full_name:
        return "Game Park GP32"
    if "IBM PC Compatibles" in full_name:
        return "IBM PC"
    if "IBM PCjr" in full_name:
        return "IBM PCjr"
    if "MSX MSX " in full_name:
        return "MSX"
    if "MSX MSX2" in full_name:
        return "MSX2"
    if "NEC PC-6001" in full_name:
        return "NEC PC-6001"
    if "NEC PC-8001" in full_name:
        return "NEC PC-8001"
    if "NEC PC-8801" in full_name:
        return "NEC PC-8801"
    if "NEC PC-88VA" in full_name:
        return "NEC PC-88VA"
    if "NEC PC-9801" in full_name:
        return "NEC PC-9801"
    if "NEC PC-9821" in full_name:
        return "NEC PC-9821"
    if "Luxor ABC 80 " in full_name:
        return "Luxor ABC 80"
    if "Luxor ABC 800" in full_name:
        return "Luxor ABC 800"
    if "MGT Sam Coupe" in full_name:
        return "Sam Coupe"
    if "DAI Personal Computer" in full_name:
        return "DAI"
    if "Hanimex Pencil II" in full_name:
        return "Hanimex Pencil II"
    if "Hector 2HR" in full_name:
        return "Hector 2HR"
    if "Hitachi Basic Master Jr." in full_name:
        return "Hitachi Basic Master Jr."
    if "Hitachi S1" in full_name:
        return "Hitachi S1"
    if "IMLAC Corporation PDS-1" in full_name:
        return "IMLAC PDS-1"
    if "Jupiter Cantab Jupiter Ace" in full_name:
        return "Jupiter Ace"
    if "Kaypro II" in full_name:
        return "Kaypro II"
    if "MEGA MEGA65" in full_name:
        return "MEGA65"
    if "MITS Altair 8800" in full_name:
        return "Altair 8800"
    if "Matra Hachette Alice 32" in full_name:
        return "Matra Alice 32"
    if "Matsushita JR-100" in full_name:
        return "Matsushita JR-100"
    if "Matsushita JR-200" in full_name:
        return "Matsushita JR-200"
    if "Mattel Aquarius" in full_name:
        return "Mattel Aquarius"
    if "Memotech MTX" in full_name:
        return "Memotech MTX"
    if "Microkey Primo" in full_name:
        return "Microkey Primo"
    if "Mitsubishi Multi 8" in full_name:
        return "Mitsubishi Multi 8"
    if "NCR Decision Mate V" in full_name:
        return "NCR Decision Mate V"
    if "Nascom I & II" in full_name:
        return "Nascom"
    if "Nichibutsu My Vision" in full_name:
        return "Nichibutsu My Vision"
    if "Nintendo Family BASIC" in full_name:
        return "Nintendo Family BASIC"
    if "OCC Osborne 1" in full_name:
        return "Osborne"
    if "Otrona Attache" in full_name:
        return "Otrona Attache"
    if "Philips VG 5000" in full_name:
        return "Philips VG 5000"
    if "Pokitto Oy Pokitto" in full_name:
        return "Pokitto"
    if "Pravetz 8D" in full_name:
        return "Pravetz 8D"
    if "Regnecentralen RC 700" in full_name:
        return "RC 700"
    if "Robotron BIC A5105" in full_name:
        return "Robotron A5105"
    if "Sanyo MBC-550" in full_name:
        return "Sanyo MBC-550/555"
    if "Sega Computer 3000" in full_name:
        return "Sega Computer 3000"
    if "Sharp MZ-80B" in full_name:
        return "Sharp MZ-80B"
    if "Sharp S-BASIC" in full_name:
        return "Sharp S-BASIC"
    if "Sony SMC-777" in full_name:
        return "Sony SMC-777"
    if "Sord M5" in full_name:
        return "Sord M5"
    if "Spectravideo SVI-318" in full_name:
        return "Spectravideo SVI-318/328"
    if "Tangerine Microtan 65" in full_name:
        return "Microtan 65"
    if "Tangerine Oric Telestrat" in full_name:
        return "Oric Telestrat"
    if "Tatung Einstein TC-01" in full_name:
        return "Tatung Einstein"
    if "Tesla Ondra Vili" in full_name:
        return "Tesla Ondra Vili"
    if "Tesla PMD 85" in full_name:
        return "Tesla PMD 85"
    if "Thomson TO8" in full_name:
        return "Thomson TO8/TO9"
    if "Toshiba Pasopia 7" in full_name:
        return "Toshiba Pasopia 7"
    if "Toshiba Pasopia" in full_name:
        return "Toshiba Pasopia"
    if "VTech V.Smile Motion" in full_name:
        return "VTech V.Smile Motion"
    if "VTech V.Smile" in full_name:
        return "VTech V.Smile"
    if "Victor Technologies Victor 9000" in full_name:
        return "Victor 9000"
    if "Videoton TV-Computer" in full_name:
        return "Videoton TV-Computer"
    if "Mattel Intellivision ECS" in full_name:
        return "Intellivision ECS"
    if "Mattel Intellivision" in full_name:
        return "Intellivision"
    if "Nokia N-Gage" in full_name:
        return "Nokia N-Gage"
    if "RCA Studio II" in full_name:
        return "RCA Studio II"
    if "Sharp MZ-2000" in full_name or "Sharp MZ-2200" in full_name:
        return "Sharp MZ-2000"
    if "Sharp MZ-800" in full_name or "Sharp MZ-1500" in full_name:
        return "Sharp MZ-800"
    if "Sharp MZ-700" in full_name:
        return "Sharp MZ-700"
    if "Sharp X1" in full_name:
        return "Sharp X1"
    if "Sinclair QL" in full_name:
        return "Sinclair QL"
    if "TRS-80 MC-10" in full_name:
        return "TRS-80 MC-10"
    if "TRS-80 Model 100" in full_name:
        return "TRS-80 Model 100"
    if "Tangerine Oric-1" in full_name or "Tangerine Oric Atmos" in full_name:
        return "Oric"
    if "Thomson MO5" in full_name:
        return "Thomson MO5"
    if "Thomson TO7" in full_name:
        return "Thomson TO7"
    if "VTech Laser 350" in full_name:
        return "VTech Laser 350/500/700/750"
    if "VTech Laser 200" in full_name:
        return "VTech Laser 200"

    return None
