#!/usr/bin/env python3


def read_config(path):
    import configparser as c
    config = c.ConfigParser()
    with open(path, 'r', encoding='utf-8') as f:
        config.read_file(f)
    return config


def load_wac(config, sempix_path):
    h = config.get('DSGV-PATHS', 'dsgv_home')
    import sys
    sys.path.append(h + '/Utils')
    import utils
    sys.path.append(h + '/WACs/WAC_Utils')
    import wac_utils
    sys.path.append('/Users/das/work/svn/Gits/p_Public/sempix/Common')
    import data_utils

    # I have zero idea why are we doing the following.
    # It's just the way the original Jupiter Notebook is written.
    from importlib import reload
    reload(wac_utils)

    return utils, wac_utils, data_utils


def main():
    config = read_config('/home/vorac/proj/wac/clp-vision/Config/default.cfg')
    utils, wac_utils, data_utils = load_wac(config, '/home/vorac/proj/wac/sempix/Common')



if __name__ == '__main __':
    main()

