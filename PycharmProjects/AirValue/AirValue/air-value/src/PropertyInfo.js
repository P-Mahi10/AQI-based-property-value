import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import "./PropertyInfo.css"; // Importing CSS
import myimg from "./img.jpeg";


function PropertyInfo() {
  const { id } = useParams();
  const [property, setProperty] = useState(null);

  useEffect(() => {
    fetch(`http://127.0.0.1:5000/property/${id}`)
      .then((response) => response.json())
      .then((data) => {
        if (!data.error) {
          setProperty(data);
        }
      })
      .catch((error) => console.error("Error fetching property details:", error));
  }, [id]);

  if (!property) {
    return <p className="loading">Loading property details...</p>;
  }

  return (
      <div className="bg">
        <div className="property-container">
          <h2 className="property-title">{property.name}</h2>

          <div className="property-box">
            {/* Image Section */}
            <div className="property-image">
              <img src={myimg} alt="Property" />
            </div>

            {/* Details Section */}
            <div className="property-content">
              <p><strong>Price:</strong> ₹{property.price || "N/A"}</p>
              <p><strong>Area:</strong> {property.area ? `${property.area} sqft` : "N/A"}</p>
              <p><strong>Location:</strong> {property.location || "N/A"}</p>
              <p><strong>AQI:</strong> {property.aqi || "N/A"}  <strong>Health Risk:</strong> {property.health_risk || "N/A"}</p>
              <p><strong>Scaled Devaluation:</strong> {property.scaled_devaluation || "N/A"}</p>
              <p><strong>Adjusted Price:</strong> ₹{property.adjusted_price || "N/A"}</p>
            </div>
          </div>
        </div>
      </div>

  );
}

export default PropertyInfo;
