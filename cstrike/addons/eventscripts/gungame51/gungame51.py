import es

def load():
    testConfigs()
    testDependencies()
    testAddonClass()
    testDependencyDenial()

def testConfigs():
    # Load, create, and excute all GunGame configs
    import core.cfg.files
    reload(core.cfg.files)
    
def testDependencies():
    from core.addons.addons import DependencyManager
    
    myAddon = DependencyManager('gg_deathmatch')
    myAddon.gg_deathmatch = 5
    if myAddon.gg_deathmatch == 5:
        es.dbgmsg(0, 'PASSED: Set gg_deathmatch to %s using attributes.' %myAddon.gg_deathmatch)
    else:
        es.dbgmsg(0, 'FAILED: Unable to set gg_deathmatch to using attributes.')
    es.dbgmsg(0, myAddon.gg_deathmatch)
    
def testAddonClass():
    from core.addons.addons import AddonManager
    
    myAddon = AddonManager('gg_deathmatch', displayName='Deathmatch', dependencyDict={'gg_turbo':1, 'gg_elimination':0})
    es.dbgmsg(0, 'Display Name: %s' %myAddon.displayName)
    
    from core.addons.addons import DependencyManager
    
    myAddon = DependencyManager('gg_deathmatch')
    
    es.dbgmsg(0, 'gg_turbo dependency = %s' %myAddon.gg_turbo)
    es.dbgmsg(0, 'gg_elimination dependency = %s' %myAddon.gg_elimination)

    # Testing Error Code
    #es.dbgmsg(0, 'gg_knife_pro dependency = %s' %myAddon.gg_knife_pro)
    
def testDependencyDenial():
    from core.addons.addons import DependencyManager
    myAddon = DependencyManager('gg_elimination')
    
    from core.addons.addons import dependencies
    
    if len(dependencies) == 1:
        es.dbgmsg(0, 'PASSED: gg_elimination dependencies denied due to prior dependency registration.')
    else:
        es.dbgmsg(0, 'FAILED: gg_elimination WAS NOT denied dependency registration.')
'''
def server_cvar(event_var):
    if 'gg_' in event_var['cvarname']:
        es.dbgmsg(0, '%s = %s' %(event_var['cvarname'], event_var['cvarvalue']))
'''