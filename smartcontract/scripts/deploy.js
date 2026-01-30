const hre = require("hardhat");

async function main() {

  const Evidence = await hre.ethers.getContractFactory("EvidenceRegistry");

  const evidence = await Evidence.deploy();

  await evidence.deployed();

  console.log("Contract deployed to:", evidence.address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
