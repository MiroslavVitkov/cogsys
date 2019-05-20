#!/usr/bin/env python3


def read_config(path):
    import configparser as c
    config = c.ConfigParser()
    with open(path, 'r', encoding='utf-8') as f:
        config.read_file(f)
    return config


def main():
    read_config('/home/vorac/proj/wac/clp-vision/Config/default.cfg')



if __name__ == '__main __':
    main()

