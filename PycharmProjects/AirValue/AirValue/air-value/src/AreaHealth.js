import React, { useEffect, useState } from "react";
import "./AreaHealth.css"; // Import the CSS file

const AreaHealth = () => {
  const [data, setData] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://localhost:5000/area-health-data");
        if (!response.ok) throw new Error(`Error ${response.status}: ${await response.text()}`);

        const result = await response.json();
        setData(result);
      } catch (err) {
        console.error("Error fetching data:", err);
        setError(err.message);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="bg">
      <div className="area-health-container">
        <h2>Area-wise Health Risk Factors</h2>
        {error && <p className="error">{error}</p>}
        {data.length === 0 ? (
          <p className="loading">Loading data...</p>
        ) : (
          <table>
            <thead>
              <tr>
                {Object.keys(data[0]).map((key) => (
                  <th key={key}>{key}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.map((row, index) => (
                <tr key={index}>
                  {Object.values(row).map((value, idx) => (
                    <td key={idx}>{value}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default AreaHealth;
