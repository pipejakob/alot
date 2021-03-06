import sys
import os
HERE = os.path.dirname(__file__)
sys.path.append(os.path.join(HERE, '..', '..', '..'))
from alot.commands import COMMANDS
from configobj import ConfigObj
from validate import Validator
import re

def rewrite_entries(config, path, sec=None, sort=False):
    file = open(path, 'w')

    if sec == None:
        sec = config
    if sort:
        sec.scalars.sort()
    for entry in sec.scalars:
        v = Validator()
        #config.validate(v)
        #print config[entry]
        #etype = re.sub('\(.*\)','', config[entry])
        ##if etype == 'option':
        etype, eargs, ekwargs, default = v._parse_check(sec[entry])
        if default is not None:
            default = config._quote(default)

        #print etype
        description = '\n.. _%s:\n' % entry.replace('_', '-')
        description += '\n.. describe:: %s\n\n' % entry
        comments = [sec.inline_comments[entry]] + sec.comments[entry]
        for c in comments:
            if c:
                description += ' '*4 + re.sub('^\s*#\s*', '', c) + '\n'
        if etype == 'option':
            description += '\n    :type: option, one of %s\n' % eargs
        else:
            description += '\n    :type: %s\n' % etype

        if default != None:
            if etype in ['string', 'string_list'] and default != 'None':
                description += '    :default: `%s`\n\n' % (default)
            else:
                description += '    :default: %s\n\n' % (default)
        file.write(description)
    file.close()

if __name__ == "__main__":
    specpath = os.path.join(HERE, '..','..', 'alot', 'defaults', 'alot.rc.spec')
    config = ConfigObj(None, configspec=specpath, stringify=False, list_values=False)
    config.validate(Validator())

    alotrc_table_file = os.path.join(HERE, 'configuration', 'alotrc_table.rst')
    rewrite_entries(config.configspec, alotrc_table_file, sort=True)

    rewrite_entries(config, os.path.join(HERE, 'configuration',
                                         'accounts_table.rst'),
                    sec=config.configspec['accounts']['__many__'])
