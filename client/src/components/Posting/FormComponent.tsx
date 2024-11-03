import React, {useState, ChangeEvent, FormEvent, Dispatch, SetStateAction} from 'react';
import axios from 'axios';
import './FormComponent.css';
import {PostingStage} from "./LLMResponseSelector/posting-stage.enum.ts";
import {showErrorToast, showSuccessToast} from "../../utils/toastUtils.ts"; // Import CSS for styling


interface FormData {
    source: string;
    post: string;
    selectedResponse: string;
    editedResponse: string;
}

interface FormComponentProps {
    onReceiveResponses: Dispatch<SetStateAction<string[]>>;
    updatePostingStage: Dispatch<SetStateAction<PostingStage>>;
    setFormData: Dispatch<SetStateAction<FormData>>;
    formData: FormData;
}



// interface SuccessResponse {
//    responses: string[]
// }

const FormComponent: React.FC<FormComponentProps> = ({ onReceiveResponses, updatePostingStage, setFormData, formData }) => {
    const [loading, setLoading] = useState<boolean>(false);

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
            const response = await axios.post('https://server-ts4i.onrender.com/posting/initiate', formData);
            showSuccessToast('Responses generated successfully');
            const {responses} = response.data;
            onReceiveResponses(responses)
            updatePostingStage(PostingStage.SELECT_RESPONSE)
        } catch (error) {
            console.error('Error submitting the form:', error);
            showErrorToast(String(error));
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
