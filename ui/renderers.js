/**
 * UI renderers for travel planning plugin results.
 * Export renderers by output class name.
 */

// Renderer for TravelPlanningOutput (the task output)
function renderTravelPlanningOutput(result) {
  if (!result) return '';

  return `
    <div class="travel-result">
      <h3>Travel Booking Summary</h3>
      <div class="booking-details">
        <div class="detail-row">
          <span class="label">Flight ID:</span>
          <span class="value">${result.flight_id || 'N/A'}</span>
        </div>
        <div class="detail-row">
          <span class="label">Hotel ID:</span>
          <span class="value">${result.hotel_id || 'N/A'}</span>
        </div>
        <div class="detail-row">
          <span class="label">Hotel Nights:</span>
          <span class="value">${result.hotel_nights || 'N/A'}</span>
        </div>
        <div class="detail-row">
          <span class="label">Total Cost:</span>
          <span class="value">${result.currency || ''} ${result.total_cost || 'N/A'}</span>
        </div>
      </div>
    </div>
  `;
}

// Export only the task output renderer
export default {
  TravelPlanningOutput: renderTravelPlanningOutput,
};
