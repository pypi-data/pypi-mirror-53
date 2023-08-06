import ast 
import datetime


def return_start_time():

    # now1 = datetime.datetime.now() - datetime.timedelta(hours=24)

    today=datetime.datetime.now().strftime('%Y-%m-%d')+"T00:00:01.000000"

    try:

        scan_time = open('last_scan.txt','r').read()
        start_settings = ast.literal_eval(scan_time)

        

        if start_settings['last_scan'] !='':
            to_return = start_settings['last_scan']
            #update it now
            start_settings['last_scan'] = today
            #save it into the file
            open('last_scan.txt','w').write(str(start_settings))
            return to_return
        else:
            #if the last_scan is empty, put the today value in it
            start_settings['last_scan'] = today
            #save it into the file

            open('last_scan.txt','w').write(str(start_settings))

            return start_settings['default_start']

    except:

        default_start=(datetime.datetime.now()-datetime.timedelta(30)).strftime('%Y-%m-%d')

        start_settings = {'default_start' : default_start,
                         "last_scan": today }

        open('last_scan.txt','w').write(str(start_settings))

        return start_settings['default_start']






            






