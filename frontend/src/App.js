import React, { useState } from "react";
import axios from "axios";
import MapUploader from "./components/MapUploader";

function App() {
  const [demUrl, setDemUrl] = useState("");
  const [pathUrl, setPathUrl] = useState("");
  const [gearthUrl, setGearthUrl] = useState("");
  const [floodUrl, setFloodUrl] = useState(""); 
  const [place, setPlace] = useState(""); 
  const [dataRows, setDataRows] = useState([]);  // Store path data
  const [placeData, setPlaceData] = useState(null);  // Store place data

  const handleProcess = async (place) => {
    try {
      setPlace(place); 
      const formData = new FormData();
      formData.append("place", place);

      const response = await axios.post("http://127.0.0.1:8000/process/", formData);

      setDemUrl(response.data.dem_path);
      setPathUrl(response.data.path_result);
      setGearthUrl(`http://127.0.0.1:8000/get-gearth/?place=${place}`);
      setFloodUrl("http://127.0.0.1:8000/get-flood");

      // Fetch the path data
      fetchData();

      // Fetch the place data
      fetchPlaceData(place);

    } catch (error) {
      console.error("Error processing data:", error);
    }
  };

  const fetchData = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/get-data");
      setDataRows(response.data.data);  // Set the fetched data
    } catch (error) {
      console.error("Error fetching path data:", error);
    }
  };

  const fetchPlaceData = async (placeName) => {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/get-place-data/${placeName}`);
      setPlaceData(response.data);  // Set the fetched place data
    } catch (error) {
      console.error("Error fetching place data:", error);
    }
  };

  return (
    <div className="App">
      <h1>Flood Navigation System</h1>

      <MapUploader onProcess={handleProcess} />

      {/* Display Place Data below the search box */}
      {placeData && (
        <div className="table-container">
          <h2>Place Data</h2>
          <table border="1">
            <thead>
              <tr>
                <th>Place Name</th>
                <th>Population Density</th>
                <th>Area</th>
                <th>Elevation</th>
                <th>Boats Needed</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>{placeData.placeName}</td>
                <td>{placeData.populationDensity}</td>
                <td>{placeData.area}</td>
                <td>{placeData.elevation}</td>
                <td>{placeData.boatsNeeded}</td>
              </tr>
            </tbody>
          </table>
        </div>
      )}

      <div className="image-container">
        {demUrl && (
          <div>
            <h2>DEM Image</h2>
            <img src={`http://127.0.0.1:8000/get-dem`} alt="DEM" />
          </div>
        )}

        {gearthUrl && (
          <div>
            <h2>Google Earth Image</h2>
            <img src={gearthUrl} alt="Google Earth" />
          </div>
        )}
      </div>

      {/* Display Shortest Path & Flood Image Side-by-Side */}
      {pathUrl && floodUrl && (
        <div className="side-by-side-container">
          <div>
            <h2>Shortest Path</h2>
            <img src={`http://127.0.0.1:8000/get-path`} alt="Shortest Path" />
          </div>
          <div>
            <h2>Flood Image</h2>
            <img src={floodUrl} alt="Flood Img" />
          </div>
        </div>
      )}

      {/* Display Path Data in a Table */}
      {dataRows.length > 0 && (
        <div className="table-container">
          <h2>Path Data</h2>
          <table border="1">
            <thead>
              <tr>
                <th>Path Number</th>
                <th>Path Length(metres)</th>
                <th>Evacuation Time(secs)</th>
              </tr>
            </thead>
            <tbody>
              {dataRows.map((row, index) => (
                <tr key={index}>
                  <td>{row.pathNumber}</td>
                  <td>{row.pathLength}</td>
                  <td>{row.time}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default App;