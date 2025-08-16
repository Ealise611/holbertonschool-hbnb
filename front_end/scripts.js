document.addEventListener('DOMContentLoaded', async () => {
    console.log('🚀 Page loaded:', window.location.pathname);

    checkAuthentication();

    // LOGIN FORM (login.html)
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            await loginUser(email, password);
        });
    }

    // INDEX PAGE (index.html)
    if (document.getElementById('places-list')) {
        initializePriceFilter();
    }

    // PLACE DETAILS PAGE (place.html)
    if (document.getElementById('place-details')) {
        const token = getCookie('token');
        const placeID = getPlaceIdFromURL();

        if (!placeID) {
            alert('No place id provided');
            return;
        }

        const ok = await fetchPlaceDetails(placeID);
        if (!ok) alert('Failed to load place details');

        addReviewButtonToPlacePage();
    }
    // ADD REVIEW PAGE (add_review.html)
    if (window.location.pathname.includes('add_review.html')) {
        console.log('📝 Add review page detected');

        const token = getCookie('token');

        // Enhanced token validation
        if (!isTokenValid(token)) {
            showError('You must be logged in to add a review. Please log in again.');
            setTimeout(() => {
                window.location.href = 'login.html';
            }, 2000);
            return;
        }

        const urlParams = new URLSearchParams(window.location.search);
        const placeId = urlParams.get('place_id');

        if (!placeId) {
            showError('No place specified. Redirecting to home page...');
            setTimeout(() => {
                window.location.href = 'index.html';
            }, 2000);
            return;
        }

        console.log('✅ Place ID found:', placeId);

        // Setup review form with enhanced error handling
        const reviewForm = document.getElementById('review-form');
        if (reviewForm) {
            reviewForm.addEventListener('submit', async (event) => {
                event.preventDefault();

                const reviewText = document.getElementById('review').value.trim();
                const rating = document.getElementById('rating').value;

                if (!reviewText || !rating) {
                    showError('Please fill in both review text and rating.');
                    return;
                }

                // Disable form during submission
                const submitButton = event.target.querySelector('button[type="submit"]');
                const originalText = submitButton.textContent;
                submitButton.disabled = true;
                submitButton.textContent = 'Submitting...';

                try {
                    console.log('📤 Submitting review...');

                    // Use enhanced authenticated request
                    const response = await makeAuthenticatedRequest('http://localhost:5000/api/v1/reviews/', {
                        method: 'POST',
                        body: JSON.stringify({
                            text: reviewText,
                            rating: parseInt(rating),
                            place_id: placeId
                        })
                    });

                    if (!response) {
                        // Error already handled by makeAuthenticatedRequest
                        return;
                    }

                    if (response.ok) {
                        showSuccess('Review submitted successfully! Redirecting...');
                        reviewForm.reset();
                        setTimeout(() => {
                            window.location.href = `place.html?id=${placeId}`;
                        }, 1500);
                    } else {
                        const errorData = await response.json();
                        const errorMessage = errorData.error || errorData.message || 'Failed to submit review';
                        showError(`Failed to submit review: ${errorMessage}`);
                    }
                } catch (error) {
                    console.error('Network error:', error);
                    showError('Network error. Please check your connection and try again.');
                } finally {
                    // Re-enable form
                    submitButton.disabled = false;
                    submitButton.textContent = originalText;
                }
            });
        }
        loadPlaceInfoForReview(placeId);
    }
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

            // Re-check authentication to update UI immediately
            checkAuthentication();

            showSuccess('Login successful! Redirecting...');
            setTimeout(() => {
                window.location.href = 'index.html';
            }, 1000);
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

function clearExpiredToken() {
    document.cookie = 'token=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    console.log('Expired token cleared');
}

