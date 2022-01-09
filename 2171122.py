def sumem(l):

    sum = 0
    badlist = []
    pops = []                             # indexes to be popped
    counter = 0                             # number of pops done to keep track of the list length

    for i in range(len(l)):

        try:
            sum = sum + l[i]                  # to increase the sum

        except:
            try:

                if (type(l[i]) is list):
                    for ii in range(len(l[i])):
                        sum = sum + l[i][ii]
                else:
                    badlist.append(l[i])          # list of non-summables
                    pops.append(i)                # non-summable indexes list

            except:
                pass

    for j in pops:
        l.pop(j-counter)                  # since when an item is removed indexs change hence -counter corrects for initial index
        counter += 1                       # after pop increase counter

    return sum, badlist
