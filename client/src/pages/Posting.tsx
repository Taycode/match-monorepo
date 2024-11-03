import FormComponent from "../components/Posting/FormComponent";
import {useState} from "react";
import {LLMResponseSelector} from "../components/Posting/LLMResponseSelector/LLMResponseSelector.tsx";
import {PostingStage} from "../components/Posting/LLMResponseSelector/posting-stage.enum.ts";
import {EditResponseComponent} from "../components/Posting/EditResponseComponent/EditResponseComponent.tsx";
import axios from "axios";

interface FormData {
    source: string;
    post: string;
    selectedResponse: string;
    editedResponse: string;
}

function Posting() {
    const [postingStage, setPostingStage] = useState<PostingStage>(PostingStage.INITIATE_POST);
    const [responses, setResponses] = useState<string[]>([])
    const [selectedResponse, setSelectedResponse] = useState<string >('');
    const [formData, setFormData] = useState<FormData>({
        source: '',
        post: '',
        selectedResponse: '',
        editedResponse: '',
    });
    const [loading, setLoading] = useState<boolean>(false);

    const handleSubmit = async (editedResponse: string) => {
        setLoading(true);
        try {
            const requestData = {
                source: formData.source,
                post: formData.post,
                generatedTweet: selectedResponse,
                editedTweet: editedResponse,
            }
            console.log(requestData)
            await axios.post('http://127.0.0.1:8000/posting/create', requestData);
            setFormData({
                source: '',
                post: '',
                selectedResponse: '',
                editedResponse: '',
            })
            setSelectedResponse('')
            setResponses([])
            setPostingStage(PostingStage.INITIATE_POST)
        } catch (error) {
            console.error('Error submitting the form:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <>
            {
                postingStage === PostingStage.INITIATE_POST ? <FormComponent onReceiveResponses={setResponses} updatePostingStage={setPostingStage} setFormData={setFormData} formData={formData} /> :
                postingStage === PostingStage.SELECT_RESPONSE ? <
                    LLMResponseSelector responses={responses}
                                        updatePostingStage={setPostingStage}
                                        selectedResponse={selectedResponse}
                                        setSelectedResponse={setSelectedResponse}
                    /> :
                postingStage === PostingStage.EDIT_RESPONSE ? <
                    EditResponseComponent onSave={handleSubmit}
                                          onCancel={() => setPostingStage(PostingStage.SELECT_RESPONSE)}
                                          loading={loading}
                                          initialResponse={selectedResponse}
                /> : undefined
            }
        </>
    );
}

export { Posting };
