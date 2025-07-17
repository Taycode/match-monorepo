import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import { toast } from "react-toastify";
import gridlines from "../assets/grid-layer.png";
import logo from "../assets/logo.svg";
import { BASE_URL } from "../utils";

interface Job {
  id: string;
  title: string;
  description: string;
  google_form_url: string;
  google_sheet_url: string;
  twitter_post_id: string;
  created_at: string;
  updated_at: string;
}

const JobList = () => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    try {
      const response = await axios.get(`${BASE_URL}/posting/jobs/list/`);
      setJobs(response.data.results || response.data);
    } catch (error) {
      console.error("Error fetching jobs:", error);
      toast.error("Failed to fetch jobs");
    } finally {
      setLoading(false);
    }
  };

  const filteredJobs = jobs.filter(job =>
    job.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    job.description.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const truncateDescription = (description: string, maxLength: number = 150) => {
    if (description.length <= maxLength) return description;
    return description.substring(0, maxLength) + "...";
  };

  if (loading) {
    return (
      <div className="w-screen min-h-screen bg-[#E2E1EC] flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading jobs...</p>
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
          <div className="flex justify-between items-center mb-8">
            <div>
              <h1 className="text-3xl font-bold text-gray-800">Job Postings</h1>
              <p className="text-gray-600">Manage your job postings and view candidate matches</p>
            </div>
            <Link
              to="/create-job"
              className="bg-primary text-white px-6 py-3 rounded-lg font-medium hover:bg-primary/90 transition-colors"
            >
              Create New Job
            </Link>
          </div>

          {/* Search */}
          <div className="mb-6">
            <input
              type="text"
              placeholder="Search jobs..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent outline-none"
            />
          </div>

          {/* Jobs List */}
          {filteredJobs.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-500 text-lg">
                {searchTerm ? "No jobs found matching your search." : "No jobs posted yet."}
              </p>
              {!searchTerm && (
                <Link
                  to="/create-job"
                  className="mt-4 inline-block bg-primary text-white px-6 py-3 rounded-lg font-medium hover:bg-primary/90 transition-colors"
                >
                  Create Your First Job
                </Link>
              )}
            </div>
          ) : (
            <div className="space-y-4">
              {filteredJobs.map((job) => (
                <div
                  key={job.id}
                  className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow"
                >
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <h3 className="text-xl font-semibold text-gray-800 mb-2">
                        {job.title}
                      </h3>
                      <p className="text-gray-600 mb-4">
                        {truncateDescription(job.description)}
                      </p>
                      <div className="flex items-center gap-4 text-sm text-gray-500">
                        <span>Created: {formatDate(job.created_at)}</span>
                        <span>•</span>
                        <span>Updated: {formatDate(job.updated_at)}</span>
                      </div>
                    </div>
                    
                    <div className="ml-6 flex flex-col gap-2">
                      <Link
                        to={`/jobs/${job.id}`}
                        className="bg-primary text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-primary/90 transition-colors text-center"
                      >
                        View Details
                      </Link>
                      <Link
                        to={`/jobs/${job.id}/matches`}
                        className="bg-green-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-green-700 transition-colors text-center"
                      >
                        View Matches
                      </Link>
                    </div>
                  </div>

                  {/* Automation Status */}
                  <div className="mt-4 pt-4 border-t border-gray-200">
                    <div className="flex items-center gap-6 text-sm">
                      <div className="flex items-center gap-2">
                        <span className={`w-3 h-3 rounded-full ${job.google_form_url ? 'bg-green-500' : 'bg-gray-300'}`}></span>
                        <span className={job.google_form_url ? 'text-green-600' : 'text-gray-500'}>
                          Google Form
                        </span>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className={`w-3 h-3 rounded-full ${job.google_sheet_url ? 'bg-green-500' : 'bg-gray-300'}`}></span>
                        <span className={job.google_sheet_url ? 'text-green-600' : 'text-gray-500'}>
                          Google Sheet
                        </span>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className={`w-3 h-3 rounded-full ${job.twitter_post_id ? 'bg-green-500' : 'bg-gray-300'}`}></span>
                        <span className={job.twitter_post_id ? 'text-green-600' : 'text-gray-500'}>
                          Twitter Post
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default JobList; 