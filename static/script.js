// static/script.js
document.addEventListener('DOMContentLoaded', () => {
    console.log("Frontend JavaScript loaded.");

    const bookingDateInput = document.getElementById('bookingDate');
    bookingDateInput.addEventListener('change', () => {
        const selectedDate = bookingDateInput.value;
        if (selectedDate) {
            loadAvailableSlots(selectedDate);
        }
    });

    loadIPads();
    loadPeriods();

    const bookingForm = document.getElementById('booking-form');
    if (bookingForm) {
        bookingForm.addEventListener('submit', handleBookingSubmit);
    } else {
        console.error("Booking form element not found!");
    }

    const loadBookingsButton = document.getElementById('load-bookings-btn');
    if (loadBookingsButton) {
        loadBookingsButton.addEventListener('click', loadAllBookings);
    } else {
        console.error("Load bookings button not found!");
    }

    const bookingSearchInput = document.getElementById('booking-search');
    if (bookingSearchInput) {
        bookingSearchInput.addEventListener('keyup', () => {
            const searchTerm = bookingSearchInput.value.toLowerCase();
            const allBookingsListDiv = document.getElementById('all-bookings-list');
            const bookings = allBookingsListDiv.getElementsByTagName('li');
            Array.from(bookings).forEach(booking => {
                if (booking.textContent.toLowerCase().includes(searchTerm)) {
                    booking.style.display = '';
                } else {
                    booking.style.display = 'none';
                }
            });
        });
    }
});

async function loadAvailableSlots(date) {
    const ipadsListDiv = document.getElementById('ipads-list');
    const periodsListDiv = document.getElementById('periods-list');
    if (!ipadsListDiv || !periodsListDiv) {
        console.error("DOM elements for iPads or periods list not found.");
        return;
    }

    ipadsListDiv.innerHTML = '<p class="loading-message">Loading available iPads...</p>';
    periodsListDiv.innerHTML = '<p class="loading-message">Loading available periods...</p>';

    try {
        const response = await fetch(`/api/available_slots?date=${date}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status} ${response.statusText}`);
        }
        const data = await response.json();

        // Populate iPads
        if (data.ipads && data.ipads.length > 0) {
            ipadsListDiv.innerHTML = '';
            data.ipads.forEach(ipad => {
                const div = document.createElement('div');
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.id = `ipad-${ipad.id}`;
                checkbox.name = 'selectedIpadIds';
                checkbox.value = ipad.id;

                const label = document.createElement('label');
                label.htmlFor = `ipad-${ipad.id}`;
                label.textContent = `${ipad.id}: ${ipad.description}`;

                div.appendChild(checkbox);
                div.appendChild(label);
                ipadsListDiv.appendChild(div);
            });
        } else {
            ipadsListDiv.innerHTML = '<p>No iPads available for this date.</p>';
        }

        // Populate Periods
        if (data.periods && data.periods.length > 0) {
            periodsListDiv.innerHTML = '';
            data.periods.forEach(period => {
                const div = document.createElement('div');
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.id = `period-${period.id}`;
                checkbox.name = 'selectedPeriodIds';
                checkbox.value = period.id;

                const label = document.createElement('label');
                label.htmlFor = `period-${period.id}`;
                label.textContent = `${period.id}: ${period.start_time} - ${period.end_time}`;

                div.appendChild(checkbox);
                div.appendChild(label);
                periodsListDiv.appendChild(div);
            });
        } else {
            periodsListDiv.innerHTML = '<p>No periods available for this date.</p>';
        }

    } catch (error) {
        console.error('Error loading available slots:', error);
        ipadsListDiv.innerHTML = `<p class="error-message">Error loading iPads: ${error.message}</p>`;
        periodsListDiv.innerHTML = `<p class="error-message">Error loading periods: ${error.message}</p>`;
    }
}

async function loadIPads() {
    const ipadsListDiv = document.getElementById('ipads-list');
    if (!ipadsListDiv) { console.error("DOM element #ipads-list not found."); return; }
    ipadsListDiv.innerHTML = '<p>Loading iPads...</p>';

    try {
        const response = await fetch('/api/ipads');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status} ${response.statusText}`);
        }
        const ipads = await response.json();

        if (ipads && ipads.length > 0) {
            ipadsListDiv.innerHTML = '';
            ipads.forEach(ipad => {
                const div = document.createElement('div');
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.id = `ipad-${ipad.id}`;
                checkbox.name = 'selectedIpadIds';
                checkbox.value = ipad.id;

                const label = document.createElement('label');
                label.htmlFor = `ipad-${ipad.id}`;
                label.textContent = `${ipad.id}: ${ipad.description}`;

                div.appendChild(checkbox);
                div.appendChild(label);
                ipadsListDiv.appendChild(div);
            });
        } else {
            ipadsListDiv.innerHTML = '<p>No iPads available or failed to load.</p>';
        }
    } catch (error) {
        console.error('Error loading iPads:', error);
        ipadsListDiv.innerHTML = `<p class="error-message">Error loading iPads: ${error.message}</p>`;
    }
}

async function loadPeriods() {
    const periodsListDiv = document.getElementById('periods-list');
    if (!periodsListDiv) { console.error("DOM element #periods-list not found."); return; }
    periodsListDiv.innerHTML = '<p>Loading periods...</p>';

    try {
        const response = await fetch('/api/periods');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status} ${response.statusText}`);
        }
        const periods = await response.json();

        if (periods && periods.length > 0) {
            periodsListDiv.innerHTML = '';
            periods.forEach(period => {
                const div = document.createElement('div');
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.id = `period-${period.id}`;
                checkbox.name = 'selectedPeriodIds';
                checkbox.value = period.id;

                const label = document.createElement('label');
                label.htmlFor = `period-${period.id}`;
                label.textContent = `${period.id}: ${period.start_time} - ${period.end_time}`;

                div.appendChild(checkbox);
                div.appendChild(label);
                periodsListDiv.appendChild(div);
            });
        } else {
            periodsListDiv.innerHTML = '<p>No periods available or failed to load.</p>';
        }
    } catch (error) {
        console.error('Error loading periods:', error);
        periodsListDiv.innerHTML = `<p class="error-message">Error loading periods: ${error.message}</p>`;
    }
}

