import { useState, ChangeEvent, FormEvent, DragEvent } from "react";
import axios from "axios";
import { toast } from "react-toastify";

const TalentPoolForm = () => {
  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    role: "",
    phone_number: "",
    email: "",
    years_of_experience: "",
    resume_file: null as File | null,
  });

  const [loading, setLoading] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const [selectedFileName, setSelectedFileName] = useState("");

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value, files } = e.target;

    if (name === "resume_file" && files && files[0]) {
      handleFile(files[0]);
    } else if (name === "years_of_experience") {
      const sanitizedValue = value.replace(/^0+(?!$)/, ""); // Remove leading zeros
      setFormData({ ...formData, [name]: sanitizedValue });
    } else {
      setFormData({ ...formData, [name]: value });
    }
  };

  const handleFile = (file: File) => {
    const allowedTypes = [
      "application/pdf",
      "application/msword",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ];

    if (!allowedTypes.includes(file.type)) {
      toast.error("Please upload PDF, DOC, or DOCX files only");
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      toast.error("File size must be less than 10MB");
      return;
    }

    setFormData({ ...formData, resume_file: file });
    setSelectedFileName(file.name);
  };

  const handleDrag = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const validateForm = () => {
    const phoneRegex = /^\+?[\d\s-()]+$/;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!formData.first_name || !formData.last_name || !formData.role) {
      toast.error("Please fill in all required fields");
      return false;
    }

    if (!phoneRegex.test(formData.phone_number)) {
      toast.error("Please enter a valid phone number");
      return false;
    }

    if (!emailRegex.test(formData.email)) {
      toast.error("Please enter a valid email address");
      return false;
    }

    if (!formData.resume_file) {
      toast.error("Please upload a resume file");
      return false;
    }

    return true;
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!validateForm()) return;

    setLoading(true);

    try {
      const form = new FormData();
      Object.entries(formData).forEach(([key, value]) => {
        if (key === "resume_file" && value) {
          form.append(key, value as File);
        } else if (key === "years_of_experience") {
          form.append(key, parseInt(value as string, 10).toString()); // Convert to integer
        } else {
          form.append(key, String(value));
        }
      });

      const response = await axios.post(
        "https://server-ts4i.onrender.com/talents/add-to-pool",
        form,
        { headers: { "Content-Type": "multipart/form-data" } }
      );

      if (response.data) {
        toast.success("Application submitted successfully!");
        setFormData({
          first_name: "",
          last_name: "",
          role: "",
          phone_number: "",
          email: "",
          years_of_experience: "",
          resume_file: null,
        });
        setSelectedFileName("");
      }
    } catch (error: any) {
      console.error("Error during submission", error);
      const errorMessage =
        error.response?.data?.message ||
        "Failed to submit application. Please try again.";
      toast.error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  console.log(formData);
  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-2xl mx-auto">
        <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
          <div className="bg-primary px-8 py-6">
            <h2 className="text-2xl font-bold text-white text-center font-satoshi">
              Join Our Talent Pool
            </h2>
            <p className="mt-2 text-secondary-100 text-center text-white/80">
              Take the first step towards your next opportunity
            </p>
          </div>

          <form onSubmit={handleSubmit} className="px-8 py-8 space-y-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <label className="block text-sm font-medium text-secondary">
                  First Name
                </label>
                <input
                  type="text"
                  name="first_name"
                  value={formData.first_name}
                  onChange={handleChange}
                  className="w-full px-4 py-3 rounded-lg border border-gray focus-within:border-primary transition duration-200"
                  placeholder="Enter your first name"
                  required
                />
              </div>
              <div className="space-y-2">
                <label className="block text-sm font-medium text-secondary">
                  Last Name
                </label>
                <input
                  type="text"
                  name="last_name"
                  value={formData.last_name}
                  onChange={handleChange}
                  className="w-full px-4 py-3 rounded-lg border border-gray focus-within:border-primary transition duration-200"
                  placeholder="Enter your last name"
                  required
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <label className="block text-sm font-medium text-secondary">
                  Role
                </label>
                <input
                  type="text"
                  name="role"
                  value={formData.role}
                  onChange={handleChange}
                  className="w-full px-4 py-3 rounded-lg border border-gray focus-within:border-primary transition duration-200"
                  placeholder="e.g. Software Engineer"
                  required
                />
              </div>
              <div className="space-y-2">
                <label className="block text-sm font-medium text-secondary">
                  Years of Experience
                </label>
                <input
                  type="number"
                  name="years_of_experience"
                  value={formData.years_of_experience}
                  onChange={handleChange}
                  className="w-full px-4 py-3 rounded-lg border border-gray focus-within:border-primary transition duration-200"
                  min={0}
                  required
                />
              </div>
            </div>

            <div className="space-y-2">
              <label className="block text-sm font-medium text-secondary">
                Email Address
              </label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className="w-full px-4 py-3 rounded-lg border border-gray focus-within:border-primary transition duration-200"
                placeholder="you@example.com"
                required
              />
            </div>

            <div className="space-y-2">
              <label className="block text-sm font-medium text-secondary">
                Phone Number
              </label>
              <input
                type="tel"
                name="phone_number"
                value={formData.phone_number}
                onChange={handleChange}
                className="w-full px-4 py-3 rounded-lg border border-gray focus-within:border-primary transition duration-200"
                placeholder="Enter your phone number"
                required
              />
            </div>

            <div className="space-y-2">
              <label className="block text-sm font-medium text-secondary">
                Upload Resume
              </label>
              <div
                className={`mt-1 flex flex-col items-center justify-center px-6 pt-5 pb-6 border-2 border-dashed rounded-lg transition duration-200 
                  ${
                    dragActive
                      ? "border-primary bg-primary/5"
                      : "border-gray hover:border-primary/50"
                  }
                `}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
              >
                <div className="space-y-3 text-center">
                  <div className="flex flex-col items-center text-sm text-gray">
                    <label
                      htmlFor="resume_file"
                      className="relative cursor-pointer rounded-md font-medium text-primary hover:text-secondary focus-within:outline-none focus-within:ring-2 focus-within:ring-primary focus-within:ring-offset-2"
                    >
                      <span>Upload a file</span>
                      <input
                        id="resume_file"
                        name="resume_file"
                        type="file"
                        className="sr-only"
                        onChange={handleChange}
                        accept=".pdf,.doc,.docx"
                      />
                    </label>
                    <p className="pl-1">or drag and drop</p>
                  </div>
                  {selectedFileName ? (
                    <p className="text-sm text-primary font-medium">
                      Selected: {selectedFileName}
                    </p>
                  ) : (
                    <p className="text-xs text-gray">
                      PDF, DOC, DOCX up to 10MB
                    </p>
                  )}
                </div>
              </div>
            </div>

            <div className="pt-4">
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-primary text-white py-4 px-6 rounded-lg font-medium hover:bg-primary/90 focus:outline-none focus:ring-primary focus:ring-offset-2 transition duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? "Submitting..." : "Submit Application"}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default TalentPoolForm;
