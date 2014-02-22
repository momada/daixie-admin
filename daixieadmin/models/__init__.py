# -*- coding: utf-8 -*-

def enum(*sequential, **named):
    mapping = dict(zip(sequential, range(len(sequential))), **named)

    enums = {}
    enums['values'] = sorted(mapping.values())
    enums['reverse_mapping'] = dict((value, key) for key, value in mapping.iteritems())
    enums.update(mapping)

    return type('Enum', (), enums)