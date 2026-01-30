// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/*
  Evidence Registry Smart Contract
  Stores IPFS CID and Hash of Evidence
  Maintains Chain of Custody on Blockchain
*/

contract EvidenceRegistry {

    // Evidence structure
    struct Evidence {
        string ipfsCID;       // IPFS file hash
        string sha256Hash;    // SHA-256 hash
        address owner;        // Evidence owner
        uint256 timestamp;    // Upload time
        bool exists;          // Check existence
    }

    // Evidence counter
    uint256 public evidenceCount = 0;

    // Mapping ID → Evidence
    mapping(uint256 => Evidence) private evidences;

    // Events (for audit trail)
    event EvidenceAdded(
        uint256 indexed id,
        address indexed owner,
        string cid,
        uint256 time
    );

    event OwnershipTransferred(
        uint256 indexed id,
        address from,
        address to,
        uint256 time
    );

    // ============================
    // Add Evidence
    // ============================
    function addEvidence(
        string memory _cid,
        string memory _hash
    ) public {

        require(bytes(_cid).length > 0, "Invalid CID");
        require(bytes(_hash).length > 0, "Invalid Hash");

        evidenceCount++;

        evidences[evidenceCount] = Evidence({
            ipfsCID: _cid,
            sha256Hash: _hash,
            owner: msg.sender,
            timestamp: block.timestamp,
            exists: true
        });

        emit EvidenceAdded(
            evidenceCount,
            msg.sender,
            _cid,
            block.timestamp
        );
    }

    // ============================
    // Get Evidence
    // ============================
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
        require(evidences[_id].exists, "Evidence not found");

        Evidence memory e = evidences[_id];

        return (
            e.ipfsCID,
            e.sha256Hash,
            e.owner,
            e.timestamp
        );
    }

    // ============================
    // Transfer Custody
    // ============================
    function transferOwnership(
        uint256 _id,
        address _newOwner
    ) public {

        require(evidences[_id].exists, "Evidence not found");
        require(msg.sender == evidences[_id].owner, "Not owner");
        require(_newOwner != address(0), "Invalid address");

        address oldOwner = evidences[_id].owner;

        evidences[_id].owner = _newOwner;

        emit OwnershipTransferred(
            _id,
            oldOwner,
            _newOwner,
            block.timestamp
        );
    }

    // ============================
    // Verify Ownership
    // ============================
    function isOwner(uint256 _id, address _user)
        public
        view
        returns (bool)
    {
        require(evidences[_id].exists, "Evidence not found");

        return evidences[_id].owner == _user;
    }

    // ============================
    // Total Evidence Count
    // ============================
    function totalEvidence()
        public
        view
        returns (uint256)
    {
        return evidenceCount;
    }
}
