pragma solidity ^0.4.24;

contract Sorter {
    int public size;
    int public storedData;
    int[] public data;

    constructor(int initVal) public {
        size = initVal;

        for (int x = 0; x < size; x++) {
            data.push(size-x);
            //data[x]=size-x;
        }
        //quickSort(data, 0, size - 1);
        storedData = data[uint(size-1)];
    }

    

    function get() public constant returns (int retVal) {
        return storedData;
    }

    function sort() public{
        //uint[] memory data = new uint[](size);
        
         if(data[0]>data[uint(size-1)])
            quickSort(0, size - 1);
        else
            quickSortReverse(0, size - 1);
        
        storedData = data[uint(size-1)];
    }

    function quickSort(int left, int right) internal {

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
            quickSort(left, j);

        if (i < right)
            quickSort(i, right);
    }


    function quickSortReverse(int left, int right) internal {

        int i = int(left);
        int j = int(right);

        if (i == j) return;
        int pivot = data[uint(left + (right - left) / 2)];
        while (i <= j) {
            while (data[uint(i)] > pivot) i++;
            while (pivot > data[uint(j)]) j--;
            if (i <= j) {
                (data[uint(i)], data[uint(j)]) = (data[uint(j)], data[uint(i)]);
                i++;
                j--;
            }
        }

        if (left < j)
            quickSortReverse(left, j);

        if (i < right)
            quickSortReverse(i, right);
    }
    
}