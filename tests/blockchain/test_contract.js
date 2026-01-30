/**
 * Smart Contract Test Suite
 * Tests EvidenceRegistry Contract
 */

const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("EvidenceRegistry Contract", function () {

  let Evidence;
  let evidence;
  let owner;
  let user1;

  // Run before each test
  beforeEach(async function () {

    [owner, user1] = await ethers.getSigners();

    Evidence = await ethers.getContractFactory("EvidenceRegistry");

    evidence = await Evidence.deploy();

    await evidence.deployed();
  });


  // ================================
  // Test: Deployment
  // ================================
  it("Should deploy successfully", async function () {

    expect(evidence.address).to.properAddress;
  });


  // ================================
  // Test: Add Evidence
  // ================================
  it("Should add new evidence", async function () {

    await evidence.addEvidence("QmCID123", "HASH123");

    const record = await evidence.getEvidence(1);

    expect(record[0]).to.equal("QmCID123");
    expect(record[1]).to.equal("HASH123");
    expect(record[2]).to.equal(owner.address);
  });


  // ================================
  // Test: Evidence Count
  // ================================
  it("Should increase evidence count", async function () {

    await evidence.addEvidence("CID1", "HASH1");
    await evidence.addEvidence("CID2", "HASH2");

    const count = await evidence.totalEvidence();

    expect(count).to.equal(2);
  });


  // ================================
  // Test: Transfer Ownership
  // ================================
  it("Should transfer ownership", async function () {

    await evidence.addEvidence("CID", "HASH");

    await evidence.transferOwnership(1, user1.address);

    const record = await evidence.getEvidence(1);

    expect(record[2]).to.equal(user1.address);
  });


  // ================================
  // Test: Unauthorized Transfer
  // ================================
  it("Should prevent non-owner from transfer", async function () {

    await evidence.addEvidence("CID", "HASH");

    await expect(
      evidence
        .connect(user1)
        .transferOwnership(1, user1.address)
    ).to.be.revertedWith("Not owner");
  });


  // ================================
  // Test: Invalid Evidence
  // ================================
  it("Should fail for invalid ID", async function () {

    await expect(
      evidence.getEvidence(99)
    ).to.be.revertedWith("Evidence not found");
  });

});
