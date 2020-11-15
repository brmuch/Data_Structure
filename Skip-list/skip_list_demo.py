from random import random

class SkipNode:
    
    def __init__(self, val, height = 0):
        self.val = val                                  # 值域
        self.forwards = [None] * height                 # 索引表, [底层->高层]， 底层为所有n个元素

'''
通过随机数在索引表内分层， 
实现O(logn)的查找，插入，删除时间复杂度， 空间复杂度为O(n)
'''
class Skiplist:

    def __init__(self):
        self.max_level = 16                              
        self.level = 1
        self.head = SkipNode(None, self.max_level)

    def search(self, target: int) -> bool:
        p = self.head
        
        for i in range(self.level - 1, -1, -1):            # 从最高层开始检索, 加快搜索速度
            while p.forwards[i] and p.forwards[i].val < target:
                p = p.forwards[i]
            
            if p.forwards[i] and p.forwards[i].val == target:
                return True
        return False

    def add(self, num: int) -> None:
        level = self.random_level()
        self.level = max(self.level, level)
        
        newNode = SkipNode(num, level)                      # 新建一个node
        p = self.head
        
        for i in range(level - 1, -1, -1):                  # 从元素比较少的高层开始更改每一层的索引表
            while p.forwards[i] and p.forwards[i].val < num:
                p = p.forwards[i]
            
            newNode.forwards[i] = p.forwards[i]
            p.forwards[i] = newNode
            
    def erase(self, num: int) -> bool:
        p, flag, target = self.head, False, None
        
        for i in range(self.level - 1, -1, -1):                    # 查找skip-list中是否有这个元素
            while p.forwards[i] and p.forwards[i].val < num:
                p = p.forwards[i]
                
            if p.forwards[i] and p.forwards[i].val == num:              # 找到了这个元素, 更改这层的索引表
                target = p.forwards[i]
                flag = True
                p.forwards[i] = p.forwards[i].forwards[i]       
                
        if flag:
            del target                                                  # 释放内存
        return flag
    
    def random_level(self, factor = 0.5):
        level = 1
        while random() < factor and level < self.max_level:
            level += 1
        return level
    
    def show(self):
        for i in range(self.max_level - 1, -1, -1):
            p = self.head
            if p.forwards[i] != None:
                print("level", i, ": ", end="")
                p = p.forwards[i]
                while p != None:
                    print(p.val, end="")
                    if p.forwards[i] != None:
                        print("->", end="")
                    p = p.forwards[i]
                print()
        print("--------------------------------")

obj = Skiplist()
for i in range(0, 30, 3):
    obj.add(i)
obj.show()
obj.search(12)
obj.erase(12)
obj.show()