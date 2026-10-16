/**
 * UI renderers for travel planning plugin results.
 * Export renderers by output class name.
 */

// Renderer for TravelPlanningOutput (task output)
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

// Renderer for ValidateSelectionOutput (same as task output)
function renderValidateSelectionOutput(result) {
  return renderTravelPlanningOutput(result);
}

// Export renderers by output class name as default export
export default {
  TravelPlanningOutput: renderTravelPlanningOutput,
  ValidateSelectionOutput: renderValidateSelectionOutput,
  LoadRequestOutput: (result) => `<pre>${JSON.stringify(result, null, 2)}</pre>`,
  SearchFlightsOutput: (result) => `<pre>${JSON.stringify(result, null, 2)}</pre>`,
  SearchHotelsOutput: (result) => `<pre>${JSON.stringify(result, null, 2)}</pre>`,
  CheckBudgetOutput: (result) => `<pre>${JSON.stringify(result, null, 2)}</pre>`,
};
