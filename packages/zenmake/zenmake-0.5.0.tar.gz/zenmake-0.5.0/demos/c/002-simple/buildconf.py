
tasks = {
    'test' : {
        'features' : 'c cprogram',
        'source'   : 'test.c util.c',
        'includes' : '.',
    },
}

buildtypes = {
    'debug' : {
        'toolchain' : 'auto-c',
    },
    'default' : 'debug',
}

