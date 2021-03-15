#!/usr/bin/env python3

from xml.dom.minidom import parse
import sys
import re
import os
import sqlite3
import argparse
import uuid

tosec_system = ['+2','+2a','+3','130XE','A1000','A1200','A1200-A4000','A2000','A2000-A3000','A2024','A2500-A3000UX','A3000','A4000','A4000T','A500','A500+','A500-A1000-A2000','A500-A1000-A2000-CDTV','A500-A1200','A500-A1200-A2000-A4000','A500-A2000','A500-A600-A2000','A570','A600','A600HD','AGA','AGA-CD32','Aladdin Deck Enhancer','CD32','CDTV','Computrainer','Doctor PC Jr.','ECS','ECS-AGA','Executive','Mega ST','Mega-STE','OCS','OCS-AGA','ORCH80','Osbourne 1','PIANO90','PlayChoice-10','Plus4','Primo-A','Primo-A64','Primo-B','Primo-B64','Pro-Primo','ST','STE','STE-Falcon','TT','TURBO-R GT','TURBO-R ST','VS DualSystem','VS UniSystem']
tosec_video = ['CGA','EGA','HGC','MCGA','MDA','NTSC','NTSC-PAL','PAL','PAL-60','PAL-NTSC','SVGA','VGA','XGA']
tosec_country = ['AE','AL','AS','AT','AU','BA','BE','BG','BR','CA','CH','CL','CN','CS','CY','CZ','DE','DK','EE','EG','ES','EU','FI','FR','GB','GR','HK','HR','HU','ID','IE','IL','IN','IR','IS','IT','JO','JP','KR','LT','LU','LV','MN','MX','MY','NL','NO','NP','NZ','OM','PE','PH','PL','PT','QA','RO','RU','SE','SG','SI','SK','TH','TR','TW','US','VN','YU','ZA']
tosec_dev_status = ['alpha','beta','preview','pre-release','proto']
tosec_media = ['Disc','Disk','File','Part','Side','Tape']
tosec_copyright = ['CW','CW-R','FW','GW','GW-R','LW','PD','SW','SW-R']
tosec_dump_flags = ['cr','tr','f','h','m','p','t','o','u','v','b','a','!']

def parse_tosec_name(tosec_name):
    # Title version (demo) (Date)(Publisher)(System)(Video)(Country)(Language)(Copyright)(Devstatus)(Media Type)(Media Label)[cr][f][h][m][p][t][tr][o][u][v][b][a][!][more info]
    # Search for the date, anything before that is the full name and possibly a demo tag.
    date_regexp = re.compile(r'\(((19|20)[x0-9][x0-9](\-[x0-9][x0-9](\-[x0-9][x0-9])?)?)\)')
    m = date_regexp.search(tosec_name)
    if m is None:
        print('Invalid TOSEC name "{}" found. Cannot find date.'.format(tosec_name))
        return None
    title = tosec_name[:m.start()]
    if len(title) == 0:
        print('Invalid TOSEC name "{}" found. Title is empty.'.format(tosec_name))
        return None

    title = title.strip()
    date = m.group(1)

    # The next token is the publisher.
    rest = tosec_name[m.end():]
    if rest[0] != '(':
        print('Invalid TOSEC name "{}" found. No publisher found.'.format(tosec_name))
        return None
    i = rest.find(')')
    if i == -1:
        print('Invalid TOSEC name "{}" found. No publisher found.'.format(tosec_name))
        return None
    publisher = rest[1:i]
    info = {'title':title, 'date':date, 'publisher':publisher}

    # The rest are optional. Start by grabbing any tokens within parenteses. 
    rest = rest[i+1:]
    token_regexp = re.compile(r'\(([^\(\)]+)\)')
    m = token_regexp.match(rest)
    while not m is None:
        for group in m.groups():
            if group in tosec_system:
                info['system'] = group
            if group in tosec_video:
                info['video'] = group
            tokens = group.split('-')
            all_countries = True
            for token in tokens:
                if not token in tosec_country:
                    all_countries = False
            if all_countries:
                info['country'] = group 
            if group in tosec_dev_status:
                info['dev_status'] = group
            if group[:4] in tosec_media:
                info['media'] = group
            if group in tosec_copyright:
                info['copyright'] = group
        rest = rest[m.end():]
        m = token_regexp.match(rest)

    # Read dump info flags.
    token_regexp = re.compile(r'\[([^\[\]]+)\]')
    info['tags'] = []
    info['full_tags'] = []
    m = token_regexp.match(rest)
    while not m is None:
        for group in m.groups():
            info['full_tags'].append(group)
            dump_flag = group.split(' ')[0]
            for flag in tosec_dump_flags:
                if dump_flag[:len(flag)] == flag:
                    info['tags'].append(flag)

        rest = rest[m.end():]
        m = token_regexp.match(rest)

    return info
    
def get_text_value(node):
    text_nodes = []
    for child in node.childNodes:
        if child.nodeType == child.TEXT_NODE:
            text_nodes.append(child)
    return ' '.join([str.strip(t.nodeValue) for t in text_nodes])

def typecheck_dir(path):
    if not os.path.isdir(path):
        print(f'The path {path} does not point to a directory.')
        raise ValueError()
    return path

