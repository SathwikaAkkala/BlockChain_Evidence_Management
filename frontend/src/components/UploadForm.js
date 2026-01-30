import React, { useState } from "react";
import axios from "axios";

function UploadForm() {

  const [file, setFile] = useState(null);
  const [result, setResult] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) {
      alert("Please select a file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post(
        "http://localhost:8000/submit",
        formData
      );

      setResult(JSON.stringify(res.data, null, 2));

    } catch (err) {
      console.error(err);
      setResult("Upload failed");
    }
  };

  return (
    <form onSubmit={handleSubmit}>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button type="submit">
        Upload Evidence
      </button>

      {result && (
        <div className="result">
          <pre>{result}</pre>
        </div>
      )}

    </form>
  );
}

export default UploadForm;
