import React, { useState } from 'react';

function FileUploader() {
    const [fileName, setFileName] = useState('');
    const [filePreview, setFilePreview] = useState(null);

    const handleFileChange = (e) => {
        const file = e.target.files[0];

        if (file) {
            setFileName(file.name);

            // Beispiel: als Data URL (für Bilder, PDF-Vorschau etc.)
            const reader = new FileReader();
            reader.onload = (event) => {
                setFilePreview(event.target.result);
            };
            // reader.readAsDataURL(file);

            // Alternativ: Datei als Text lesen
            reader.readAsText(file);

            // Oder als ArrayBuffer: reader.readAsArrayBuffer(file);
        }
    };

    return (
        <div>
            <input type="file" onChange={handleFileChange} />
            {fileName && <p>Datei: {fileName}</p>}
            {filePreview && (
                <div>
                    <p>Vorschau:</p>
                    <div>{filePreview}</div>
                </div>
            )}
        </div>
    );
}

export default FileUploader;
