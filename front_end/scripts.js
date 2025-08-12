// TASK 1 - login form

document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      // Call the login function (NO ALERT HERE)
      await loginUser(email, password);
    });
  }
});

// Function to handle the API request
async function loginUser(email, password) {
  try {
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

async function fetchPlaces(token) {
  if (typeof fetch === 'undefined') {
    return showError('Browser not supported.');
  }

  console.log('Fetching places...');

  try {
    const response = await fetch('http://localhost:5000/api/v1/places/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` })
      }
    });

    if (!response) {
      return showError('No response from server.');
    }

    if (!response.ok) {
      const errorMessages = {
        401: 'Please log in to view places.',
        403: 'Access denied.',
        404: 'Places service unavailable.',
        500: 'Server error. Try again later.'
      };

      return showError(errorMessages[response.status] || `Error: ${response.status}`);
    }

    const places = await response.json();
    console.log('Success:', places);
    displayPlaces(places);

  } catch (error) {
    console.error('Error:', error);

    const errorMessage = error.message.includes('fetch')
      ? 'Cannot connect to server. Is the API running?'
      : 'Network error. Check your connection.';

    showError(errorMessage);
  }
}

//testing whether cookies function works -- DELETE LATER
console.log('getCookie works');
console.log('Current token:', getCookie('token'));

// Test when page loads
document.addEventListener('DOMContentLoaded', () => {
  console.log('Page loaded - checking authentication');
  const token = checkAuthentication();
  console.log('Auth result:', token ? 'Authenticated' : 'Not authenticated');
});