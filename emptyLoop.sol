pragma solidity ^0.4.24;

contract Sorter {
    uint public loopVar;
    

    constructor(uint initVal) public {
        loopVar = initVal*4;
    }

    function runLoop() view public{
    	uint a=0;
	    for (uint i = 0; i < loopVar; i++) 
	    { 
	        a++;
	    } 
    }

}