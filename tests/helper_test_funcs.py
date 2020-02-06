def compare_lists(list_A, list_B):
    if len(list_A) != len(list_B):
        return False
    for i in range(len(list_A)):
        if list_A[i] != list_B[i]:
            return False

    return True