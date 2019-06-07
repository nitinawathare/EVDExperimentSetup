pragma solidity ^0.4.24;

contract Sorter {
    uint size;

    constructor(uint matrixDimension) public {
    	size=matrixDimension;
    }

    function multiply() public{
        uint[5][5] memory data;
        uint[5][5] memory data1;
        uint[5][5] memory result;

        for (uint x = 0; x < 5; x++)
            for (uint y = 0; y < 5; y++)
                data[x][y]=x+y;

        for ( x = 0; x < 5; x++)
            for ( y = 0; y < 5; y++)
                data1[x][y]=x+y+2;

    	
	    for (uint i = 0; i < 5; i++) 
	    { 
	        for (uint j = 0; j < 5; j++) 
	        { 
	            result[i][j] = 0; 
	            for (uint k = 0; k < 5; k++) 
	                result[i][j] += data[i][k] *  
	                             data1[k][j]; 
	        } 
	    }
    }
}