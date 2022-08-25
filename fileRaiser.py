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
    for directory in directorylist:
        # if this directory doesn't exist, return None
        print(os.path.exists(directory))
        print(directory)
        if not os.path.exists(directory):
            continue
        filelist = []
        for root, dirs, file in os.walk(directory):
            # case: directory exists and n > 0
            # update result with recursive of (subdirectories in directory, n-1)
            if n > 0:
                dirs = [os.path.join(root, directory) for directory in dirs]
                result.update(directoryWalk(dirs, n-1))
            # case: directory exists and n = 0
            # return dict version of old dirWalk()
            else:
                for r, d, f in os.walk(directory, topdown=False):
                    for name in f:
                        scanFile = os.path.join(root, name)  # Identify it by its full path
                        filelist.append(scanFile)  # Make a list with all of those files
                # Check if there are any files in filelist
                if filelist:
                    result.update({directory: filelist})

    # after looping through, return result
    return result



# Return list of bool values that indicate settings
def startupConfig():
    deleteMode = False
    unsafeMode = False
    dirNoExist = True

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

    # Take input from user, to an exiting directory
    while dirNoExist:
        #directory = input(
        #   '\nPlease input a directory to scan for files to raise.')
        directory = 'C:\\Users\\Tyler\\Documents\\GitHub\\file-raiser\\a'
        print('\n')

        # TODO Make sure that all calls to directoryWalk arent broken after refactoring
        # Any other input will skip straight to this check.
        directorydict, count = directoryWalk([directory], 1)

        # If the function fails, it prints this error message for the user
        # This way, code checks for if the directory works regardless of which method is used
        if not directorydict:
            print('The directory doesn\'t work. Please try another directory.')

        else:
            count = len(directorydict)
            dirNoExist = False

    # Display the amount of files that would be raised by the program. By this point in the code, the only relevant
    # variables called should be a list of directories, count, and the directory string
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

    # Now, with the list of directories
    for itemPath in directorydict:
        # The code will create a list with where all the files WILL go
        fileDestinationList.append(os.path.join(directory, ntpath.basename(itemPath)))

    # For each file, take it and move it to original directory
    while i < count:
        # TODO redo this so it actually makes sense to do with a dict object

        print('\nMoving file', directorydict[i])

        # Try to raise the files
        try:
            # If deleteMode is on use the move function instead of copyfile
            if deleteMode:
                shutil.move(directorydict[i], fileDestinationList[i])
                print(directorydict[i], 'moved to\n', fileDestinationList[i])

                emptyDir = directorydict[i]
                shutil.rmtree(emptyDir)
                directorydict.remove(emptyDir)

            # Otherwise, just copy the file
            else:
                shutil.move(directorydict[i], fileDestinationList[i])
                print(directorydict[i], 'moved to\n', fileDestinationList[i])

        except:
            errorIndexes.append(i)  # Keep track of failed raises' indexes
            errorList.append(sys.exc_info()[0])  # Keep track of the errors of the raise errors
            print('Error. Moving to next file.')

        i += 1

    for dirs in os.walk(directory, topdown=False):
        print(dirs)

    if len(errorList) > 0:
        for error in errorList:
            print('Could not raise the following files:')
            print(error)


main()
