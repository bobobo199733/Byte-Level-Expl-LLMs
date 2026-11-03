class ListNode:

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def merge_k_sorted_lists(lists):

    def merge_two_lists(l1, l2):
        dummy = ListNode()
        current = dummy
        while l1 and l2:
            if l1.val < l2.val:
                current.next = l1
                l1 = l1.next
            else:
                current.next = l2
                l2 = l2.next
            current = current.next
        current.next = l1 if l1 else l2
        return dummy.next
    while len(lists) > 1:
        merged_lists = []
        for i in range(0, len(lists), 2):
            l1 = lists[i]
            l2 = lists[i + 1] if i + 1 < len(lists) else None
            merged_lists.append(merge_two_lists(l1, l2))
        lists = merged_lists
    return lists[0] if lists else None

def print_linked_list(node):
    while node:
        print(node.val, end=' -> ')
        node = node.next
    print('None')