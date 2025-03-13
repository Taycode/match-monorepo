import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import axios from "axios";
import gridlines from "../assets/grid-layer.png";
import logo from "../assets/logo.svg";
import { BASE_URL } from "../utils";
import { Helmet } from "react-helmet";

interface Post {
  id: string;
  post: string;
  source: string;
}

const PostDetails = () => {
  const { id } = useParams<{ id?: string }>();
  const [selectedPost, setSelectedPost] = useState<Post | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isExpanded, setIsExpanded] = useState(false);

  useEffect(() => {
    if (id) {
      fetchPostDetails(id);
    }
  }, [id]);

  const fetchPostDetails = async (postId: string) => {
    try {
      setLoading(true);
      const res = await axios.get(`${BASE_URL}/posting/view/${postId}`);
      setSelectedPost(res.data);
    } catch (err) {
      setError("Error fetching post details.");
      console.error("Error fetching post details:", err);
    } finally {
      setLoading(false);
    }
  };

  const SkeletonLoader = () => (
    <div className="animate-pulse space-y-6">
      <div className="h-4 bg-gray-200 rounded w-24"></div>
      <div className="space-y-3">
        <div className="h-4 bg-gray/50 rounded w-5/6"></div>
        <div className="h-4 bg-gray/50 rounded w-4/6"></div>
        <div className="h-4 bg-gray/50 rounded w-3/6"></div>
      </div>
      <div className="h-4 bg-gray-200 rounded w-32 mt-8"></div>
    </div>
  );

  const truncateText = (text: string) => {
    const lines = text.split("\n").slice(0, 8);
    return lines.join("\n");
  };

  return (
      <>
          <Helmet>
              {/* Basic tags */}
              <title>{selectedPost?.title}</title>
              <meta name="description" content={selectedPost?.description} />

              {/* Open Graph meta tags */}
              <meta property="og:title" content={selectedPost?.title} />
              <meta property="og:description" content={post.description} />
              <meta property="og:image" content={post.image} />
              <meta property="og:url" content={`https://yoursite.com/posts/${post.id}`} />
              <meta property="og:type" content="article" />

              {/* Twitter Card meta tags */}
              <meta name="twitter:card" content="summary_large_image" />
              <meta name="twitter:title" content={post.title} />
              <meta name="twitter:description" content={post.description} />
              <meta name="twitter:image" content={post.image} />
          </Helmet>
          <div
              style={{ backgroundImage: `url(${gridlines})` }}
              className="w-screen min-h-screen flex justify-center items-center bg-[#E2E1EC] bg-cover bg-no-repeat bg-center p-4"
          >
              <a
                  href="/"
                  className="absolute text-center top-6 md:left-20 mb-4 md:mb-0"
              >
                  <img src={logo} alt="logo" />
              </a>

              <div className="bg-white shadow-xl rounded-2xl p-8 max-w-2xl w-full md:mx-4 my-20 md:my-12">
                  {loading ? (
                      <SkeletonLoader />
                  ) : error ? (
                      <div className="bg-red-50 border-l-4 border-red-500 md:p-4 rounded-lg">
                          <p className="text-red-700">{error}</p>
                      </div>
                  ) : selectedPost ? (
                      <div className="space-y-8">
                          <div className="prose max-w-none">
                              <div className="rounded-xl md:p-6 leading-relaxed whitespace-pre-wrap text-lg">
                                  {isExpanded
                                      ? selectedPost.post
                                      : truncateText(selectedPost.post)}
                                  {selectedPost.post.split("\n").length > 8 && (
                                      <button
                                          onClick={() => setIsExpanded(!isExpanded)}
                                          className="mt-4 text-primary hover:text-primary/80 font-medium transition-colors"
                                      >
                                          {isExpanded ? "Read Less" : "Read More"}
                                      </button>
                                  )}
                              </div>
                          </div>

                          <div className="border-t pt-6">
                              <div className="flex flex-col space-y-2">
                                  <span className="text-sm text-gray-500">Source</span>
                                  <a
                                      href={selectedPost.source}
                                      target="_blank"
                                      rel="noopener noreferrer"
                                      className="text-primary hover:text-primary/80 transition-colors break-all"
                                  >
                                      {new URL(selectedPost.source).hostname}
                                  </a>
                              </div>
                          </div>

                          <div className="border-t pt-6 mt-8">
                              <div className="text-center space-y-4">
                                  <p className="text-gray-700">
                                      Want to be part of our talented community?
                                  </p>
                                  <Link
                                      to="/talent-pool"
                                      className="inline-block px-6 py-3 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors"
                                  >
                                      Join Our Talent Pool
                                  </Link>
                              </div>
                          </div>
                      </div>
                  ) : null}
              </div>
          </div>
      </>
  );
};

export default PostDetails;
