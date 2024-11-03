import React, {Dispatch, SetStateAction } from 'react';
import './LLMResponseSelector.css';
import {PostingStage} from "./posting-stage.enum.ts"; // Import the CSS file

interface LLMResponseSelectorProps {
    responses: string[];
    updatePostingStage: Dispatch<SetStateAction<PostingStage>>;
    selectedResponse: string;
    setSelectedResponse: Dispatch<SetStateAction<string>>;
}

// Function to replace URLs with "link" anchors
const replaceURLsWithLinks = (text: string) => {
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    return text.split(urlRegex).map((part, index) => {
        if (urlRegex.test(part)) {
            return (
                <a key={index} href={part} target="_blank" rel="noopener noreferrer">
                    link
                </a>
            );
        }
        return part;
    });
};

const LLMResponseSelector: React.FC<LLMResponseSelectorProps> = ({ responses, updatePostingStage, selectedResponse,  setSelectedResponse }) => {
    const handleSelectResponse = (response: string) => {
        setSelectedResponse(response);
    };

    return (
        <div className="container">
            {!selectedResponse ? (
                <div className="responsesContainer">
                    {responses && responses.length > 0 ? (
                        responses.map((response, index) => (
                            <ResponseItem
                                key={index}
                                response={response}
                                index={index}
                                onSelectResponse={handleSelectResponse}
                            />
                        ))
                    ) : (
                        <p className="noResponses">No responses available.</p>
                    )}
                </div>
            ) : (
                <div className="selectedContainer">
                    <h3 className="selectedTitle">Selected Response</h3>
                    <p className="selectedResponse">{replaceURLsWithLinks(selectedResponse)}</p>
                    <button className="button" onClick={() => updatePostingStage(PostingStage.EDIT_RESPONSE)}>
                        Action Button
                    </button>
                </div>
            )}
        </div>
    );
};

interface ResponseItemProps {
    response: string;
    index: number;
    onSelectResponse: (response: string) => void;
}

const ResponseItem: React.FC<ResponseItemProps> = ({ response, index, onSelectResponse }) => (
    <div className="responseItem">
        <h3>Response {index + 1}</h3>
        <p>{replaceURLsWithLinks(response)}</p>
        <button className="button" onClick={() => onSelectResponse(response)}>
            Select Response {index + 1}
        </button>
    </div>
);

export { LLMResponseSelector };
