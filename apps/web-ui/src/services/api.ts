import axios from "axios";

// Create an axios instance pointing to the Nginx
const api = axios.create({
  baseURL: "/api", // Nginx will route this to localhost:8000
});

export interface ShortenedUrl {
  short_code: string;
  original_url: string;
}

export const shortenUrl = async (
  originalUrl: string
): Promise<ShortenedUrl> => {
  const response = await api.post("/shorten", { url: originalUrl });
  return response.data;
};

// getStats will be discussed later when we implement that endpoint
