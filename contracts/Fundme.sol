//SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.6;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol"; //This is the link where the code for the ABI is

contract FundMe {
    mapping(address => uint256) public AddressToFunds;
    address[] public funders;

    uint256 minimumUSD = 50 * 10**18;
    address public owner;

    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeed) {
        //constructor is a class that is like a function but gets executed without anyone calling it as soon as the contract is deployed.
        owner = msg.sender;
        priceFeed = AggregatorV3Interface(_priceFeed); //This says that at that address if there exists a contract which has the defined functions, then priceFeed is equal to that.
    }

    function fund() public payable {
        require(
            getConversionRate(msg.value) >= minimumUSD,
            "You need to spend more ETH!"
        );
        // This require function checks to see if the values given are true to the condition
        // If yes, the function is executed properly.
        // If no, then the function is reverted, i.e, whatever the sender sent will be returned and the gas money will also be returned. And the function will stop executing.

        AddressToFunds[msg.sender] += msg.value; //msg.sender is the sender of the funds and msg.value is the how much they sent
        // These 2 are keywords for keeping track of who sent what.
        funders.push(msg.sender);
    }

    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        (
            uint80 roundID,
            int256 answer,
            uint256 startedAt,
            uint256 updatedAt,
            uint80 answeredInRound
        ) = priceFeed.latestRoundData();
        //We can also make it better looking and make it use less space
        // (, int256 answer, , , ) = priceFeed.latestRoundData();
        // return uint256(answer);
        return uint256(answer * 10000000000);
    }

    function getConversionRate(uint256 ethAmnt) public view returns (uint256) {
        uint256 ethPrice = getPrice();
        uint256 ethAmntinUSD = (ethPrice * ethAmnt) / 1000000000000000000;
        return ethAmntinUSD;
    }

    modifier OnlyOwner() {
        //Modifiers change the way a function operates, so if modifiers are called in a functions keyword,
        // then the function will have complete the requirements of the modifier first before running its code in the '_;' place
        require(msg.sender == owner, "You aren't the Owner!");
        _;
    }

    function withdraw() public payable OnlyOwner {
        payable(msg.sender).transfer(address(this).balance); //transfer function sends a bunch of ethereum to a specific address
        // here it is sending it to the sender(msg.sender).
        //'this' keywords refers back to the contract that we are currently in, like 'self' in python.
        for (
            uint256 funderIndex = 0;
            funderIndex < funders.length;
            funderIndex++
        ) {
            address funder = funders[funderIndex];
            AddressToFunds[funder] = 0;
        }
        funders = new address[](0);
    }

    function getEntranceFee() public view returns (uint256) {
        // minimumUSD
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        return (minimumUSD * precision) / price;
    }
} //1,565.63434645 $ = 1 ETH;
