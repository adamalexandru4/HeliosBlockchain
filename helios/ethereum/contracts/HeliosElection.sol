pragma solidity ^0.5.16;
pragma experimental ABIEncoderV2;

contract HeliosElection {

    struct Vote {
        string hash;
        address voterAddr;

        bool valid; // PROOF is VALID or NOT
        uint castAt;
        uint verifiedAt;
    }

    struct Question {
        int min;
        int max;
        bytes32[] answers;
        bytes32 resultType;
        bool registered;
    }

    string public name;
    bytes32 public short_name; // for URL
    bytes32 public pubKey;

    address owner;

    mapping(string => Question) questions;
    string[] public questionNames;

    mapping(address => bool) eligibleVoters;
    mapping(address => Vote) public votes;
    address[] votersWhoVoted;

    bool public isElectionPublic;
    uint public createdAt;
    uint public startAt;
    uint public endAt;

    constructor(string memory _name, bytes32 _short_name,
                uint _createdAt, uint _startAt, uint _endAt) public {
        owner = msg.sender;
        name = _name;
        short_name = _short_name;

        isElectionPublic = false;

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

    function getNoQuestions() public view returns(uint) {
        return questionNames.length;
    }

    function addQuestion(string memory _name, bytes32[] memory _answers, int _min, int _max, bytes32 _type) public onlyOwner {
        require(questions[_name].registered == false, "Question already registered");

        Question memory newQuestion;
        newQuestion.min = _min;
        newQuestion.max = _max;
        newQuestion.resultType = _type;
        newQuestion.answers = _answers;
        newQuestion.registered = true;
        questions[_name] = newQuestion;

        questionNames.push(_name);
    }

    function setPublicKey(bytes32 _pubKey) public onlyOwner {
        pubKey = _pubKey;
    }

    function vote(string memory _hash, uint _castAt) public {
        if(!isElectionPublic)
            require(eligibleVoters[msg.sender] == true, "You are not eligible to vote");

        Vote memory newVote;
        newVote.voterAddr = msg.sender;
        newVote.hash = _hash;
        newVote.castAt = _castAt;
        newVote.valid = false;

        votes[msg.sender] = newVote;
    }

    function validateVote(string memory _hash, address _voter, uint _verifiedAt) public onlyOwner {
        require(keccak256(abi.encode(votes[_voter].hash)) == keccak256(abi.encode(_hash)), "Hash not matching");
        require(votes[_voter].castAt < _verifiedAt, "Don't fraud vote!");

        if(votes[_voter].castAt > 0) {
            require(votes[_voter].voterAddr == _voter);
        }
        else
            votersWhoVoted.push(_voter);


        votes[_voter].valid = true;
        votes[_voter].verifiedAt = _verifiedAt;
    }
}