function isTokenValid(token) {
    if (!token) return false;

    try {
        const parts = token.split('.');
        if (parts.length !== 3) return false;

        const payload = JSON.parse(atob(parts[1]));
        const currentTime = Math.floor(Date.now() / 1000);

        if (payload.exp && payload.exp < currentTime) {
            console.log('Token has expired');
            clearExpiredToken();
            return false;
        }

        return true;
    } catch (error) {
        console.log('Invalid token format');
        clearExpiredToken();
        return false;
    }
}

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    // Validate token before using it
    const isValidToken = isTokenValid(token);

    // Handle login button visibility on ALL pages
    if (loginLink) {
        if (!isValidToken) {
            loginLink.style.display = 'block';
            loginLink.textContent = 'Login';
            loginLink.href = 'login.html';
            console.log('User not logged in - showing login button');

            // If on add_review page and no valid token, redirect
            if (window.location.pathname.includes('add_review.html')) {
                showError('Your session has expired. Please log in again.');
                setTimeout(() => {
                    window.location.href = 'login.html';
                }, 2000);
                return;
            }
        } else {
            loginLink.style.display = 'none';
            console.log('User logged in - hiding login button');
        }
    }

    // Handle places loading for index page
    if (document.getElementById('places-list')) {
        if (!isValidToken) {
            fetchPlaces(); // Public access
        } else {
            fetchPlaces(token); // Authenticated access
        }
    }
}

