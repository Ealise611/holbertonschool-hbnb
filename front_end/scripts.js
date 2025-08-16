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

// TASK 2 - index.html

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
        placeCard.className = 'place-card';

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

    const currentFilter = document.getElementById('price-filter').value;
    if (currentFilter !== 'all') {
        filterPlacesByPrice(currentFilter);
    }
}

function initializePriceFilter() {
    const filterSelect = document.getElementById('price-filter');
    if (!filterSelect) {
        return;
    }

    // Only set up the event listener once
    filterSelect.addEventListener('change', (event) => {
        const selectedPrice = event.target.value;
        console.log('Filter changed to:', selectedPrice);
        filterPlacesByPrice(selectedPrice);
    });
}

// FIXED: Improved filter function
function filterPlacesByPrice(maxPrice) {
    console.log('Filtering by max price:', maxPrice);

    const placeCards = document.querySelectorAll('.place-card');
    console.log('Found place cards:', placeCards.length);

    placeCards.forEach(card => {
        const placePrice = parseFloat(card.getAttribute('data-price')) || 0;
        console.log('Place price:', placePrice, 'Max price:', maxPrice);

        const column = card.parentElement;

        if (maxPrice === 'all' || placePrice <= parseFloat(maxPrice)) {
            column.style.display = 'flex';
        } else {
            column.style.display = 'none';
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

    setTimeout(() => {
        if (errorDiv.parentNode) {
            errorDiv.remove();
        }
    }, 5000);
}

// Task 3 - Place details
document.addEventListener('DOMContentLoaded', async () => {
    if (!document.getElementById('place-details')) {
        return;
    }
    //use getCookie to get the token
    const token = getCookie('token');
    // get the place id from the URL
    const placeID = getPlaceIdFromURL();
    if (!placeID) {
        alert('No place id provided');
        return;
    }
    //only show add review button if user is logged in
    const addReviewSection = document.getElementById('add-review');
    if (addReviewSection) {
        addReviewSection.style.display = token ? 'block' : 'none';
        // get details if failed then alert
        const ok = await fetchPlaceDetails(placeID);
        if (!ok) alert('Failed to load place details');
    }
});

function getPlaceIdFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id'); //if id is not found, it will return null
}

async function fetchPlaceDetails(placeID) {
    try {
        const res = await fetch(`http://localhost:5000/api/v1/places/${placeID}`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });

        if (!res.ok) {
            // if response is not 2xx, failed
            return false;
        }
        const place = await res.json();
        displayPlaceDetails(place);
        return true;
    } catch (err) {
        console.error('Error fetching place details:', err);
        return false;
    }
}
function displayPlaceDetails(place) {
    const container = document.getElementById('place-details');
    if (!container) return;

    container.innerHTML = `
    <h2>${place.title || 'No title'}</h2>
    <p>${place.description || 'No description'}</p>
    <p>Price per night: $${place.price || 'N/A'}</p>
    <h3>Amenities:</h3>
    <ul>
        ${(place.amenities || []).map(a => `<li>${a.name}</li>`).join('')}
    </ul >
    <h3>Reviews:</h3>
    <div>
    ${(place.reviews || []).map(r => `<p>$(r.comment} - ${r.user?.name || 'Anonymous'}</p>`).join('')}
    </div>
`;
}

// Task 4

const token = getCookie('token');

function checkAuthentication() {
    const token = getCookie('token');
    if (!token) {
        window.location.href = 'index.html';
        return null;
    }
    return token;
}

function getPlaceIdFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('place_id');
}

async function submitReview(token, placeId, reviewText, rating) {
    try {
        const response = await fetch('/api/v1/reviews/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                text: reviewText,
                rating: parseInt(rating),
                place_id: placeId
            })
        });

        return response;
    } catch (error) {
        console.error('Error submitting review:', error);
        throw error;
    }
}

function handleResponse(response, reviewForm) {
    if (response.ok) {
        alert('Review submitted successfully!');
        reviewForm.reset();
    } else {
        alert('Failed to submit review. Please try again.');
    }
}

async function displayPlaceInfo(token, placeId) {
    try {
        const response = await fetch(`/api/v1/places/${placeId}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const place = await response.json();

            const main = document.querySelector('main');
            const existingPlaceInfo = document.querySelector('.place-info');

            if (!existingPlaceInfo) {
                const placeInfoDiv = document.createElement('div');
                placeInfoDiv.className = 'place-info';
                placeInfoDiv.innerHTML = `
                    <h3>Reviewing: ${place.title}</h3>
                    <p><strong>Host:</strong> ${place.owner.first_name} ${place.owner.last_name}</p>
                    <p><strong>Price:</strong> $${place.price} per night</p>
                    <p><strong>Description:</strong> ${place.description}</p>
                `;

                // Insert before the form
                const form = document.querySelector('#review-form');
                main.insertBefore(placeInfoDiv, form);
            }
        }
    } catch (error) {
        console.error('Error fetching place details:', error);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const token = checkAuthentication();

    const placeId = getPlaceIdFromURL();

    if (!placeId) {
        alert('Invalid place ID. Redirecting to home page.');
        window.location.href = 'index.html';
        return;
    }

    displayPlaceInfo(token, placeId);

    const reviewForm = document.getElementById('review-form');

    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const reviewText = document.getElementById('review').value.trim();
            const rating = document.getElementById('rating').value;

            if (!reviewText) {
                alert('Please enter a review text.');
                return;
            }

            if (!rating) {
                alert('Please select a rating.');
                return;
            }

            try {
                const response = await submitReview(token, placeId, reviewText, rating);
                handleResponse(response, reviewForm);

                if (response.ok) {
                    setTimeout(() => {
                        window.location.href = `place.html?place_id=${placeId}`;
                    }, 2000);
                }
            } catch (error) {
                alert('An error occurred while submitting your review. Please try again.');
            }
        });
    }

    const loginLink = document.getElementById('login-link');
    if (loginLink && token) {
        loginLink.textContent = 'Logout';
        loginLink.href = '#';
        loginLink.addEventListener('click', (e) => {
            e.preventDefault();
            // Clear the token cookie
            document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
            window.location.href = 'index.html';
        });
    }
});