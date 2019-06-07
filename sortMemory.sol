pragma solidity ^0.4.24;

contract Sorter {    
    
    function sort(int size) public {
        int[] memory data = new int[](uint(size));
        for (int x = 0; x < size; x++) {
            data[uint(x)] = size-x;
        }
        quickSort(data, 0, size - 1);
    }   

    function quickSort(int[] arr, int left, int right) internal {
        int i = left;
        int j = right;
        if (i == j) return;
        int pivot = arr[uint(left + (right - left) / 2)];
        while (i <= j) {
            while (arr[uint(i)] < pivot) {
                i++;
            }
            while (pivot < arr[uint(j)]){
                j--;
            }
            if (i <= j) {
                int temp = arr[uint(i)];
                arr[uint(i)] = arr[uint(j)];
                arr[uint(j)] = temp;
                i++;
                j--;
            }
        }
    }
}