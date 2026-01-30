const hre = require("hardhat");

/*
  Deploy Script for EvidenceRegistry Contract
*/

async function main() {

  console.log("Starting deployment...");

  // Get contract factory
  const EvidenceRegistry = await hre.ethers.getContractFactory(
    "EvidenceRegistry"
  );

  // Deploy contract
  const contract = await EvidenceRegistry.deploy();

  // Wait until deployed
  await contract.deployed();

  console.log("EvidenceRegistry deployed at:");
  console.log(contract.address);

  // Save address (optional)
  console.log("Save this address for frontend/backend use.");
}

// Run deploy
main()
  .then(() => process.exit(0))
  .catch((error) => {

    console.error("Deployment failed:");
    console.error(error);

    process.exit(1);
  });