def typecheck_file(path):
    if not os.path.exists(path) and os.access(path, os.R_OK):
        print(f'The path {path} does not point to a readable file.')
        raise ValueError()
    return path

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dbfile', help='The SQLite database file.')
    parser.add_argument('--system',dest='system', help='The system specifier string, e.g. "Amiga"', required=False)
    parser.add_argument('--folder', dest='folder', help='The file system path to scan for TOSEC ROM files.', required=False, type=typecheck_dir)
    parser.add_argument('--datfile', dest='datfile', help='The file system path to a TOSEC dat file.', required=False, type=typecheck_file)
    args = parser.parse_args()
    
    # Folder and system are dependant on each other.
    if args.folder is not None:
        if args.system is None:
            print('If you use the --folder argument you must provide the --system argument as well.')
            sys.exit(1)
    if args.system is not None:
        if args.folder is None:
            print('If you use the --system argument you must provide the --folder argument as well.')
            sys.exit(1)

    # We must have either --folder or --datfile, not both.
    mode = None
    if args.folder is not None:
        if args.datfile is not None:
            print('Arguments --folder and --datfile cannot be used together.')
            sys.exit(1)
        mode = 'folder'
    elif args.datfile is not None:
        mode = 'datfile'
    else:
        print('One of --folder or --datfile must be used.')
        sys.exit(1)

    # Assign the arguments to sensible named variables.
    dbfile = args.dbfile
    
    # Connect to the database.
    try: 
        conn = sqlite3.connect(dbfile)
    except Exception:
        print('Error opening database file.')
        sys.exit(1)

    # Make sure the tables are there.
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT,
            title TEXT,
            date TEXT,
            publisher TEXT,
            system TEXT,
            video TEXT,
            country TEXT,
            dev_status TEXT,
            media TEXT,
            copyright TEXT,
            uuid TEXT
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS tags (
            game_id INTEGER,
            tag TEXT,
            uuid TEXT
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS fulltags (
            game_id INTEGER,
            tag TEXT,
            uuid TEXT
        )''')
    except Exception as e:
        print('DB while creating tables error: {}'.format(str(e)))
        sys.exit(1)
    
    if mode == 'folder':
        platform = args.system

        try:
            entries = os.listdir(args.folder)
        except Exception:
            print('Error reading directory contents.')
            sys.exit(1)

        for entry in entries:
            info = parse_tosec_name(entry)
            _uuid = str(uuid.uuid4())
            print(type(info['title']))
            if not info is None:
                try:
                    c.execute('INSERT INTO games (platform, title, date, publisher, system, video, country, dev_status, media, copyright, uuid) VALUES(?,?,?,?,?,?,?,?,?,?,?)',\
                        (platform, info['title'], info['date'], info['publisher'], info['system'] if 'system' in info else '', info['video'] if 'video' in info else '', info['country'] if 'country' in info else '', info['dev_status'] if 'dev_status' in info else '', info['media'] if 'media' in info else '', info['copyright'] if 'copyright' in info else '', _uuid))
                    game_id = c.lastrowid
                    c.executemany('INSERT INTO tags (game_id, tag, uuid) VALUES (?,?,?)', [(game_id, x, _uuid) for x in info['tags']])
                    c.executemany('INSERT INTO fulltags (game_id, tag) VALUES (?,?,?)', [(game_id, x, _uuid) for x in info['full_tags']])
                except Exception as e:
                    print('Database error while inserting data: {}'.format(str(e)))
                    sys.exit(1)
        conn.commit()

    else:
        datfile = args.datfile

        print(f'Processing file {datfile}.')
        try:
            dom = parse(datfile)
        except:
            print(f'Error parsing XML file {datfile}.')
            sys.exit(1)

        header = dom.getElementsByTagName('header')
        if len(header) != 1:
            print('Invalid or no header information found in dat file.')
            sys.exit(1)
        header_name = header[0].getElementsByTagName('name')
        if len(header_name) != 1:
            print('Invalid header information found in dat file. No name tag.')
            sys.exit(1)
        platform = get_text_value(header_name[0])

        games = dom.getElementsByTagName('game')
        for game in games:
            info = parse_tosec_name(game.getAttribute('name'))
            rom = game.getElementsByTagName('rom')[0]
            print('Name: %s, Size: %s, CRC: %s' % (rom.getAttribute('name'), rom.getAttribute('size'), rom.getAttribute('crc')))
            if not info is None:
                _uuid = str(uuid.uuid4())
                try:
                    c.execute('INSERT INTO games (platform, title, date, publisher, system, video, country, dev_status, media, copyright, uuid) VALUES(?,?,?,?,?,?,?,?,?,?,?)',\
                        (platform, info['title'], info['date'], info['publisher'], info['system'] if 'system' in info else '', info['video'] if 'video' in info else '', info['country'] if 'country' in info else '', info['dev_status'] if 'dev_status' in info else '', info['media'] if 'media' in info else '', info['copyright'] if 'copyright' in info else '', _uuid))
                    game_id = c.lastrowid
                    c.executemany('INSERT INTO tags (game_id, tag, uuid) VALUES (?,?,?)', [(game_id, x, _uuid) for x in info['tags']])
                    c.executemany('INSERT INTO fulltags (game_id, tag, uuid) VALUES (?,?,?)', [(game_id, x, _uuid) for x in info['full_tags']])
                except Exception as e:
                    print('Database error while inserting data: {}'.format(str(e)))
                    sys.exit(1)
            else:
                print(f'Error parsing TOSEC name "{game.getAttribute("name")}')
        conn.commit()

    sys.exit(0)
