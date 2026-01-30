// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EvidenceRegistry {

    struct Evidence {
        string ipfsCID;
        string sha256Hash;
        address owner;
        uint256 timestamp;
    }

    mapping(uint256 => Evidence) public evidences;
    uint256 public evidenceCount;

    event EvidenceAdded(uint256 id, address owner);

    function addEvidence(
        string memory _cid,
        string memory _hash
    ) public {

        evidenceCount++;

        evidences[evidenceCount] = Evidence(
            _cid,
            _hash,
            msg.sender,
            block.timestamp
        );

        emit EvidenceAdded(evidenceCount, msg.sender);
    }

    function getEvidence(uint256 _id)
        public
        view
        returns (
            string memory,
            string memory,
            address,
            uint256
        )
    {
        Evidence memory e = evidences[_id];

        return (
            e.ipfsCID,
            e.sha256Hash,
            e.owner,
            e.timestamp
        );
    }
}
