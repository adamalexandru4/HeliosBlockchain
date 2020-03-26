pragma solidity ^0.5.16;
pragma experimental ABIEncoderV2;

import "./HeliosElection.sol";

contract HeliosAdministrator {

    // string serverURL;
    address[] public elections;
    address owner;

    constructor() public {
        owner = msg.sender;
    }

    function createElection(address _electionAddress) public {
        require(msg.sender == owner);
        elections.push(_electionAddress);
    }

}


