document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault(); // Stop the form from submitting normally
            
            // Get the email and password from the form
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            // For now, just show an alert to test it works
            alert(`Email: ${email}, Password: ${password}`);
        });
    }
});

async function loginUser(email, password) {
    try {
        // Replace 'http://localhost:5000' with your actual server URL
        const response = await fetch('http://localhost:5000/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();
            document.cookie = `token=${data.access_token}; path=/`;
            window.location.href = 'index.html';
        } else {
            alert('Login failed: Invalid credentials');
        }
    } catch (error) {
        alert('Error: Could not connect to server');
    }
}
