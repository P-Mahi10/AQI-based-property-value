import React, { useState } from "react";
import "./PropertySearch.css";

const PropertySearch = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [filters, setFilters] = useState({
    sortBy: "price_low_high",
    priceRange: [5000, 50000],
    maxAQI: 200,
    minArea: 500,
    maxArea: 5000,
    rooms: "",
    bathrooms: "",
    balconies: "",
  });
  const [properties, setProperties] = useState([]);

  const handleSearch = async () => {
    const response = await fetch(`/api/search?area=${searchQuery}`);
    const data = await response.json();
    setProperties(data);
  };

  return (
    <div className="flex flex-col items-center p-4">
      {/* Search Bar */}
      <div className="mb-4 w-full max-w-md">
        <input
          type="text"
          placeholder="Search for an area..."
          className="border p-2 w-full rounded"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <button className="bg-blue-600 text-white p-2 rounded ml-2" onClick={handleSearch}>
          Search
        </button>
      </div>

      {/* Filters */}
      <div className="w-full max-w-md bg-gray-100 p-4 rounded shadow-md mb-4">
        <h3 className="font-semibold mb-2">Filters</h3>
        <div className="mb-2">
          <label>Sort By:</label>
          <select className="border p-2 w-full" onChange={(e) => setFilters({ ...filters, sortBy: e.target.value })}>
            <option value="price_low_high">Price: Low to High</option>
            <option value="price_high_low">Price: High to Low</option>
            <option value="area_high_low">Area: High to Low</option>
          </select>
        </div>
        <div className="mb-2">
          <label>Price Range: {filters.priceRange[0]} - {filters.priceRange[1]}</label>
          <input
            type="range"
            min="5000"
            max="50000"
            value={filters.priceRange[1]}
            className="w-full"
            onChange={(e) => setFilters({ ...filters, priceRange: [filters.priceRange[0], parseInt(e.target.value)] })}
          />
        </div>
        <div className="mb-2">
          <label>Max AQI:</label>
          <input
            type="number"
            className="border p-2 w-full"
            value={filters.maxAQI}
            onChange={(e) => setFilters({ ...filters, maxAQI: e.target.value })}
          />
        </div>
        <div className="mb-2">
          <label>Rooms:</label>
          <select className="border p-2 w-full" onChange={(e) => setFilters({ ...filters, rooms: e.target.value })}>
            <option value="">Any</option>
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
          </select>
        </div>
      </div>

      {/* Property Listings */}
      <div className="w-full max-w-4xl overflow-auto">
        {properties.length > 0 ? (
          properties.map((property) => (
            <div key={property.id} className="border p-4 mb-4 rounded shadow-md">
              <h3 className="font-bold">{property.name}</h3>
              <p>Price: {property.price}</p>
              <p>Area: {property.area} sq ft</p>
              <p>Rooms: {property.rooms}</p>
              <p>AQI: {property.aqi}</p>
            </div>
          ))
        ) : (
          <p>No properties found</p>
        )}
      </div>
    </div>
  );
};

export default PropertySearch;
