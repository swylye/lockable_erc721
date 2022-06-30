// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "./Lockable.sol";

contract TestNFT is ERC721, Lockable {
    uint256 public tokenCounter;
    uint256 public immutable maxSupply;

    constructor() ERC721("Test NFT", "TNFT") Lockable(address(this)) {
        tokenCounter = 1;
        maxSupply = 1000;
    }

    function mint() external {
        require(tokenCounter <= maxSupply);
        uint256 tokenId = tokenCounter;
        tokenCounter += 1;
        _safeMint(msg.sender, tokenId);
    }

    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 tokenId
    ) internal override(ERC721) {
        require(tokenIdLocked[tokenId] != true);
        super._beforeTokenTransfer(from, to, tokenId);
    }
}
