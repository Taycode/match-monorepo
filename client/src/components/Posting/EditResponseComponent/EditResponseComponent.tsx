import React, { useState} from 'react';
import './EditResponseComponent.css';

interface EditResponseComponentProps {
    onSave: (updatedResponse: string) => void;
    onCancel: () => void;
    loading: boolean;
    initialResponse: string;
}

const EditResponseComponent: React.FC<EditResponseComponentProps> = (
    {
        initialResponse,
        loading,
        onSave,
        onCancel,
    }) => {
    const handleSave = () => {
        onSave(editedResponse);
    };

    const handleCancel = () => {
        onCancel();
    };

    const [editedResponse, setEditedResponse] = useState<string>(initialResponse);

    return (
        <div className="edit-container">
            <h3>Edit Response</h3>
            <textarea
                className="edit-textarea"
                value={editedResponse}
                onChange={(e) => setEditedResponse(e.target.value)}
                rows={10}
            />
            <div className="edit-buttons">
                <button className="button save-button" onClick={handleSave} disabled={loading}>
                    Save
                </button>
                <button className="button cancel-button" onClick={handleCancel} disabled={loading}>
                    Cancel
                </button>
            </div>
        </div>
    );
};

export { EditResponseComponent };
