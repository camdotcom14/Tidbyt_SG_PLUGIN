#!/Library/Frameworks/Python.framework/Versions/3.11/bin/python3

import shotgun_api3
import configparser
import os

# Load configuration
config = configparser.ConfigParser()
config.read('/Users/cameronbriantarget/Desktop/VS_Code/Tidbyt/shotgunEvents/shotgunEventDaemon.conf')

SHOTGUN_URL = config.get('shotgun', 'server')
SCRIPT_NAME = config.get('shotgun', 'name')
SCRIPT_KEY = config.get('shotgun', 'key')

def get_current_cnv_count():
    """
    Return the current number of Versions with status "CNV".
    """
    sg = shotgun_api3.Shotgun(SHOTGUN_URL, SCRIPT_NAME, SCRIPT_KEY)
    filters = [['sg_status_list', 'is', "cnv"], ['project.Project.sg_status', 'is', 'Active']]
    result = sg.find('Version', filters)

    return len(result)

previous_cnv_count = get_current_cnv_count()

def registerCallbacks(reg):
    """
    Register all necessary or appropriate callbacks for this plugin.
    """
    # The Shotgun event types we're interested in.
    eventFilter = {
        'Shotgun_Version_Change': ['sg_status_list']
    }

    reg.registerCallback(
        SCRIPT_NAME,
        SCRIPT_KEY,
        listen_for_cnv_change,
        eventFilter,
        None
    )

    reg.logger.debug("Registered callback.")

def listen_for_cnv_change(sg, logger, event, args):
    global previous_cnv_count
    
    # Get the current CNV count
    current_cnv_count = get_current_cnv_count()

    # If the count has changed, execute your script
    if previous_cnv_count != current_cnv_count:
        logger.info(f"The number of CNVs has changed from {previous_cnv_count} to {current_cnv_count}!")
        
        previous_cnv_count = current_cnv_count

        # Call your other script
        os.system("python3 /Users/cameronbriantarget/Desktop/VS_Code/Tidbyt/shotgunEvents/plugins/SG_Data.py")

