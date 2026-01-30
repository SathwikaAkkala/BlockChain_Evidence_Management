require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();

/*
  Hardhat Configuration
  For Avalanche Fuji & Local Network
*/

module.exports = {

  // Solidity compiler version
  solidity: {
    version: "0.8.20",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200
      }
    }
  },

  // Networks
  networks: {

    // Local Hardhat Network
    hardhat: {},

    // Avalanche Fuji Testnet
    fuji: {
      url: "https://api.avax-test.network/ext/bc/C/rpc",
      accounts: process.env.PRIVATE_KEY
        ? [process.env.PRIVATE_KEY]
        : []
    }
  },

  // Paths (Optional)
  paths: {
    sources: "./contracts",
    tests: "./test",
    cache: "./cache",
    artifacts: "./artifacts"
  }
};
