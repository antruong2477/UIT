import sys

class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None
class LinkedList:
    def __init__(self):
        self.head = None

    def addhead(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def addtail(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def add_after(self, key, data):
        if not self.head:
            self.addhead(data)
            return
        current = self.head
        while current:
            if current.data == key:
                break
            current = current.next
        if current is None:
            self.addhead(data)
        else:
            new_node = Node(data)
            new_node.next = current.next
            current.next = new_node

    def display(self):
        current = self.head
        while current:
            print(current.data, end=" ")
            current = current.next
        print()

linked_list = LinkedList()

def solve(arr,linked_list):
    for a in arr:
        if a[0] == 0:
            linked_list.addhead(a[1])
        elif a[0] == 1:
            linked_list.addtail(a[1])
        elif a[0] == 2:
            linked_list.add_after(a[1], a[2])
    return linked_list

arr = []
while True:
    line = sys.stdin.readline().strip()
    if line == '3':
        break
    operations = list(map(int, line.split()))
    arr.append(operations)
    
   
solve(arr,linked_list)
linked_list.display()
