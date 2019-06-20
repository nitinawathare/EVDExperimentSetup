pragma solidity ^0.4.24;

contract Sorter { 
    int size;   
    constructor(int arraySize) public {
        size = arraySize;
    }
    function sort() public {
        int[] memory data = new int[](uint(size));
        for (int x = 0; x < size; x++) {
            data[uint(x)] = size-x;
        }
        quickSort(data, 0, size - 1);
    }   

    function quickSort(int[] data, int left, int right) internal {

        int i = int(left);
        int j = int(right);

        if (i == j) return;
        int pivot = data[uint(left + (right - left) / 2)];
        while (i <= j) {
            while (data[uint(i)] < pivot) i++;
            while (pivot < data[uint(j)]) j--;
            if (i <= j) {
                (data[uint(i)], data[uint(j)]) = (data[uint(j)], data[uint(i)]);
                i++;
                j--;
            }
        }

        if (left < j)
            quickSort(data, left, j);

        if (i < right)
            quickSort(data, i, right);
    }
}