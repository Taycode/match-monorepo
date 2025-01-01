interface SuccessModalProps {
  isOpen: boolean;
  onClose: () => void;
}

function SuccessModal({ isOpen, onClose }: SuccessModalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/50 backdrop-blur-sm"
        onClick={onClose}
      ></div>

      {/* Modal */}
      <div className="relative bg-white rounded-2xl shadow-xl max-w-md w-full mx-auto p-6 z-10">
        <div className="flex flex-col items-center text-center space-y-8">
          <h3 className="text-xl font-bold text-gray-900">
            Application Submitted!
          </h3>

          <p className="text-gray">
            Thank you for your interest. Your application has been successfully
            submitted to our talent pool.
          </p>

          <button
            onClick={onClose}
            className="mt-6 w-full bg-primary text-white py-3 px-4 rounded-lg font-medium hover:bg-primary/90 transition duration-200"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

export default SuccessModal;
