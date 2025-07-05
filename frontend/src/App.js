// ✅ THIS IS YOUR UPDATED App.js
import React, { useState } from "react";
import ReactMarkdown from "react-markdown";
import "./App.css";

const API_URL = process.env.REACT_APP_API_URL || "https://resume-analyzer-pro-ko4b.onrender.com";

function App() {
  const [file, setFile] = useState(null);
  const [feedback, setFeedback] = useState("");
  const [score, setScore] = useState(null);
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [role, setRole] = useState("General");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setFeedback("");
    setScore(null);
    setJobs([]);
  };

  const handleSubmit = async () => {
    if (!file) {
      alert("Please select a resume PDF first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file); // ✅ FIXED KEY for FastAPI backend

    setLoading(true);
    setFeedback("");
    setScore(null);
    setJobs([]);

    try {
      const uploadRes = await fetch(`${API_URL}/upload-resume/`, {
        method: "POST",
        body: formData,
      });

      const uploadData = await uploadRes.json();
      const extractedText = uploadData.text;

      const feedbackRes = await fetch(`${API_URL}/suggest-improvements/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ resume_text: extractedText, role }),
      });

      const feedbackText = await feedbackRes.text();
      setFeedback(feedbackText);

      const scoreRes = await fetch(`${API_URL}/score-resume/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ resume_text: extractedText, role }),
      });

      const scoreData = await scoreRes.json();
      setScore(scoreData.score);

      const jobRes = await fetch(`${API_URL}/match-jobs/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ resume_text: extractedText, role }),
      });

      const jobData = await jobRes.json();
      setJobs(jobData.matches || []);
    } catch (error) {
      console.error("❌ Error:", error);
      setFeedback("❌ Failed to fetch feedback.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-black text-white px-4 py-8 font-sans">
      <div className="max-w-3xl mx-auto text-center">
        <h1 className="text-4xl font-extrabold mb-2">🚀 Resume Analyzer Pro</h1>
        <p className="text-gray-300 mb-6">
          AI-powered feedback, scoring, and job matching tailored to your resume.
        </p>

        <div className="flex flex-col md:flex-row items-center justify-center gap-4 mb-6">
          <input
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
            className="bg-gray-800 border border-gray-600 text-white rounded p-2"
          />
          <select
            value={role}
            onChange={(e) => setRole(e.target.value)}
            className="bg-gray-800 border border-gray-600 text-white rounded p-2"
          >
            <option value="General">General</option>
            <option value="Software Developer">Software Developer</option>
            <option value="Data Scientist">Data Scientist</option>
            <option value="Frontend Engineer">Frontend Engineer</option>
          </select>
          <button
            onClick={handleSubmit}
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded text-white font-semibold"
          >
            {loading ? "Analyzing..." : "Upload & Analyze"}
          </button>
        </div>

        {file && <p className="text-green-400 mb-4">✅ File selected: {file.name}</p>}
      </div>

      <div className="max-w-3xl mx-auto mt-8 space-y-6">
        {feedback && (
          <div className="bg-gray-800 p-6 rounded-lg shadow">
            <h2 className="text-2xl font-bold text-blue-400 mb-2">📝 Feedback</h2>
            <ReactMarkdown className="prose prose-invert">{feedback}</ReactMarkdown>
          </div>
        )}

        {score !== null && (
          <div className="bg-gray-800 p-6 rounded-lg shadow">
            <h2 className="text-2xl font-bold text-yellow-400">📊 Resume Score</h2>
            <p className="text-3xl font-extrabold mt-2">{score}/100</p>
          </div>
        )}

        {jobs.length > 0 && (
          <div className="bg-gray-800 p-6 rounded-lg shadow">
            <h2 className="text-2xl font-bold text-green-400 mb-2">🎯 Job Matches</h2>
            <ul className="list-disc ml-6 text-left text-gray-300">
              {jobs.map((job, idx) => (
                <li key={idx}>{job}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;

