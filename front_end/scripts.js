
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


// TASK 2  - index.html

function getCookie(name) {
  // Function to get a cookie value by its name -- reads cookies for JWT token
  const cookies = `; ${document.cookie}`;
  const cookieName = cookies.split(`; ${name}=`);
  console.log(cookieName)
  if (cookieName.length === 2) {
    return cookieName.pop().split(';').shift();
  }
  return null; // if cookie not foudn
}

//testing whether cookies function works -- DELETE LATER
console.log('getCookie works');
console.log('Current token:', getCookie('token'));

function checkAuthentication() {
  // Checks if user is logged in and controls the login link visibility 
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');

  if (!loginLink) {
    return;
  }
  if (!token) {
    loginLink.style.display = 'block';
  } else {
    loginLink.style.display = 'none';
    // Fetch places data if the user is authenticated ??????????????
    fetchPlaces(token);
  }
}
