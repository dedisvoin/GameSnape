from library.libtypes import List

l = [1,2,3,4,5,'hello, world','Tima rakov']

l = list(filter(lambda elem: isinstance(elem, int), l))
print(l)