function FormComponent({
  loading,
  formData,
  handleChange,
  handleSubmit,
  selectedFileName,
  dragActive,
  handleDrag,
  handleDrop,
}: any) {
  return (
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
              <p className="text-xs text-gray">PDF, DOC, DOCX up to 10MB</p>
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
  );
}

export default FormComponent;
