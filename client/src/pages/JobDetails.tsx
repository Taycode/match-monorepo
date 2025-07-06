import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import axios from "axios";
import { toast } from "react-toastify";
import gridlines from "../assets/grid-layer.png";
import logo from "../assets/logo.svg";
import { BASE_URL } from "../utils";

interface JobData {
  id: string;
  title: string;
  description: string;
  google_form_id: string;
  google_form_url: string;
  google_sheet_id: string;
  google_sheet_url: string;
  twitter_post_id: string;
  created_at: string;
  updated_at: string;
}

interface JobStats {
  job_title: string;
  created_at: string;
  total_matches: number;
  talent_pool_matches: number;
  form_response_matches: number;
  shortlisted_candidates: number;
  google_form_url: string;
  google_sheet_url: string;
  twitter_posted: boolean;
  avg_similarity_score: number;
}

const JobDetails = () => {
  const { jobId } = useParams<{ jobId: string }>();
  const [job, setJob] = useState<JobData | null>(null);
  const [stats, setStats] = useState<JobStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [syncingResponses, setSyncingResponses] = useState(false);

  // DEBUG: Log to see if component is mounting
  console.log("JobDetails component mounting, jobId:", jobId);

  // Early return for debugging - remove this later
  if (!jobId) {
    return (
      <div className="w-screen min-h-screen bg-[#E2E1EC] flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 text-lg">DEBUG: No jobId found in URL</p>
          <p className="text-gray-600">Current jobId: {String(jobId)}</p>
        </div>
      </div>
    );
  }

  useEffect(() => {
    if (jobId) {
      console.log("Fetching job details for:", jobId);
      fetchJobDetails();
      fetchJobStats();
    }
  }, [jobId]);

  const fetchJobDetails = async () => {
    try {
      console.log("Fetching from URL:", `${BASE_URL}/posting/jobs/${jobId}/`);
      const response = await axios.get(`${BASE_URL}/posting/jobs/${jobId}/`);
      console.log("Job details response:", response.data);
      setJob(response.data);
    } catch (error) {
      console.error("Error fetching job details:", error);
      toast.error("Failed to fetch job details");
    }
  };

  const fetchJobStats = async () => {
    try {
      const response = await axios.get(`${BASE_URL}/posting/jobs/${jobId}/stats/`);
      setStats(response.data);
    } catch (error) {
      console.error("Error fetching job stats:", error);
      toast.error("Failed to fetch job stats");
    } finally {
      setLoading(false);
    }
  };

  const handleSyncResponses = async () => {
    setSyncingResponses(true);
    try {
      const response = await axios.post(`${BASE_URL}/posting/jobs/${jobId}/sync-responses/`);
      toast.success(response.data.message || "Form responses synced successfully");
      fetchJobStats(); // Refresh stats after sync
    } catch (error: any) {
      console.error("Error syncing responses:", error);
      const errorMessage = error.response?.data?.error || "Failed to sync responses";
      toast.error(errorMessage);
    } finally {
      setSyncingResponses(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const formatPercentage = (score: number) => {
    return `${(score * 100).toFixed(1)}%`;
  };

  if (loading) {
    return (
      <div className="w-screen min-h-screen bg-[#E2E1EC] flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading job details...</p>
        </div>
      </div>
    );
  }

  if (!job || !stats) {
    return (
      <div className="w-screen min-h-screen bg-[#E2E1EC] flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600 text-lg">Job not found</p>
          <Link to="/jobs" className="mt-4 inline-block text-primary hover:underline">
            Back to Jobs
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div
      style={{ backgroundImage: `url(${gridlines})` }}
      className="w-screen min-h-screen bg-[#E2E1EC] bg-cover bg-no-repeat bg-center p-4"
    >
      <a
        href="/"
        className="absolute text-center top-6 md:left-20 mb-4 md:mb-0"
      >
        <img src={logo} alt="logo" />
      </a>

      <div className="max-w-6xl mx-auto pt-20">
        <div className="bg-white shadow-xl rounded-2xl p-8 mx-4">
          {/* Header */}
          <div className="flex justify-between items-start mb-8">
            <div>
              <h1 className="text-3xl font-bold text-gray-800 mb-2">{job.title}</h1>
              <p className="text-gray-600">Created: {formatDate(job.created_at)}</p>
              <p className="text-gray-600">Updated: {formatDate(job.updated_at)}</p>
            </div>
            <div className="flex gap-3">
              <Link
                to={`/jobs/${jobId}/matches`}
                className="bg-green-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-green-700 transition-colors"
              >
                View Matches ({stats.total_matches})
              </Link>
              <Link
                to="/jobs"
                className="bg-gray-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-gray-700 transition-colors"
              >
                Back to Jobs
              </Link>
            </div>
          </div>

          {/* Job Description */}
          <div className="mb-8">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Job Description</h2>
            <div className="bg-gray-50 rounded-lg p-6">
              <p className="text-gray-700 whitespace-pre-wrap">{job.description}</p>
            </div>
          </div>

          {/* Statistics */}
          <div className="mb-8">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Matching Statistics</h2>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <div className="text-2xl font-bold text-blue-600">{stats.total_matches}</div>
                <div className="text-sm text-blue-700">Total Matches</div>
              </div>
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <div className="text-2xl font-bold text-green-600">{stats.talent_pool_matches}</div>
                <div className="text-sm text-green-700">Talent Pool</div>
              </div>
              <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
                <div className="text-2xl font-bold text-purple-600">{stats.form_response_matches}</div>
                <div className="text-sm text-purple-700">Form Responses</div>
              </div>
              <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
                <div className="text-2xl font-bold text-orange-600">{stats.shortlisted_candidates}</div>
                <div className="text-sm text-orange-700">Shortlisted</div>
              </div>
            </div>
            {stats.avg_similarity_score > 0 && (
              <div className="mt-4 bg-gray-50 rounded-lg p-4">
                <p className="text-sm text-gray-600">
                  Average Match Score: <span className="font-semibold text-gray-800">{formatPercentage(stats.avg_similarity_score)}</span>
                </p>
              </div>
            )}
          </div>

          {/* Automation Status */}
          <div className="mb-8">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold text-gray-800">Automation Status</h2>
              <button
                onClick={handleSyncResponses}
                disabled={syncingResponses}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {syncingResponses ? "Syncing..." : "Sync Responses"}
              </button>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Google Form */}
              <div className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-center gap-3 mb-3">
                  <span className={`w-4 h-4 rounded-full ${job.google_form_url ? 'bg-green-500' : 'bg-gray-300'}`}></span>
                  <h3 className="font-semibold text-gray-800">Google Form</h3>
                </div>
                {job.google_form_url ? (
                  <div>
                    <p className="text-sm text-gray-600 mb-2">Application form is live</p>
                    <a
                      href={job.google_form_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-primary hover:underline text-sm"
                    >
                      View Form ↗
                    </a>
                  </div>
                ) : (
                  <p className="text-sm text-gray-500">Form not created</p>
                )}
              </div>

              {/* Google Sheet */}
              <div className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-center gap-3 mb-3">
                  <span className={`w-4 h-4 rounded-full ${job.google_sheet_url ? 'bg-green-500' : 'bg-gray-300'}`}></span>
                  <h3 className="font-semibold text-gray-800">Google Sheet</h3>
                </div>
                {job.google_sheet_url ? (
                  <div>
                    <p className="text-sm text-gray-600 mb-2">Responses are being collected</p>
                    <a
                      href={job.google_sheet_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-primary hover:underline text-sm"
                    >
                      View Responses ↗
                    </a>
                  </div>
                ) : (
                  <p className="text-sm text-gray-500">Sheet not created</p>
                )}
              </div>

              {/* Twitter Post */}
              <div className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-center gap-3 mb-3">
                  <span className={`w-4 h-4 rounded-full ${job.twitter_post_id ? 'bg-green-500' : 'bg-gray-300'}`}></span>
                  <h3 className="font-semibold text-gray-800">Twitter Post</h3>
                </div>
                {job.twitter_post_id ? (
                  <div>
                    <p className="text-sm text-gray-600 mb-2">Job posted on Twitter</p>
                    <a
                      href={`https://twitter.com/intent/tweet?text=Check out this job posting!`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-primary hover:underline text-sm"
                    >
                      View Post ↗
                    </a>
                  </div>
                ) : (
                  <p className="text-sm text-gray-500">Not posted to Twitter</p>
                )}
              </div>
            </div>
          </div>

          {/* Actions */}
          <div className="border-t pt-6 mt-8">
            <div className="flex gap-4">
              <Link
                to={`/jobs/${jobId}/matches`}
                className="flex-1 bg-green-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-green-700 transition-colors text-center"
              >
                View All Matches ({stats.total_matches})
              </Link>
              {job.google_form_url && (
                <a
                  href={job.google_form_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex-1 bg-primary text-white py-3 px-6 rounded-lg font-medium hover:bg-primary/90 transition-colors text-center"
                >
                  Share Application Form
                </a>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default JobDetails; 