async function makeAuthenticatedRequest(url, options = {}) {
    const token = getCookie('token');

    if (!isTokenValid(token)) {
        showError('Your session has expired. Please log in again.');
        setTimeout(() => {
            window.location.href = 'login.html';
        }, 2000);
        return null;
    }

    const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
        ...options.headers
    };

    try {
        const response = await fetch(url, { ...options, headers });

        // Handle token expiration from server
        if (response.status === 401) {
            const errorData = await response.json();
            if (errorData.msg && errorData.msg.includes('expired')) {
                clearExpiredToken();
                showError('Your session has expired. Please log in again.');
                setTimeout(() => {
                    window.location.href = 'login.html';
                }, 2000);
                return null;
            }
        }

        return response;
    } catch (error) {
        console.error('API request failed:', error);
        showError('Network error. Please check your connection.');
        return null;
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
        placesContainer.innerHTML = '<div class="no-places"><p>No places available at the moment.</p></div>';
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
            ${place.description ? `<p class="description">${place.description.substring(0, 100)}${place.description.length > 100 ? '...' : ''}</p>` : ''}
            <div class="button-container">
                <button class="details-button" onclick="viewPlaceDetails('${place.id}')">View Details</button>
            </div>
        `;

        column.appendChild(placeCard);
        row.appendChild(column);
    });

    placesContainer.appendChild(row);

    const currentFilter = document.getElementById('price-filter')?.value || 'all';
    if (currentFilter !== 'all') {
        filterPlacesByPrice(currentFilter);
    }
}

function initializePriceFilter() {
    const filterSelect = document.getElementById('price-filter');
    if (!filterSelect) {
        return;
    }

    filterSelect.addEventListener('change', (event) => {
        const selectedPrice = event.target.value;
        console.log('Filter changed to:', selectedPrice);
        filterPlacesByPrice(selectedPrice);
    });
}

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
    // Remove existing error messages
    const existingErrors = document.querySelectorAll('.error-message');
    existingErrors.forEach(error => error.remove());

    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.style.cssText = `
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
        color: white;
        padding: 12px 20px;
        margin: 15px 0;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
        font-weight: 500;
        animation: slideIn 0.3s ease-out;
    `;
    errorDiv.textContent = message;

    const main = document.querySelector('main');
    if (main) {
        main.insertBefore(errorDiv, main.firstChild);
    } else {
        document.body.insertBefore(errorDiv, document.body.firstChild);
    }

    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (errorDiv.parentNode) {
            errorDiv.remove();
        }
    }, 5000);
}

// Task 3 - Place details

function getPlaceIdFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id');
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
        <div class="place-info">
            <h2>${place.title || 'No title'}</h2>
            <p><strong>Description:</strong> ${place.description || 'No description available'}</p>
            <p><strong>Price per night:</strong> $${place.price || 'N/A'}</p>
            <p><strong>Location:</strong> ${place.latitude}, ${place.longitude}</p>
            
            ${place.owner ? `
                <div class="host-info">
                    <h3>Host Information</h3>
                    <p><strong>Host:</strong> ${place.owner.first_name} ${place.owner.last_name}</p>
                    <p><strong>Email:</strong> ${place.owner.email}</p>
                </div>
            ` : ''}
            
            ${place.amenities && place.amenities.length > 0 ? `
                <div class="amenities-section">
                    <h3>Amenities</h3>
                    <ul>
                        ${place.amenities.map(amenity => `<li>${amenity.name}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
        </div>
        
        <div class="reviews-section">
            <h3>Reviews</h3>
            ${place.reviews && place.reviews.length > 0 ?
            place.reviews.map(review => `
                    <div class="review-card">
                        <p><strong>Rating:</strong> ${'⭐'.repeat(review.rating || 0)}</p>
                        <p><strong>Comment:</strong> ${review.text || review.comment || 'No comment'}</p>
                        <p><strong>Reviewer:</strong> ${review.user ?
                    `${review.user.first_name} ${review.user.last_name}` :
                    'Anonymous'}</p>
                    </div>
                `).join('') :
            '<p>No reviews yet.</p>'
        }
        </div>
    `;
}

// Task 4

function addReviewButtonToPlacePage() {
    if (!window.location.pathname.includes('place.html')) return;

    const token = getCookie('token');
    if (!token) {
        console.log('No token found - user not logged in');
        return;
    }

    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');

    if (!placeId) {
        console.log('No place ID found in URL');
        return;
    }

    const placeDetailsSection = document.getElementById('place-details');
    if (!placeDetailsSection) {
        console.log('Place details section not found');
        return;
    }

    if (document.getElementById('review-button-container')) {
        return;
    }


    // Create the button
    const reviewButtonContainer = document.createElement('div');
    reviewButtonContainer.id = 'review-button-container';
    reviewButtonContainer.innerHTML = `
        <div class="add-review-section" style="text-align: center; margin: 30px 0; padding: 20px; background: #f8f9fa; border-radius: 10px;">
            <button 
                onclick="goToAddReview('${placeId}')" 
                class="details-button"
                style="margin-top: 15px; padding: 12px 25px; font-size: 16px;">
                Write a Review
            </button>
        </div>
    `;

    placeDetailsSection.appendChild(reviewButtonContainer);
    console.log('Review button added to place page');
}

function goToAddReview(placeId) {
    const token = getCookie('token');
    if (!token) {
        alert('Please log in to write a review.');
        window.location.href = 'login.html';
        return;
    }

    window.location.href = `add_review.html?place_id=${placeId}`;
}

function showSuccess(message) {
    // Remove existing messages
    const existingMessages = document.querySelectorAll('.success-message');
    existingMessages.forEach(msg => msg.remove());

    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.style.cssText = `
        background: linear-gradient(135deg, #51cf66 0%, #40c057 100%);
        color: white;
        padding: 12px 20px;
        margin: 15px 0;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(81, 207, 102, 0.3);
        font-weight: 500;
        animation: slideIn 0.3s ease-out;
    `;
    successDiv.textContent = message;

    const main = document.querySelector('main');
    if (main) {
        main.insertBefore(successDiv, main.firstChild);
    }

    // Auto-remove after 3 seconds
    setTimeout(() => {
        if (successDiv.parentNode) {
            successDiv.remove();
        }
    }, 3000);
}

async function loadPlaceInfoForReview(placeId) {
    try {
        const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`);

        if (!response.ok) {
            showError('Could not load place information.');
            return;
        }

        const place = await response.json();

        const form = document.querySelector('#review-form');
        if (form && place) {
            // Remove any existing place info
            const existingInfo = document.querySelector('.place-info-context');
            if (existingInfo) {
                existingInfo.remove();
            }

            const infoDiv = document.createElement('div');
            infoDiv.className = 'place-info-context';
            infoDiv.innerHTML = `
                <h3>Reviewing: ${place.title}</h3>
                <p><strong>Host:</strong> ${place.owner ? place.owner.first_name + ' ' + place.owner.last_name : 'Unknown'}</p>
                <p><strong>Price:</strong> $${place.price}/night</p>
                <p><strong>Location:</strong> ${place.latitude}, ${place.longitude}</p>
            `;
            form.parentNode.insertBefore(infoDiv, form);
        }
    } catch (error) {
        console.error('Could not load place info:', error);
        showError('Could not load place information.');
    }
}