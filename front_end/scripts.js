document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      await loginUser(email, password);
    });
  }
  initializePriceFilter();
  checkAuthentication();
});


// TASK 1 - login form

// Function to handle the API request
async function loginUser(email, password) {
  try {
    const response = await fetch('http://localhost:5000/api/v1/auth/login', {
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
      showError('Login failed: Invalid credentials');
    }
  } catch (error) {
    showError('Error: Could not connect to server');
  }
}

// TASK 2  - index.html

function getCookie(name) {

  const cookies = document.cookie.split(';');
  let foundToken = null;

  for (let cookie of cookies) {
    const [cookieName, cookieValue] = cookie.trim().split('=');
    if (cookieName === name && cookieValue) {
      foundToken = cookieValue;
    }
  }
  return foundToken;
}

function checkAuthentication() {

  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');

  if (!loginLink) {
    return;
  }

  if (!token) {
    loginLink.style.display = 'block';
    loginLink.textContent = 'Login';
    loginLink.href = 'login.html';
    fetchPlaces();
  } else {
    loginLink.style.display = 'none';
    fetchPlaces(token);
  }

}

async function fetchPlaces(token = null) {
  if (typeof fetch === 'undefined') {
    return showError('Browser not supported.');
  }

  console.log('Fetching places...');

  try {
    const headers = {
      'Content-Type': 'application/json'
    };

    // Add authorization header if token exists
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch('http://localhost:5000/api/v1/places/', {
      method: 'GET',
      headers: headers
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

function displayPlaces(places) {
  const placesContainer = document.getElementById('places-list');
  if (!placesContainer) {
    console.error('places-list container not found');
    return;
  }

  placesContainer.innerHTML = '';

  if (!places || places.length === 0) {
    placesContainer.innerHTML = '<p>No places available.</p>';
    return;
  }

  const row = document.createElement('div');
  row.className = 'row';

  places.forEach(place => {
    const column = document.createElement('div');
    column.className = 'column';

    const placeCard = document.createElement('div');
    placeCard.className = 'place-card'
    placeCard.setAttribute('data-price', place.price || 0);

    placeCard.innerHTML = `
  <h3>${place.title || 'Unknown place'}</h3>
  <p>Price per night: $${place.price || 'N/A'}</p>
  <div class="button-container">
    <button class="details-button" onclick="viewPlaceDetails('${place.id}')">View Details</button>
  </div>
`;
    column.appendChild(placeCard);
    row.appendChild(column);

  });
  placesContainer.appendChild(row);
}

function setupPriceFilter(places) {
  const filterSelect = document.getElementById('price-filter');
  if (!filterSelect) {
    return;
  }

  if (filterSelect.children.length === 0) {
    const options = [
      { value: 'all', text: 'All' },
      { value: '10', text: 'Up to $10' },
      { value: '50', text: 'Up to $50' },
      { value: '100', text: 'Up to $100' }
    ];

    options.forEach(option => {
      const optionElement = document.createElement('option');
      optionElement.value = option.value;
      optionElement.textContent = option.text;
      filterSelect.appendChild(optionElement);
    });

    filterSelect.addEventListener('change', (event) => {
      const selectedPrice = event.target.value;
      filterPlacesByPrice(selectedPrice);
    });
  }
}

function initializePriceFilter() {
  const filterSelect = document.getElementById('price-filter');
  if (!filterSelect) {
    return;
  }

  if (filterSelect.children.length === 0) {
    const options = [
      { value: 'all', text: 'All' },
      { value: '10', text: 'Up to $10' },
      { value: '50', text: 'Up to $50' },
      { value: '100', text: 'Up to $100' }
    ];

    options.forEach(option => {
      const optionElement = document.createElement('option');
      optionElement.value = option.value;
      optionElement.textContent = option.text;
      filterSelect.appendChild(optionElement);
    });

    filterSelect.addEventListener('change', (event) => {
      const selectedPrice = event.target.value;
      filterPlacesByPrice(selectedPrice);
    });
  }
}

function filterPlacesByPrice(maxPrice) {
  const placeCards = document.querySelectorAll('.place-card');

  placeCards.forEach(card => {
    const placePrice = parseFloat(card.getAttribute('data-price')) || 0;

    if (maxPrice === 'all' || placePrice <= parseFloat(maxPrice)) {
      card.parentElement.style.display = 'block';
    } else {
      card.parentElement.style.display = 'none';
    }
  });
}

function viewPlaceDetails(placeId) {
  window.location.href = `place.html?id=${placeId}`;
}

function showError(message) {

  const existingError = document.getElementById('error-message');
  if (existingError) {
    existingError.remove();
  }
  const errorDiv = document.createElement('div');
  errorDiv.id = 'error-message';
  errorDiv.className = 'error-message';
  errorDiv.style.cssText = `
    background-color: #f8d7da;
    color: #721c24;
    padding: 10px;
    margin: 10px 0;
    border: 1px solid #f5c6cb;
    border-radius: 5px;
    text-align: center;
    position: relative;
    z-index: 1000;
  `;
  errorDiv.textContent = message;

  const main = document.querySelector('main');
  if (main) {
    main.insertBefore(errorDiv, main.firstChild);
  } else {
    document.body.insertBefore(errorDiv, document.body.firstChild);
  }

  // Auto-hide after 5 seconds
  setTimeout(() => {
    if (errorDiv.parentNode) {
      errorDiv.remove();
    }
  }, 5000);
}