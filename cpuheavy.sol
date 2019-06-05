pragma solidity ^0.4.24;

contract Sorter {
    uint public size;
    uint public storedData;
    uint[] public data;

    event finish(uint size, uint signature);

    constructor(uint initVal) public {
        size = initVal;

        for (uint x = 0; x < size; x++) {
            data.push(size-x);
            //data[x]=size-x;
        }
        //quickSort(data, 0, size - 1);
        storedData = data[size-1];
    }

    function sort(uint signature) public{
        //uint[] memory data = new uint[](size);
        
        if(data[0]>data[size-1])
            quickSort(0, size - 1);
        else
            quickSortReverse(0, size - 1);

        storedData = data[size-1];
        emit finish(size, signature);
    }

    function get() public constant returns (uint retVal) {
        return storedData;
    }

    function quickSort(uint left, uint right) internal {

        uint i = left;
        uint j = right;

        if (i == j) return;
        uint pivot = data[left + (right - left) / 2];
        while (i <= j) {
            while (data[i] < pivot) i++;
            while (pivot < data[j]) j--;
            if (i <= j) {
                (data[i], data[j]) = (data[j], data[i]);
                i++;
                j--;
            }
        }

        if (left < j)
            quickSort(left, j);

        if (i < right)
            quickSort(i, right);
    }


    function quickSortReverse(uint left, uint right) internal {

        uint i = left;
        uint j = right;

        if (i == j) return;
        uint pivot = data[left + (right - left) / 2];
        while (i <= j) {
            while (data[i] > pivot) i++;
            while (pivot > data[j]) j--;
            if (i <= j) {
                (data[i], data[j]) = (data[j], data[i]);
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