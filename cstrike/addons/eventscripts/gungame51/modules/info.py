# ../modules/info.py

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame Imports
from gungame51.core import GunGameInfo as info


# =============================================================================
# >> ADDON REGISTRATION
# =============================================================================
info.About = ('\n' +
                '\t' * 4 + 'GunGame 5.1 (v%s)\n\n' % info.version)

info.Authors = ('\n' +
             '\t' * 4 + 'Michael Barr (XE_ManUp)\n' +
             '\t' * 4 + 'Luke Robinson (Monday)\n' +
             '\t' * 4 + 'Warren Alpert\n' +
             '\t' * 4 + 'Paul Smith (RideGuy)\n' +
             '\t' * 4 + 'Deniz Sezen (your-name-here)\n' +
             '\t' * 4 + 'Stephen Toon (satoon101)\n\n')

info.Website = ('\n' + '\t' * 4 + 'http://forums.gungame.net/\n')


# =============================================================================
# >> CLASSES
# =============================================================================
class Credits(dict):
    def __init__(self):
        self.order = []

    def __setitem__(self, item, value):
        self.order.append(item)
        super(Credits, self).__setitem__(item, value)

# =============================================================================
# >> GG THANKS
# =============================================================================
# Credits used for the !thanks command
credits = Credits()
credits['Core Team'] = ['XE_ManUp',
                        'cagemonkey',
                        'Warren Alpert',
                        'your-name-here',
                        'Monday',
                        'RideGuy',
                        'satoon101']

credits['Contributers'] = ['llamaelite']

credits['Beta Testers'] = ['Sir_Die',
                            'pyro',
                            'D3X',
                            'nad',
                            'Knight',
                            'Evil_SNipE',
                            'k@rma',
                            'tnarocks',
                            'Warbucks',
                            'daggersarge']

credits['Special Thanks'] = ['gameservers.pro',
                            'Predator',
                            'tnb=[porsche]911',
                            'RG3 Community',
                            "L'In20Cible",
                            'counter-strike.com',
                            'The Cheebs']
