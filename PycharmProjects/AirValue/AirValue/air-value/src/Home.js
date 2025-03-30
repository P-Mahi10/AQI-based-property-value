import React from "react";
import { Link } from "react-router-dom";
import "./Home.css"; // Import the CSS file

const Home = () => {
  return (
    <div className="home-container">
      {/* Left Side - Company Name */}
      <div className="left-section">
        <h1 className="company-name">Air Value</h1>
        <p className="company-tagline">Know the air, Know the price</p>
      </div>

      {/* Right Side - Buttons */}
      <div className="right-section">
        <Link to="/Discover">
          <button className="home-button">Popular Listings</button>
        </Link>
        <Link to="/AreaHealth">
          <button className="home-button">Area wise risk factor</button>
        </Link>
      </div>
    </div>
  );
};

export default Home;
