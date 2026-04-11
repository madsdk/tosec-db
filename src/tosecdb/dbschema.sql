-- Platform table
create table if not exists platform (
    id serial primary key,
    name varchar(128) not null unique,
    short_name varchar(32),
    format varchar(8)
);

-- Game table
create table if not exists game (
    id serial primary key,
    name varchar(256) not null,
    date varchar(16) not null,
    publisher varchar(128) not null
);

-- Gameversion table
create table if not exists gameversion (
    id serial primary key,
    name varchar(256) not null,
    demo boolean not null,
    system varchar(64),
    video varchar(64),
    country varchar(32),
    language varchar(32),
    dev_status varchar(16),
    media varchar(32),
    copyright varchar(4),
    cracked boolean default false,
    fixed boolean default false,
    hacked boolean default false,
    modified boolean default false,
    pirated boolean default false,
    trained boolean default false,
    translated boolean default false,
    overdumped boolean default false,
    underdumped boolean default false,
    virus boolean default false,
    baddump boolean default false,
    alternate boolean default false,
    verified boolean default false,
    platform_id integer not null references platform(id) on delete cascade,
    game_id integer not null references game(id) on delete cascade,
    rom_count integer not null
);

-- ROM table
create table if not exists rom (
    id serial primary key,
    name varchar(256) not null,
    gameversion_id integer not null references gameversion(id) on delete cascade,
    size integer not null,
    crc32 varchar(8) not null,
    md5 varchar(32) not null,
    sha1 varchar(40) not null
);

create index if not exists idx_rom_crc32 on rom(crc32);
create index if not exists idx_rom_md5 on rom(md5);
create index if not exists idx_rom_sha1 on rom(sha1);
