#!/bin/sh
if ! [ "$BASH_SOURCE" ]; then
    echo 'This file is meant for sourcing, not execution.'
    return 1
fi

if ! which truffle; then
    echo 'truffle not found'
    return 1
fi

# Initialize truffle if needed.
if [ ! -r './truffle.js' ]; then
    truffle init
    ln ./Paket.sol ./contracts/.
    cat << EOF > ./truffle.js
module.exports = {
  // See <http://truffleframework.com/docs/advanced/configuration>
  // to customize your Truffle configuration!
  networks: {
    development: {
      host: "localhost",
      port: 8545,
      network_id: "*" // Match any network id
    }
  }
};
EOF
    cat << EOF > ./migrations/2_deploy_contracts.js
const Paket = artifacts.require("./Paket");
module.exports = function(deployer, network, accounts){
    deployer.deploy(Paket);
};
EOF
    npm install zeppelin-solidity
fi

# Deploy contract and set address.
PAKET_ADDRESS="$(truffle migrate --reset | grep -Po '(?<=Paket: ).*')"
export PAKET_ADDRESS

# Get ABI.
PAKET_ABI="$(solc --abi Paket.sol | sed -e '/Paket.sol:Paket/,/=======/{//!b};d' | tail -n+2)"
export PAKET_ABI