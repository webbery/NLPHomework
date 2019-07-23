
def edit_distance(str1,str2):
    len1=len(str1)
    len2=len(str2)
    if len1==0:
        return len2
    if len2==0:
        return len1
    char1 = str1[0]
    char2 = str2[0]
    dist1 = 1+edit_distance(str1[1:],str2)
    dist2 = 1+edit_distance(str1,str2[1:])
    dist3 = edit_distance(str1[1:],str2[1:]) if char1==char2 else edit_distance(str1[1:],str2[1:])+1
    min_dist = min(dist1,dist2,dist3)
    # if min_dist==dist1:
    #     print(char1)
    # elif min_dist==dist2:
    #     print(char2)
    # else:
    #     if char1!=char2:
    #         print(char1,char2)
    return min_dist

def edit_distance_dynamic_program(src,dst):
    # edit_table use 'src*dst' as key and distance as its value
    edit_table={}
    def edit_distance_impl(src,dst):
        key = src+'*'+dst
        if edit_table.__contains__(key):
            return edit_table[key]
        len1=len(src)
        len2=len(dst)
        if len1==0:
            edit_table[key] = len2
            return len2
        if len2==0:
            edit_table[key] = len1
            return len1
        char1 = src[0]
        char2 = dst[0]
        dist1 = 1+edit_distance_impl(src[1:],dst)
        dist2 = 1+edit_distance_impl(src,dst[1:])
        dist3 = edit_distance_impl(src[1:],dst[1:]) if char1==char2 else edit_distance_impl(src[1:],dst[1:])+1
        edit_table[key] = min(dist1,dist2,dist3)
        return edit_table[key]
    return edit_distance_impl(src,dst)
    
# print(edit_distance('SilentKnig','RecyclerView'))
# print(edit_distance_dynamic_program('SilentKnig','RecyclerView'))