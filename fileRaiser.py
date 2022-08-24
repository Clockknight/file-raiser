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

    Does: Return list of file paths in the input directory

    Should: return dict of n-deep root keys, with array of >n deep file arrays
    """
    result = {}
    for directory in directorylist:
        # if this directory doesnt exist, return None
        if not os.path.exists(directory):
            return None

        # if its not empty and...
        # if n > 0
        # update result with recursive of (subdirectories in directory, n-1)
        # if n =0
        # return dict version of below

    # after looping through, return result

    '''
    # If the path exists, leave the loop and continue with the rest of the program.
    if os.path.exists(directory):
        print('Path found. Processing for any subfiles in subdirectories.')

        # Use os.walk to find every file in every folder/subfolder
        for root, dirs, file in os.walk(directory, topdown=False):

            if root != directory:  # Check if the root of a file is different from the inputted directory
                for name in file:  # If so...
                    scanFile = os.path.join(root, name)  # Identify it by its full path
                    pathList.append(scanFile)  # Make a list with all of those files

    return pathList
    '''

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

    raiseCount = 0
    i = 0

    # Take input from user, to an exiting directory
    while dirNoExist:
        directory = input(
            '\nPlease input a directory to scan for files to raise.')
        print('\n')

        # Any other input will skip straight to this check.
        directoryList = directoryWalk([directory], 0)

        # If the function fails, it prints this error message for the user
        # This way, code checks for if the directory works regardless of which method is used
        if not directoryList:
            print(directoryList)
            print('The directory doesn\'t work. Please try another directory.')

        else:
            raiseCount = len(directoryList)
            dirNoExist = False

    # Display the amount of files that would be raised by the program. By this point in the code, the only relevant
    # variables called should be a list of directories, raiseCount, and the directory string
    while not unsafeMode:
        # Check with user that the directory and all details of the directory are correct.
        print('\n', raiseCount,
              'files in sub-folders were found. Please type\n\tRAISE\tor\tQUIT\nto raise the highlighted files or '
              'stop the program now, respectively.')
        confirmation = input()

        if confirmation.casefold() == 'RAISE'.casefold():
            unsafeMode = True
            print('\nProcessing...')
        elif confirmation.casefold() == 'QUIT'.casefold():
            print('\nClosing down...')
            sys.exit()
        else:
            print('\nNo valid input was found. Try again.')

    # Now, with the list of directories
    for itemPath in directoryList:
        # The code will create a list with where all the files WILL go
        fileDestinationList.append(os.path.join(directory, ntpath.basename(itemPath)))

    # For each file, take it and move it to original directory
    while i < raiseCount:
        print('\nMoving file', directoryList[i])

        # Try to raise the files
        try:
            # If deleteMode is on use the move function instead of copyfile
            if deleteMode:
                shutil.move(directoryList[i], fileDestinationList[i])
                print(directoryList[i], 'moved to\n', fileDestinationList[i])

                emptyDir = directoryList[i]
                shutil.rmtree(emptyDir)
                directoryList.remove(emptyDir)

            # Otherwise, just copy the file
            else:
                shutil.move(directoryList[i], fileDestinationList[i])
                print(directoryList[i], 'moved to\n', fileDestinationList[i])

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
