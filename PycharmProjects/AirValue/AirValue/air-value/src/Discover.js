import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./Discovery.css";

function Discovery() {
  const [properties, setProperties] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [sortBy, setSortBy] = useState(""); // Sorting criteria
  const navigate = useNavigate();

  useEffect(() => {
    fetch("http://127.0.0.1:5000/properties")
      .then(response => response.json())
      .then(data => setProperties(data))
      .catch(error => console.error("Error fetching properties:", error));
  }, []);

  const handleSearch = () => {
    fetch(`http://127.0.0.1:5000/search?query=${searchQuery}`)
      .then(response => response.json())
      .then(data => setProperties(data))
      .catch(error => console.error("Error searching properties:", error));
  };

  const handleClick = (id) => {
    navigate(`/property/${id}`);
  };

  function convertPriceToNumber(price) {
    if (!price || typeof price !== 'string') {
        return 0; // Default to 0 if price is missing or not a string
    }

    let num = 0;

    if (price.includes('Cr')) {
        num = parseFloat(price.replace('₹', '').replace('Cr', '')) * 100; // Convert Cr to Lakh
    } else if (price.includes('L')) {
        num = parseFloat(price.replace('₹', '').replace('L', '')); // Keep in Lakhs
    }

    return isNaN(num) ? 0 : num; // Handle potential NaN values
  }

  const sortedProperties = [...properties].sort((a, b) => {
    const priceA = convertPriceToNumber(a.price);
    const priceB = convertPriceToNumber(b.price);

    if (sortBy === "price_low_high") return priceA - priceB;
    if (sortBy === "price_high_low") return priceB - priceA;
    if (sortBy === "name_a_z") return a.name.localeCompare(b.name);
    if (sortBy === "name_z_a") return b.name.localeCompare(a.name);
    if (sortBy === "area_low_high") {
        const areaA = parseInt(a.area.replace(/[^0-9]/g, ""), 10);
        const areaB = parseInt(b.area.replace(/[^0-9]/g, ""), 10);
        return areaA - areaB;
    }
    if (sortBy === "area_high_low") {
        const areaA = parseInt(a.area.replace(/[^0-9]/g, ""), 10);
        const areaB = parseInt(b.area.replace(/[^0-9]/g, ""), 10);
        return areaB - areaA;
    }

    return 0; // Default: No sorting
  });

  return (
    <div className="discovery-container">
      <h2 className='title1'>Discover Properties</h2>

      <div className="filters">
        <input
          type="text"
          placeholder="Search by name or location..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
          <button className="nature-btn" onClick={handleSearch}>Search</button>

          <select onChange={(e) => setSortBy(e.target.value)} value={sortBy}>
          <option value="">Sort By</option>
          <option value="price_low_high">Price: Low to High</option>
          <option value="price_high_low">Price: High to Low</option>
          <option value="area_low_high">Area: Low to High</option>
          <option value="area_high_low">Area: High to Low</option>
        </select>
      </div>

      <div className="table-container">
        {sortedProperties.length > 0 ? (
          <table className="property-table">
            <thead>
              <tr>
                <th>Property Name</th>
                <th>Price</th>
                <th>Area (sqft)</th>
                <th>Location</th>
              </tr>
            </thead>
            <tbody>
              {sortedProperties.map((property) => (
                <tr key={property.id} onClick={() => handleClick(property.id)}>
                  <td>{property.name}</td>
                  <td>{property.price}</td>
                  <td>{property.area.toLocaleString()}</td>
                  <td>{property.location}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>No properties found.</p>
        )}
      </div>
    </div>
  );
}

export default Discovery;
