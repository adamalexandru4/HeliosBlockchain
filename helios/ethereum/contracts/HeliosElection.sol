pragma solidity ^0.5.16;
pragma experimental ABIEncoderV2;

contract HeliosElection {

    struct Vote {
        string hash;

        bool valid; // PROOF is VALID or NOT
        uint castAt;
        uint verifiedAt;
    }

    struct Question {
        string name;
        int min;
        int max;
        bytes32[] answers;
        bytes32 resultType;
    }

    string name;
    bytes32 short_name; // for URL
    string pubKey;

    address owner;

    Question[] questions;
    string[] trusteesPubKeys;
    mapping(address => bool) eligibleVoters;
    mapping(address => Vote) public votes;
    address[] votersWhoVoted;

    uint createdAt;
    uint startAt;
    uint endAt;

    constructor(string memory _name, bytes32 _short_name,
                uint _createdAt, uint _startAt, uint _endAt) public {
        owner = msg.sender;
        name = _name;
        short_name = _short_name;

        createdAt = _createdAt;
        startAt = _startAt;
        endAt = _endAt;
    }

    modifier onlyOwner () {
      require(msg.sender == owner);
      _;
    }

    function addEligibleVoters(address[] memory _votersAddresses) public onlyOwner {
        for (uint i = 0; i < _votersAddresses.length; ++i) {
            eligibleVoters[_votersAddresses[i]] = true;
        }
    }

    function isEligibleVoter(address _voterAddress) public view returns(bool) {
        return eligibleVoters[_voterAddress];
    }

    function addQuestion(string memory _name, bytes32[] memory _answers, int _min, int _max, bytes32 _type) public onlyOwner {
        Question memory newQuestion;
        newQuestion.name = _name;
        newQuestion.min = _min;
        newQuestion.max = _max;
        newQuestion.resultType = _type;
        newQuestion.answers = _answers;
        questions.push(newQuestion);
    }

    function addTrusteeKeys(string[] memory _trusteePubKeys) public onlyOwner {
        trusteesPubKeys = _trusteePubKeys;
    }

    function vote(string memory _hash, uint _castAt) public {
        require(eligibleVoters[msg.sender] == true, "You are not eligible to vote");

        Vote memory newVote;
        newVote.hash = _hash;
        newVote.castAt = _castAt;
        newVote.valid = false;

        votes[msg.sender] = newVote;
    }

    function validateVote(string memory _hash, address _voter, uint _verifiedAt) public onlyOwner {
        require(keccak256(abi.encode(votes[_voter].hash)) == keccak256(abi.encode(_hash)), "Hash not matching");
        require(votes[_voter].castAt < _verifiedAt, "Don't fraud vote!");

        votersWhoVoted.push(_voter);
        votes[_voter].valid = true;
        votes[_voter].verifiedAt = _verifiedAt;
    }
}