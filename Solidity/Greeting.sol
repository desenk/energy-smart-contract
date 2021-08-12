// Use VS Code, install Solidity extension from VS Code (the one from Juan Blanco), and compile with F5.

pragma solidity >=0.4.21 <0.7.0;

contract Greeter {
    string public greeting;

    constructor() public {
        greeting = 'Hello';
    }

    function setGreeting(string memory _greeting) public {
        greeting = _greeting;
    }

    function greet() view public returns (string memory) {
        return greeting;
    }
}