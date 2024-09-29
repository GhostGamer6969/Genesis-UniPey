// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

contract Ownable {
    address private _owner;
    
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
    
    constructor() {
        _transferOwnership(msg.sender);
    }

    modifier onlyOwner() {
        require(owner() == msg.sender, "Ownable: caller is not the owner");
        _;
    }

    function owner() public view returns (address) {
        return _owner;
    }

    function transferOwnership(address newOwner) public onlyOwner {
        require(newOwner != address(0), "Ownable: new owner is the zero address");
        _transferOwnership(newOwner);
    }

    function _transferOwnership(address newOwner) internal {
        address oldOwner = _owner;
        _owner = newOwner;
        emit OwnershipTransferred(oldOwner, newOwner);
    }

    
}

interface IERC20 {
    function totalSupply() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
    function transfer(address recipient, uint256 amount) external returns (bool);
    function allowance(address owner, address spender) external view returns (uint256);
    function approve(address spender, uint256 amount) external returns (bool);
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
    
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}

library SafeMath {
    function add(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        require(c >= a, "SafeMath: addition overflow");
        return c;
    }

    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b <= a, "SafeMath: subtraction overflow");
        uint256 c = a - b;
        return c;
    }

    function mul(uint256 a, uint256 b) internal pure returns (uint256) {
        if (a == 0) {
            return 0;
        }
        uint256 c = a * b;
        require(c / a == b, "SafeMath: multiplication overflow");
        return c;
    }

    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b > 0, "SafeMath: division by zero");
        uint256 c = a / b;
        return c;
    }
}

contract SendEtherComplex is Ownable {
    using SafeMath for uint256;

    address public erc20Address;  // ERC20 token contract address
    uint256 public transferFee = 5; // 5% fee for each transfer
    mapping(address => bool) public allowedReceivers;

    event EtherSent(address indexed sender, address indexed receiver, uint256 amount, uint256 fee);
    event TokenSent(address indexed sender, address indexed receiver, uint256 amount);
    event AllowedReceiverSet(address indexed receiver, bool status);

    // Invoking the parent (Ownable) constructor using correct inheritance
    constructor(address _erc20Address) Ownable() {  
        require(_erc20Address != address(0), "Invalid ERC20 address");
        erc20Address = _erc20Address;
    }

    modifier validateReceiver(address _to) {
        require(allowedReceivers[_to], "Receiver not authorized");
        _;
    }

    function setAllowedReceiver(address _receiver, bool _status) public onlyOwner {
        allowedReceivers[_receiver] = _status;
        emit AllowedReceiverSet(_receiver, _status);
    }

    // Complex Ether sending function with fees and validation
    function sendEtherWithFee(address payable _to) public payable validateReceiver(_to) {
        require(msg.value > 0, "No Ether sent");
        
        uint256 fee = msg.value.mul(transferFee).div(100);
        uint256 amountToSend = msg.value.sub(fee);
        
        (bool sent, ) = _to.call{value: amountToSend}("");
        require(sent, "Failed to send Ether");
        
        (bool feeSent, ) = owner().call{value: fee}("");
        require(feeSent, "Failed to send fee to owner");

        emit EtherSent(msg.sender, _to, amountToSend, fee);
    }

    // Function to transfer ERC20 tokens
    function transferTokens(address _to, uint256 _amount) public validateReceiver(_to) {
        IERC20 token = IERC20(erc20Address);
        uint256 allowance = token.allowance(msg.sender, address(this));
        require(allowance >= _amount, "Check the token allowance");
        
        bool success = token.transferFrom(msg.sender, _to, _amount);
        require(success, "Token transfer failed");
        
        emit TokenSent(msg.sender, _to, _amount);
    }

    // Fallback function to receive Ether
    receive() external payable {
        revert("Direct Ether transfers not allowed, use sendEtherWithFee()");
    }
    
    // Only callable by the owner to withdraw the contract's Ether balance
    function withdrawEther(uint256 _amount) public onlyOwner {
        require(address(this).balance >= _amount, "Insufficient balance");
        (bool success, ) = owner().call{value: _amount}("");
        require(success, "Withdraw failed");
    }

    // Function to update transfer fee percentage (owner only)
    function updateTransferFee(uint256 _newFee) public onlyOwner {
        require(_newFee <= 100, "Fee cannot exceed 100%");
        transferFee = _newFee;
    }
}
