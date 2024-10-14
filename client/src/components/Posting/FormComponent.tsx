import React, { useState, ChangeEvent, FormEvent } from 'react';
import axios from 'axios';
import './FormComponent.css'; // Import CSS for styling

interface FormData {
    source: string;
    post: string;
}

interface SuccessResponse {
    message: string;
    data: any;
}

interface ErrorResponse {
    error: string;
}

type ResponseData = SuccessResponse | ErrorResponse;

const FormComponent: React.FC = () => {
    const [formData, setFormData] = useState<FormData>({
        source: '',
        post: ''
    });
    const [loading, setLoading] = useState<boolean>(false);
    const [response, setResponse] = useState<ResponseData | null>(null);

    const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value
        });
    };

    const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setLoading(true);

        try {
            const apiResponse = await axios.post<ResponseData>('https://server-ts4i.onrender.com/posting/create', formData);
            setResponse(apiResponse.data);
        } catch (error) {
            console.error('Error submitting the form:', error);
            setResponse({ error: 'An error occurred while submitting the form' });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="form-container">
            <form onSubmit={handleSubmit} className="form">
                <h2>Submit Your Post</h2>

                <div className="form-group">
                    <label htmlFor="source">Source</label>
                    <input
                        type="text"
                        id="source"
                        name="source"
                        value={formData.source}
                        onChange={handleChange}
                        className="form-input"
                        placeholder="Enter source"
                        required
                        aria-label="Source"
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="post">Post</label>
                    <textarea
                        id="post"
                        name="post"
                        value={formData.post}
                        onChange={handleChange}
                        className="form-textarea"
                        placeholder="Enter your post"
                        rows={8} // Larger default height
                        required
                        aria-label="Post"
                    />
                </div>

                <button type="submit" className="submit-button" disabled={loading}>
                    {loading ? 'Submitting...' : 'Submit'}
                </button>
            </form>
        </div>
    );
};

export default FormComponent;
