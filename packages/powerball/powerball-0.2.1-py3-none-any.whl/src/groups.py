from numpy import array
import numpy


def make_3d_jagged_array(nrows, ncol):
    # nrows: array of ints, specifying the number
    # of rows to output in each subarray.
    # wrapper function that takes only one arg,
    # needed for map. y is number of cols for
    # all subarrays.
    def empty_wrapper(nrows, y=ncol): return(numpy.empty((nrows, y)))
    return list(map(empty_wrapper, nrows))


def filter_groups(groups, groupSize):
    # Groups is a list representing all the groups in the last column of our input matrix
    # groupSize is a command line argument that specifies the min number of rows a group needs
    # to avoid being filtered
    unique = list(numpy.unique(groups))
    # Creating an empty list the same size as unique for storing the number of members of each group
    groupSizes = [0] * len(unique)
    for i in range(len(unique)):
        # The size of each group equals the number of times the name appears in groups
        groupSizes[i] = sum(groups == unique[i])

    # This list will store the indices of any groups that need to be filtered.
    # It's used to avoid any issues with removing elements while looping through the list.
    indicesToRemove = []

    # Filtering out groups based on the minimum group size.
    for i in range(len(unique)):
        if groupSizes[i] < groupSize:
            indicesToRemove.append(i)

    for x in indicesToRemove:
        del groupSizes[x]
        # We also delete these entries from unique so that we have a filtered list. Return this.
        del unique[x]
    return unique

def group_submatrices(data, groups, unique):
    # data - a 2d array (D below)
    # gets columns of matrix "data" subset by each unique element within groups
    # unique is a list of the unique groups in groups that meet the minimum size requirement
    # This is used for filtering out groups below this size.
    # Returns an array of the submatrix of each group

    if len(unique) < len(numpy.unique(groups)):
        # If anything is going to be filtered, print a warning message.
        print("\nWarning:", len(numpy.unique(groups)) - len(unique),
              "group(s) were below the minimum group size and were ignored.")
        ignoredNames = []
        for i in groups:
            if i not in unique:
                ignoredNames.append(unique[i])
        print("The ignored groups are:", ignoredNames, "\n")

    groupSizes = [0] * len(unique)
    for i in range(len(unique)):
        # The size of each group equals the number of times the name appears in groups
        groupSizes[i] = sum(groups == unique[i])

    submatrices = make_3d_jagged_array(nrows=groupSizes, ncol=len(data[0]))

    for i in range(len(unique)):
        submatrices[i] = group_submatrix(data, groups, unique[i])

    return array(submatrices)


def group_submatrix(data, groups, groupName):
    # # data is a 2d array of all the numerical data of species across samples
    # from the input file. groups is a list of the groups that each species
    # belongs to taken from the final column of the inpt file.
    # group is an element of groups and is the specific group that a submatrix
    # will be generated for.
    # Returns a 2d array of the data for a single group specified by group
    rows = (groups == groupName)
    cols = [True] * len(data[0])
    return(data[numpy.ix_(rows, cols)])
"""
def group_submatrices(data, groups, unique):
    # This function returns an array of the submatrix of each group

    Submatrices = []  # This is where we'll store the end results

    for groupName in unique:
        submatrix = group_submatrix(data, groups, groupName)
        Submatrices.append(submatrix)

    return array(Submatrices)
def group_submatrix(data, groups, groupName):
    # Returns the data for a single group specified by groupName

    submatrix = []
    # Get the submatrix where all members belong to the same group
    for i in range(data.shape[0]):
        if groupName == groups[i]:  # If the group name == that row's group
            submatrix.append(data[i])
    return array(submatrix)
"""
