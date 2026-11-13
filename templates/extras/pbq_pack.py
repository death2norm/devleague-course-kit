# PBQ Practice Pack source: one add() per PBQ (about 10). Format: see tools/build_pbq_pack.py.
# Example item kept from Network+; replace with the course's own. Never copy a Session 17 workshop PBQ or a practice-bank item.
COMPANY = '<Company> is a fictional company'

add(id='P01', obj='1.7', title='Whose subnet is it?', minutes=6,
    intro='The Harbor Point help desk pulled seven addresses from device configs. For each one, drag the network address of the subnet it belongs to (group 1) and what the address is inside that subnet (group 2).',
    header=['Address and prefix', 'Network address', 'The address is the...'],
    rows=[['172.18.45.130/26', '[[1:172.18.45.128]]', '[[2:Usable host address]]'],
          ['172.18.45.191/26', '[[1:172.18.45.128]]', '[[2:Broadcast address]]'],
          ['10.4.66.0/23', '[[1:10.4.66.0]]', '[[2:Network address]]'],
          ['10.4.67.0/23', '[[1:10.4.66.0]]', '[[2:Usable host address]]'],
          ['10.4.67.255/23', '[[1:10.4.66.0]]', '[[2:Broadcast address]]'],
          ['192.168.9.17/28', '[[1:192.168.9.16]]', '[[2:Usable host address]]'],
          ['192.168.9.32/27', '[[1:192.168.9.32]]', '[[2:Network address]]']],
    extras={'1': ['172.18.45.0', '10.4.67.0', '192.168.9.0']},
    explain='Find the block size from the prefix, then the multiple of it at or below the address. /26 is blocks of 64 in the last octet: 130 and 191 fall in 128-191, so the network is .128 and .191 is its broadcast. /23 is blocks of 2 in the third octet: 66 and 67 both belong to 10.4.66.0/23 (10.4.66.0-10.4.67.255), so 10.4.67.0 is an ordinary host in the middle and 10.4.67.255 is the broadcast. /28 is blocks of 16: 17 is in 16-31. /27 is blocks of 32: .32 is the first address of 32-63, the network address. The trap is 10.4.67.0: it ends in .0 but is not a network address with a /23.')

