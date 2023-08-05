
import binascii
from importlib import import_module

from alnitak import prog as Prog

#
# /etc/alnitak.conf
#   [a.com]
#   tlsa = 311 25
#   [b.com]
#   tlsa = 211 443
#
# alnitak reset
# alnitak pre
#   -> append to datafile (create) with (a.com, b.com) in prog.target_list
# alnitak pre
#   -> append to datafile (<nothing>): nothing added.
# RENEWED_DOMAINS='a.com' alnitak deploy
#   -> remove b.com lines, add a.com posthook line
# alnitak pre
#   -> append (b.com) in prog.target_list: no 'a.com' lines added.
#          ^^^^
#   FIXME: This is a problem. As a binary file, we will end up writing
#           two headers. We could just open the file if it exists, confirm
#           the header and then skip the header. Opening any existing datafile
#           is probably a good idea since we currently just blindly append
#           when calling write_prehook.
#   TODO: read datafile:
#           if magic matches: append data without duplicating the header.
#           if magic mismatches: we _CANNOT_ write to another file since
#           the deploy mode will follow soon -- before the user can do
#           anything about it. Probably we should write our data first, and
#           then whatever the contents of the prev file was, even if it was
#           completely unrelated. When reading datafiles, we should ignore
#           all data after the EOF marker, even if there is data after it.
#           And, if 'deleting' the file, we need to just remove the alnitak
#           lines and leave the rest as it was before.



# A datafile group is divided into chunks
class DataGroup:
    def __init__(self):
        self.config = None
        self.prehook = None
        self.posthook = None
        self.delete = None

# This class is to be populated by reading a datafile (which is first
# created by the prehook mode call).
# A datafile is divided into groups
class DataFile:
    def __init__(self, major, minor, version, time):
        self.major = major
        self.minor = minor
        self.version = version
        self.time = time
        self.groups = []



def write_posthook(prog):
    return # FIXME

    data = make_header(prog)

    for g in prog.data.groups:
        data += make_posthook_group(prog, g)

    data += make_footer(len(prog.data.groups))

    with open('./d2.data', 'wb') as file:
        file.write(data)

    return Prog.RetVal.ok


def write_prehook(prog):
    # TODO: alnitak pre && alnitak pre
    #
    # first prehook call will write prehook lines as expected (and have
    # live -> archive). Second prehook call (since certs already at archive)
    # will not have populated prog.target_list, so the second call of this
    # function will rewrite the prev datafile with no data in it.
    #
    #

    # prog.target_list: [ Target... ]
    #   Target:
    #     - domain: "example.com"
    #     - certs: [ Cert... ]
    #         - dane
    #         - live
    #         - archive
    #     - tlsa: [ Tlsa... ]
    #         - usage
    #         - selector
    #         - matching
    #         - port
    #         - protocol
    #         - domain
    #     - api: (Api object)
    #         - key
    #         - email
    #         ---------
    #         - command
    #         - uid
    #         - gid


    data = make_header(prog)

    for t in prog.target_list:
        data += make_prehook_group(prog, t)

    data += make_footer(len(prog.target_list))

    with open('./d2.data', 'wb') as file:
        file.write(data)

    return Prog.RetVal.ok



def make_header(prog):
    '''Return the status file header.

    Return the header in the format:

      +-5-----+-1-----+-1-----+-N-----------+-1--+-8---------+-4---+
      | magic | major | minor | progversion | \0 | unix time | crc |
      +-------+-------+-------+-------------+----+-----------+-----+

    magic: (\xAC)ALNK
    major: \x00 (for example)
    minor: \x00 (for example)
    progversion: 0.0.1 (for example)
    unix time: \x00\x00\x00\x00\xF0\xE1\xD2\xC3 (for example)

    Args:
        prog (State): progrma state, containing the program data.

    Returns:
        bytes: return the header (including the checksum).
    '''
    header = b'\xACALNK' + prog.datafile_major + prog.datafile_minor \
              + prog.version.encode() + b'\x00' \
              + int('{0:%s}'.format(prog.timenow)).to_bytes(8, byteorder='big')
    checksum = binascii.crc32(header)
    return header + checksum.to_bytes(4, byteorder='big')

def make_chunk(id, data):
    '''Create a datafile chunk with specified ID.

    A chunk has the format:

    +-1--+-2------------+-N-------+-4--------+
    | id | data size, N | data... | checksum |
    +----+--------------+---------+----------+

    Args:
        id (bytes): the chunk ID.
        data (bytes): the data in the chunk.

    Returns:
        tuple (bytes, int): the status file chunk as a byte string
            (including the checksum), along with the checksum (as a positive
            integer).
    '''
    chunk = id + len(data).to_bytes(2, byteorder='big') + data
    checksum = binascii.crc32(chunk)
    return chunk + checksum.to_bytes(4, byteorder='big')

def make_group(domain, data):
    '''Create the datafile group with specified ID.

    The group format is:

    type(data) == bytes
    +-1------+-4-------+-M------+-1--+-N-M-1---+-4--------+
    | id (G) | size, N | domain | \0 | data... | checksum |
    +--------+---------+--------+----+---------+----------+
                       +---------- N ----------+

    Args:
        domain (bytes): the group domain.
        data (bytes): byte string to write, typically data chunks.

    Returns:
        bytes: the byte string to write (including the checksum).
    '''
    group = b'G' + (len(domain) + 1 + len(data)).to_bytes(4, byteorder='big') \
                 + domain + b'\x00' + data
    checksum = binascii.crc32(group)

    return group + checksum.to_bytes(4, byteorder='big')

