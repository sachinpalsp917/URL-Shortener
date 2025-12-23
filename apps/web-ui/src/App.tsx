import React, { useState } from "react";
import { shortenUrl, type ShortenedUrl } from "./services/api";

const App = () => {
  const [inputUrl, setInputUrl] = useState("");
  const [result, setResult] = useState<ShortenedUrl | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const data = await shortenUrl(inputUrl);
      setResult(data);
      setInputUrl(""); // Clear input on success
    } catch (err) {
      setError("Failed to shorten URL. Please try again.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };
  return (
    <div className="container">
      <h1>✂️ URL Shortener</h1>

      <div className="card">
        <form onSubmit={handleSubmit}>
          <input
            type="url"
            placeholder="Enter a long URL here..."
            value={inputUrl}
            onChange={(e) => setInputUrl(e.target.value)}
            required
            disabled={loading}
          />
          <button type="submit" disabled={loading}>
            {loading ? "Shortening..." : "Shorten URL"}
          </button>
        </form>

        {error && <p className="error">{error}</p>}

        {result && (
          <div className="result">
            <p>Success! Here is your short link:</p>
            <div className="link-box">
              <a
                href={`${window.location.origin}/${result.short_code}`}
                target="_blank"
                rel="noreferrer"
              >
                {window.location.origin}/{result.short_code}
              </a>
            </div>
            <p className="note">
              (Click to test the redirect & trigger analytics)
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
