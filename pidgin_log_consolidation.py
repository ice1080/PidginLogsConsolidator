
import os
import sys
import datetime
import argparse
from html.parser import HTMLParser

parser = argparse.ArgumentParser()
parser.add_argument(
    '--folder_name', 
    default='all',
    help='select the folder to run the consolidation for'
)

parser.add_argument(
    '--start_date',
    help='select a beginning date of chats'
)

args = parser.parse_args()

def get_current_time_filename() :
    """
    Returns the correctly formatted filename based on the current_time
    Example file name: 2017-02-23.112630-0700MST.html
    """
    time = datetime.datetime.now()

    # does the following need to include daylight saving in the timezone?
    file_name = "{0}-{1}-{2}.{3}{4}{5}-0700MST.html".format(
        time.year,
        time.month,
        time.day,
        time.hour,
        time.minute
        time.second
    )
    
    return file_name

def get_top_path() :
    """
    simple method to return logs path of pidgin
    """
    base_path = os.path.join( os.environ['APPDATA'], ".purple/logs/jabber" )
    
    user = os.listdir( base_path )
    
    if len( user ) != 1 and isinstance( user, list ) :
        raise Exception( 'More than one user found for Pidgin: {0}'.format( user ) )
    
    return os.path.join( base_path, user[0] )


def consolidate_chats( file_path ) :
    """
    consolidate all log files that exist in file_path

    creates/modifies a txt file with the name of the consolidated file
    to keep track of the most recently created file.
    Also deletes the last created file in order to avoid duplicate messages.
    """
    print( file_path )
    file_name = get_current_time_filename()



def run() :
    top_path = get_top_path()
    
    if args.folder_name != 'all' :
        user_path = os.path.join( top_path, args.folder_name )
        if not os.path.exists( user_path ) :
            raise Exception( 'user path does not exist {0}'.format( top_path ) )
        consolidate_chats( user_path )
    else :
        for chat in os.listdir( top_path ) :
            user_path = os.path.join( top_path, chat )
            consolidate_chats( user_path )
    



if __name__ == "__main__" :
    run()

