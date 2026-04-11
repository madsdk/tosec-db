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
    return None
