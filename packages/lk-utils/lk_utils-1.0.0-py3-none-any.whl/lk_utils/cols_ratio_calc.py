from difflib import SequenceMatcher


def main(list1, list2):
    ratio = []
    
    for i in range(len(list1)):
        a = list1[i]
        b = list2[i]
        
        r = SequenceMatcher(None, a.lower(), b.lower()).ratio()
        
        ratio.append(round(r, 2))
    
    return ratio
