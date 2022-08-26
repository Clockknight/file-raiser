import os
import sys
import shutil
import ntpath


# TODO ask user for how deep they want to raise files
# TODO add option to use the script from context menu
# Guide: https://www.youtube.com/watch?v=jS2LuG1p8Vw

# Returns list of file paths in the input directory
def directoryWalk(directorylist, n):
    """
    Given a list of root directories to walk through, and target depth of n >= 0:

    Return: dict of n-deep root keys, with array of >n deep file arrays
    """
    result = {}
    count = 0
    for directory in directorylist:
        # if this directory doesn't exist, return None
        if not os.path.exists(directory):
            continue
        filelist = []
        # TODO refactor this for loop to only give immediate subdirectories
        # case: directory exists and n > 0
        # update result with recursive of (subdirectories in directory, n-1)
        if n > 0:
            for subdirs in next(os.walk(directory))[1]:
                dirs = [os.path.join(directory, subdir) for subdir in subdirs]
                res = directoryWalk(dirs, n - 1)
                result.update(res[0])
                count += res[1]
        # case: directory exists and n = 0
        # return dict version of old dirWalk()
        else:
            for r, d, f in os.walk(directory, topdown=False):
                for name in f:
                    # Identify it by its full path
                    curfile = os.path.join(r, name)
                    if curfile not in filelist and r != directory:
                        filelist.append(curfile)  # Make a list with all of those files
            # Check if there are any files in filelist
            if filelist:
                result.update({directory: filelist})
                count = len(filelist)

    # after looping through, return result
    return result, count


# Return list of bool values that indicate settings
def startupConfig():
    deleteMode = False
    unsafeMode = False

    filePath = './settings.txt'

    settingsFile = open(filePath, 'r+')
    settingsData = settingsFile.read()

    for char in settingsData:
        settingsFile.close()

        # Check argv for any modes passed through
        if deleteMode:
            print('\nDelete Mode activated! The program will now delete files\' folders instead of just moving them.')
        if unsafeMode:
            print('\nUnsafe Mode activated! The program will no longer prompt to okay moving or copying files.')


def main():
    errorList = []
    errorIndexes = []
    fileDestinationList = []

    deleteMode = False
    unsafeMode = False
    dirNoExist = True

    count = 0
    i = 0

    # CODEBLOCK
    # Infinite loop to get valid input from user
    while True:
        # directory = input(
        #   '\nPlease input a directory to scan for files to raise.')
        directory = 'C:\\Users\\Tyler\\Documents\\GitHub\\file-raiser\\a'
        print('\n')

        # TODO Make sure that all calls to directoryWalk arent broken after refactoring
        # Any other input will skip straight to this check.
        directorydict, count = directoryWalk([directory], 1)

        # If the function fails, it prints this error message for the user
        # This way, code checks for if the directory works regardless of which method is used
        if not directorydict:
            print('The directory is empty. Please double check you\'ve input a valid directory, and try again.')
        else:
            break

    # TODO Double check this to make sure it's not messed up
    # CODEBLOCK
    # Block to let user validate results
    # Display the amount of files that would be raised by the program. By this point in the code, the only relevant
    while not unsafeMode:
        # Check with user that the directory and all details of the directory are correct.
        print('\n', count,
              'files in sub-folders were found. Please type\n\tRAISE\tor\tQUIT\nto raise the highlighted files or '
              'stop the program now, respectively.')
        # confirmation = input()
        confirmation = 'RAISE'

        if confirmation.casefold() == 'RAISE'.casefold():
            unsafeMode = True
            print('\nProcessing...')
        else:
            print('\nNo valid input was found. Try again.')

    # CODEBLOCK
    # Actual processing of files gotten from directoryWalk()
    for key in directorydict:
        for originalpath in directorydict[key]:
            destinationpath = os.path.join(key, os.path.basename(originalpath))
            shutil.move(originalpath, destinationpath)

    # TODO Figure out how to deal with duplicate files (what if multiple files are called d.txt?)
    ''''
    if len(errorList) > 0:
        for error in errorList:
            print('Could not raise the following files:')
            print(error)
    '''


main()
