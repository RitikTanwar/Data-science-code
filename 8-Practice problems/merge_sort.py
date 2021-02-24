def merge(list1, s, e):
    mid = (s+e)//2
    i = 0
    j = mid+1
    temp = []
    while (i <= mid and j <= e):
        if(list1[i] < list1[j]):
            temp.append(list1[i])
            i += 1
        else:
            temp.append(list1[j])
            j += 1
    while(i <= mid):
        temp.append(list1[i])
        i += 1
    while(j <= e):
        temp.append(list1[j])
        j += 1
    # list1.clear()
    k = 0
    print(temp)
    for i in range(len(temp)):
        list1[k] = temp[i]
        k += 1


def mergesort(list1, s, e):
    if s == e:
        return
    mid = (s+e)//2
    # print(s, e, mid)
    mergesort(list1, s, mid)
    mergesort(list1, mid+1, e)
    merge(list1, s, e)


list1 = [6, 4, 7, 98, 5, 9, 2]
s = 0
e = len(list1)-1
mergesort(list1, s, e)
print(list1)
