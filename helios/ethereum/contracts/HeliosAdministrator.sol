pragma solidity ^0.5.16;

contract HeliosAdministrator {
    mapping(bytes32 => address) elections;
    address owner;

    constructor() public {
        owner = msg.sender;
    }

    function createElection(address _electionAddress, bytes32 _electionURL) public {
        require(msg.sender == owner);
        elections[_electionURL] = _electionAddress;
    }

    function getElection(bytes32 _electionURL) public view returns(address) {
        return elections[_electionURL];
    }
}


