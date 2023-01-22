// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.0;

contract Auction {
    address payable highestBidder;
    address public winnerAddress;
    uint highestBid;

    event NewBid(address bidder, uint bid);

    function bid(uint _bid) public {
        require(_bid > highestBid);
        highestBid = _bid;
        winnerAddress = msg.sender;
        emit NewBid(msg.sender, _bid);
    }

    function endAuction() public {
        require(msg.sender == highestBidder);
        highestBidder.transfer(address(this).balance);
    }

    function getHighestBidder() public view returns (address) {
        return winnerAddress;
    }
}
