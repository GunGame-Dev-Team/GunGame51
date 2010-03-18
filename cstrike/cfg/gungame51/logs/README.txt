Error logs are generated in the format GunGame<version>_Log<configuration#>.txt

If your server's configuration has changed (such as an updated version of
    EventScripts), the current errorlog will be copied into:
                    GunGame<version>_Log_Old[1].txt
    If the configuration is changed yet again, you will see:
                    GunGame<version>_Log.txt          (Newest)
                    GunGame<version>_Log_Old[1].txt   (Oldest)
                    GunGame<version>_Log_Old[2].txt   (In Between)

    The most recent error log is always located in GunGame<version>_Log.txt