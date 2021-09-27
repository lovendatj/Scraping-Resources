from Taps.GoogleRSS import GoogleRSS

with GoogleRSS(verbose=True, outpath='./output') as goog:
    results = goog.get_xml(
        query=['APPL new phone', 'GME stock'], when='24h', dump_file=True)