async function handleBookingSubmit(event) {
    event.preventDefault();

    const bookingMessageDiv = document.getElementById('booking-message');
    if (!bookingMessageDiv) { console.error("DOM element #booking-message not found."); return; }
    bookingMessageDiv.innerHTML = '<p>Submitting booking...</p>';
    bookingMessageDiv.className = 'loading-message';

    const userName = document.getElementById('userName').value;
    const userEmail = document.getElementById('userEmail').value;
    const bookingDate = document.getElementById('bookingDate').value;

    const selectedIpadCheckboxes = document.querySelectorAll('input[name="selectedIpadIds"]:checked');
    const ipadIds = Array.from(selectedIpadCheckboxes).map(cb => cb.value);

    const selectedPeriodCheckboxes = document.querySelectorAll('input[name="selectedPeriodIds"]:checked');
    const periodIds = Array.from(selectedPeriodCheckboxes).map(cb => cb.value);

    if (!userName || !userEmail || !bookingDate) {
        bookingMessageDiv.textContent = 'Name, Email, and Date are required.';
        bookingMessageDiv.className = 'error-message';
        return;
    }
    if (ipadIds.length === 0) {
        bookingMessageDiv.textContent = 'Please select at least one iPad.';
        bookingMessageDiv.className = 'error-message';
        return;
    }
    if (periodIds.length === 0) {
        bookingMessageDiv.textContent = 'Please select at least one Period.';
        bookingMessageDiv.className = 'error-message';
        return;
    }

    const bookingData = {
        userName: userName,
        userEmail: userEmail,
        date: bookingDate,
        ipadIds: ipadIds,
        periodIds: periodIds
    };

    try {
        const response = await fetch('/api/bookings', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(bookingData),
        });

        const result = await response.json();

        if (response.ok && result.success) {
            bookingMessageDiv.textContent = result.message || 'Booking successful!';
            bookingMessageDiv.className = 'success-message';
            document.getElementById('booking-form').reset();
            loadIPads();
            loadPeriods();
        } else {
            bookingMessageDiv.textContent = result.message || `Booking failed. Status: ${response.status}`;
            bookingMessageDiv.className = 'error-message';
        }
    } catch (error) {
        console.error('Error submitting booking:', error);
        bookingMessageDiv.textContent = `Error submitting booking: ${error.message}`;
        bookingMessageDiv.className = 'error-message';
    }
}

async function loadAllBookings() {
    const allBookingsListDiv = document.getElementById('all-bookings-list');
    if (!allBookingsListDiv) { console.error("DOM element #all-bookings-list not found."); return; }
    allBookingsListDiv.innerHTML = '<p class="loading-message">Loading bookings...</p>';

    try {
        const response = await fetch('/api/bookings');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status} ${response.statusText}`);
        }
        const bookings = await response.json();

        if (bookings && bookings.length > 0) {
            allBookingsListDiv.innerHTML = ''; // Clear loading message

            const bookingsByDate = bookings.reduce((acc, booking) => {
                const date = booking.date;
                if (!acc[date]) {
                    acc[date] = [];
                }
                acc[date].push(booking);
                return acc;
            }, {});

            const sortedDates = Object.keys(bookingsByDate).sort((a, b) => new Date(a) - new Date(b));

            sortedDates.forEach(date => {
                const dateHeader = document.createElement('h3');
                dateHeader.textContent = date;
                allBookingsListDiv.appendChild(dateHeader);

                const ul = document.createElement('ul');
                bookingsByDate[date].forEach(booking => {
                    const li = document.createElement('li');
                    li.textContent = `User: ${booking.user_name} (${booking.user_email}) - ` +
                                     `iPad: ${booking.ipad_id} (${booking.ipad_description}) - ` +
                                     `Period: ${booking.period_id} (${booking.period_start_time} - ${booking.period_end_time})`;
                    ul.appendChild(li);
                });
                allBookingsListDiv.appendChild(ul);
            });
        } else {
            allBookingsListDiv.innerHTML = '<p>No bookings found.</p>';
        }
    } catch (error) {
        console.error('Error loading all bookings:', error);
        allBookingsListDiv.innerHTML = `<p class="error-message">Error loading bookings: ${error.message}</p>`;
    }
}
