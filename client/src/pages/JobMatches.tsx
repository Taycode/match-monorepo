import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import axios from "axios";
import { toast } from "react-toastify";
import gridlines from "../assets/grid-layer.png";
import logo from "../assets/logo.svg";
import { BASE_URL } from "../utils";

interface Candidate {
  id: string;
  job: string;
  candidate_id: string;
  candidate_type: 'talent' | 'form_response';
  similarity_score: number;
  is_shortlisted: boolean;
  created_at: string;
  candidate_name: string;
  candidate_email: string;
  candidate_resume_url: string;
  candidate_skills: string[];
}

interface JobMatchesData {
  job_id: string;
  job_title: string;
  total_matches: number;
  talent_pool_matches: {
    count: number;
    candidates: Candidate[];
  };
  form_response_matches: {
    count: number;
    candidates: Candidate[];
  };
}

const JobMatches = () => {
  const { jobId } = useParams<{ jobId: string }>();
  const [matchesData, setMatchesData] = useState<JobMatchesData | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'all' | 'talent' | 'form' | 'shortlisted'>('all');

  useEffect(() => {
    if (jobId) {
      fetchMatches();
    }
  }, [jobId]);

  const fetchMatches = async () => {
    try {
      const response = await axios.get(`${BASE_URL}/posting/jobs/${jobId}/matches/`);
      setMatchesData(response.data);
    } catch (error) {
      console.error("Error fetching matches:", error);
      toast.error("Failed to fetch job matches");
    } finally {
      setLoading(false);
    }
  };

  const handleShortlist = async (matchId: string, action: 'shortlist' | 'remove') => {
    try {
      await axios.post(`${BASE_URL}/posting/matches/${matchId}/shortlist/`, { action });
      toast.success(action === 'shortlist' ? 'Candidate shortlisted' : 'Candidate removed from shortlist');
      fetchMatches(); // Refresh data
    } catch (error) {
      console.error("Error updating shortlist:", error);
      toast.error("Failed to update shortlist");
    }
  };

  const handleRefreshMatches = async () => {
    try {
      setLoading(true);
      await axios.post(`${BASE_URL}/posting/jobs/${jobId}/refresh-matches/`);
      toast.success('Matches refreshed successfully');
      fetchMatches();
    } catch (error) {
      console.error("Error refreshing matches:", error);
      toast.error("Failed to refresh matches");
    } finally {
      setLoading(false);
    }
  };

  const getFilteredCandidates = () => {
    if (!matchesData) return [];
    
    const allCandidates = [
      ...matchesData.talent_pool_matches.candidates,
      ...matchesData.form_response_matches.candidates
    ];

    switch (activeTab) {
      case 'talent':
        return matchesData.talent_pool_matches.candidates;
      case 'form':
        return matchesData.form_response_matches.candidates;
      case 'shortlisted':
        return allCandidates.filter(c => c.is_shortlisted);
      default:
        return allCandidates;
    }
  };

  const formatScore = (score: number) => {
    return `${(score * 100).toFixed(1)}%`;
  };

  if (loading) {
    return (
      <div className="w-screen min-h-screen bg-[#E2E1EC] flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading matches...</p>
        </div>
      </div>
    );
  }

  if (!matchesData) {
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

  const filteredCandidates = getFilteredCandidates();

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
          {/* Header with Back Arrow */}
          <div className="flex items-center gap-4 mb-6">
            <Link
              to={`/jobs/${jobId}`}
              className="flex items-center justify-center w-10 h-10 rounded-full bg-gray-100 hover:bg-gray-200 transition-colors group"
              title="Back to Job Details"
            >
              <svg
                className="w-5 h-5 text-gray-600 group-hover:text-gray-800 transition-colors"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M15 19l-7-7 7-7"
                />
              </svg>
            </Link>
            <div className="flex-1">
              <h1 className="text-3xl font-bold text-gray-800">Candidate Matches</h1>
              <p className="text-gray-600">{matchesData.job_title}</p>
            </div>
            <div className="flex gap-3">
              <button
                onClick={handleRefreshMatches}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-blue-700 transition-colors"
              >
                Refresh Matches
              </button>
              
            </div>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div className="text-2xl font-bold text-blue-600">{matchesData.total_matches}</div>
              <div className="text-sm text-blue-700">Total Matches</div>
            </div>
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <div className="text-2xl font-bold text-green-600">{matchesData.talent_pool_matches.count}</div>
              <div className="text-sm text-green-700">Talent Pool</div>
            </div>
            <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
              <div className="text-2xl font-bold text-purple-600">{matchesData.form_response_matches.count}</div>
              <div className="text-sm text-purple-700">Form Responses</div>
            </div>
            <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
              <div className="text-2xl font-bold text-orange-600">
                {[...matchesData.talent_pool_matches.candidates, ...matchesData.form_response_matches.candidates]
                  .filter(c => c.is_shortlisted).length}
              </div>
              <div className="text-sm text-orange-700">Shortlisted</div>
            </div>
          </div>

          {/* Tabs */}
          <div className="flex border-b border-gray-200 mb-6">
            {[
              { key: 'all', label: 'All Candidates', count: matchesData.total_matches },
              { key: 'talent', label: 'Talent Pool', count: matchesData.talent_pool_matches.count },
              { key: 'form', label: 'Form Responses', count: matchesData.form_response_matches.count },
              { key: 'shortlisted', label: 'Shortlisted', count: [...matchesData.talent_pool_matches.candidates, ...matchesData.form_response_matches.candidates].filter(c => c.is_shortlisted).length }
            ].map(tab => (
              <button
                key={tab.key}
                onClick={() => setActiveTab(tab.key as any)}
                className={`px-4 py-2 text-sm font-medium border-b-2 ${
                  activeTab === tab.key
                    ? 'border-primary text-primary'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                {tab.label} ({tab.count})
              </button>
            ))}
          </div>

          {/* Candidates List */}
          {filteredCandidates.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-500 text-lg">No candidates found in this category.</p>
            </div>
          ) : (
            <div className="space-y-4">
              {filteredCandidates.map((candidate) => (
                <div
                  key={candidate.id}
                  className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow"
                >
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="text-xl font-semibold text-gray-800">
                          {candidate.candidate_name}
                        </h3>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                          candidate.candidate_type === 'talent' 
                            ? 'bg-green-100 text-green-800' 
                            : 'bg-purple-100 text-purple-800'
                        }`}>
                          {candidate.candidate_type === 'talent' ? 'Talent Pool' : 'Form Response'}
                        </span>
                        {candidate.is_shortlisted && (
                          <span className="px-2 py-1 rounded-full text-xs font-medium bg-orange-100 text-orange-800">
                            Shortlisted
                          </span>
                        )}
                      </div>
                      
                      <p className="text-gray-600 mb-2">{candidate.candidate_email}</p>
                      
                      <div className="flex items-center gap-4 text-sm text-gray-500 mb-3">
                        <span>Match Score: {formatScore(candidate.similarity_score)}</span>
                        <span>•</span>
                        <span>Found on: {new Date(candidate.created_at).toLocaleDateString()}</span>
                      </div>

                      {candidate.candidate_skills && candidate.candidate_skills.length > 0 && (
                        <div className="flex flex-wrap gap-2">
                          {candidate.candidate_skills.map((skill, index) => (
                            <span
                              key={index}
                              className="px-2 py-1 bg-gray-100 text-gray-700 rounded-md text-sm"
                            >
                              {skill}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                    
                    <div className="ml-6 flex flex-col gap-2">
                      {candidate.candidate_resume_url && (
                        <a
                          href={candidate.candidate_resume_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors text-center"
                        >
                          View Resume
                        </a>
                      )}
                      <button
                        onClick={() => handleShortlist(
                          candidate.id,
                          candidate.is_shortlisted ? 'remove' : 'shortlist'
                        )}
                        className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                          candidate.is_shortlisted
                            ? 'bg-red-600 text-white hover:bg-red-700'
                            : 'bg-green-600 text-white hover:bg-green-700'
                        }`}
                      >
                        {candidate.is_shortlisted ? 'Remove from Shortlist' : 'Shortlist'}
                      </button>
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

export default JobMatches;