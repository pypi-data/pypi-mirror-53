import os, requests
import datetime

def load_default_id():
    userid = ''
    config_path = get_config_path()
    if os.path.isfile(config_path):
        config_file = open(config_path,"r") 
        userid = config_file.readlines() 
        config_file.close()
    
    return userid

USERID = load_default_id()
API_ENDPOINT = 'https://us-central1-toaster-253815.cloudfunctions.net/toaster_message'

def toast(method):
    if USERID == '':
        raise UnboundLocalError('You have not configured your Telegram ID. Run set_id(<telegram id>) first.')

    def insert_toast(*args, **kw):      
        try:
            start = datetime.datetime.now()
            result = method(*args, **kw)
            end = datetime.datetime.now()
            diff = start - end
            # Create Message
            msg = "🍞 Ding! Function <i>{}</i> has completed!\n<b>Start Time:</b> {}\n<b>End Time:</b> {}\n<b>Time Taken:</b> {}".format(
                method.__name__, start.strftime("%Y-%m-%d %H:%M:%S"), end.strftime("%Y-%m-%d %H:%M:%S"), format_time(diff)
            )
            data = {
                'userid':USERID,
                'msg':msg
            }

            res = requests.post(url = API_ENDPOINT, data = data)
            return result

        except Exception as e:
            msg = '⚠️ An error has occurred with function <i>{}</i>\n<b>Error message:</b> {}'.format(method.__name__, str(e))
            print('Error caught:',e)
            data = {
                'userid':USERID,
                'msg':msg
            }
            # Send Telegram Message
            res = requests.post(url = API_ENDPOINT, data = data)

    return insert_toast

def set_id(userid):
    if userid.isnumeric():
        config_path = get_config_path()
        config_file = open(config_path,"w") 
        config_file.write(str(userid))
        config_file.close()
        global USERID
        USERID = userid
    else:
        raise TypeError('Your Telegram ID should be all numbers.')

def format_time(time_diff):
    days = time_diff.days
    hours, remainder = divmod(time_diff.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if days > 0:
        return '{} days, {} hours, {} mins, {} sec'.format(days, int(hours), int(minutes), seconds)
    return '{} hours, {} mins, {} sec'.format(int(hours), int(minutes), seconds)

def get_config_path():
    current_dir = __file__
    parent_dir = os.path.dirname(current_dir)
    config_path = os.path.join(parent_dir, 'config.txt')
    return config_path