import { useState, ChangeEvent, FormEvent, DragEvent } from "react";
import axios from "axios";
import { toast } from "react-toastify";
import gridlines from "../assets/grid-layer.png";
import logo from "../assets/logo.svg";
import { BASE_URL } from "../utils";
import SuccessModal from "../components/TalentPool/SuccessModal";
import FormComponent from "../components/TalentPool/FormComponent";

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
  const [showSuccessModal, setShowSuccessModal] = useState(false);

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value, files } = e.target;

    if (name === "resume_file" && files && files[0]) {
      handleFile(files[0]);
    } else if (name === "years_of_experience") {
      let sanitizedValue = value.replace(/^0+(?!$)/, ""); // Remove leading zeros
      if (parseInt(sanitizedValue, 10) < 0) {
        sanitizedValue = "0"; // Set to 0 if negative
      }
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
        `${BASE_URL}/talents/add-to-pool`,
        form,
        { headers: { "Content-Type": "multipart/form-data" } }
      );

      if (response.data) {
        setShowSuccessModal(true);
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

  return (
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
      <div className="max-w-2xl w-full mx-auto my-20 md:my-12">
        <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
          <div className="bg-primary px-8 py-6">
            <h2 className="text-2xl font-bold text-white text-center font-satoshi">
              Join Our Talent Pool
            </h2>
            <p className="mt-2 text-secondary-100 text-center text-white/80">
              Take the first step towards your next opportunity
            </p>
          </div>

          <FormComponent
            loading={loading}
            formData={formData}
            handleChange={handleChange}
            handleSubmit={handleSubmit}
            selectedFileName={selectedFileName}
            dragActive={dragActive}
            handleDrag={handleDrag}
            handleDrop={handleDrop}
          />
        </div>
      </div>

      <SuccessModal
        isOpen={showSuccessModal}
        onClose={() => setShowSuccessModal(false)}
      />
    </div>
  );
};

export default TalentPoolForm;
