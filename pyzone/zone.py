'''
Ctypes Wrapper around zone.h, zonecfg.h and partly zoneadm...

Tested on an OpenIndiana box.

Created on Jul 12, 2011

@author: tmetsch
'''

from ctypes import cdll, CDLL, c_char_p, Structure, c_ulonglong, c_int, \
    c_uint, byref, create_string_buffer, c_void_p, c_long, c_char, c_bool

cdll.LoadLibrary("libzonecfg.so.1")

LIBRARY = CDLL("libzonecfg.so.1")

STATES = {
    0: 'ZONE_IS_UNINITIALIZED',
    1: 'ZONE_IS_INITIALIZED',
    2: 'ZONE_IS_READY',
    3: 'ZONE_IS_BOOTING',
    4: 'ZONE_IS_RUNNING',
    5: 'ZONE_IS_SHUTTING_DOWN',
    6: 'ZONE_IS_EMPTY',
    7: 'ZONE_IS_DOWN',
    8: 'ZONE_IS_DYING',
    9: 'ZONE_IS_DEAD',
    None: 'UNKNOWN'  # added here to verify that nothing goes wrong...
}  # copied from zone_status_t in /usr/include/sys/zone.h

COMMANDS = {
            'Z_READY': 0,
            'Z_BOOT': 1,
            'Z_FORCEBOOT': 2,
            'Z_REBOOT': 3,
            'Z_HALT': 4,
            'Z_NOTE_UNINSTALLING': 5,
            'Z_MOUNT': 6,
            'Z_FORCEMOUNT': 7,
            'Z_UNMOUNT': 8
}  # copied from zone_cmd in /usr/src/uts/common/sys/zone.h


class ZoneCmdArg(Structure):
    '''
    Class to wrap the ZoneCmdArg struct.
    '''

    # disabling 'Too few public methods' check (not needed)
    # pylint: disable=R0903

    # defined in /usr/include/sys/zone.h

    _fields_ = [("uniqid", c_ulonglong),
                ("cmd", c_int),
                ("_pad", c_uint),
                ("locale", c_char_p),
                ("bootbut", c_char_p)]


def list_zones():
    '''
    Returns a dictionary {id:name} with the zones in STATES other than
    installed.
    '''
    zones = {}
    length = c_int(0)

    LIBRARY.zone_list(None, byref(length))
    int_array = c_int * length.value
    zids = int_array()
    LIBRARY.zone_list(byref(zids), byref(length))

    for ids in zids:
        name = create_string_buffer(64)  # ZONENAME_MAX = 64
        LIBRARY.getzonenamebyid(c_int(ids), byref(name), c_int(64))
        zones[ids] = name.value

    return zones


def get_state(zid):
    '''
    Returns the state a zone is in.

    zone -- Id of the zone.
    '''
    void_pointer = c_void_p()
    # attribute nr 3 is the state of the zone...
    LIBRARY.zone_getattr(c_int(zid), c_int(3), byref(void_pointer), c_long(1))
    return void_pointer.value, STATES[void_pointer.value]


def boot_zone(zid):
    '''
    Boot a zone.

    zid -- Id of the zone.
    '''
    if zid == 0:
        raise AttributeError('Cannot handle global zone...')
    elif get_state(zid) not in [(2, 'ZONE_IS_READY'), (7, 'ZONE_IS_DOWN')]:
        raise AttributeError('Zone needs to be in ready or down state')

    try:
        zonename = list_zones()[zid]
        call_zone_adm(zonename, 'Z_BOOT')
    except AttributeError as attribute_excection:
        raise AttributeError('Could not boot zone with id: ' + str(zid),
                             attribute_excection)


def halt_zone(zid, ready=True):
    '''
    Will halt the zone and put it in ready state (default).

    zid -- Id of the zone.
    ready -- Indicates if the zone should be set to ready state or not.
    '''
    if zid == 0:
        raise AttributeError('Cannot handle global zone...')
    elif get_state(zid) != (4, 'ZONE_IS_RUNNING'):
        raise AttributeError('Cannot halt zone which is not running...')

    try:
        zonename = list_zones()[zid]
        call_zone_adm(zonename, 'Z_HALT')
        if ready:
            call_zone_adm(zonename, 'Z_READY')
    except AttributeError as attribute_excection:
        raise AttributeError('Could not halt zone with id: ' + str(zid),
                             attribute_excection)


def shutdown_zone(zid):
    '''
    Will shutdown the zone an put it in down state.

    zid -- Id of the zone.
    '''
    # taken from zone.h
    if not LIBRARY.zone_shutdown(c_int(zid)) == 0:
        raise AttributeError('Something went wrong...')


def restart_zone(zid):
    '''
    Restart a zone

    zid -- Id of the zone.
    '''
    if zid == 0:
        raise AttributeError('Cannot handle global zone...')
    elif get_state(zid) != (4, 'ZONE_IS_RUNNING'):
        raise AttributeError('Cannot reboot a zone which is not running...')

    try:
        zonename = list_zones()[zid]
        call_zone_adm(zonename, 'Z_REBOOT')
    except AttributeError as attribute_excection:
        raise AttributeError('Could not reboot zone with id: ' + str(zid),
                             attribute_excection)


def ready_zone(zid):
    '''
    Brings a zone into ready state.

    zid -- Id of the zone.
    '''
    if zid == 0:
        raise AttributeError('Cannot handle global zone...')

    try:
        zonename = list_zones()[zid]
        call_zone_adm(zonename, 'Z_READY')
    except AttributeError as attribute_excection:
        raise AttributeError('Could not ready zone with id: ' + str(zid),
                             attribute_excection)


def call_zone_adm(zonename, cmd):
    '''
    Call COMMANDS on zoneadmd...

    zonename -- Name of the zone.
    cmd -- Name of the cmd.
    '''
    if cmd not in COMMANDS.values() and cmd not in COMMANDS.keys():
        raise AttributeError('Unknown command...')

    if isinstance(cmd, int):
        zarg = ZoneCmdArg(cmd)
    else:
        zarg = ZoneCmdArg(COMMANDS[cmd])

    if not LIBRARY.zonecfg_call_zoneadmd(zonename, byref(zarg),
                                         byref(c_char('C')), c_bool(0)) == 0:
        raise AttributeError('Something went wrong...')
