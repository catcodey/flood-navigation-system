import React, { useState } from "react";

function MapUploader({ onProcess }) {
  const [place, setPlace] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    onProcess(place);
  };

  return (
    <form onSubmit={handleSubmit} className="map-form">
      <input
        type="text"
        value={place}
        onChange={(e) => setPlace(e.target.value)}
        placeholder="Enter Place Name"
        required
      />
      <button type="submit">Process</button>
    </form>
  );
}

export default MapUploader;
