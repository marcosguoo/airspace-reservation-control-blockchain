//SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.3;

contract AirspaceReservation {
    mapping (address => bool) public reservations;

    function reserveAirspace() public {
        require(!reservations[msg.sender]);
        reservations[msg.sender] = true;
    }

    function releaseAirspace() public {
        require(reservations[msg.sender]);
        reservations[msg.sender] = false;
    }
}
