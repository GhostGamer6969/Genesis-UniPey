const contractAddress = "0xeC4c382aBF991b844435Ad8602DD0d5C64552F7d"; // Your contract address
const contractABI = [
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

window.onload = async () => {
    if (window.ethereum) {
        window.web3 = new Web3(window.ethereum);
        await window.ethereum.request({ method: 'eth_requestAccounts' }); // Request account access
    } else {
        alert('Please install MetaMask to use this app');
        return;
    }

    const contract = new web3.eth.Contract(contractABI, contractAddress);

    document.getElementById('sendBtn').onclick = async () => {
        const recipient = document.getElementById('recipient').value;
        const amount = document.getElementById('amount').value;

        // Input validation
        if (!web3.utils.isAddress(recipient)) {
            document.getElementById('message').innerText = 'Invalid address!';
            return;
        }

        if (isNaN(amount) || amount <= 0) {
            document.getElementById('message').innerText = 'Invalid amount!';
            return;
        }

        const accounts = await web3.eth.getAccounts();
        const sender = accounts[0];

        console.log("Sending from:", sender);
        console.log("Recipient Address:", recipient);
        console.log("Amount in Wei:", web3.utils.toWei(amount, 'ether'));

        try {
            const gasEstimate = await contract.methods.sendViaTransfer(recipient).estimateGas({
                from: sender,
                value: web3.utils.toWei(amount, 'ether'),
            });

            const tx = await contract.methods.sendViaTransfer(recipient).send({
                from: sender,
                value: web3.utils.toWei(amount, 'ether'),
                gas: gasEstimate // Use the estimated gas
            });

            document.getElementById('message').innerText = 'Transaction successful!';
        } catch (error) {
            console.error("Transaction error:", error); // Log the error for more insights
            document.getElementById('message').innerText = 'Transaction failed: ' + error.message;
        }
    };
};