def make_footer(num):
    '''Create file footer.

    The footer format is:

    +-1------+-2----------+-4--------+
    | id (E) | no. groups | checksum |
    +--------+------------+----------+

    Args:
        num (int): number of groups to write.

    Returns:
        bytes: the footer to write, including the checksum and a final newline.
    '''
    footer = b'E' + num.to_bytes(2, byteorder='big')
    checksum = binascii.crc32(footer)
    return footer + checksum.to_bytes(4, byteorder='big') + b'\n'


def make_prehook_group(prog, target):
    '''Create a group for a specific domain.

    Call 'make_group' to create a group, the data field containing:

    +--------------+---------------+
    | config chunk | prehook chunk |
    +--------------+---------------+

    Args:
        prog (State): the program state.
        target (Target): element of prog.target_list containing the data.

    Returns:
        bytes: the byte string of the group, including the checksum.
    '''
    # create config chunk
    data = make_config_chunk(prog, target)

    # create prehook chunk
    data += make_prehook_chunk(target)

    return make_group(target.domain.encode(), data)


def make_posthook_group(prog, group):
    # create config chunk

    # create prehook chunk

    # create posthook chunk

    # create delete chunk

    return


def make_config_chunk(prog, target):
    '''Create a 'config' chunk.

    Format for the data field is:

    +-1------------+-1----+-X-------+-1--+-----+-1----+-X-------+-1--+
    | param num, N | id_1 | value_1 | \0 | ... | id_N | value_N | \0 | ...
    +--------------+------+---------+----+-----+------+---------+----+

    +-2---------------+-W_1----+-----+-W_M----+-P---+
    | tlsa records, M | tlsa_1 | ... | tlsa_M | api |
    +-----------------+--------+-----+--------+-----+

    where 'id' can have values:
        'l' for prog.letsencrypt_directory (-C or config:letsencrypt_directory)
        'd' for prog.dane_directory (-D or config:dane_directory)
        't' for prog.ttl (-t or config:ttl)
        'w' for prog.log.level (-L or config:log_level)

    Args:
        prog (State): program state, containing the program config data.
        target (Target): element of prog.target_list containing the config
            file tlsa records and api scheme.

    Returns:
        bytes: return the data bytes (including the checksum).
    '''
    data = b'\x04' \
            + b'l' + str(prog.letsencrypt_directory).encode() + b'\x00' \
            + b'd' + str(prog.dane_directory).encode() + b'\x00' \
            + b't' + int(prog.ttl).to_bytes(4, byteorder='big') + b'\x00' \
            + b'w' + int(prog.log.level.value).to_bytes(1, byteorder='big') \
            + b'\x00' \
            + len(target.tlsa).to_bytes(2, byteorder='big')

    for t in target.tlsa:
        data += make_data_tlsa(t)

    data += make_data_api(target.api)

    return make_chunk(b'C', data)

def make_prehook_chunk(target):
    '''Make a 'prehook' chunk.

    Args:
        target (Target): element of prog.target_list.

    Returns:
        bytes: the chunk as a byte string (including the checksum).
    '''
    return make_chunk(b'p', make_certs_data(target))


def make_certs_data(target):
    '''Make a data block of the certs to be included in the prehook chunk.

    The data is in the format:

    +-1----------+-1---------+-X_1----+-1--+-Y_1----+-1--+-Z_1-------+-1--+
    | records, N | pending_1 | dane_1 | \0 | live_1 | \0 | archive_1 | \0 | ...
    +------------+-----------+--------+----+--------+----+-----------+----+

    +-----+-1---------+-X_N----+-1--+-Y_N----+-1--+-Z_N-------+-1--+
    | ... | pending_N | dane_N | \0 | live_N | \0 | archive_N | \0 |
    +-----+-----------+--------+----+--------+----+-----------+----+

    records: number of (archive, live, dane) certificate triplets.
    pending: \x01 (for pending '0'), \x10 (for pending '1')

    Args:
        target (Target): element of prog.target_list.

    Returns:
        bytes: the data as a byte string.
    '''
    data = len(target.certs).to_bytes(1, byteorder='big')

    for c in target.certs:
        data += b'\x01' \
                + str(c.dane).encode() + b'\x00' \
                + str(c.live).encode() + b'\x00' \
                + str(c.archive).encode() + b'\x00'

    return data

def make_data_tlsa(tlsa):
    '''Make a tlsa data block for a 'config' chunk.

    The format is:

    +-1----+-2----+-N--------+-1--+-M-----------+-1--+
    | spec | port | protocol | \0 | tlsa_domain | \0 |
    +------+------+----------+----+-------------+----+

    spec: the byte value is calculated as:
        (36 * usage) + (6 * selector) + (matching type).
        E.g., (usage, selector, matching type) = (3,1,1):
            spec value = 3*36 + 1*6 + 1 = 115

    Args:
        tlsa (Tlsa): object containing the TLSA data.

    Returns:
        bytes: the data block as a byte string.
    '''
    return (36*int(tlsa.usage) + 6*int(tlsa.selector)
                + int(tlsa.matching)).to_bytes(1, byteorder='big') \
            + int(tlsa.port).to_bytes(2, byteorder='big') \
            + tlsa.protocol.encode() + b'\x00' + tlsa.domain.encode() + b'\x00'

def make_data_api(api):
    '''Make an api data block for a 'config' chunk.

    Will call the 'write_datafile' functions in the API scheme's own api/
    file.

    Args:
        api (Api): object containing the API details.

    Returns:
        bytes: the byte string to write.
    '''
    apimod = import_module('alnitak.api.' + api.type.value)
    return apimod.write_datafile(api)


