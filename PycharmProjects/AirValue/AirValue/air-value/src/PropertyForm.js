import React, { useState } from "react";
import './PropertyForm.css'; // Ensure this file is correctly linked

const PropertyForm = () => {
  const [formData, setFormData] = useState({
    location: "",
    area: "",
    rooms: "",
    bathrooms: "",
    balconies: "",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <div className="form-container">
      <h2>Enter Property Details</h2>

      {/* Location Input */}
      <label>Location (Only Bangalore areas available):</label>
      <input
        type="text"
        name="location"
        value={formData.location}
        onChange={handleChange}
        placeholder="e.g., Koramangala, Whitefield..."
      />

      {/* Size Dropdown */}
      <label>Size:</label>
      <select name="rooms" value={formData.rooms} onChange={handleChange}>
        <option value="">Select size</option>
        <option value="1BHK">1BHK</option>
        <option value="2BHK">2BHK</option>
        <option value="3BHK">3BHK</option>
        <option value="4BHK">4BHK</option>
      </select>

      {/* Area Input */}
      <label>Total Area (sq ft):</label>
      <input
        type="number"
        name="area"
        value={formData.area}
        onChange={handleChange}
        placeholder="Enter area in sq ft"
      />

      {/* Bathrooms Input */}
      <label>Number of Bathrooms:</label>
      <input
        type="number"
        name="bathrooms"
        value={formData.bathrooms}
        onChange={handleChange}
        placeholder="Mention the number of bathrooms"
      />

      {/* Balconies Input */}
      <label>Number of Balconies:</label>
      <input
        type="number"
        name="balconies"
        value={formData.balconies}
        onChange={handleChange}
        placeholder="Mention the number of balconies"
      />

      {/* Submit Button */}
      <button className="submit-btn">Submit</button>
    </div>
  );
};

export default PropertyForm;
