// MetaMask connection
let web3;
const contractAddress = '0xeC4c382aBF991b844435Ad8602DD0d5C64552F7d';
const abi = [
  {
    "inputs": [
      {
        "internalType": "address payable",
        "name": "_to",
        "type": "address"
      }
    ],
    "name": "sendViaTransfer",
    "outputs": [],
    "stateMutability": "payable",
    "type": "function"
  }
];

// Function to connect MetaMask
async function connectMetamask() {
  if (window.ethereum) {
    try {
      // Request account access
      await window.ethereum.request({ method: 'eth_requestAccounts' });
      web3 = new Web3(window.ethereum);
      return web3;
    } catch (error) {
      console.error("User denied account access", error);
      document.getElementById('status').innerText = 'MetaMask connection failed: User denied account access';
    }
  } else {
    console.log("Non-Ethereum browser detected. You should consider trying MetaMask!");
    document.getElementById('status').innerText = 'MetaMask is not installed. Please install it to continue.';
  }
}

// Send Transaction function
async function sendTransaction(recipient, amount) {
  const accounts = await web3.eth.getAccounts();
  const sender = accounts[0];

  // Initialize contract instance
  const contract = new web3.eth.Contract(abi, contractAddress);

  // Convert amount to wei (1 Ether = 10^18 wei)
  const ethAmount = web3.utils.toWei(amount, 'ether');

  try {
    // Estimate gas for the transaction
    const gasEstimate = await contract.methods.sendViaTransfer(recipient).estimateGas({
      from: sender,
      value: ethAmount
    });

    // Send the transaction
    await contract.methods.sendViaTransfer(recipient).send({
      from: sender,
      value: ethAmount,
      gas: gasEstimate // Use the estimated gas value
    });

    document.getElementById('status').innerText = `Transaction successful! Sent ${amount} ETH to ${recipient}`;
  } catch (error) {
    console.error('Transaction failed', error);

    // Handle specific errors
    if (error.code === -32603) {
      document.getElementById('status').innerText = 'Internal JSON-RPC error: Make sure your contract is deployed on the correct network.';
    } else if (error.message.includes('insufficient funds')) {
      document.getElementById('status').innerText = 'Transaction failed: Insufficient funds for gas or transaction.';
    } else {
      document.getElementById('status').innerText = `Transaction failed: ${error.message}`;
    }
  }
}

// Form submission handler
document.getElementById('transactionForm').addEventListener('submit', async function (e) {
  e.preventDefault(); // Prevent form from refreshing the page

  const recipient = document.getElementById('recipient').value;
  const amount = document.getElementById('amount').value;

  if (recipient && amount) {
    // Connect to MetaMask and send the transaction
    await connectMetamask();
    sendTransaction(recipient, amount);
  } else {
    document.getElementById('status').innerText = 'Please provide both recipient address and amount.';
  }
});
