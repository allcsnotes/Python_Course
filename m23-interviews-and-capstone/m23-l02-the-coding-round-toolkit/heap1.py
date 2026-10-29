import heapq

nums = [5, 1, 8, 3, 9, 2]
print(heapq.nlargest(3, nums))
print(heapq.nsmallest(2, nums))
heap = []
for n in nums:
    heapq.heappush(heap, n)
print(heap[0])
print(heapq.heappop(heap))
print(heapq.heappop(heap))
print(heap)
