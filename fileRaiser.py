import os
import shutil


def directoryWalk(directorylist, n):
    """Given a list of root directories to walk through, and target depth of n >= 0:

    Return: dict of n-deep root keys, each with array of >n deep file arrays,
    and number of files to be moved.
    """
    result = {}
    count = 0
    for directory in directorylist:
        # if this directory doesn't exist, return None
        if not os.path.exists(directory):
            continue
        filelist = []
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


def main():
    # CODEBLOCK
    # Infinite loop to get valid input from user
    while True:
        directory = input('\nPlease input a directory to scan for files to raise.\n\t')

        while True:
            depth = input('\nHow deep do you want files to be brought up?'
                          '\nFor example, if you wanted all files to be brought to the directory you input, '
                          'you\'d input 0.'
                          '\nIf you wanted every immediate subdirectory to have all its subdirectories bring up their '
                          'files, you\'d input 1, and so on.\n\t')
            try:
                depth = int(depth)
            except:
                print('\nInvalid format. Try a different depth.')
                continue

            break

        directorydict, count = directoryWalk([directory], depth)

        # If the function fails, it prints this error message for the user
        # This way, code checks for if the directory works regardless of which method is used
        if not directorydict:
            print('The directory is empty. Please double check you\'ve input a valid directory, and try again.')
        else:
            break

    # CODEBLOCK
    # Display the amount of files that would be raised by the program. By this point in the code, the only relevant
    while True:
        # Check with user that the directory and all details of the directory are correct.
        print('\n', count, 'files in sub-folders were found. Please type\n\tRAISE to raise the highlighted files.\n\t')
        confirmation = input()

        if confirmation.casefold() == 'RAISE'.casefold():
            print('\nProcessing...')
            break
        else:
            print('\nNo valid input was found. Try again.')

    # CODEBLOCK
    # Actual processing of files gotten from directoryWalk()
    for key in directorydict:
        for originalpath in directorydict[key]:
            destinationpath = os.path.join(key, os.path.basename(originalpath))
            while os.path.exists(destinationpath):
                name, ext = os.path.splitext(destinationpath)
                destinationpath = '{} copy{}'.format(name, ext)
            shutil.move(originalpath, destinationpath)


main()
