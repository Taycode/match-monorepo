import { toast } from 'react-toastify';

// Function to show a success toast
export const showSuccessToast = (message: string) => {
    toast.success(message, {
        position: "top-right",
        autoClose: 3000,  // Auto close after 3 seconds
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
    });
};

// Function to show an error toast
export const showErrorToast = (message: string) => {
    toast.error(message, {
        position: "top-right",
        autoClose: 3000,  // Auto close after 3 seconds
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
    });
};
