"""
add more logging using prints
"""

import os
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

parser.add_argument(
    '--include_chats',
    default=False,
    help='includes the group chats'
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
        time.minute,
        time.second
    )
    
    return file_name

def get_top_path() :
    """
    simple method to return logs path of pidgin on a windows machine
    """
    base_path = os.path.join( os.environ['APPDATA'], ".purple/logs/jabber" )
    
    users = os.listdir( base_path )
    
    if len( users ) != 1 and isinstance( users, list ) :
        raise Exception( 'More than one user found for Pidgin: {0}'.format( users ) )
    
    return os.path.join( base_path, users[0] )

def delete_file( file_path ) :
    """
    deletes file at file_path
    """
    if os.path.exists( file_path ) :
        print( "deleting file: {0}".format( file_path ) )
        os.remove( file_path )
    else :
        print( "file did not exist, not deleting: {0}".format( file_path ) )

def get_consolidated_filenames_path( chat_path ) :
    """
    returns the path of the text file containing the names of
    the consolidated files
    """
    return os.path.join( chat_path, "consolidated_filenames.txt")

def delete_existing_consolidated_files( path ) :
    """
    deletes any existing files that have been the product of
    the log consolidator
    """
    print( "deleting existing consolidated files in: {0}".format( path ) )
    consolidated_files_text_path = get_consolidated_filenames_path( path )
    with open( consolidated_files_text_path, "rw" ) as consolidated_list_file :
        for consolidated_file in consolidated_list_file :
            delete_file( consolidated_file )
            # include a delete of the filename in the consolidated list text file
            ## maybe only do this if they are all successful

def add_filename_to_consolidated_list( chat_path, new_filename ) :
    """
    adds new_filename to consolidated
    """
    consolidated_files_text_path = get_consolidated_filenames_path( chat_path )
    with open(consolidated_files_text_path, "a" ) as consolidated_file :
        consolidated_file.write( new_filename + "\n" )

def consolidate_chats( user_path ) :
    """
    consolidate all log files that exist in file_path

    creates/modifies a txt file with the name of the consolidated file
        to keep track of the most recently created file.
    Also deletes the last created file in order to avoid duplicate messages.
    """
    # print( user_path )
    delete_existing_consolidated_files( user_path )
    consolidated_filename = get_current_time_filename()
    add_filename_to_consolidated_list( user_path, consolidated_filename )


def run() :
    """
    do it
    """
    top_path = get_top_path()
    
    if args.folder_name != 'all' :
        user_path = os.path.join( top_path, args.folder_name )
        if not os.path.exists( user_path ) :
            raise Exception( 'user path does not exist {0}'.format( top_path ) )
        consolidate_chats( user_path )
    else :
        for chat in os.listdir( top_path ) :
            user_path = os.path.join( top_path, chat )
            if "conference.icdt.net.chat" in user_path :
                if not args.include_chats :
                    continue
            consolidate_chats( user_path )




if __name__ == "__main__" :
    run()

