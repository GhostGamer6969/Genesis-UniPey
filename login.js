document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form from submitting normally

    // Show the loading spinner
    document.getElementById('loadingSpinner').style.display = 'block';

    // Simulate a delay for processing (e.g., 3 seconds)
    setTimeout(function() {
        // After processing, redirect to home.html
        window.location.href = 'home.html';
    }, 3000); // 3 seconds delay
});
